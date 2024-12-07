CREATE DATABASE twitter;
USE twitter;
CREATE TABLE `followings` (
  `user_id` varchar(255),
  `following_user_id` varchar(255),
  PRIMARY KEY (`user_id`, `following_user_id`)
);

CREATE TABLE `followers` (
  `user_id` varchar(255),
  `follower_user_id` varchar(255),
  PRIMARY KEY (`user_id`, `follower_user_id`)
);

CREATE TABLE `users` (
  `user_id` varchar(255) PRIMARY KEY,
  `username` varchar(255),
  `role` varchar(255),
  `joined_at` timestamp,
  `following` integer DEFAULT 0,
  `follower` integer DEFAULT 0,
  `posts_cnt` integer DEFAULT 0,
  `saved_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE `tweets` (
  `tweet_id` varchar(255) PRIMARY KEY,
  `created_at` timestamp,
  `content` varchar(255) NULL,
  `media` text NULL,
  `comment_cnt` integer DEFAULT 0,
  `repost_cnt` integer DEFAULT 0,
  `like_cnt` integer DEFAULT 0,
  `view_cnt` integer DEFAULT 0,
  `saved_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE `user_post_tweet` (
  `user_id` varchar(255),
  `tweet_id` varchar(255),
  PRIMARY KEY (`user_id`, `tweet_id`)
);

CREATE TABLE `user_comment_tweet` (
  `user_id` varchar(255),
  `tweet_id` varchar(255),
  `parent_comment_id` varchar(255) NULL,
  PRIMARY KEY (`user_id`, `tweet_id`)
);

CREATE TABLE `reposts` (
  `user_id` varchar(255),
  `tweet_id` varchar(255),
  `parent_tweet_id` varchar(255) NULL,
  `type` varchar(255),
  `content` text NULL,
  PRIMARY KEY (`user_id`, `tweet_id`)
);

CREATE TABLE `hashtags` (
  `hashtag_name` varchar(255) PRIMARY KEY
);

CREATE TABLE `tweet_have_hashtags` (
  `hashtag_name` varchar(255),
  `tweet_id` varchar(255),
  PRIMARY KEY (`user_id`, `hashtag_name`)
);

CREATE TABLE `mentions` (
  `user_id` varchar(255),
  `tweet_id` varchar(255),
  PRIMARY KEY (`user_id`, `tweet_id`)
);

ALTER TABLE `followings` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `followings` ADD FOREIGN KEY (`following_user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `followers` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `followers` ADD FOREIGN KEY (`follower_user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `user_post_tweet` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `user_post_tweet` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `user_comment_tweet` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `user_comment_tweet` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `reposts` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `reposts` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `tweet_have_hashtags` ADD FOREIGN KEY (`hashtag_name`) REFERENCES `hashtags` (`hashtag_name`);

ALTER TABLE `tweet_have_hashtags` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);

ALTER TABLE `mentions` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `mentions` ADD FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`);
