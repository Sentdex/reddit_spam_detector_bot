# reddit_spam_detector_bot
Bot that detects spam/affiliate marketing authors, and posts some stats on their threads.

To use:

Fill in your API credentials to `praw_creds.py`

Edit to_catch_a_spammer.py's `current_search_query = random.choice(["udemy"])` to be something other than what I am already doing with this bot.

Run with 

`python to_catch_a_spammer.py`

I am already running this on Udemy-specific spam, so you shouldn't do the same thing as I am doing. There's no need to have multiple reddit bots posting on the same threads. 

# To do:
Conquer new spams!

It was suggested that humblebundle would be a good next one to watch for.
