# Some shits
from selenium import webdriver
import argparse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# creating argument parser
parser = argparse.ArgumentParser(description='It will scrape Twetter using folowing inputs')
parser.add_argument('-s','--searchterm',metavar='search_term', required=True, help='tere bap yaha pe chodker gaya tha ki teri ma')
parser.add_argument( '-f' ,'--filename', metavar='file_name' ,required=False , type=str, help='Le Gov. workers :Kripya kerke dusre counter pe jaeye ')

# ahi maja aegana bidu
args = parser.parse_args()

class Scraper:
    def __init__(self , driver , timeout = 5) :
        self.driver = driver
        self.timeout = timeout

    def init_args(self , search_term , file_name='Scraped_data'):
        self.search_term = search_term
        self.file_name = file_name

    def ma_hu_bula_kerta_hu_data_ka_khula(self , data):
        with open(f'{self.file_name}.csv', 'w', newline='', encoding='utf-8') as f:
            header = ['Channel Name' , 'Description' , 'Subscribers' , 'links']
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

    def get_channel_details(self, channelUrl):
        self.driver.get(channelUrl+ "/about")
        css_selector_url = '#link-list-container.style-scope.ytd-channel-about-metadata-renderer a.yt-simple-endpoint.style-scope.ytd-channel-about-metadata-renderer'

        wait = WebDriverWait(self.driver , self.timeout)

        try:
            name = wait.until(
            EC.presence_of_element_located((By.ID , 'channel-name'))
            ).text

            try: 
                description = wait.until(
                    EC.presence_of_element_located((By.ID , 'description'))
                    ).text
            except Exception: 
                description = 'Sorry but this bitch dont add description'
            
            subscriberCount = wait.until(
                EC.presence_of_element_located((By.ID , 'subscriber-count'))
                ).text 
            try:
                links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , css_selector_url)))
            except TimeoutException:
                links = []
        except TimeoutException:
            print(f'khatam smaye khatam. {self.timeout} second khatam ab kya ladu chaiye nikal pahali pursat ma nikal')
        
        Channel_links = []

        if len(links) != 0:
            for channel_link in links:
                Channel_links.append(channel_link.get_attribute('href'))

        # print(Channel_links , end= "\n\n")

        channel_data = (name , description , subscriberCount , Channel_links)

        return channel_data
    
    def TeraBapAya(self):
        self.driver.get(f'https://www.youtube.com/results?search_query={self.search_term}')

        time.sleep(5)
        channelsElement = self.driver.find_elements_by_xpath('//*[@id="text"]/a')

        ChannelsUrl = set()

        for url in channelsElement: 
            url = url.get_attribute('href')
            ChannelsUrl.add(url)
            # print(url)

        print(f'Length of data: {len(ChannelsUrl)}')
        
        Channels_Data = []
        for channelUrl in ChannelsUrl:
            channel_data = self.get_channel_details(channelUrl)
            Channels_Data.append(channel_data)

        self.driver.close()

        # Calling by bro bula to khula all of them
        self.ma_hu_bula_kerta_hu_data_ka_khula(Channels_Data)



'-----------------BRAVE -- OP-------------------'
driver_path = "C:/chromedriver.exe"
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
option.add_argument("--incognito")

driver = webdriver.Chrome(driver_path, chrome_options=option)

# driver.maximize_window()

# Initial time
start_time=time.time()

scraper = Scraper(driver ,timeout=5)
scraper.init_args(args.searchterm , args.filename)

scraper.TeraBapAya()

print(f"Total time taken by scraping is {time.time()-start_time}")