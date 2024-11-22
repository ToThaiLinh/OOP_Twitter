CREATE DATABASE twitter;
USE twitter;
CREATE TABLE `follows` (
  `following_user_id` varchar(255),
  `followed_user_id` varchar(255)
);

CREATE TABLE `users` (
  `user_id` varchar(255) PRIMARY KEY,
  `username` varchar(255),
  `role` varchar(255),
  `joined_at` timestamp,
  `following` integer DEFAULT 0,
  `follower` integer DEFAULT 0,
  `posts_cnt` integer DEFAULT 0
);

CREATE TABLE `tweets` (
  `tweet_id` varchar(255) PRIMARY KEY,
  `content` varchar(255) NULL,
  `created_at` timestamp,
  `media` text NULL,
  `comment_cnt` integer DEFAULT 0,
  `repost_cnt` integer DEFAULT 0,
  `like_cnt` integer DEFAULT 0,
  `view_cnt` integer DEFAULT 0
);

CREATE TABLE `user_post_tweet` (
  `post_id` varchar(255) PRIMARY KEY,
  `user_id` varchar(255),
  `tweet_id` varchar(255)
);

CREATE TABLE `user_comment_tweet` (
  `comment_id` varchar(255) PRIMARY KEY,
  `user_id` varchar(255),
  `tweet_id` varchar(255),
  `parent_comment_id` varchar(255) NULL
);

CREATE TABLE `reposts` (
  `respost_id` varchar(255) PRIMARY KEY,
  `user_id` varchar(255),
  `tweet_id` varchar(255),
  `parent_tweet_id` varchar(255) NULL,
  `type` varchar(255),
  `content` text NULL
);

CREATE TABLE `hashtags` (
  `hashtag_id` varchar(255) PRIMARY KEY,
  `hashtag_name` varchar(255)
);

CREATE TABLE `tweet_have_hashtags` (
  `have_hashtag_id` varchar(255) PRIMARY KEY,
  `hashtag_id` varchar(255),
  `tweet_id` varchar(255)
);

CREATE TABLE `mentions` (
  `mention_id` varchar(255) PRIMARY KEY,
  `user_id` varchar(255),
  `tweet_id` varchar(255)
);

ALTER TABLE `follows` ADD FOREIGN KEY (`following_user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `follows` ADD FOREIGN KEY (`followed_user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `user_post_tweet` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `user_post_tweet` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `user_comment_tweet` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `user_comment_tweet` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `user_comment_tweet` ADD FOREIGN KEY (`comment_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `reposts` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `reposts` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `reposts` ADD FOREIGN KEY (`respost_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `tweet_have_hashtags` ADD FOREIGN KEY (`hashtag_id`) REFERENCES `hashtags` (`hashtag_id`);

ALTER TABLE `tweet_have_hashtags` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `mentions` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `mentions` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);
