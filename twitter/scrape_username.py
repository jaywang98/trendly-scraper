import csv
from Scweet.scweet import scrape
from Scweet.utils import init_driver
from Scweet.user import get_user_information, get_users_following, get_users_followers

usernames = ['nagouzil', '@yassineaitjeddi', 'TahaAlamIdrissi',
             '@Nabila_Gl', 'geceeekusuu', '@pabu232', '@av_ahmet', '@x_born_to_die_x']

# usernames = ['@Nabila_Gl']
# driver = init_driver(headless=False, show_images=False, proxy=None)

# this function return a list that contains :
# ["nb of following","nb of followers", "join date", "birthdate", "location", "website", "description"]
users_info = get_user_information(usernames, headless=False, env='.env')

# 以写入模式打开CSV文件
with open('twitter_data.csv', 'w', newline='') as csvfile:
    # 创建CSV写入对象
    csv_writer = csv.writer(csvfile)

    # 写入CSV文件的表头（字典的键）
    csv_writer.writerow(['Username', 'Followers', 'Following', 'Joined Date', 'Born Date', 'Location', 'Profile URL', 'Des'])

    # 遍历字典，将数据写入CSV文件
    for username, values in users_info.items():
        csv_writer.writerow([username] + values)

