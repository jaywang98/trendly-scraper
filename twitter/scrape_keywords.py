import time
from Scweet.scweet import scrape
from Scweet.utils import init_driver
from datetime import datetime, timedelta



time_intervals = [["2024-02-21", "2024-02-22"]]
for time_interval in time_intervals:
    start_date = time_interval[0]
    end_date = time_interval[1]
    format_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    format_end_date = datetime.strptime(end_date, "%Y-%m-%d")
    save_dir = 'outputs'
    interval = 1

    current_date = format_start_date
    while current_date < format_end_date:
        driver = init_driver(headless=True, show_images=False, proxy=None)
        next_date = current_date + timedelta(days=interval)
        formatted_since_date = current_date.strftime("%Y-%m-%d")
        formatted_until_date = next_date.strftime("%Y-%m-%d")
        data = scrape(
            since=formatted_since_date,
            until=formatted_until_date,
            from_account='AirdropAlertAAD',
            interval=1,
            display_type="Top",
            save_images=False,
            proxy=None,
            save_dir=save_dir,
            resume=False,
            filter_replies=True,
            proximity=False,
            driver=driver,
            env='.env'
        )
        current_date += timedelta(days=interval)
        driver.quit()
        time.sleep(60)


