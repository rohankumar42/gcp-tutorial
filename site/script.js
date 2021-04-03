const getTwitterFeed = async() => {
    var tweetsDiv = document.getElementById("tweetsDiv");
    tweetsDiv.textContent = "Getting latest Tweets...";

    console.log("Fetching latest Twitter feed");
    const response = await fetch('https://us-central1-lexical-descent-308922.cloudfunctions.net/get_twitter_feed', {
        method: 'POST',
        body: '',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const responseJSON = await response.json();
    console.log("Got Twitter feed: ", responseJSON);
    feed = responseJSON['feed'];

    tweetsDiv.textContent = null;
    var numTweets = feed.length;
    for (var i = 0; i < numTweets; i++) {
        var tweetDetails = feed[i];
        var tweet = document.createElement('div');
        tweet.className = "tweet";
        tweetsDiv.appendChild(tweet);

        var topLine = document.createElement('p');
        topLine.className = "tweetTopLine";
        tweet.appendChild(topLine);
        var fullName = document.createElement('span');
        fullName.className = "fullName";
        fullName.textContent = tweetDetails["first_name"] + " " + tweetDetails["last_name"];
        topLine.appendChild(fullName);
        var userName = document.createElement('span');
        userName.className = "userName";
        userName.textContent = " @" + tweetDetails["user_name"];
        topLine.appendChild(userName);
        var time = document.createElement('span');
        time.className = "time";
        time.textContent = tweetDetails["time"];
        topLine.appendChild(time);

        var contents = document.createElement('p');
        contents.className = "tweetContents";
        contents.textContent = tweetDetails['contents'];
        tweet.appendChild(contents);
    }
}