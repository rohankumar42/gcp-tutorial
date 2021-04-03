CREATE TABLE Users (
    UserId INT64 NOT NULL,
    UserName STRING(128) NOT NULL,
    FirstName STRING(1024) NOT NULL,
    LastName STRING(1024) NOT NULL,
    Bio STRING(MAX),
) PRIMARY KEY (UserId);

CREATE TABLE Tweets (
    TweetId INT64 NOT NULL,
    UserId INT64 NOT NULL,
    Contents STRING(140) NOT NULL,
    Timestamp TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp = true),
    CONSTRAINT FK_UserId FOREIGN KEY (UserId) REFERENCES Users (UserId)
) PRIMARY KEY (TweetId);

CREATE INDEX TweetsByUserId ON Tweets(UserId);

CREATE TABLE Followers (
    FollowerId INT64 NOT NULL,
    FollowingId INT64 NOT NULL,
    CONSTRAINT FK_FollowerId FOREIGN KEY (FollowerId) REFERENCES Users (UserId),
    CONSTRAINT FK_FollowingId FOREIGN KEY (FollowingId) REFERENCES Users (UserId),
) PRIMARY KEY (FollowerId, FollowingId);