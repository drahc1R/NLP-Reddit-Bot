import praw
import os
import re
from tracery1 import expand_rule
from keep_alive import keep_alive
import time
from textblob import TextBlob
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

reddit = praw.Reddit(
  client_id = os.getenv('client_id'), 
  client_secret = os.getenv('client_secret'),
  username = os.getenv('username'),
  password = os.getenv('password'),
  user_agent = '<ReplyCommentBot1.0>'
)

top_posts = reddit.subreddit('showerthoughts').hot(limit=10)


def clean_string(raw_string):
  cleaned_string = raw_string.lower()
  cleaned_string = re.sub(r'[^A-Za-z0-9 ]+', '', cleaned_string)
  return cleaned_string


my_grammar = {
	"food": ["ketchup", "spaghetti", "pancake", "cheese"],
	"nouns": ["poem", "story", "#item# recipe", "trick", "sitution", "episode"],"items" :['keyboard','reddit','clothes','house','calculator'],
	"vehicle": ["boat", "bobsled", "bird", "tractor", "bulldozer", "steamroller"],
	"people": ["astronaut", "food critic", "farmer", "student"],
	"adjectives": ["salty", "stanky", "jank", "wack", "busted", "toasted"],
	"origin": "Here is a cool #nouns#: 'Thanks for the #food#!' I said as the #people# ran off on a #adjectives# #vehicle.capitalizeALL#"
}

pos = f'Sentiment analysis: positive! Have a great day! Beep. Boop.'

neutral = f'Sentiment analysis: Neutral! Have a great day! Beep. Boop.'

keep_alive()

def replies_of(top_level_comment, 
               count_comment, 
               sub_entries_textblob, 
               sub_entries_nltk):
  if len(top_level_comment.replies) == 0:
    count_comment = 0
    return
  else:
    for num, comment in enumerate(top_level_comment.replies):
      try:
        count_comment += 1
        print('-' * count_comment, comment.body)
        text_blob_sentiment(comment.body,
                           sub_entries_textblob)
        nltk_sentiment(comment.body, sub_entries_nltk)
      except:
        continue
      replies_of(comment,
                count_comment,
                sub_entries_textblob,
                sub_entries_nltk)

def text_blob_sentiment(review, sub_entries_textblob):
  analysis = TextBlob(review)
  if analysis.sentiment.polarity >= 0.0001:
    if analysis.sentiment.polarity > 0:
      sub_entries_textblob['positive'] = sub_entries_textblob['positive'] + 1
      return 'Positive'

  elif analysis.sentiment.polarity <= -0.0001:
    if analysis.sentiment.polarity <= 0:
      sub_entries_textblob['negative'] = sub_entries_textblob['negative'] + 1
      return 'Negative'

  else:
    sub_entries_textblob['neutral'] = sub_entries_textblob['neutral'] + 1
    return 'Neutral'

sia = SentimentIntensityAnalyzer()

# sentiment analysis function for VADER tool
def nltk_sentiment(review, sub_entries_nltk):
    vs = sia.polarity_scores(review)
    if not vs['neg'] > 0.05:
        if vs['pos'] - vs['neg'] > 0:
            sub_entries_nltk['positive'] = sub_entries_nltk['positive'] + 1
            return 'Positive'
        else:
            sub_entries_nltk['neutral'] = sub_entries_nltk['neutral'] + 1
            return 'Neutral'

    elif not vs['pos'] > 0.05:
        if vs['pos'] - vs['neg'] <= 0:
            sub_entries_nltk['negative'] = sub_entries_nltk['negative'] + 1
            return 'Negative'
        else:
            sub_entries_nltk['neutral'] = sub_entries_nltk['neutral'] + 1
            return 'Neutral'
    else:
        sub_entries_nltk['neutral'] = sub_entries_nltk['neutral'] + 1
        return 'Neutral'
      
# def main():
    
#     for submission in top_posts:
#         sub_entries_textblob = {'negative': 0, 'positive' : 0, 'neutral' : 0}
#         sub_entries_nltk = {'negative': 0, 'positive' : 0, 'neutral' : 0}
#         print('Title of the post :', submission.title)
#         text_blob_sentiment(submission.title, sub_entries_textblob)
#         nltk_sentiment(submission.title, sub_entries_nltk)
#         print("\n")
#         submission_comm = reddit.submission(id=submission.id)

#         for count, top_level_comment in enumerate(submission_comm.comments):
#             print(f"-------------{count} top level comment start--------------")
#             count_comm = 0
#             try :
#                 print(top_level_comment.body)
#                 text_blob_sentiment(top_level_comment.body, sub_entries_textblob)
#                 nltk_sentiment(top_level_comment.body, sub_entries_nltk)
#                 replies_of(top_level_comment,
#                            count_comm,
#                            sub_entries_textblob,
#                            sub_entries_nltk)
#             except:
#                 continue
#         print('Over all Sentiment of Topic by TextBlob :', sub_entries_textblob)
#         print('Over all Sentiment of Topic by VADER :', sub_entries_nltk)
#         print("\n\n\n")

def main():
    
    for submission in top_posts:
        sub_entries_textblob = {'negative': 0, 'positive' : 0, 'neutral' : 0}
        sub_entries_nltk = {'negative': 0, 'positive' : 0, 'neutral' : 0}
        print('Title of the post :', submission.title)
        text_blob_sentiment(submission.title, sub_entries_textblob)
        nltk_sentiment(submission.title, sub_entries_nltk)
        print("\n")
        submission_comm = reddit.submission(id=submission.id)
        

        for count, top_level_comment in enumerate(submission.comments):
            print(f"-------------{count} top level comment start--------------")
            count_comm = 0
            try:
              print(top_level_comment.body)
              text_blob_sentiment(top_level_comment.body, sub_entries_textblob)
              nsen = nltk_sentiment(top_level_comment.body, sub_entries_nltk)
              replies_of(top_level_comment,
                         count_comm,
                         sub_entries_textblob,
                         sub_entries_nltk)
              if nsen == 'Positive':
                top_level_comment.reply(body=pos)
                time.sleep(60*60*3)
                
              elif nsen == 'Negative':
                finished_rule = expand_rule(my_grammar, "#origin#")
                tocomment = f'Sentiment analysis: negative! I will try to brighten your day! {finished_rule}'
                top_level_comment.reply(body=tocomment)
                time.sleep(60*60*3)
                
              else:
                top_level_comment.reply(body=neutral)
                time.sleep(60*60*3)
                  
            except:
              pass
        #         continue
        # print('Over all Sentiment of Topic by TextBlob :', sub_entries_textblob)
        # print('Over all Sentiment of Topic by VADER :', sub_entries_nltk)
        # print("\n\n\n")

# def main()
#   for submission in top_posts:


  
#           finished_rule = expand_rule(my_grammar, "#origin#")
#           tocomment = f'I noticed that someone might be sad! :( {finished_rule}'
#           comment.reply(body=tocomment)
#           print(finished_rule)
#           time.sleep(60*60*3)
        
if __name__ == '__main__' :
    main()