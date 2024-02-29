import time
import pandas as pd
from Scweet.scweet import scrape
from Scweet.utils import init_driver, log_in
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By

df = pd.read_csv('../fake_news/afp_fake_twitter.csv')

target_urls = df['target_url'].tolist()
# tweets_urls

driver = init_driver(headless=False, show_images=False, proxy=None)

header = ['UserScreenName', 'UserName', 'Date', 'Text', 'Likes', 'Comments',
          'Retweets', 'Image link', 'If_video', 'Tweet URL', 'Replies']
data = []
tweet_ids = set()
write_mode = 'w'
save_images = True
refresh = 0
replies_dir = 'outputs/replies'
log_in(driver, env='.env')
for url in target_urls:
    driver.get(url)
    userScreenName = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]').text
    userName = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]').text
    date = (driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[''1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[1]/a/time').get_attribute('datetime'))
    text = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div/span').text
    views = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[3]/span/div').text
    like = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[3]/div/div/div[2]').text
    comments = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[1]/div/div/div[2]').text
    retweets = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[2]/div/div/div[2]').text

    scroll = 0
    while scroll < 3:
        reply_dict = {}
        last_position = driver.execute_script("return window.pageYOffset;")
        comments_set = driver.find_elements(by=By.XPATH, value='//article[@data-testid="tweet"]')[1:]
        for comment in comments_set:
            response = comment.text.split('\n')
            reply_dict['UserScreenName'] = response[0]
            reply_dict['UserName'] = response[1]
            reply_dict['Date'] = response[3]
            reply_dict['Text'] = response[4]
            reply_dict['Likes'] = response[6]