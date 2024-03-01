import time
from Scweet.scweet import scrape
from Scweet.utils import init_driver
from datetime import datetime, timedelta
from Scweet.utils import get_last_date_from_data
import mysql.connector


def check_existence(cursor, name):
    query = "SELECT COUNT(*) FROM tweet_user WHERE username = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()[0]
    if result > 0:
        return True  # 名字存在
    else:
        return False  # 名字不存在

def new_tweet_user_info(cursor, from_account, is_monitor):
    sql = "INSERT INTO tweet_user (username, is_monitor) VALUES (%s, %s)"
    val = (from_account, is_monitor)
    cursor.execute(sql, val)

def update_tweet_user_date(cursor, from_account):
    last_datetime = get_last_date_from_data(cursor, from_account)
    update_query = "UPDATE tweet_user SET last_datetime = '" + last_datetime + "' WHERE username = '" + from_account + "'"
    cursor.execute(update_query)

def scrape_tweet_for_account(from_account, is_monitor):
    connection = mysql.connector.connect(
        host="192.168.2.108",
        user="root",
        password="",
        database="twitter"
    )
    cursor = connection.cursor()
    if not check_existence(cursor, from_account):
        # 创建用户表 是否监控 和 最新的爬取推文时间
        new_tweet_user_info(cursor, from_account, is_monitor)
        start_date = "2024-03-01"
        format_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        format_end_date = tomorrow.strftime("%Y-%m-%d")
        format_end_date = datetime.strptime(format_end_date, "%Y-%m-%d")
        interval = 1
        current_date = format_start_date
        while current_date < format_end_date:
            driver = init_driver(headless=False, show_images=False, proxy=None)
            next_date = current_date + timedelta(days=interval)
            formatted_since_date = current_date.strftime("%Y-%m-%d")
            formatted_until_date = next_date.strftime("%Y-%m-%d")
            data = scrape(
                since=formatted_since_date,
                until=formatted_until_date,
                from_account=from_account,
                interval=1,
                display_type="Top",
                save_images=False,
                proxy=None,
                resume=False,
                filter_replies=True,
                proximity=False,
                driver=driver,
                env='.env',
                cursor=cursor,
            )
            current_date += timedelta(days=interval)
            # driver.quit()
            time.sleep(10)
        update_tweet_user_date(cursor, from_account)
        connection.commit()
        connection.close()


scrape_tweet_for_account('AirdropAlertAAD', True)