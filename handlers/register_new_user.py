from loader import bot
from database.commands import insert, insert2
import datetime
from database.commands import winner_check, select_id_from_users,\
    temp_save, buttons_remover, storage_cleaner, is_winner_id_select, is_winner_record, other_lucky_check, data_finder
from telebot import types


@bot.message_handler(content_types=['new_chat_members'])
def handler_new_member(message):
    count = bot.get_chat_members_count(message.chat.id)
    user_number=message.from_user.id
    chat_name = message.chat.title
    nickname = message.from_user.username
    user_name = message.from_user.first_name
    dtime = datetime.datetime.now()



    markup = types.InlineKeyboardMarkup(row_width=1)
    congratulations = types.InlineKeyboardButton(text='Поздравляем', callback_data='grac')
    shame = types.InlineKeyboardButton(text='Не поздравляем', callback_data='decline')
    markup.add(congratulations, shame)


    if not message.from_user.is_bot and not winner_check(user_number): # тут будет еще проверка count % 500 == 0


        insert2(
            nickname=message.from_user.username, user_name=message.from_user.first_name,
            congr_number = count, chat_name=message.chat.title,
            user_id=message.from_user.id, dtime=datetime.datetime.now(),
            chat_id=message.chat.id, is_winner=0)


        if not other_lucky_check(count_users=502, chat_id=message.chat.id):


            bot_message = bot.send_message(258281993,
                    f'В {chat_name} вступил юбилейный пользователь {nickname} {user_name}\n'
                    f'Порядковый номер вступления: {count}, время вступления: {dtime}',
                             reply_markup=markup)

            temp_save(chat_id=258281993,
                      record_id=select_id_from_users(user_id=message.from_user.id),
                      bot_message_id=bot_message.id, users_chat=message.chat.id
                      )


    else:
        bot.send_message(message.chat.id, f'Что-то пошло не так')

@bot.callback_query_handler(func=lambda call: call.data == "grac" or call.data == "decline")
def callback(call):
    if call.message:
        if call.data == 'grac':
            winner = is_winner_id_select(bot_message_id=call.message.message_id)
            is_winner_record(winner_id=winner)

            name = data_finder(bot_message_id=call.message.message_id)[0][0]
            congr_number = data_finder(bot_message_id=call.message.message_id)[0][1]
            users_chat = data_finder(bot_message_id=call.message.message_id)[0][2]


            remove_list = buttons_remover(chat_id=users_chat)

            print(remove_list)
            for message in remove_list:
                bot.delete_message(chat_id=call.message.chat.id, message_id=message)



            storage_cleaner(chat_id=users_chat)

            bot.send_message(users_chat, f'Поздравляю, {name}, '
                                        f'как же удачно попали в нужное время. Вы  '
                                        f'участник {congr_number} коммьюнити. Вас ждут плюшки и печенюшки.')

        else:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, 'Что-то пошло не так')
