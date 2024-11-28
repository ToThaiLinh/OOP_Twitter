from services.tweet_service import TweetService
from services.user_service import UserService
from data.mysql_database import MySQLDatabase

db = MySQLDatabase(host='localhost', user='root', password='', database='twitter')
tweet_service = TweetService(db = db)
user_service = UserService(db = db)

# user = {
#     "user_id": "@elonmusk",
#     "username": "Elon Musk",
#     "role": "KOL",
#     "joined_at": "2009-06-01 00:00:00",
#     "following": 852.0,
#     "follower": 852.0,
#     "posts_cnt": 60500.0
# }

tweet = {
    "tweet_id": "1860951753987920344",
    "created_at": "2024-11-25 07:40:47",
    "content": "Mako Shark eaten by something HUGE whilst being reeled in, head alone weighed 100kg ",
    "media": "https://pbs.twimg.com/media/GdNtwhhXAAIjuVK?format=jpg&name=medium",
    "comment_cnt": 1500.0,
    "repost_cnt": 4900.0,
    "like_cnt": 102000.0,
    "view_cnt": 24500000.0
}


tweet_service.create(**tweet)
tweet_service.close()
