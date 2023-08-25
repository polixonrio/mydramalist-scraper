from selenium import webdriver # Import Selenium
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors') # Ignore certificate errors
options.add_argument("--start-maximized") # Open in maximized mode
driver = webdriver.Chrome(options=options) 

import time

def get_soup_with_url(url,time_sleep=10):
    """This function returns a Beautiful Soup object for a given url"""
    driver.set_window_size(1920, 1080) # Set window size
    driver.maximize_window()
    driver.get(url) # Open the url in the webdriver
    time.sleep(time_sleep) # sleep for specified time

import requests
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import re



for zx in tqdm(range(7000,8000), desc="Progress - Running", unit="page"):
    
    URL = f"https://mydramalist.com/reviews/shows?page={zx}"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
    response = requests.get(URL, timeout=600, headers=headers)
    soup_data = BeautifulSoup(response.text, 'html.parser')
    single_page_review_list = []
    review_ratings = soup_data.find_all("div", class_="box pull-right text-sm m-a-sm")
    people_found_useful = soup_data.find_all("div", class_="user-stats")# works
    datetimestamp = soup_data.find_all("small", class_="datetime") # works
    col_to_get_watch_status = soup_data.find_all("div", class_="col-sm-3 text-sm text-right hidden-xs-down") # works
    episode_watched = soup_data.find_all("div", class_="episodes-seen text-muted")
    col_with_review_show_title = soup_data.find_all("div", class_="col-sm-9")
    col_with_review = soup_data.find_all("div", class_="col-sm-12")

    review_ratings_list = [item.text.strip() for item in review_ratings]
    people_found_useful_list = [item.text.strip() for item in people_found_useful]
    datetimestamp_list = [item.text.strip() for item in datetimestamp]
    episode_watched_list = [item.text.strip() for item in episode_watched]
    

    col_to_get_watch_status_list = []

    for b in col_to_get_watch_status:
        vs = b.find("span", class_="review-tag")
        col_to_get_watch_status_list.append(vs.text.strip())

    col_with_review_show_title_list = []

    for c in col_with_review_show_title:
        show_title = c.find("a", class_="text-primary")
        col_with_review_show_title_list.append(show_title.text.strip())

    col_with_review_list = []

    for xc in col_with_review:
        col_with_review_list.append(xc.text.strip())

    while len(col_with_review_list) != 15:
        if len(col_with_review_list):
            print(zx)
        URL = f"https://mydramalist.com/reviews/shows?page={zx}"
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
        # response = requests.get(URL, timeout=600, headers=headers)
        soup_data = get_soup_with_url(URL,time_sleep=10)

        single_page_review_list = []
        review_ratings = soup_data.find_all("div", class_="box pull-right text-sm m-a-sm")
        people_found_useful = soup_data.find_all("div", class_="user-stats")# works
        datetimestamp = soup_data.find_all("small", class_="datetime") # works
        col_to_get_watch_status = soup_data.find_all("div", class_="col-sm-3 text-sm text-right hidden-xs-down") # works
        episode_watched = soup_data.find_all("div", class_="episodes-seen text-muted")
        col_with_review_show_title = soup_data.find_all("div", class_="col-sm-9")
        col_with_review = soup_data.find_all("div", class_="col-sm-12")

        review_ratings_list = [item.text.strip() for item in review_ratings]
        people_found_useful_list = [item.text.strip() for item in people_found_useful]
        datetimestamp_list = [item.text.strip() for item in datetimestamp]
        episode_watched_list = [item.text.strip() for item in episode_watched]
        

        col_to_get_watch_status_list = []

        for b in col_to_get_watch_status:
            vs = b.find("span", class_="review-tag")
            col_to_get_watch_status_list.append(vs.text.strip())

        col_with_review_show_title_list = []

        for c in col_with_review_show_title:
            show_title = c.find("a", class_="text-primary")
            col_with_review_show_title_list.append(show_title.text.strip())

        col_with_review_list = []

        for xc in col_with_review:
            col_with_review_list.append(xc.text.strip())




    col_with_review_list_cleaned = []
    review_content_pattern = r'Overall \d\.?\d\s+Story\s+\d\.?\d\s+Acting\/Cast\s+\d\.?\d\s+Music\s+\d\.?\d\s+Rewatch\s+Value\s+\d\.?\d\s*(?:\bThis review may contain spoilers\b)?(.+?)(?:\bRead More\b)?\s*Was this review helpful to you\? Yes No Cancel'
    for mc in col_with_review_list:
        
        modified_string = mc.replace("\n", "")
        modified_string = modified_string.replace("\r", "")
        review_result = re.search(review_content_pattern, modified_string)
        # Find the matching string
        

        if review_result:
            extracted_string = review_result.group(1)
            col_with_review_list_cleaned.append(extracted_string.strip())
    
    if len(col_with_review_list) != len(col_with_review_list_cleaned):
        print(len(col_with_review_list))
        print("--------------------------------------------------")
        print(len(col_with_review_list_cleaned))
        print(col_with_review_list)
        print(col_with_review_list_cleaned)
        break


    pp = col_with_review_list
    lp = col_with_review_list_cleaned
    overall_rating_list = []
    story_rating_list = []
    cast_rating_list = []
    music_rating_list = []
    rewatch_value_list = []
    ratings_pattern = r'(\w+)\s+([\d.]+)'
    values = 0
    terms = 0  

    for mc in review_ratings_list:

        matches = re.findall(ratings_pattern, mc)

        values = [match[1].strip() for match in matches]
        terms = [match[0].strip() for match in matches]  
        # print(terms)
        # print(values)
        for mci in range(len(terms)):
            if terms[mci] == "Overall":
                overall_rating_list.append(values[mci])
            elif terms[mci] == "Story":
                story_rating_list.append(values[mci])
            elif terms[mci] == "Cast":
                cast_rating_list.append(values[mci])
            elif terms[mci] == "Music":
                music_rating_list.append(values[mci])
            elif terms[mci] == "Value":
                rewatch_value_list.append(values[mci])     


    for i in range(15):
        single_review_dict = {'Show Title':col_with_review_show_title_list[i], 'Overall_Rating': overall_rating_list[i], 'Story_Rating': story_rating_list[i], 'Acting/Cast_Rating': cast_rating_list[i], 
                            'Music_Rating': music_rating_list[i], 'Rewatch Value': rewatch_value_list[i] ,'Episode Watched':episode_watched_list[i], 
                            'Watch Status':col_to_get_watch_status_list[i], 'People Found Useful':people_found_useful_list[i], 
                            'Review Posted How Long Ago':datetimestamp_list[i], 'Review':col_with_review_list_cleaned[i]}
        single_page_review_list.append(single_review_dict)
    # print(zx, single_page_review_list)
    new_df = pd.DataFrame(single_page_review_list)
    if zx == 7000:
        new_df.to_csv('re8.csv', mode='a', index=False)
    else:
        new_df.to_csv('re8.csv', mode='a', header=False,index=False)