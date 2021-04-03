var cloud_functions_url = ''; // Enter your cloud functions base URL here

const getTwitterFeed = async(user_id = null) => {
    var tweetsDiv = document.getElementById('tweetsDiv');
    tweetsDiv.textContent = 'Getting latest Tweets...';

    console.log('Fetching latest Twitter feed');
    var body = user_id == null ? '' : JSON.stringify({ 'user_id': user_id });
    const response = await fetch(cloud_functions_url + '/get_twitter_feed', {
        method: 'POST',
        body: body,
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const responseJSON = await response.json();
    console.log('Got Twitter feed: ', responseJSON);
    feed = responseJSON['feed'];

    tweetsDiv.textContent = null;
    var numTweets = feed.length;
    for (var i = 0; i < numTweets; i++) {
        var tweetDetails = feed[i];
        var tweet = document.createElement('div');
        tweet.className = 'tweet';
        tweetsDiv.appendChild(tweet);

        var topLine = document.createElement('p');
        topLine.className = 'tweetTopLine';
        tweet.appendChild(topLine);
        var fullName = document.createElement('span');
        fullName.className = 'fullName';
        topLine.appendChild(fullName);
        var userName = document.createElement('span');
        userName.className = 'userName';
        userName.textContent = '@' + tweetDetails['user_name'];
        topLine.appendChild(userName);
        var time = document.createElement('span');
        time.className = 'time';
        time.textContent = tweetDetails['time'];
        topLine.appendChild(time);

        // Link to user profile
        var profileLink = document.createElement('a');
        profileLink.href = 'profile.html?user_id=' + tweetDetails['user_id'].toString();
        profileLink.textContent = tweetDetails['first_name'] + ' ' + tweetDetails['last_name'];
        fullName.appendChild(profileLink);

        var contents = document.createElement('p');
        contents.className = 'tweetContents';
        contents.textContent = tweetDetails['contents'];
        tweet.appendChild(contents);
    }
    if (numTweets == 0) {
        tweetsDiv.textContent = "No Tweets found.";
    }
}

const getUserInfo = async(user_id) => {
    var userInfoDiv = document.getElementById('userInfoDiv');
    userInfoDiv.textContent = 'Getting user info...';

    const response = await fetch(cloud_functions_url + '/get_user_info', {
        method: 'POST',
        body: JSON.stringify({ 'user_id': user_id }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const responseJSON = await response.json();
    console.log('Got user info: ', responseJSON);
    info = responseJSON;

    userInfoDiv.textContent = null;
    var fullNameProfile = document.createElement('p');
    fullNameProfile.className = 'fullNameProfile';
    fullNameProfile.textContent = info['first_name'] + ' ' + info['last_name'];
    userInfoDiv.appendChild(fullNameProfile);
    var userNameProfile = document.createElement('p');
    userNameProfile.className = 'userNameProfile';
    userNameProfile.textContent = ' @' + info['user_name'];
    userInfoDiv.appendChild(userNameProfile);
    var bioProfile = document.createElement('p');
    bioProfile.className = 'bioProfile';
    bioProfile.textContent = info['bio'];
    userInfoDiv.appendChild(bioProfile);
}

const getUserPage = async() => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var user_id = urlParams.get("user_id");
    if (user_id) {
        getUserInfo(user_id);
        getTwitterFeed(user_id);
    } else {
        var tweetsDiv = document.getElementById('tweetsDiv');
        tweetsDiv.textContent("Invalid URL: no user id provided.")
    }
}