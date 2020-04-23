def scrape():
    # Import Libraries
    #import requests
    #from requests_html import AsyncHTMLSession
    #asession = AsyncHTMLSession()
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import pymongo
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    # declaring element names to grab
    article_header = 'slide'
    content_title = 'content_title'
    content_body = 'article_teaser_body'
    wait_element = 'news'
    mars_news_url = "https://mars.nasa.gov/news/"
    driver = webdriver.Chrome(r'C:\Users\sonal\Documents\USCBootCamp\Drivers\chrome\chromedriver.exe')
    # get url and wait until page is fully loaded before proceeding
    driver.get(mars_news_url)
    time.sleep(10)    
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,wait_element))
        )
    except:
        pass
    
    slide = driver.find_elements_by_class_name(article_header)[0]

    first_article_headline = slide.find_element_by_class_name(content_title).text
    first_article_paragraph = slide.find_element_by_class_name(content_body).text

    # ## Part 2 JPL Mars Space Images

    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    featured_image_response = requests.get(featured_image_url)

    if featured_image_response.status_code == 200:
        featured_image_html = featured_image_response.text

    featured_image_soup = BeautifulSoup(featured_image_html, "html.parser")
    image_element = featured_image_soup.find("a", {"class": "button fancybox"}).get('data-fancybox-href')
    
    featured_image_url = "https://www.jpl.nasa.gov" + image_element


    # ## Part 3 Mars Weather

    weather_tweets_url = "https://twitter.com/marswxreport?lang=en"
    driver = webdriver.Chrome(r'C:\Users\sonal\Documents\USCBootCamp\Drivers\chrome\chromedriver.exe')
    driver.get(weather_tweets_url)
    time.sleep(10)
    #Get using Xpath
    mars_weather = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div[2]/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span")
   
    weather_tweet = mars_weather.text


    # ## Part 4 Mars Facts

    mars_fact_url = "https://space-facts.com/mars/"
    all_mars_fact_tables = pd.read_html(mars_fact_url)
    df_mars_facts = all_mars_fact_tables[0]
    df_mars_facts.columns = ["Measure", "Number"]


    # ## Part 5 Mars Hemispheres


    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    mars_hemisphere_response = requests.get(mars_hemisphere_url)

    if mars_hemisphere_response.status_code == 200:
        mars_hemisphere_html = mars_hemisphere_response.text

    def get_full_image_link(link):

        response = requests.get(link)

        if response.status_code == 200:
            html = response.text
        
        soup = BeautifulSoup(html, "html.parser")
        
        img_link = soup.find("a", text="Original").get("href")
        title = soup.find("h2", class_="title").text.split(" Enhanced")[0]
            
        return [title, img_link]

    mars_hemisphere_soup = BeautifulSoup(mars_hemisphere_html, "html.parser")
    link_elements = mars_hemisphere_soup.findAll("a", {"class": "itemLink product-item"})
    full_page_links = [dict(title=get_full_image_link("https://astrogeology.usgs.gov" + le.get('href'))[0], img_url=get_full_image_link("https://astrogeology.usgs.gov" + le.get('href'))[1]) for le in link_elements]

    return dict(first_article_headline=first_article_headline,
    first_article_paragraph = first_article_paragraph,
    featured_image_url=featured_image_url,
    weather_tweet=weather_tweet,
    df_mars_facts=df_mars_facts.to_dict("records"),
    full_page_links=full_page_links
    )
if __name__ == "__main__":

    print(scrape())

