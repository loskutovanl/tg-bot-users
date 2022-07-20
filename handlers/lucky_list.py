from telebot.types import Message
from loader import bot
import database.commands as usersbase
import datetime
from telebot import types

g_chat_id = 0

def lucky_keyboard(luckylist) -> types.InlineKeyboardMarkup:
    wins_chat_name = list({i[0] for i in luckylist})
    wins_chat_id = list({i[6] for i in luckylist})

    wins_chat_name.append('Все группы')
    wins_chat_id.append(0)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    for i in range(len(wins_chat_name)):
        lucky_name = wins_chat_name[i]
        lucky_id = wins_chat_id[i]

        # print(type(lucky_id), lucky_id, lucky_name)
        keyboard.add(types.InlineKeyboardButton(text=f"{lucky_name}", callback_data=f'{lucky_id}'))

        # if i == 6:
        #     break

    return keyboard

@bot.message_handler(commands=['luckylist'])

def bot_lucky_list(message: Message):
    winners = usersbase.select_lucky(message.chat.id)
    # print(lucky_keyboard(winners))
    markup =lucky_keyboard((winners))
    mesg = bot.send_message(chat_id=message.chat.id, text='Какие группы отобразить?', reply_markup=markup)
    # bot.register_next_step_handler(mesg, callback)
    # bot_lucky_list_2(mesg)


# def bot_lucky_list_2(message: Message):
#     print(type(callback))
#     bot.send_message(chat_id=message.chat.id, text='test')
#     winners = usersbase.select_lucky(callback())
#     print(winners)


    # for winner in winners:
    #     dtime = datetime.datetime.strptime(winner[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%y %H:%M')
    #     if winner[5] == 1:
    #         bot.send_message(chat_id=message.chat.id,
    #                          text=f'\U0001F451\U0001F451\U0001F451  "{winner[0]}"  \U0001F464  {winner[1]}'
    #                               f'(@{winner[2]})\n\U0001F522  {winner[3]}  \U0001F550 	{dtime}')
    #     else:
    #         bot.send_message(chat_id=message.chat.id,
    #                          text=f'\U0001F389  "{winner[0]}"  \U0001F464  {winner[1]}  '
    #                               f'(@{winner[2]})\n\U0001F522  {winner[3]}  \U0001F550 	{dtime}')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    luk = ['0', '123', '234']


    if call.message:
        for i in luk:
            if call.data == i:
                winners = usersbase.select_lucky_id(i)
                print(winners)
                # print(i)
                # return i

    # bot.register_next_step_handler(mesg, bot_lucky_list)

