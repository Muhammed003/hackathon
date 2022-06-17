""" Importing modules """
import requests
from bs4 import BeautifulSoup
from decouple import config
URL = "https://www.furniture.kg/"
html = requests.get(URL).text
DOMEN = 'https://www.furniture.kg/'

def get_html(url: str):
	html = requests.get(url, proxies={'http': '', 'https': ''})
	return html.text


# def get_last_page(html):
# 	soup = BeautifulSoup(html, "lxml")
# 	pagination = soup.find("div", class_="pager-wrap").find_all("a")[-1].text
# 	return int(pagination)


DATA = []
count = 0
list_category = ['/bedroom-sets', '/wardrobes', '/dressers', '/hallways', '/tv-stand', '/living-room-sets', '/kitchens',
				 '/children-sets']
# list_category = ['/bedroom-sets', ]


def get_manufacture(url, title, description, image, price, id, link):
	url = url
	html2 = requests.get(url).text
	soup2 = BeautifulSoup(html2, 'lxml')
	try:
		manufacture = soup2.find(
			"div", class_="product-additional-info").text
	except:
		manufacture = ''
	baza = {
		"id": id,
		"title": title,
		"description": description,
		"image": image,
		"price": price,
		"manufacture": manufacture,
		"type": link
	}
	DATA.append(baza)


def get_data(html):
	global count
	soup = BeautifulSoup(html, "lxml")
	link = soup.find("ul", class_="gkmenu level0").find('li', class_="active").find('a').get('href')[1::]
	all_cards = soup.find('div', class_="browse-view").find_all("div", class_="product")
	for cards in all_cards:
		count += 1
		try:
			title = cards.find("div", class_="Cat_prod_info").find("h3").find("a").text
		except:
			title = ""
		try:
			desc_modified = cards.find("div", class_="razmeri_cat").text.split('|')
			description = [i.replace('\n', "").replace('\t', "") for i in desc_modified]
			description = "".join(description)
		except:
			description = ""
		try:
			image = DOMEN + cards.find("div", class_="product_img_bloc").find("a").find("img").get("src")
		except:
			image = ""
		try:
			price = cards.find("div", class_="product-price marginbottom12").find("span", 'PricesalesPrice').text.split(' сом')[0].replace(" ", "")
		except:
			price = DOMEN + cards.find("div", class_="product_img_bloc").find("a").find("img").get("src")
		get_link_manufacture = cards.find("div", class_="spacer").find("a", class_="product-overlay").get("href")
		get_link_manufacture = "https://www.furniture.kg" + get_link_manufacture

		id = count
		get_manufacture(url=get_link_manufacture, title=title, link=link,
						description=description, image=image, price=price, id=id)


def main():
	s = 0
	for list in list_category:
		s+=1
		URL = "https://www.furniture.kg"+list
		html = get_html(url=URL)
		get_data(html=html)
		print(f"Сейчас сайт парсит пожалуйста ждите осталось: {len(list_category)-s} ")


if config("parsing") == "True":
	main()



