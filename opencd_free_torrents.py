import requests
import sys
import re
import time
import os
import pickle
from requests import RequestException
from bs4 import BeautifulSoup


url = 'https://open.cd/torrents.php'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0'
}

# set cookies
cookies = {
}


def get_torrent_info_url(url, cookies, headers):
    try:
        response = requests.get(url=url, headers=headers, cookies=cookies)
    except RequestException as e:
        print("Get some error", e)
        sys.exit(1)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        alt_free = soup.find_all(alt="Free")
        torrent_info_urls = ["https://open.cd/" + a.parent.parent.find_previous(
            "td").find_next("a")["href"] for a in alt_free]
        print(torrent_info_urls)
        return torrent_info_urls



def get_download_torrent_url(download_urls, cookies, headers):
    download_torrent_urls = []
    for u in download_urls:
        try:
            response = requests.get(url=u, cookies=cookies, headers=headers)
        except RequestException as e:
            print("Get download url error", e)
            sys.exit(1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            download_torrent_urls.append(soup.find(href=re.compile('open.cd/download'))["href"])
        time.sleep(5)
    print(download_torrent_urls)
    return download_torrent_urls


def download_torrent(download_torrent_urls):
    for url in download_torrent_urls:
        try:
            response = requests.get(url=url, headers=headers, cookies=cookies)
        except RequestException as e:
            print("Download torrent error", e)
        if response.status_code == 200:
            h = response.headers['content-disposition']
            file_name = re.split(r'[;=]', h)[2].strip('" ').encode("ISO-8859-1").decode()
            if not os.path.exists(file_name):
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                    print(f"{file_name} saved.")
            else:
                print('torrent exists.')
        time.sleep(5)
    print("Download all done.")



if __name__ == '__main__':
    torrent_info_urls = get_torrent_info_url(url=url, cookies=cookies, headers=headers)
    try:
        with open('saved_list.pkl', 'rb') as pkl:
            save_list = pickle.load(pkl)
    except FileNotFoundError as e:
        save_list = []
        pass
    if save_list == torrent_info_urls:
        print("Have not new free torrent.")
        sys.exit(1)
    else:
        pkl = open('saved_list.pkl', 'wb')
        pickle.dump(torrent_info_urls, pkl)
        pkl.close()

        download_urls = get_download_torrent_url(download_urls=torrent_info_urls, cookies=cookies, headers=headers)
        download_torrent(download_torrent_urls=download_urls)
