import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import numpy as np

from pprint import pprint

import csv

"""
 Project originally made for Data Collection and Visualization class
 this is a refactored version of the webscraper, hoping to make it more readable and easily edited

 This web-scraper goes to www.stockx.com and gathers information about sneaker
 resell prices (across various brands)

 It selects a sneaker category from the dropdown menu
 and creates a list of all the subcategories (different shoe models)

 Within these subcategories there are links to individual shoe colorways, 
 information about resell price history, retail price, release date and more 
 is within this page. The program pulls this data from this page
"""


"""
Gathers desired information about the sneaker at the given url.

@param url: url to a sneaker's stockX listing
@param driver: reference to selenium webdriver object
@return: dictionary of information
"""
def get_shoe_data(url, driver):
    output = {}

    # open link to shoe
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    print("\tOpening ", url)
    driver.get(url)

    # store url in dictionary
    output.update({'url' : url})

    # get release date
    try:
        release_date = {'release_date'  : driver.find_element_by_xpath(
            "//span[@data-testid='product-detail-release date']").text}
    except:
        release_date = {'release_date'	: 'N/A'}
    output.update(release_date)

    # get retail price
    try: 
        retail_price = {'retail_price' : driver.find_element_by_css_selector(
    	"div.detail:nth-child(3) > span:nth-child(2)").text}
    except:
        retail_price = {'retail_price' : 'N/A'}
    output.update(retail_price)

    gauges = driver.find_elements_by_xpath("//div[@class='gauges']/div[@class='gauge-container']")

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    for gauge in gauges:
        gauge_text = gauge.find_element_by_css_selector("div:nth-child(2)").text
        if gauge_text == "# of Sales":
            # get # of sales
            number_of_sales = {'number_of_sales' : gauge.find_element_by_css_selector("div:nth-child(3)").text}
            output.update(number_of_sales)

        elif "Price Premium" in gauge_text:
            # get price premium
            price_premium = {'price_premium' : gauge.find_element_by_css_selector("div:nth-child(3)").text}
            output.update(price_premium)

        elif gauge_text == "Average Sale Price":
            # get average sale price
            average_sale_price = {'average_sale_price' : gauge.find_element_by_css_selector("div:nth-child(3)").text}
            output.update(average_sale_price)


    # TODO: save image of the shoe
    # TODO: save name of the shoe
    # TODO: save style code
    # TODO: save StockX Ticker code

    # close tab
    driver.close()

    return output

"""
Traverses a list of categories and finds every shoe in that category
saving the dictionary of data scraped from that shoe's page

Ex:
    <traverse_model_category_list>
    Brand:Jordan
        <get_category_data>
        Category:1
            <get_all_data_on_page>
            Page:3
                <get_shoe_data>
                shoe1
                <get_shoe_data>
                shoe2
                ...
                <get_shoe_data>
                shoen

@param category_list: list of all shoe categories
@param driver: reference to selenium webdriver object
"""
def traverse_model_category_list(category_list, driver):
    for shoe_category in category_list:
        get_category_data(shoe_category, driver)

        #close category page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

"""
helper function to save lists of dictionaries to the correct file

@param directory: directory to be saved in
@param page_num: number of the page it was pulled from
@param page_dicts: list of data-containing dictionaries
"""
def save_dict_to_file(directory, page_num, page_dicts):
    with open(directory + "page" + str(page_num) + ".csv", 'w') as f:
        w = csv.DictWriter(f, page_dicts[0].keys())
        w.writeheader()
        w.writerows(page_dicts)

"""
helper function that gets all of the data within one category and writes them 
to files in the data directory

@param shoe_category: shoe category web element
@return: dictionary of all data within that category
"""
def get_category_data(shoe_category,driver):
    link_to_shoe_category = shoe_category.get_attribute('href')

    category_directory = "./data/sneakers/" + link_to_shoe_category[19:] + "/"
    # if the desired directory doesn't exist
    if (not os.path.isdir("./data/sneakers/" + link_to_shoe_category[19:])):
        # create the desired directory
        os.makedirs(category_directory, exist_ok=True)

    #TODO: go to next page if there is another page
    page_num = 1
    page_url = link_to_shoe_category

    # get all data on the page, if there is a next page get the info on that page too
    while True:
        # open link to category in new tab
        driver.execute_script("window.open('');")
        if (page_num != 1):
            driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        print("Opening ", page_url)
        driver.get(page_url)
        time.sleep(2)

        page_dicts = get_all_data_on_page(driver)
        save_dict_to_file(category_directory, page_num, page_dicts)


        # check if the right arrow refers to stockx home page because for some 
        # reason that's what the right arrow does if there isn't a next page

        right_arrows = driver.find_elements_by_xpath(
        	"//ul[contains(@class,'ButtonList')]/a[contains(@class,'NavButton')]")

        page_url = right_arrows[1].get_attribute('href')
        if (page_url == 'https://stockx.com/'):
            break

        page_num += 1
        #print(right_arrows)


"""
helper function that gets all shoe data on the current open page and returns it in a list of dictionaries

@param driver: reference to selenium webdriver object
"""
def get_all_data_on_page(driver):
    page_dicts = []
    # grab all links to shoes on the page
    list_of_shoes = driver.find_elements_by_xpath(
            "//div[@class='browse-grid']/div[@class='tile browse-tile']/*/a"
            )
    for i, shoe in enumerate(list_of_shoes):
        shoe_link = shoe.get_attribute('href')
        shoe_dict = get_shoe_data(shoe_link, driver)
        # switch back to shoe listings page
        driver.switch_to.window(driver.window_handles[1])

        pprint(shoe_dict, indent=9)
        # add to page's dictionary
        page_dicts.append(shoe_dict)

        #
        # COMMENT/REMOVE THIS BREAK TO ALLOW THE SCRAPER TO ACCESS EVERY LISTING
        #
        # 
        break

    return page_dicts



"""
Main function
Calls get_brands to obtain elements

"""
def main():
    driver = webdriver.Firefox()

    url = 'https://stockx.com/'
    driver.get(url)

    print("waiting 2 seconds")
    time.sleep(2)
    print("done waiting\n\n")

    for brand_element in get_brands(driver):
        # hover over brand menu element
        brand_element.click() # don't know why but you have to click to open this dropdown
        print("hovering on ",brand_element)
        time.sleep(1)

        #generate list of models/categories
        model_list = driver.find_element_by_css_selector('div.categoryColumn:nth-child(3)')
        model_list = model_list.find_elements_by_xpath('./a')
        
        traverse_model_category_list(model_list, driver)

        print("All Done!")

"""
Obtains a list of all brand web elements using the "browse" dropdown at the top of the site

@param: reference to selenium webdriver object
"""
def get_brands(driver):
    action = ActionChains(driver)

    wait = WebDriverWait(driver, 10)
    # hover over browse menu
    browse_dropdown = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.dropdown:nth-child(1)'))
                )
    action.move_to_element(browse_dropdown).perform()
    print("browser_dropdown")
#    time.sleep(1)

    # hover over sneakers menu
    sneaker_dropdown = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,'a.category:nth-child(1)'))
               )
    action.move_to_element(sneaker_dropdown).perform()
    print("sneaker_dropdown")
#    time.sleep(1)

    # make list of all brand elements

# I want to make a list of all clickable elements underneath the sneakers node in the dropdown menu
# 
# However, the html of the dropdown menu doesn't function as a tree with each clickable element as a node and instead 
# puts them all on the same level with the same class name. This means that we can't use xpath to simply 
# grab all clickable subelements underneath the element we have selected (there will be none)
#
# the element div.categoryColumn:nth-child(2) doesn't exist until 
# sneaker_dropdown is hovered over once it is hovered the element is there and we can use xpath to make a 
# list of all clickable elements in that category

    brand_list_dropdown = driver.find_element_by_css_selector('div.categoryColumn:nth-child(2)')
    brand_list_dropdown = brand_list_dropdown.find_elements_by_xpath('./a')

    # get rid of extra glitchy link
    del brand_list_dropdown[-1]

    return brand_list_dropdown

out = None
if __name__ == '__main__':
    out = main()


driver = webdriver.Firefox()

#pprint(get_shoe_data("https://stockx.com/adidas-yeezy-750-cleat", driver))


