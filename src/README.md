# Product Hunt Scraper 
###`Version 0.8`

> This package is built above one main website [Product Hunt](https://www.producthunt.com) followed by an assist website [Twitter](https://twitter.com)

> We are using product_hunt API and Twitter API for our scraping purposes with our own Keys. 

The main motto of this package is to look regularly(daily) for new products released on the above website by Indian makers, scrape off those product's data and send Automatic direct messages via twitter to the relevant makers.



## Package contents

	.
	├── brain.py				# Master script controlling all endpoints
	├── india_verifier.py		# Python script to verify maker locations in India
	├── india_verifier.pyc		# Compiled india_verifer.py script
	├── list_former.py			# Python script to extract unique strings from pincodes.csv
	├── pincodes.csv			# Indian postal codes data.
	├── product_hunt.sh			# Bash script run by cron job everyday.
	├── run.sh					# Bash script run by product_hunt.sh
	├── scraped_india.csv		# The list of unique postal codes in india(output of list_former.py)
	├── scraper_with_API.py		# Python script for retrieving locations of makers from a product
	├── scraper_with_API.pyc	# Compiled scraper_with_API.py script
	└── README.md

## I/O
### Input

```shell
$./path/to/the/folder/ python brain.py -h
```
or

```shell
$./path/to/the/folder/ python brain.py
```

### Output

```shell
Usage: brain.py [options] arguments

Options:
  --version          show program's version number and exit
  -h, --help         show this help message and exit
  -y, --yesterday    Yesterday's results
  -d, --date         Fetch results for a particular date in yyyy-mm-dd format
  -p, --post         Sends a post request to the server with the JSON data.
  -m, --sendmessage  Sends the message to the maker on twitter.
```

### Input

```shell
$./path/to/the/folder/ python brain.py -d 2018-06-05
```
or

```shell
$./path/to/the/folder/ python brain.py -y
```

### Output

```shell
Running day: 2018-06-04

https://twitter.com/SistaniSays
user not found
[{u'message': u'User not found.', u'code': 50}]
https://twitter.com/slmosl
https://twitter.com/sarahvorhaus
https://twitter.com/benrbn
https://twitter.com/itaidanino
https://twitter.com/nadavwiz
https://twitter.com/juliaonken
https://twitter.com/kimbermk
https://twitter.com/pchekuri
https://twitter.com/jontra1
https://twitter.com/jsneedles
https://twitter.com/alan
https://twitter.com/jakubswiadek
https://twitter.com/swisspol
____________________________________________________________________________________________

Title: Houseparty for Mac
Upvotes: 304
here are the locations:
{'Nadav Weizmann': u'', 'Itai Danino': u'', 'Jakub Swiadek': u'San Francisco, CA', 'Mor Sela': u'', 'Sarah Vorhaus': u'San Francisco, CA', 'Yoni Londner': u'Israel', 'Praveen Chekuri': u'San Francisco', 'Julia Onken': u'California/London', 'sima sistani': '', 'Alan': u'Mimico, Ontario', 'Pierre-Olivier Latour': u'San Francisco', 'Ben Rubin': u'San Francisco', 'Jeff Needles': u'San Francisco, CA', 'Kimberly Kalb': u''}

FIN.
the bool list: 
{'Nadav Weizmann': False, 'Itai Danino': False, 'Jakub Swiadek': False, 'Mor Sela': False, 'Sarah Vorhaus': False, 'Yoni Londner': False, 'Praveen Chekuri': False, 'Julia Onken': False, 'sima sistani': False, 'Alan': False, 'Pierre-Olivier Latour': False, 'Ben Rubin': False, 'Jeff Needles': False, 'Kimberly Kalb': False}
____________________________________________________________________________________________
 .
 .
 .
 .

https://twitter.com/alinp32
____________________________________________________________________________________________

Title: Noiseblend
Upvotes: 400
here are the locations:
{'Alin Panaitiu': u'Romania'}

FIN.
the bool list: 
{'Alin Panaitiu': False}
____________________________________________________________________________________________

 
```
