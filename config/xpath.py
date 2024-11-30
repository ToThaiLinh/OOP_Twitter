xpath_user = {
    'user_id' : './div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/span',
    'username' : './div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/span/span[1]',
    'role': './div/div/div/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div/div/span/span[2]/span/span/div/button',
    'joined_at' : "//span[contains(text(), 'Joined')]",
    'following': "//a[contains(@href, 'following')]/span/span",
    'follower' : "//a[contains(@href, 'verified_followers')]/span/span",
    'posts_cnt': './div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div'
}

xpath_tweet = {
    #'tweet_id': '',
    'created_at' : './div/div/div[3]/div[4]/div/div[1]/div/div[1]/a/time',
    'content' : './div/div/div[3]/div[1]/div/div',
    'media' : './div/div/div[3]/div[2]/div/div/div/div/div/div/div/a/div/div[2]/div',
    'comment_cnt' : './div/div/div[3]/div[5]/div/div/div[1]/button/div/div[2]/span/span/span',
    'repost_cnt' : './div/div/div[3]/div[5]/div/div/div[2]/button/div/div[2]/span/span/span',
    'like_cnt' : './div/div/div[3]/div[5]/div/div/div[3]/button/div/div[2]/span/span/span',
    'view_cnt' : './div/div/div[3]/div[4]/div/div[1]/div/div[3]/span/div/span/span/span'
}

xpath_quote = {
    'repost_id' : "",
    'user_id' : ''
}

xpath_retweet = {
    'user_id': '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span'
    
}
