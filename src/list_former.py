import csv


the_list = []
with open('pincodes.csv', 'r') as csvfile:
	pincodereader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in pincodereader:
		# print list(row)
		row_counter = 0
		# print "["
		for item in list(row):
			if row_counter != 1:
				item = item.strip('"')
				item  = item.lower()
				if item not in the_list:
					the_list.append(str(item))
					# print item+","
			row_counter+=1
		# print "]\n"

# print the_list
the_list = sorted(the_list, key=str.lower)
		
with open('scraped_india.csv', 'wb') as csvfile2:
	writer = csv.writer(csvfile2, dialect='excel')
	for item_final in the_list:
		# print item_final
		writer.writerow([item_final]) 