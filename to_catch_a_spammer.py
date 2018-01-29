import praw
import re
from praw_creds import client_id, client_secret, password, user_agent, username
import random
import time

common_spammy_words = []

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret, password=password,
                     user_agent=user_agent, username=username)


DEBUG_MODE = False  # For Debug: Don't post to reddit, only print
debug_posted = []  # In debug mode, remember links


def find_spam_by_name(search_query):
    authors = []
    for submission in reddit.subreddit("all").search(search_query, sort="new", limit=11):
        print(submission.title, submission.author, submission.url)
        if submission.author not in authors:
            authors.append(submission.author)
    return authors


if __name__ == "__main__":
    # Compile regex from spam_words.txt for checking titles
    with open("spam_words.txt") as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            try:
                common_spammy_words.append(re.compile(line))
            except:
                print(f"Failed to compile {line}")
                continue

    while True:
        current_search_query = random.choice(["udemy"])
        spam_content = []
        trashy_users = {}
        smelly_authors = find_spam_by_name(current_search_query)
        for author in smelly_authors:
            user_trashy_urls = []
            sub_count = 0
            dirty_count = 0
            try:
                for sub in reddit.redditor(str(author)).submissions.new():
                    submit_links_to = sub.url
                    submit_id = sub.id 
                    submit_subreddit = sub.subreddit
                    submit_title = sub.title
                    dirty = False
                    for regex in common_spammy_words:
                        if re.search(regex, submit_title.lower()):
                            dirty = True
                            junk = [submit_id,submit_title]
                            if junk not in user_trashy_urls:
                                user_trashy_urls.append([submit_id,submit_title,str(author)])

                    if dirty:
                        dirty_count += 1
                    sub_count += 1

                try:
                    trashy_score = dirty_count/sub_count
                except: trashy_score = 0.0
                print("User {} trashy score is: {}".format(str(author), round(trashy_score,3)))

                if trashy_score >= 0.5 and sub_count > 1:
                    trashy_users[str(author)] = [trashy_score,sub_count]

                    for trash in user_trashy_urls:
                        spam_content.append(trash)  

            except Exception as e:
                print(str(e))

        for spam in spam_content:
            spam_id = spam[0]
            spam_user = spam[2]
            submission = reddit.submission(id=spam[0])
            created_time = submission.created_utc
            tagged = False

            for comment in submission.comments.list():
                comment_text = comment.body
                if "*Beep boop*" in comment_text:
                    print("This submission has already been tagged.")
                    tagged = True

            if tagged:
                continue

            if time.time()-created_time <= 86400:
                link = "https://reddit.com"+submission.permalink

                message = """*Beep boop*

I am a bot that sniffs out spammers, and this smells like spam.

At least {}% out of the {} submissions from /u/{} appear to be for Udemy affiliate links. 

Don't let spam take over Reddit! Throw it out!

*Bee bop*""".format(round(trashy_users[spam_user][0]*100,2), trashy_users[spam_user][1], spam_user)
                try:
                    if DEBUG_MODE:
                        if link in debug_posted:
                            continue
                        print(f"Would've posted reply to post by {spam_user}: {link}")
                        debug_posted.append(link)
                        continue

                    with open("posted_urls.txt","r") as f:
                        already_posted = f.read().split('\n')
                    if link not in already_posted:
                        print(message)
                        submission.reply(message)
                        print("We've posted to {} and now we need to sleep for 12 minutes".format(link))
                        with open("posted_urls.txt","a") as f:
                            f.write(link+'\n')
                        time.sleep(12*60)
                        break
                except Exception as e:
                    print(str(e))
                    time.sleep(12*60)

