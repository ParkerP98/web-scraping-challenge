# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time

def scrape():

    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(nasa_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    p_result = soup.find('div', class_='rollover_description_inner')
    news_p = p_result.text.strip()
    result = soup.find('div', class_='content_title')
    news_title = result.text.strip()

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    splint_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(splint_url)
    time.sleep(1)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(1)
    browser.links.find_by_partial_text('more info').click()
    time.sleep(1)
    soup = BeautifulSoup(browser.html, 'html.parser')

    img = soup.findAll('img', class_='main_image')

    img_url = 'https://www.jpl.nasa.gov'
    for image in img:
        img_url = img_url + image['src']

    browser.quit()

    browser = Browser('chrome', **executable_path, headless=False, incognito=True)

    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter_url)
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')
    first_tweet = soup.findAll('div', class_='css-1dbjc4n r-18u37iz' )

    soup = BeautifulSoup(str(first_tweet), 'html.parser')

    f_tweet = soup.findAll('span')
    mars_weather = f_tweet[4].text.strip()

    browser.quit()

    table_url = 'https://space-facts.com/mars/'
    df = pd.read_html(table_url)
    time.sleep(1)
    mars_facts = df[0]
    mars_earth = df[1]
    mars_facts.rename(columns={0: 'Descriptor', 1:'Description'}, inplace=True)
    mars_facts = mars_facts.to_html()
    mars_earth = mars_earth.to_html()

    hem_dicts = []
    hem_titles = []
    hem_url_list = []
    hem_names = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser('chrome', **executable_path, headless=False)

    def hem_to_dict(title, url):
        d = {'title': title, 'img_url': url}
        return d

    def get_pic_url():
        browser.links.find_by_partial_text('Sample').click()
        time.sleep(2)
        parent_window = browser.driver.current_window_handle
        all_windows = browser.driver.window_handles
        for window in all_windows:
            if window != parent_window:
                browser.driver.switch_to.window(window)
        time.sleep(1)
        temp_url = browser.url
        browser.driver.close()
        browser.driver.switch_to.window(parent_window)
        return temp_url

    for hem in hem_names:
        browser.visit(hem_url)
        time.sleep(1)
        browser.links.find_by_partial_text(hem).click()
        time.sleep(1)
        t = browser.title.split('|')
        t = t[0]
        t = t.strip()
        hem_titles.append(t)

        url = get_pic_url()
        hem_url_list.append(url)
    
    browser.quit()

    for i, x in enumerate(hem_titles):
        hem_dicts.append(hem_to_dict(x, hem_url_list[i]))

    

    return_dict = { 'news_title': news_title,
                    'news_p': news_p, 
                    'featured_image_url': img_url, 
                    'mars_weather': mars_weather,
                    'mars_facts': mars_facts,
                    'hem_dicts': hem_dicts
                    }

    return return_dict













