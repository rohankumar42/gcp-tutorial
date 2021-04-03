import json
import uuid
from datetime import timezone, timedelta
from google.cloud import spanner

instance_id = 'test-instance'
database_id = 'test-database'

client = spanner.Client()
instance = client.instance(instance_id)
database = instance.database(database_id)


def package_response(func):
    # Set CORS headers for the preflight request
    def packaged(request):
        if request.method == 'OPTIONS':
            # Allows GET requests from any origin with the Content-Type
            # header and caches preflight response for an 3600s
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }

            return ('', 204, headers)
        else:
            response = func(request)
            headers = {'Access-Control-Allow-Origin': '*'}
            return json.dumps(response), 200, headers

    return packaged


def _get_user_bio_internal(user_id):
    query = 'SELECT Bio FROM Users WHERE UserId = @user_id'
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            query, params={'user_id': user_id},
            param_types={'user_id': spanner.param_types.INT64})

        for row in results:
            bio = row[0]
            print(f'Got bio for user id {user_id}: {bio}')
            return bio

    raise ValueError(f"No user with user id {user_id} found")


@package_response
def get_user_bio(request):
    request_json = request.get_json(silent=True)
    user_id = request_json['user_id']
    print(f'Trying to get bio for user id {user_id}')
    bio = _get_user_bio_internal(user_id)
    return {'bio': bio}


def _create_new_user_internal(user_name, first_name, last_name, bio):
    user_id = uuid.uuid1().int >> 64  # Generate unique user id

    def insert_user(transaction):
        transaction.insert(
            table="Users",
            columns=("UserId", "UserName", "FirstName", "LastName", "Bio"),
            values=[(user_id, user_name, first_name, last_name, bio)]
        )
        print(
            f"Adding new user {first_name} {last_name} ({user_name}) "
            f"with id {user_id}")

    database.run_in_transaction(insert_user)
    print(f"User {user_name} added successfully")
    return user_id


@package_response
def create_new_user(request):
    request_json = request.get_json(silent=True)
    user_id = _create_new_user_internal(
        request_json['user_name'], request_json['first_name'],
        request_json['last_name'], request_json['bio'])
    return {'user_id': user_id}


def _add_new_tweet_internal(user_id, contents):
    tweet_id = uuid.uuid1().int >> 64  # Generate unique tweet id

    def insert_tweet(transaction):
        transaction.insert(
            table="Tweets",
            columns=("TweetId", "UserId", "Contents", "Timestamp"),
            values=[(tweet_id, user_id, contents, spanner.COMMIT_TIMESTAMP)]
        )

    database.run_in_transaction(insert_tweet)
    print(f"Added tweet with id {tweet_id} for user id {user_id}")
    return tweet_id


@package_response
def add_new_tweet(request):
    request_json = request.get_json(silent=True)
    user_id = request_json['user_id']
    contents = request_json['contents']
    print(
        f'Tweeting new tweet for user id {user_id} with content "{contents}"')
    tweet_id = _add_new_tweet_internal(user_id, contents)
    return {'tweet_id': tweet_id}


def _get_twitter_feed_internal():
    query = '''
    SELECT
        T.Timestamp, T.TweetId, T.Contents, T.UserId,
        U.UserName, U.FirstName, U.LastName
    FROM Tweets AS T JOIN Users AS U USING (UserId)
    ORDER BY T.Timestamp DESC
    '''

    tweets = []
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query)

        for row in results:
            tweet_details = {
                # Convert time to CDT
                "time": row[0].astimezone(timezone(timedelta(hours=-5))) \
                .strftime('%b %d, %I:%M %p'),
                "tweet_id": row[1],
                "contents": row[2],
                "user_id": row[3],
                "user_name": row[4],
                "first_name": row[5],
                "last_name": row[6]
            }
            tweets.append(tweet_details)

    return tweets


@package_response
def get_twitter_feed(request):
    print('Fetching latest Twitter feed')
    feed = _get_twitter_feed_internal()
    return {'feed': feed}
