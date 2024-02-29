from Scweet.scweet import scrape
from Scweet.utils import init_driver
from Scweet.user import get_user_information, get_users_following, get_users_followers
usernames = ['nagouzil', '@yassineaitjeddi', 'TahaAlamIdrissi',
             '@Nabila_Gl', 'geceeekusuu', '@pabu232', '@av_ahmet', '@x_born_to_die_x']

following = get_users_following(users=usernames, env='.env', verbose=0, headless=False, wait=5, limit=50, file_path='following.txt')