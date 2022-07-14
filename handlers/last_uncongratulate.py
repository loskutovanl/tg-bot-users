from telebot.types import Message
from loader import bot
import database.commands as usersbase
import datetime


# @bot.message_handler(commands=['unceleb'])
# def bot_uncongratulate(message: Message):
#     # usersbase.MODERATOR_ID = message.chat.id
#     uncelebs = usersbase.select_last_uncongratulate(message.chat.id)
#     print(uncelebs)
#     # print(message.chat.id)
#     # print(winners)
#     for unceleb in uncelebs:
#         dtime = datetime.datetime.strptime(unceleb[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%y %H:%M')
#         # bot.send_message(chat_id=message.chat.id, text=f'\U0001F451\U0001F451\U0001F451  ★★★ "{unceleb[0]}"  \U0001F464  {unceleb[1]}'
#         #                                                    f'(@{unceleb[2]})\n\U0001F522  {unceleb[3]}  \U0001F550 	{dtime}')
#         # else:
#         bot.send_message(chat_id=message.chat.id, text=f'\U0001F389  "{unceleb[0]}"  \U0001F464  {unceleb[1]}  '
#                                                        f'(@{unceleb[2]})\n\U0001F522  {unceleb[3]}  \U0001F550 	{dtime}')
uncelebs = usersbase.select_last_uncongratulate(1001521772742)
gr_id = usersbase.select_group_id(1001521772742)
print(gr_id)
print(uncelebs)
temp_id = 0
for id, gr in enumerate(gr_id):
    temp_id += gr_id[id][1]
    print(uncelebs[temp_id- 1])
