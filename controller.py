import os
import logging

import tweeter
import reddit_scraper

from settings import LOG_FILENAME

logging.basicConfig(
  filename=LOG_FILENAME,
  level=logging.INFO,
  format='%(asctime)s %(message)s'
  )


def run():
	try:
		img_filepath = reddit_scraper.image_scraper()
		tweeter.tweet_image_with_status(img_filepath)
	except Exception as e:
		logging.error(str(e))


if __name__=="__main__":
	run()