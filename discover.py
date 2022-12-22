#!/usr/bin/python -tt
import requests
import re
from bs4 import BeautifulSoup
import csv


def scrape_category_links(html):
	dict= {}
	url = 'https://www.pexels.com'
	soup = BeautifulSoup(html, 'lxml')
	url_link = soup.find('div', class_='l-container-center clear').find('ul', class_="collections l-row js-collection-container").find_all('a', class_='absolute')

	names = []
	numb = []
	for ww in range(0,9):
		url_name = soup.find('div', class_='l-container-center clear').find('ul', class_="collections l-row js-collection-container").find_all('h3', class_='collection__title')[ww].text
		url_no = soup.find('div', class_='l-container-center clear').find('ul', class_="collections l-row js-collection-container").find_all('p', class_='collection__subtitle')[ww].text
		match1 = re.search(r'\w+.*',url_name)
		match2 = re.search(r'\d+',url_no)
		names.append(match1.group()+'__'+match2.group())

	links = []
	for a in url_link :
		category_url = url + a.get('href')
		links.append(category_url)

	for i in range(9):
		dict[names[i]] = links[i]
	#print(dict)

	return dict


def link_number(cat_name,link_no):
	for key in cat_name.keys():
		print(key+'\n'+cat_name[key]+'\t\t\t\t\t'+str(link_no))
		link_no = link_no + 1
	return link_no


def main():
	main_url = 'https://www.pexels.com/discover/?page={}'
	link_no = 1
	dict_main = {}
	for page_no in range(1,24):
		r = requests.get(main_url.format(page_no), allow_redirects=True)
		if not r.ok:
			print('Ooops . . .\t'+r.url+'\tNOT FOUND')
		
		category = scrape_category_links(r.text)
		dict_main.update(category)
		if len(category) == 0:
			print('\nCategory links completed\n\n')
			return

		print('\n'+r.url+'\t\t\t\t\t\t\t\t\t\t\t\t\t'+str(page_no)+'\n')
		total_link = link_number(category,link_no)
		link_no = total_link

		#print('\n__0__\n')
		print(category)
	print('\n\n')
	print(dict_main)

	w = csv.writer(open("category_links.csv","w"))
	for key, val in dict_main.items():
		w.writerow([key,val])




if __name__ == '__main__':
	main()