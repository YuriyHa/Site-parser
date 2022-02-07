import csv
from bs4 import BeautifulSoup
import requests
from datetime import datetime

csv_file=open('CAVALLO.csv', 'w', encoding='UTF8')
wr=csv.writer(csv_file)

count_=0
time=datetime.now()

def find_cats(url) : 
    html=requests.get(url).text
    # print(datetime.now()-start_time)

    soup = BeautifulSoup(html)
    cats = soup.find_all('a', class_='teaser teaser-3col')
    for cat in cats: 
        find_links(cat.find('h2').text, cat['href'])
        
    # soup = BeautifulSoup(html)
    # cats = soup.find_all('div', class_='teaser-3col')
    # for cat in cats: 
    #     href=cat.find('a')['href']
    #     text=cat.find('span').text
    #     find_links(text, href)

def find_links(cat, url): 
    html=requests.get(url).text
    # print(datetime.now()-start_time)

    soup = BeautifulSoup(html)
    links = soup.find_all('a', class_='catalog-product-list-grid')
    
    # print("\n\n-----\n\n")
    
    global count_    
    
    for link in links:
    # link=links[0]        
        product_url=link.get('href')
        parse_url(cat,product_url)
        count_+= 1
        print(count_, ' -- time: ', datetime.now()-time)
        
    iNext=soup.find('a', class_='i-next')
    if iNext != None:
        find_links(cat ,iNext['href']) 
        


def parse_url(cat, url): 
    print('request get')

    product_html=requests.get(url).text
    product_soup=BeautifulSoup(product_html)

    # find name
    product_div_name=product_soup.find_all('div', class_="product-name")
    product_name=product_div_name[0].text
    # print(product_name)


    # find short dscription
    product_description_short=product_soup.find_all('div',class_='std')[0].text
    # print(product_description_short)

    # find full description
    product_description_full=product_soup.find_all('div',{'id': 'product_tabs_description_tabbed_contents'})
    product_description_full_text=product_description_full[0].find('div', class_='std').text
    # print(product_description_full_text)

    # # find colors 
    # product_colors=product_soup.find('ul', {"id": "swatches-options-92"})
    # print(product_colors)
    # colors=product_colors.find_all('a')
    # for a in colors: 
    #     print(a["style"].split(':')[1])
    # find image 
    image_links=[]
    images=product_soup.find_all('li',class_='product-image-thumbs')
    for image in images: 
        a=image.find('a')
        image_links.append(a['href'])


    # find prise 
    product_prise=product_soup.find_all('span', class_='price')[0].text
    # print(product_prise)
    
    
    wr.writerow([{
        'category':cat, 
        'name':product_name.strip(), 
        'short-description':product_description_short.strip(), 
        'full-description': product_description_full_text.strip(), 
        'price': product_prise, 
        'images': image_links, 
    }])
        
find_cats("https://www.waldhausen.com/it/cavallo.html")        

csv_file.close()