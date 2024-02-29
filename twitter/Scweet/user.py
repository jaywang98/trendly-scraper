from . import utils
from time import sleep
import random
import json

from .utils import log_in
from selenium.common.exceptions import NoSuchElementException

def get_user_information(users, driver=None, headless=True, env=None):
    """ get user information if the "from_account" argument is specified """

    driver = utils.init_driver(headless=headless, show_images=False)
    log_in(driver, env=env)

    users_info = {}

    for i, user in enumerate(users):

        log_user_page(user, driver, headless=headless)

        # 尝试查找特定XPath并处理异常
        try:
            element = driver.find_element_by_xpath(
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[2]/div/div[1]/span')
            if element.text == "This account doesn’t exist":
                print("* @" + user + "不存在")
                continue
            else:
                print("scrape @" + user + "...")
        except NoSuchElementException:
            # 如果元素不存在，也跳过
            print("scrape @" + user + "...")

        if user is not None:
            website = driver.current_url
            try:
                following = driver.find_element_by_xpath(
                    '//a[contains(@href,"/following")]/span[1]/span[1]').text
                followers = driver.find_element_by_xpath(
                    '//a[contains(@href,"/verified_followers")]/span[1]/span[1]').text
            except Exception as e:
                # print(e)
                return

            try:
                desc = driver.find_element_by_xpath('//div[contains(@data-testid,"UserDescription")]').text
            except Exception as e:
                desc = ""
            a = 0
            try:
                join_date = driver.find_element_by_xpath(
                    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/span[3]/span').text
            except Exception as e:
                # print(e)
                join_date = ""
            try:
                birthday = driver.find_element_by_xpath(
                    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/span[2]').text
            except Exception as e:
                # print(e)
                birthday = ""

            try:
                location = driver.find_element_by_xpath(
                    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/span[1]/span/span').text
            except Exception as e:
                # print(e)
                location = ""

            print("--------------- " + user + " information : ---------------")
            print("Following : ", following)
            print("Followers : ", followers)
            print("Join date : ", join_date)
            print("Birthday : ", birthday)
            print("Location : ", location)
            print("Description : ", desc)
            print("Website : ", website)
            users_info[user] = [following, followers, join_date, birthday, location, website, desc]

            # users_info[user] = [following, followers, join_date, birthday, location, website, desc]

            # if i == len(users) - 1:
            #     driver.close()
            #     return users_info
        else:
            print("You must specify the user")
            continue
    return users_info


def log_user_page(user, driver, headless=True):
    sleep(random.uniform(1, 2))
    driver.get('https://twitter.com/' + user)
    sleep(random.uniform(1, 2))


def get_users_followers(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    followers = utils.get_users_follow(users, headless, env, "followers", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs_bak/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'followers.json'
    with open(file_path, 'w') as f:
        json.dump(followers, f)
        print(f"file saved in {file_path}")
    return followers


def get_users_following(users, env, verbose=1, headless=True, wait=2, limit=float('inf'), file_path=None):
    following = utils.get_users_follow(users, headless, env, "following", verbose, wait=wait, limit=limit)

    if file_path == None:
        file_path = 'outputs_bak/' + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    else:
        file_path = file_path + str(users[0]) + '_' + str(users[-1]) + '_' + 'following.json'
    with open(file_path, 'w') as f:
        json.dump(following, f)
        print(f"file saved in {file_path}")
    return following


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
