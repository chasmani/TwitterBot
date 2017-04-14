import os
import time
import shutil
import logging

from bs4 import BeautifulSoup
import requests

from settings import LOG_FILENAME


logging.basicConfig(
  filename=LOG_FILENAME,
  level=logging.INFO,
  format='%(asctime)s %(message)s'
  )


def get_subreddit_page_and_print():

	url = "http://www.reddit.com/r/dogpictures"
	page = requests.get(url)
	soup = BeautifulSoup(page.content)
	print(soup.prettify())


def get_reddit_soup(url, attempt=1, max_attempts=5):
	#Get soup from a reddit url
	# If reddit blocks the request the try again after a time delay
	print("Attempt " + str(attempt) + " - Fetching soup from " + url)
	if attempt <= max_attempts:
		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")
		# If reddit blocks the scraper, be nice and wait a while
		if (soup.title.text == "Too Many Requests") or (not soup):
			print("Blocked by reddit")
			time.sleep(2 + attempt)
			get_reddit_soup(url, attempt=attempt+1)
		else:
			return soup


def get_reddit_image_post_urls(subreddit):
	# Return a list of post urls from a subreddit
	url = "http://www.reddit.com/r/" + subreddit
	soup = get_reddit_soup(url)
	try:
		# Get list of forum posts as html
		post_divs = soup.find_all("div", {"class":"thing"})
		# Get list of urls of reddit image posts
		reddit_image_links = []
		for post_div in post_divs:
			# Get the post type
			post_type = post_div.find("span",{"class":"domain"}).find("a").getText()
			# Add the urls of the reddit image post types to our url list
			if post_type == "i.redd.it":
				post_link = post_div.find("a", {"class":"may-blank"})["href"]
				reddit_image_links.append(post_link)
		return reddit_image_links
	except:
		print(soup)
		logging.error(soup.title)


def get_img(post_url):
	# Download an image form a reddit post url
	remove_existing_images("images")
	try:
		soup = get_reddit_soup(post_url)
		img_div = soup.find("div", {"class":"media-preview-content"})
		img_src = img_div.find("img")["src"]
		download_img(img_src)
		if test_image("images"):
			return get_image_filepath("images")
	except Exception as e:
		logging.error(str(e))
	return None


def download_img(img_src):

	file_type = img_src.split("?")[0].split(".")[-1]
	response = requests.get(img_src, stream=True)
	with open('images/dog.' + file_type, 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)


def remove_existing_images(directory):
	# remove all exiting images form directory
	directory_path = os.path.join(os.getcwd(), directory)
	for file in os.listdir(directory_path):
		file_path = os.path.join(directory_path, file)
		os.unlink(file_path)


def test_image(directory):
	# Test that 1 image exists in directory
	# And that it meets any and all requirements
	directory_path = os.path.join(os.getcwd(), directory)
	if len(os.listdir(directory_path)) == 1:
		logging.info("Downloaded image passed validation tests")
		return True
	

def get_image_filepath(directory):
	# Get an image filepath from a directory
	directory_path = os.path.join(os.getcwd(), directory)
	return os.path.join(directory_path, os.listdir(directory_path)[0])
	

def image_scraper():
	# Scrape a dog pic and return the filepath of the saved pic
	post_links = get_reddit_image_post_urls("dogpictures")
	for post_link in post_links:		
		time.sleep(2)
		img_filepath = get_img("http://www.reddit.com" + post_link)
		if img_filepath:
			return img_filepath


if __name__=="__main__":
	image_scraper()
