from tweepy import API
from tweepy import Cursor
from tweepy import Stream
from tweepy.streaming import StreamListener     #allow us to listen to tweets based on keywords and hashtags
from tweepy import OAuthHandler                 #responsible for authentication based on access token file
import Access_token                            #twitter credentials

#  #  #  # TWITTER CLIENT  #  #  #  #
class TwitterClient():

	def __inti__(self):
		self.auth = TwitterAuthenticater().authenticate_twitter_app()
		self.twitter_client = API(self.auth)

	def get_user_timeline_tweets(self, num_tweets):
		tweets = []
		for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
			tweets.append(tweet)
		return tweets


#  #  #  #  TWITTER AUTHENTICATER  #  #  #  #
class TwitterAuthenticater():

	def authenticate_twitter_app(self):
		auth = OAuthHandler(Access_token.CONSUMER_,KEY, Access_token.CONSUMER_SECRET)
		auth.set_access_token(Access_token.ACCESS_TOKEN,Access_token.ACCESS_TOKEN_SECRET)
		return auth

#  #  #  #  TWITTER STREAMER  #  #  #  #
class TwitterStreamer():
	"""
	Class for streaming and processing live tweets.
	"""
	def __init__(self):
		self.twitter_authenticater = TwitterAuthenticater()

	def stream_tweets(self, fetched_tweets_filename,hashtags_list):
		# This  handles twitter authentication and the connection to the twitter streaming API
		listener = TwitterListner()
		auth = self.twitter_authenticater.authenticate_twitter_app()
		stream = Stream(auth, listener)


 		#This lines filter the Twitter Streams to capture data by the keywords:
		stream.filter(track = hashtags_list)


#  #  #  #  TWITTER STREAM LISTENER  #  #  #  #
class TwitterListner(StreamListener):	
	"""
	This is a basic Listener class that just prints received to stdout
	"""	
	def __init__(self,fetched_tweets_filename):
		self.fetched_tweets_filename = fetched_tweets_filename

	def on_data(self, data):
		try:
			print(data)
			with open(self.fetched_tweets_filename,'a') as tf:
				tf.write(data)
			return True

		except BaseException as e:
			print("Error on_data: {}".format(str(e)))
		return True

	def on_error(self, status):
		if status == 420:
			# Returning false on data method incase rate limit occurs
			return False
		print(status)


if __name__ == "__main__":

	hashtags_list = ['coronavirus','covid19','pandemic','covid-19']
	fetched_tweets_filename = "tweets.json"

	twitter_client = TwitterClient()
	print(twitter_client.get_user_timeline_tweets(5))

	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(fetched_tweets_filename,hashtags_list)

