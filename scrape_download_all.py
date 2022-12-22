#!/usr/bin/pyton -tt

import requests
import re
from bs4 import BeautifulSoup
import os
import csv


def scrape_category_links(html):###############################################		CALL 1
	dict= {}
	url = 'https://www.pexels.com'
	soup = BeautifulSoup(html, 'lxml')
	url_link = soup.find('div', class_='l-container-center clear').find('ul', class_="collections l-row js-collection-container").find_all('a', class_='absolute')

	names = []
	numb = []
	for ww in range(0,9):
		url_name = soup.find('div', class_='l-container-center clear').find('ul', class_="collections l-row js-collection-container").find_all('h3', class_='collection__title')[ww].text
		url_no = soup.find('div', class_='l-container-center clear').find('ul', class_="collections l-row js-collection-container").find_all('p', class_='collection__subtitle')[ww].text
		token = re.search(r'\w+video\w+',url_name)
		if token:
			continue
		match1 = re.search(r'\w+.*',url_name)
		text = " ".join(re.findall(r"[\w']+", match1.group(0)))
		#text = match1.group()
		#if len(text.split(':')) > 1:
		#	text = "".join(text.split(':'))
		match2 = re.search(r'\d+',url_no)
		names.append(text+'__'+match2.group())

	links = []
	for a in url_link :
		category_url = url + a.get('href')
		links.append(category_url)

	for i in range(9):
		dict[names[i]] = links[i]
	
	print(sorted(dict.keys()))
	return dict


def link_number(cat_name,link_no):#############################################		CALL 2
	for key in cat_name.keys():
		print(key+'\n'+cat_name[key]+'\t\t\t\t\t'+str(link_no))
		link_no = link_no + 1
	return link_no


def createFolder(directory):###################################################		CALL 3
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def scrape_photos_links(html):#################################################		CALL 4
	dict= {}
	soup = BeautifulSoup(html, 'lxml')
	photos_items = soup.find_all('img',class_='photo-item__img')
	for img in photos_items:
		photo_url = img.get('src').split('?')[0]
		photo_name = " ".join(re.findall(r"[\w']+", img.get('alt')))		#this will split the string to char only and then join remaining to give file name to images.
		dict[photo_name] = photo_url
	return dict


def print_file_name(file_url,image_no):########################################		CALL 5
	for key in file_url.keys():
		print(key+'\n'+file_url[key]+'\t\t\t\t\t'+str(image_no))
		image_no = image_no + 1
	return image_no


def download_file(name_url):###################################################		CALL 6
	i=1
	for key in name_url.keys():
		print(key+'\n'+name_url[key])
		filename = key+str('.jpeg')
		r = requests.get(name_url[key], stream=True)
		if not r.ok:
			print('Download failed . . .\n')
		with open(filename, 'wb') as file:
			if i == 1:
				print('downloading ' + str(i) + 'st image . . . \n')
				i=i+1
			elif i == 2:
				print('downloading ' + str(i) + 'nd image . . . \n')
				i=i+1
			elif i == 3:
				print('downloading ' + str(i) + 'rd image . . . \n')
				i=i+1
			else:
				print('downloading ' + str(i) + 'th image . . . \n')
				i=i+1
			for chunk in r.iter_content(1024*1800):
				file.write(chunk)


def main():
	main_url = 'https://www.pexels.com/discover/?page={}'
	link_no = 1
	dict_main = {}
	for page_no in range(1,24):
		r = requests.get(main_url.format(page_no), allow_redirects=True)
		if not r.ok:
			print('Ooops . . .\t'+r.url+'\tNOT FOUND')
		
		category = scrape_category_links(r.text)##############################		CALL 1
		dict_main.update(category)
		if len(category) == 0:
			print('\nCategory links completed\n\n')
			break

		print('\n'+r.url+'\t\t\t\t\t\t\t\t\t\t\t\t\t'+str(page_no)+'\n')
		total_link = link_number(category,link_no)############################		CALL 2
		link_no = total_link
	print('\n\n')
	print(dict_main)
	print(sorted(dict_main.keys()))
	print(len(dict_main.keys()))

	for key in sorted(dict_main.keys()):
		match = re.search(r'\w+.*',key).group().split('nemagra')					#1
		if len(match) > 1:
			del dict_main[key]
	
	for key in sorted(dict_main.keys()):
		match = re.search(r'\w+.*',key).group().split('Video') 						#3
		if len(match) > 1:
			del dict_main[key]

	for key in sorted(dict_main.keys()):
		match = re.search(r'\w+.*',key).group().split('an patter') 						#3
		if len(match) > 1:
			del dict_main[key]

	for key in sorted(dict_main.keys()):
		match = re.search(r'\w+.*',key).group().split('apse Of Sk') 						#3
		if len(match) > 1:
			del dict_main[key]

	cwd = os.getcwd()
	print("Current working directory is:", cwd) 

	createFolder('./Raw files/')##################################################		CALL 3
	os.chdir('./Raw files/')

	w = csv.writer(open("category_links.csv","w", encoding="utf-8"))
	for key, val in sorted(dict_main.items()):
		w.writerow([key,val])

	nmn = 1
	photo_data = {}
	all_links = {}

	
	for key in sorted(dict_main.keys()):
		cwd = os.getcwd()
		print("Current working directory is:", cwd) 

		createFolder('./{}/'.format(key))
		os.chdir('./{}/'.format(key))
		print(nmn)###################################	PERFORM A OPERATOIN INSIDE CREATED DIRECTORY
		nmn = nmn + 1
		cwd = os.getcwd()
		print("Current working directory is:", cwd)

		collection_url = dict_main[key] + '?page={}'
		image_no = 1
		for page_no in range(1,24):

			r = requests.get(collection_url.format(page_no))
			
			if not r.ok:
				print('Ooops . . .\t'+r.url+'\tNOT FOUND')
			#check_image(r.text)
			photos = scrape_photos_links(r.text)##############################		CALL 4
			if len(photos) == 0:
				print('\nurl has no images\n\n')
				break
			print('\n'+r.url+'\t\t\t\t\t\t\t\t\t'+str(page_no)+'\n')
			photo_data.update(photos)
			total_images = print_file_name(photos,image_no)###################		CALL 5
			image_no = total_images
			download_file(photos)#############################################		CALL 6 		####################################!!!!!!!!!!!!!!!!!!

		print(photo_data)
		w = csv.writer(open("{}.csv".format(key),"w", encoding="utf-8"))
		for key, val in sorted(photo_data.items()):
			w.writerow([key,val])
		all_links.update(photo_data)

		photo_data.clear()

		os.chdir('..')
		cwd = os.getcwd()
		print("Current working directory is:", cwd)
		print('\n')
	w = csv.writer(open("all_links.csv","w", encoding="utf-8"))
	for key, val in sorted(all_links.items()):
		w.writerow([key,val])
	print('\n\n\n\n\nTASK COMPLETED . . . . .')
	




if __name__ == '__main__':
	main()