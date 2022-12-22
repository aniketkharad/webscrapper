#!/usr/bin/python -tt
import requests
import re
from bs4 import BeautifulSoup


def scrape_photos_links(html):
	dict= {}
	soup = BeautifulSoup(html, 'lxml')
	photos_items = soup.find_all('img',class_='photo-item__img')
	for img in photos_items:
		photo_url = img.get('data-big-src').split('?')[0]
		photo_name = img.get('alt')
		dict[photo_name] = photo_url
	return dict


def download_file(name_url):
	i=0
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
			for chunk in r.iter_content(1024*128):
				file.write(chunk)


def print_file_name(file_url,image_no):
	for key in file_url.keys():
		print(key+'\n'+file_url[key]+'\t\t\t\t\t'+str(image_no))
		image_no = image_no + 1
	return image_no


def main():
	collection_url = 'https://www.pexels.com/collections/feeling-happy-hzn4cx4/?page={}'#'https://www.pexels.com/collections/creatives-jccfd2o/?page={}' #'https://www.pexels.com/collections/analog-photography-401y055/?page={}' #'https://www.pexels.com/collections/fashion-w6q1n7s/?page={}' #'https://www.pexels.com/collections/behind-the-camera-r7ttfbd/?page={}'#'https://www.pexels.com/collections/minimalism-mxun625/' ###'URL'
	image_no = 1
	for page_no in range(1,100):

		r = requests.get(collection_url.format(page_no))
		
		if not r.ok:
			print('Ooops . . .\t'+r.url+'\tNOT FOUND')
		photos = scrape_photos_links(r.text)
		if len(photos) == 0:
			print('\nurl has no images\n\n')
			return
		print('\n'+r.url+'\t\t\t\t\t\t\t\t\t'+str(page_no)+'\n')
		total_images = print_file_name(photos,image_no)
		image_no = total_images
		

		#download_file(photos)


if __name__ == '__main__':
	main()