import requests
from Config.config import *
from DBconnect.config import *

mycursor = mydb.cursor()


def get_bithump_price():

    URL_BIP_COST_BITHUMP='https://global-openapi.bithumb.pro/market/data/ticker?symbol=BIP-USDT'
    bithump_url=requests.get(URL_BIP_COST_BITHUMP)
    sell_usdt=[]
    buy_usdt=[]
    data = bithump_url.json()['info'][0]

    return(data)

def get_username(message):
    usr = bot.get_chat_member(message.chat.id, message.from_user.id)
    if not usr.user.username:
        return usr.user.first_name
    else:
        return usr.user.username

def user_exist(chat_id):
    mycursor.execute("SELECT chat_id FROM users LIMIT 1")
    result = mycursor.fetchone()
    if result == None:
        return False
    else:
        return True

def group_exist(group_id):
    mycursor.execute("SELECT group_name FROM groups LIMIT 1")
    result = mycursor.fetchone()
    if result == None:
        return False
    else:
        return True

def bot_is_in_group(group_id):
    bot_status = bot.get_chat_member(chat_id = '@'+group_id , user_id = bot_id).status
    bot_can_post = bot.get_chat_member(chat_id = '@'+group_id , user_id = bot_id).can_post_messages
    type_of_group = bot.get_chat(chat_id = '@'+group_id).type
    if (str(bot_status) == 'administrator'):
        if(str(type_of_group) == 'supergroup'):
            return 1
        elif(str(type_of_group) == 'channel'):
            if(str(bot_can_post) == 'True'):
                return 2
            else:
                return 3
    else:
        return 0

def validate_time(post_time):
    time_value = post_time.split(':')
    if(int(time_value[0]) < 25):
        if(int(time_value[1]) < 61):
            return 1
        else:
            return 0
    else:
        return 0

def put_user(chat_id, name):
    sql = "INSERT INTO users (chat_id, username) VALUES (%s, %s)"
    val = (chat_id, name)
    mycursor.execute(sql, val)
    mydb.commit()

def put_group(chat_id, groupname):
    sql = "INSERT INTO groups (chat_id, group_name) VALUES (%s, %s)"
    val = (chat_id, groupname)
    mycursor.execute(sql, val)
    mydb.commit()

def put_post(group_id, time):
    sql = "INSERT INTO posts (group_id, time) VALUES (%s, %s)"
    val = (group_id, time)
    mycursor.execute(sql, val)
    mydb.commit()
