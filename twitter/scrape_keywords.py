import time

import pandas as pd
import schedule
from Scweet.scweet import scrape
from Scweet.utils import init_driver
from datetime import datetime, timedelta
from Scweet.utils import get_last_date_from_data
import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Zzy1286661681!",
        database="twitter"
    )
    return connection

def check_existence(connection, name):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM tweet_user WHERE username = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()[0]
    cursor.close()
    if result > 0:
        return True  # 名字存在
    else:
        return False  # 名字不存在

def new_tweet_user_info(connection, from_account, is_monitor):
    cursor = connection.cursor()
    sql = "INSERT INTO tweet_user (username, is_monitor) VALUES (%s, %s)"
    val = (from_account, is_monitor)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    print(from_account, 'new_tweet_user_info successful')

def update_tweet_user_date(connection, from_account):
    last_datetime = str(get_last_date_from_data(connection, from_account))
    cursor = connection.cursor()
    update_query = "UPDATE tweet_user SET last_datetime = '" + last_datetime + "' WHERE username = '" + from_account + "'"
    cursor.execute(update_query)
    connection.commit()
    cursor.close()
    print(last_datetime, 'update_tweet_user_date successful')

def scrape_tweet_for_account(from_account, is_monitor=None, last_datetime=None):
    connection = get_db_connection()
    if not check_existence(connection, from_account):
        # 创建用户表 是否监控 和 最新的爬取推文时间
        new_tweet_user_info(connection, from_account, is_monitor)
        start_date = "2024-03-03"
        # format_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        end_date = tomorrow.strftime("%Y-%m-%d")
        driver = init_driver(headless=False, show_images=False, proxy=None)
        data = scrape(
            since=start_date,
            until=end_date,
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
            connection=connection,
        )
        update_tweet_user_date(connection, from_account)
        connection.close()
        return True
    else:
        start_date = str(last_datetime)
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        end_date = tomorrow.strftime("%Y-%m-%d")
        driver = init_driver(headless=False, show_images=False, proxy=None)
        data = scrape(
            since=start_date,
            until=end_date,
            from_account=from_account,
            interval=1,
            display_type="Top",
            save_images=False,
            proxy=None,
            resume=True,
            filter_replies=True,
            proximity=False,
            driver=driver,
            env='.env',
            connection=connection,
        )
        update_tweet_user_date(connection, from_account)
        connection.close()
        return False

def monitor_user():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT username, last_datetime FROM tweet_user WHERE is_monitor = true"

    # 执行查询
    cursor.execute(query)

    # 提取结果
    rows = cursor.fetchall()
    columns = ['username', 'last_datetime']
    df = pd.DataFrame(rows, columns=columns)
    df['last_datetime'] = pd.to_datetime(df['last_datetime']).dt.strftime("%Y-%m-%d")
    df.apply(lambda row: scrape_tweet_for_account(row['username'], is_monitor=True, last_datetime=row['last_datetime']), axis=1)



if __name__ == "__main__":
    schedule.every().day.at("00:00").do(monitor_user())
    schedule.every().day.at("12:00").do(monitor_user())

    # 循环检查是否需要运行任务
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每隔60秒检查一次