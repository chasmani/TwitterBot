import os
import json
import logging

import tweepy

# Authorisation keys stored in twitter_key.py
import twitter_keys
import status_builder
from settings import LOG_FILENAME

logging.basicConfig(
  filename=LOG_FILENAME,
  level=logging.INFO,
  format='%(asctime)s %(message)s'
  )
   

def get_api():
  '''
  Gets a tweepy api object
  '''
  auth = tweepy.OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret)
  auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
  return tweepy.API(auth)


def test_api_connection():
  '''
  Check if api is connected
  '''
  api = get_api()
  print(api.me())
  if type(api.me()) == tweepy.models.User:
    print("API Connected")


def tweet_status(status):
  '''
  Tweets a status
  '''
  api = get_api()
  api.update_status(status)


def tweet_image(image_filepath):
  '''
  Tweets an image
  Allows formats including jpg and gif
  '''
  api = get_api()
  return api.update_with_media(image_filepath)


def tweet_image_with_status(image_filepath, status=None):
  '''
  Tweets an image and a status
  Allows formats including jpg and gif
  '''
  api = get_api()
  if status == None:
    status = status_builder.build_status()
  try:
    response = api.update_with_media(image_filepath, status=status)
    if isinstance(response, tweepy.models.Status):
      logging.info("\nTweet successful\n")
      return True
  except Exception as e:
    logging.error(str(e))


def tweet_test():

  tweet_image_with_status('test_images/dog_jpg.jpg', status="Test status")


def tweet_test_too_long_status():

  tweet_image_with_status('test_images/dog_jpg.jpg', status="Test status is too looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong")


def tweet_test_no_image():

  tweet_image_with_status('test_images/no_image.jpg', status="Test status")


if __name__ == "__main__":
  tweet_test_no_image()