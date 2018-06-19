"""
India Verifier.
It checks wether a developer is from india or not, using the Indian Pincode Directory which is in csv format.
Delivers true if address matches with any of the locations in the Indian Pincode Directory otherwise returns false.

Libraries:
	
	csv iary for handling csv filess the python libr

"""

import csv


def verify(dictionary_input):
	#initialise a ouput dictionary 
	dictionary_output = {}
	# initialise the output dictionary with all makers mapped to false
	for key in dictionary_input:
		dictionary_output[key] = False
		pass

	india_list = []
	# import the indian postal code locations into a list.
	with open('/Users/ompatel/Desktop/AdvantEdge/bamboo_home/xml-data/build-dir/PROD-MAIL-BUIL/src/scraped_india.csv', 'r') as csvfile:
		pincodereader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in pincodereader:
			for item in list(row):
				india_list.append(item)


	# for all makers split a maker's location to individual places i.e city, state and country and check for these places in india_list.
	for key,value in dictionary_input.items():
		split1 = value.split('/')
		for s1 in split1:
			split2 = s1.split(', ')
			for s2 in split2:
				# places = GeoText(s2)
				# print places.cities
				if s2.lower() in india_list:
					dictionary_output[key] = True
					break
	return dictionary_output
