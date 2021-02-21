from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pymongo
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    mars_dict = {}

    #URL of the page to scrape
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #HTML
    html = browser.html

    #Parse HTML with Beautiful Soup
    soup = bs(html, 'lxml')

    #Retrieve news titles and paragraphs
    news_title = soup.find("div", class_="content_title").text
    news_summary = soup.find("div", class_="rollover_description_inner").text

#Mars Facts

    url = 'http://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)

    mars_facts_df = tables[0]

    #Assign the columns
    mars_facts_df.columns = [Characteristics, Value]
    html_table = mars_facts_df.to_html(table_id="html_tbl_css", justify='left',index=False)

    #Use pandas to convert the data to a HTML table string
    html_table= mars_facts_df.to_html()

    #Hemisphere link
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    #HTML Object
    html_hemispheres = browser.html

    soup = bs(html_hemispheres, 'lxml')

    #Extract the hemispheres items url
    mars_hemispheres = soup.find('div', class_='collapsible results')
    hemispheres = mars_hemispheres.find_all('div', class_='item')

    mars_hemisphere_pictures = []

    for hemi in hemispheres:

        #Extract title
        hemisphere = hemi.find('div', class_="description")
        title = hemisphere.h3.text
        title = title.strip('Enhanced')

        #Extract images
        end_link = hemisphere.a["href"]
        browser.visit(main_url + end_link)

        img_html = browser.html
        img_soup = BeautifulSoup(img_html, 'html.parser')

        img_link = img_soup.find('div', class_='downloads')
        img_url = img_link.find('li').a['href']

         #Storage Dictionary
        img_dict = {}
        img_dict['title'] = title
        img_dict['Picture URL'] = img_url

          #Add data to list
        mars_hemisphere_pictures.append(img_dict)

    #close browser window
        browser.quit()

#Create a summary dictionary of scraped data.
    mars_dic = {
    'Topic': news_title,
    'Summary': news_summary,
    'Mars Facts & Values': mars_facts_html,
    'Pictures': mars_hemisphere_pictures
}
return (mars_dic)

import pymongo
from pymongo import MongoClient

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

#Define database and collection
db = client.mars_mission_db
collection = db.mars_dic
collection.insert_one(mars_dic)

mission_to_mars_data = db.mars_dic.find()
for data in mission_to_mars_data:
    print(data)

    

    
    




