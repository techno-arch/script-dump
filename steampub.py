#!/usr/bin/env python3
#writen by thomasarc (1101655450354720870) on discord under GPLv3 license
import httpx as requests
import sys
import json
from bs4 import BeautifulSoup
#pub is the publisher name as seen in the steam url
def base_url(pub):
    id_int=requests.get(f"https://store.steampowered.com/publisher/{pub}/ajaxgetfilteredrecommendations/").json()["total_count"]
    return requests.get(
        f"https://store.steampowered.com/publisher/{pub}/ajaxgetfilteredrecommendations/",
        params = {
        'query': '',
        'start': '0',
        'count': str(id_int),
        'dynamic_data': '',
        'tagids': '',
        'sort': 'newreleases',
        'app_types': 'game',
        'curations': '',
        'reset': 'false',
    }
    )

#html_list=base_url(pub).json()["results_html"]

def html2dict(html_list):
    soup = BeautifulSoup(html_list, 'html.parser')

    #initialize the result dictionary
    result_dict = {}

    #get all divs with the class 'recommendation'
    recommendations = soup.find_all('div', class_='recommendation')

    #run loop through recommendations to extract game name and id
    for i in range(len(recommendations)):
        #Get the current recommendation div
        recommendation = recommendations[i]

        #get the Steam app id from the 'a' tag
        app_id = recommendation.find('a')['data-ds-appid']

        #get the game name from the 'span' tag with the class 'color_created'
        name = recommendation.find('span', class_='color_created').text.strip()

        #append to the result dictionary
        result_dict[i] = {'name': name, 'app_id': app_id}

    return(result_dict)




if __name__ == "__main__":
     #run everything and dump to json file
     pub = sys.argv[1]
     html_list=base_url(pub).json()["results_html"]
     with open(f"{pub}.json", 'w') as outfile:
        json.dump(html2dict(html_list), outfile, indent=4)
