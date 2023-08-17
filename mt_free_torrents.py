import requests
import sys
import re
import os
import time
import pickle
import urllib.parse
from requests import RequestException
from bs4 import BeautifulSoup


url = 'https://kp.m-team.cc/'

kind = 'movie.php'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0'
}

cookies = {
    "tp": ""
}


def get_suffix_urls(url, cookies, headers):
    try:
        response = requests.get(url=url, headers=headers, cookies=cookies)
    except RequestException as e:
        print("Get some error", e)
        sys.exit(1)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        free_img = soup.find_all(alt="Free")
        suffix_urls = [href.find_previous("a")["href"].replace(
            'details', 'download').replace('hit', 'https') for href in free_img]
        return suffix_urls


def download_torrents(url, suffix_urls, headers, cookies):
    download_dir = os.path.dirname(__file__)
    for suffix_url in suffix_urls:
        download_url = url + suffix_url
        try:
            response = requests.get(url=download_url, headers=headers, cookies=cookies)
        except RequestException as e:
            print("Request error", e)
        if response.status_code == 200:
            h = response.headers["content-disposition"]
            file_name = urllib.parse.unquote(re.split(r'[;=]', h)[2].strip('" '))
            if not os.path.exists(f'{download_dir}/{file_name}'):
                with open(f'{download_dir}/{file_name}', 'wb') as f:
                    f.write(response.content)
            else:
                print("torrent exists.")
        else:
            print('repsonse code not 200.')
        time.sleep(5)
    print("Download done.")



if __name__ == '__main__':
    torrent_url = url + kind
    suffix_urls = get_suffix_urls(url=torrent_url, headers=headers, cookies=cookies)
    try:
        with open('mt_saved_list.pkl', 'rb') as pkl:
            saved_suffix_urls = pickle.load(pkl)
    except FileNotFoundError as e:
        saved_suffix_urls = []
        pass
    if saved_suffix_urls == suffix_urls:
        print("Have not new free torrent.")
        sys.exit(1)
    else:
        pkl = open('mt_saved_list.pkl', 'wb')
        pickle.dump(suffix_urls, pkl)
        pkl.close()
    
    download_torrents(url=url, suffix_urls=suffix_urls, headers=headers, cookies=cookies)
    
