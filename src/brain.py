"""
Product Hunt Scraper brain.
This module is the core of the Scraper and it includes a function that sequentially does the following processes 
1)Uses product hunt API to access a praticular type of or a particular days app.
2)After recieving the JSON object form the producthunt website scrapes the producthunt website
  of the products and passes the URLs sequentially to scraper_with_API module.
3)Receives the Product class object from the scraper module and accesses the location dictionary of makers
4)Passes this location dictionary to india_verifier module and receives a string:boolean format dictionary.
5)Now it takes the prodcuthunt python objects of products which have atleast one maker in India


Libraries:
	This module is built using python development libraries Requests,optparse, json, scraper_with_API and india_verifier

	Requests is the only Non-GMO HTTP library for Python, safe for human consumption.
	Helps generating HTTP requests to get webpages.
	
	Optparse seems like a pretty cool module for processing command line options and arguments in Python.
	It is intended to be an improvement over the old getopt module.

	json library enables handling json objects in python and exposes an API familiar to users of the standard library marshal and pickle modules

	the scraper_with_API and the india_verifier library have been describe in their respective source code files
"""
from optparse import OptionParser
import requests
import json
import scraper_with_API as scraper
import india_verifier as verifier
import sys
import twitter

def main():

	# initialise parser
	parser = OptionParser(usage="usage: %prog [options] arguments",
                          version="%prog 0.8")

	# add the relevant required options to parser, option descriptions given in help of each option
	parser.add_option("-y", "--yesterday", action="store_const",const = 'yesterday', default="null", dest='query', help="Yesterday's results")
	parser.add_option("-d", "--date", action="store_const", default='null', const = 'date', dest='query', help="Fetch results for a particular date in yyyy-mm-dd format")
	parser.add_option("-p", "--post", action='store_true', default=False, dest='post', help="Sends a post request to the server with the JSON data")
	parser.add_option("-m", "--sendmessage", action='store_true', default=False, dest='message', help="Sends the message to the maker on twitter.")


	# parse the arguments given form the command line
	(options, args) = parser.parse_args()
	
	# URL to send GET or POST request to producthunt.
	url = "https://api.producthunt.com/v1/posts"
	# here the query string is generated depending on different arguments given on the command line  using optparse
	if options.query =='yesterday':
		querystring = {"days_ago":1}
		print "yesterday running: "
	if options.query =='null':
		parser.print_help()
		sys.exit()
	if options.query =='date':
		querystring = {"day":args[0]}
		print "Running day: "+args[0]

	#initializing twitter api using our own app keys
	api = twitter.Api(consumer_key='IcA2e9oEHbcFPrkjjjp6YcYLl',
                  consumer_secret='KRvnjwCT7yBIG2Gew7VjMREO22nlmFeTubbsLAKqPWZZJiXvId',
                  access_token_key='976062736491675649-aQmTR8WgnMozA0jS9B4Y46AVGON8abx',
                  access_token_secret='9IDQSzdpnjQbgSwasXiuEsWawvnbFn6uREIesZATCUYHi')
	api.VerifyCredentials()
	#the headers necessary for authorization of user by product hunt.
	headers = {
	    'Authorization': "Bearer a0c4160b3ff9b0ca4d4f42e0bde27b504f07e0daed134c0ed7bcc69e37137802",
	    'Cache-Control': "no-cache"
	    }

	#forming the GET request and sending the request to url with above headers
	response = requests.request("GET", url, headers=headers, params=querystring)
	#receive the response and extract the json object using .text attribute and converting JSON object to python data structure
	parent_response = json.loads(response.text)

	#the python list in which all relevant products(with Indian makers) objects are going to be stored
	mailer_list = []

	#Loop over all the products
	for i in range(0,len(parent_response['posts'])):
		product_name = parent_response['posts'][i]['name']
		# print "Product: "+product_name 
		product_URL = parent_response['posts'][i]['discussion_url']
		#get the product's discussion URL which redirects us to products producthunt page
		# print product_URL

		#send the Url to scraper for scraping and store returned object in instance
		instance = scraper.Scrape_product(product_URL)
		print "____________________________________________________________________________________________\n"
		print instance
		# send the location dictionary to the india_verifier for verifyng indian makers store the output dictioanry in bools
		bools = verifier.verify(instance.locations_dict)
		print "the bool list: "
		print bools
		print "____________________________________________________________________________________________\n"
		# extract the product if it has atleast one maker in india
		product_relevant = False
		for item in bools:
			for m in range(0,len(parent_response['posts'][i]['makers'])):
				# print parent_response['posts'][i]['makers'][m]
				# print item
				# unicodedata.normalize('NFKD', parent_response['posts'][i]['makers'][m]['name']).encode('ascii','ignore')
				if parent_response['posts'][i]['makers'][m]['name'] == item:
					parent_response['posts'][i]['makers'][m]['location'] = instance.locations_dict[item]
			if bools[item] == True:
				# store this product in the mailer_list
				product_relevant = True
					

		# extract the product if it has atleast one maker in india
		if product_relevant == True:
			# this if condition handles one argument i.e. -m which shall send message if -m is given on commandline
			if options.message==True:
				# using twitter api to post direct message to makers
				for item in bools:
					if bools[item] == True:
						# checks for indian makers so that only makers based in india receive the Direct message
						a1 = api.PostDirectMessage("Hey there! product name: "+product_name+"\n",  screen_name = 'omnompatel')
						a2 = api.PostDirectMessage("maker name: "+item+"\n",  screen_name = 'omnompatel')
			mailer_list.append(parent_response['posts'][i])
			pass

	# form a python dictionary of the original format and convert it to json format

	# this if condition handles empty json objects
	if len(mailer_list)!=0:
		#form a JSON object to be sent to mailer
		mailer_json = json.dumps({'posts':mailer_list})
		#necessary headers
		headers_send = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		print mailer_json
		if(options.post==True):
			#sending json object to online jscript
			r = requests.post('https://script.google.com/macros/s/AKfycbzj5IW78ogvY39wl5Qc1ucpaMoXCgHTJ7q9Gt6gj9VfgkRr4ZXR/exec', data = mailer_json, headers = headers_send)

if __name__ == '__main__':
    main()
