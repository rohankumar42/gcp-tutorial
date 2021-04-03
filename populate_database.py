import requests

# Enter your cloud functions base URL here
CLOUD_FUNCTIONS_URL = ''

USERS = [
    ('jack', 'Jack', 'Dorsey', 'My friends call me Big Beard'),
    ('uncommonhacks', 'Uncommon', 'Hacks',
     "I'm just a hacakthon, standing in front of a student, asking them to register"),
    ('eggsbenedict', 'Ms Eggo', 'Benedicto', 'Too tasty for you'),
    ('oof', 'Oofoo', 'Faloofoo', 'ok ??!!!'),
    ('covid19', 'Corona', 'Virus', 'Coming soon to a household near you'),
]

TWEETS = [
    ('jack', 'just setting up my twttr'),
    ('oof', 'lmao YEET'),
    ('uncommonhacks', "Can't wait for Uncommon Hacks 2021!!! "
     "All my favorite people in one place!!!"),
    ('oof', 'if cat no want cuddles why cute ?'),
    ('eggsbenedict', 'hey @uncommonhacks super excited for UH 21 - '
     'do you guys do travel reimbursement?'),
    ('covid19', 'SURPRISE BITCH'),
    ('uncommonhacks', 'nooooooooooooooooooo :('),
    ('uncommonhacks', 'at least we still have celery'),
    ('jack', 'hey guys does someone wanna buy my tweet'),
    ('oof', 'what? even?? is??? javascript???????'),
]


USER_NAME_TO_ID = {}


def add_user(user_name, first_name, last_name, bio):
    url = CLOUD_FUNCTIONS_URL + '/create_new_user'
    response = requests.post(url, json={
        'user_name': user_name,
        'first_name': first_name,
        'last_name': last_name,
        'bio': bio
    })
    assert(response.ok)
    USER_NAME_TO_ID[user_name] = response.json()['user_id']


def add_tweet(user_name, contents):
    url = CLOUD_FUNCTIONS_URL + '/create_new_tweet'
    response = requests.post(url, json={
        'user_id': USER_NAME_TO_ID[user_name],
        'contents': contents
    })
    assert(response.ok)


if __name__ == '__main__':
    print(f'Creating {len(USERS)} users')
    for user_name, first_name, last_name, bio in USERS:
        add_user(user_name, first_name, last_name, bio)

    print(f'Creating {len(TWEETS)} tweets')
    for user_name, contents in TWEETS:
        add_tweet(user_name, contents)

    print('Done!')
