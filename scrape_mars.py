import datetime
from splinter import Browser
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
import requests
import time 

#!which chromedriver

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html=browser.html
    new_soup = bs(html, 'html.parser')
    slide_elem = new_soup.select_one('ul.item_list li.slide')

    slide_elem.find("div", class_='content_title')

    news_title = slide_elem.find("div", class_='content_title').get_text()

    news_p = slide_elem.find("div", class_='article_teaser_body').get_text()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    
    browser.is_element_present_by_text('Image Details', wait_time=1)

    
    html=browser.html
    image_soup= bs(html, 'html.parser')
    
    image_url_rel=image_soup.select_one('figure.lede a img').get("src")
    

    img_url = f'https://www.jpl.nasa.gov{image_url_rel}'

    df= pd.read_html('https://space-facts.com/mars/')[0]

    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    mars_facts = df.to_html()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")
    for i in range(len(links)):
        hemisphere={}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back() 
    
    Mars_data = {
        "News": news_title,
        "News_P": news_p,
        "image": img_url,
        "Mars_facts": mars_facts,
        "Hemispheres": hemisphere_image_urls
    }
    

    browser.quit()

    return Mars_data

