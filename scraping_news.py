from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# executable_path = {"executable_path': ChromeDriverManager().install()"}
# browser = Browser("chrome", executable_path="chromedriver", headless=True)

def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    

    html = browser.html
    news_soup = soup(html, "html.parser")

    try:

        list = news_soup.select_one('div', id_='news')
    
        list.find("div", class_="content_title")
    
        title = list.find("div", class_='content_title').get_text()  
        para_news = list.find("div", class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    return title, para_news


def featured_image(browser):

  url = 'https://spaceimages-mars.com/'
  browser.visit(url)

  html = browser.html
  image_soup = soup(html,'html.parser')
  try:
     image_results = image_soup.find_all("div",class_="floating_text_area")
     relative_img_path = image_results[0].a['href']
  except AttributeError:
        return None


  featured_img = 'https://spaceimages-mars.com/' + relative_img_path

  return featured_img

#Mars data

def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    try:
        html_df = pd.read_html("https://galaxyfacts-mars.com/")
        Mars_fact_df = html_df [1]
    except BaseException:
        return None
    Mars_fact_df.columns=["Description", "Value"]
    Mars_fact_df.set_index("Description", inplace=True)

    return Mars_fact_df.to_html()

#Mars Hemispheres

def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = "https://marshemispheres.com/"
    browser.visit(url)

    hemisphere_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item img")
    for i in range(len(links)):
        hemisphere={}
    
    #Find elements going to click link.
        browser.find_by_css('a.product-item img')[i].click()
    
    #Find sample image link
        sample_element=browser.links.find_by_text('Sample').first
    
    # Get hemisphere Title 
        hemisphere['img_url']=sample_element['href']
    
    # Get hemisphere Title 
        hemisphere['title']=browser.find_by_css('h2.title').text
    
    # Add Objects to hemisphere_image_urls list
        hemisphere_urls.append(hemisphere)
    
    #Go Back
        browser.back()
    return hemisphere_urls


# main Scraping 
def scrape_all():
    # browser = init_browser()
    executable_path = {'executable_path': "chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    title, para_news = mars_news(browser)
    featured_img = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()
    print(facts)
    
    data = {
        "news_title": title,
        "news_paragraph": para_news,
        "featured_image": featured_img,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }

    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())
