"""
Product Hunt Scraper.
This module scrapes a Producthunt website page of a particular product, provided the URL to the page.
It scrapes the page for the attributes: 1.Name of the product 
										2.Number of upvotes for the product
										3.Names of the Makers and their product poofile links 
										4.Twitter Links of the Makers 
										5.Location of the Makers

Libraries:
	This module is built using python development libraries BeautifulSoup, requests and unicodedata.

	Beautiful Soup is a Python library for pulling data out of HTML and XML files. 
	It provide idiomatic ways of navigating, searching, and modifying the parse tree. 

	Requests is the only Non-GMO HTTP library for Python, safe for human consumption.
	Helps generating HTTP requests to get webpages.

	unicodedata is a module that provides access to the Unicode Character Database
	which defines character properties for all Unicode characters.

	twitter this library is developed by bear no github and installation requires pip install twitter-python. 
	It is a very helpful twitter API communicator.
Class:
	The class Product bundles the scraped data to instance/Object.
	The class diagram for the following:
		________________________________________________
		|	                Product                    |
		|______________________________________________|
		|             +product_name:String             |
		|            +product_upvotes:String           |
		|        +twitter_url_dict:{String,String}     |
		|      +producthunt_url_dict:{String,String}   |
		|        +locations_dict:{String,String}       |
		|______________________________________________|
		|              +product_details()              |
		|          +maker_to_twitter_details()         |   
		|        +maker_to_producthunt_details()       |
		|         +maker_to_location_details()         |
		|______________________________________________|

"""

from bs4 import BeautifulSoup
import requests
import urllib2
import unicodedata
import twitter
#important library declarations.

#initialising twitter api using our own keys
api = twitter.Api(consumer_key='IcA2e9oEHbcFPrkjjjp6YcYLl',
                  consumer_secret='KRvnjwCT7yBIG2Gew7VjMREO22nlmFeTubbsLAKqPWZZJiXvId',
                  access_token_key='976062736491675649-aQmTR8WgnMozA0jS9B4Y46AVGON8abx',
                  access_token_secret='9IDQSzdpnjQbgSwasXiuEsWawvnbFn6uREIesZATCUYHi')
api.VerifyCredentials()

#The product class for a particular product
class Product:

	def __init__(self):
		self.twitter_url_dict = {}
		self.producthunt_url_dict = {}
		self.locations_dict = {}

	def product_details(self, product_name, product_upvotes):
		self.product_name = product_name
		self.product_upvotes = product_upvotes

	def maker_to_twitter_details(self, all_maker_names, all_maker_urls):
		for i in range(0,len(all_maker_names)):
			self.twitter_url_dict[all_maker_names[i]] = all_maker_urls[i]

	def maker_to_producthunt_details(self, all_twitter_names, all_twitter_urls):
		for i in range(0,len(all_twitter_names)):
			self.producthunt_url_dict[all_twitter_names[i]] = all_twitter_urls[i]

	def maker_to_location_details(self, all_twitter_names, all_locations):
		for i in range(0,len(all_twitter_names)):
			self.locations_dict[all_twitter_names[i]] = all_locations[i]
	
	def __str__(self):
		print "Title: " + self.product_name
		print "Upvotes: "+ self.product_upvotes
		print "here are the locations:"
		print self.locations_dict
		return "\nFIN."



def Scrape_product(url):
	# get the product website contents into variable html_doc
	html_doc = requests.get(url) 

	# apply SeautifulSoup to parse our document
	soup = BeautifulSoup(html_doc.content, 'html.parser')

	# Code for finding the title header into variable titles
	titles = [td.find('a') for td in soup.findAll('h1')]
	# access the text part of the header and print the name of product
	product_name = titles[0].text
	# print "Title: "+ product_name

	# find the upvote button and store this button division into upvote variable
	upvote = soup.find('span', class_ = "bigButtonCount_10448")
	number_of_votes = upvote.text
	# access the text part of the upvote button and print the number of votes
	# print "Number of Votes: "+number_of_votes

	#this part accesses the makers tab in the webpage 
	#and stores all the maker urls in maker_url_list and names in maker_name_list
	# print "\nThe Makers are:"
	maker_url_list = [] # list for producthunt profile url of all makers of a product
	maker_name_list = [] # list for the names of the makers

	# Find the division of the makers tab
	makers = soup.find('div', class_="makers_ce689")
	#find into division and get all single maker divisions and loop over all makers
	for td in makers.findAll('div', class_="item_99424"):
		# in a particular maker division get the maker name
		link_element2 = td.find('a', class_ = "font_9d927 black_476ed small_231df normal_d2e66 userName_1108f lineHeight_042f1 underline_57d3c")
		maker_name_list.append(unicodedata.normalize('NFKD', link_element2.text).encode('ascii','ignore'))
		# in a particular maker division get the maker URL form href
		link_element = td.find('a', class_="link_30bfd")
		maker_url_list.append("https://www.producthunt.com"+unicodedata.normalize('NFKD', link_element['href']).encode('ascii','ignore'))
		pass

	counter = 0

	#list to store all the current page makers' twitter profile links only if they have given twitter accounts
	maker_twitter_url_list = []
	#list to store all the current page makers' name only if they have given twitter accounts
	maker_twitter_name_list = []
	# print maker_twitter_name_list

	# Iterate over all makers from the producthunt website of product
	for url in maker_url_list:
		# print "Fetching twitter link of Maker, "+maker_name_list[counter]
		#fetch a producthunt url from the maker_url_list and make a soup of that page
		html_maker_doc = requests.get(url)
		maker_soup = BeautifulSoup(html_maker_doc.content, 'html.parser')
		#the try catch is to check wether a twitter link exists or not
		try:
			#from the soup find the twitter link button
			maker_twitter = maker_soup.find('a', class_ = "twitter_afdc4")
			#get the twitter link from the button division form href class and append the link to maker_twitter_url_list
			maker_twitter_url_list.append(unicodedata.normalize('NFKD', maker_twitter['href']).encode('ascii','ignore'))
			#append the makers name to maker_twitter_name_list
			maker_twitter_name_list.append(maker_name_list[counter])
		except(TypeError, KeyError) as e:
			#exception if twitter button does not exist
			print ""
		counter+=1

	# print maker_twitter_url_list
	counter2 = 0
	# a list to store all relevant makers' location
	twitter_locations_list = []
	#iterate in the twitter url list
	for twitter_url in maker_twitter_url_list:
		#use twitter api provision library by bear
		maker_screen_name = twitter_url.split('https://twitter.com/')
		# get a particular user twitter profile using his screen name
		print twitter_url
		#error handling done incase user with that id is not found
		try:
			maker = api.GetUser(screen_name = maker_screen_name[1])
			# access the user location
			twitter_locations_list.append(maker.location)
		except Exception as err:
			print "user not found"
			twitter_locations_list.append('')
			print(err)
	# print twitter_locations_list
	
	#object of product class
	current_prod = Product()
	current_prod.product_details(product_name, number_of_votes)
	current_prod.maker_to_producthunt_details(maker_name_list, maker_url_list)
	current_prod.maker_to_twitter_details(maker_twitter_name_list, maker_twitter_url_list)
	current_prod.maker_to_location_details(maker_twitter_name_list, twitter_locations_list)
	# print current_prod

	return current_prod
# Scrape_product( "https://www.producthunt.com/posts/spark-2-0")