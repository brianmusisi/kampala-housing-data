import requests
from bs4 import BeautifulSoup
import numpy as np
import sys



def get_house_data(page_num=10):
    for i in range(1,page_num+1):
    	url ='http://house.jumia.ug/central-12/kampala-3/house/for-sale/q:kampala+%28central%29/?' + 'page=%d&size=30' %i  #construct the url
        page = requests.get(url)  
        jumia = BeautifulSoup(page.content, "html.parser") #parse the page using Beautiful Soup's html parser
        property_list = jumia.find(class_='properties-list')
        properties = property_list.find_all('li', class_='highlight-box') #get the list of the properties on the page
        for prop in properties:
			location = prop.find(class_='listing-address icon-location').get_text().split(',')[0] #get the location information
			price =prop.find(class_='listing-price').get_text()   #get the price of the house
			link = prop.find("a")["href"]   # get the link of the house to use for getting and/or price
			link_page = requests.get('http://house.jumia.ug'+link)
			if price == 'see details': #check if the price is listed on the list of houses
				try:
					price =get_house_price(link_page) #get the house price from the house's page
				except:
					price = 'None' #return None if there is no price
			else:
				try:
					price = int(''.join(price.split(',')).split()[-1]) # if price is shown all the list's page then obtain
				except:
					price = 'None' #return None if there is no price

			details = ','.join(get_house_details(link_page))  
			line = ','.join([details,location, str(price)])   #create the final line that will be added to the file

			print line   #print the line to the text file



#method for getting the price of a house from the house's page
def get_house_price(page):
    soup = BeautifulSoup(page.content, "html.parser")
    pr = soup.find_all('p', class_='property-price')
    price = pr[0].find('span', class_='price').get_text().strip('~')[4:]
    price = int(''.join(price.split(',')))
    return price


#method for getting the house's details from the house's page
def get_house_details(page):
    soup = BeautifulSoup(page.content, "html.parser")
    details = soup.find(class_='details')
    tables = details.find_all('table')
    rows ={}
    dets =[]  #list that will contain the house details
    attributes ={}
    
    #the details are stored in tables so we extract them from there
    for i in range(len(tables)):
        rows[i] = tables[i].find_all('tr') #get the rows in the table
        for tr in rows[i]:
            cells =tr.find_all('td') #get the cells in the row
            atts =[]
            for td in cells:
                atts.append(td.get_text().strip())
            attributes[atts[0].encode('utf-8').split(' (')[0]]= atts[1].encode('utf-8')#store all the house's attributes
    id_ = soup.find(class_='property-id has-phone').find('strong').get_text() #get the id of the house listing
    attributes['id'] = id_.encode('utf-8')
    needed =['id', 'Rooms', 'Land Size', 'Bedrooms', 'Living area', 'Baths']
    
    
    for item in needed: #only keep the attributes that are in needed
    	if item in attributes.keys():
    		dets.append(attributes[item]) # add the attribute's value to the detals
    	else:
    		dets.append('None') #if an item is needed but not in the house's listed attributes then return None

    return dets

    
if __name__ == '__main__':
	if sys.argv[1]:
		num = int(sys.argv[1]) # if number of pages to check for is provided then get houses for those number of pages (each page has 30 houses)
	else:
		num=10
	get_house_data(num)
    

