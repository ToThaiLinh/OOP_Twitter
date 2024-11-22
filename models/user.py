class User :
    def __init__(self, user_id, username, role, joined_at, following, follower, posts_count):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.joined_at = joined_at
        self.following = following
        self.follower = follower