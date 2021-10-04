import os

import time
from replit import db
from telegram import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)
from telegram.constants import MAX_MESSAGE_LENGTH

from user_db import User

def handler_error (update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    print(context.error)
    raise context.error

def start_command(update: Update, context: CallbackContext) -> None:
    timestamp = int(time.time())

    print(f"{timestamp}: Start chat {update.effective_chat.id} ({update.effective_chat.full_name})")

    user_id = update.effective_chat.id
    user = User(user_id)

    # user_id = User(user_id)
    # user.set_full_name(update.effective_chat.full_name)
    # user.set_start_timestamp(timestamp)

    # user.set_full_name(update.effective_chat.full_name)
    # db[f"full_name:{user_id}"] = update.effective_chat.full_name # Сохраняем имя пользователя

    # if f"start:{user_id}" not in db: # Сохраняем время и дату команды старт
      # db[f"start:{user_id}"] = timestamp
    user.start()
    #db[update.effective_chat.id] = update.effective_chat.full_name

    text = f"""
Приветствую, {update.effective_chat.full_name}!

Добро пожаловать в моего бота.
    """
    update.message.reply_text(text)

    inline_keyboard = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton("Младше 18", callback_data="age:select:>18"), 
          InlineKeyboardButton("18-25", callback_data="age:select:18-25"),
          InlineKeyboardButton("25-35", callback_data="age:select:25-35"),
          InlineKeyboardButton("Старше 35", callback_data="age:select:35>")
        ]
      ]
    )

    ask_question(update, db.get(f"step:{user_id}", "age"), reply_markup = inline_keyboard)

    # user.ask_question(update)

def ask_question(update: Update, step, reply_markup=None):
    user_id = update.effective_chat.id
  
    if step == 'age':
      update.message.reply_text("Ваш возраст?", reply_markup = reply_markup)

    elif step == 'city':
      update.message.reply_text("Ваш город?")

    elif step == 'ms':
      update.message.reply_text("Ваше семейное положение?")
    
    else:
      update.message.reply_text("Ошибка")
      return

    db[f"step:{user_id}"] = step

def reset_command(update: Update, context: CallbackContext) -> None:
    User(update.effective_chat.id).reset()
    
    # user_id = update.effective_chat.id

    # del db[f"step:{user_id}"]
    # del db[f"age:{user_id}"]
    # del db[f"city:{user_id}"]
    # del db[f"ms:{user_id}"]

    update.message.reply_text("Анкета удалена")

def text_command(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id
    user = User(user_id)

    step = user.get_step()
    next_step = None

    # step = "age"
    # next_step = "city"
    
    if f"step:{user_id}" in db:
      step = db[f"step:{user_id}"]

    if step == 'age':
      try:
          user_age = int(update.message.text)
          user.set_age(user_age)
          # user_age = int(update.message.text)
          # db[f"age:{user_id}"] = user_age
      except ValueError:
          update.message.reply_text("Введите число")
          return
      next_step = "city"

    elif step == 'city':
      user_city = update.message.text
      user.set_city(user_city)
      next_step = "status"
      
      # user_city = update.message.text
      # db[f"city:{user_id}"] = user_city
      next_step = "ms"

    elif step == 'ms':
      user_ms = update.message.text
      user.set_ms(user_ms)
      next_step = "done"

    else:
      update.message.reply_text("Ошибка")

    # user_age = int(update.message.text)
    
    #data = db[user_id]

    # db[user_id] = {
    #   'name': update.effective_chat.full_name,
    #   'age': user_age
    # }

    update.message.reply_text("Принято")
    if next_step == "done":
      update.message.reply_text(f"""
Возраст: {db[f"age:{user_id}"]}
Город: {db[f"city:{user_id}"]}
Семеное положение: {db[f"ms:{user_id}"]}
      """)
    else:
      ask_question(update, next_step)

def list_command(update: Update, context: CallbackContext) -> None:
    if context.args:
        list_user_id = context.args[0]
    else:
        list_user_id = None

    key_map = {}

    for k in db.keys():
        user_id = k.split(":")[-1]

        if list_user_id and list_user_id != user_id:
            continue
        
        if user_id not in key_map:
          key_map[user_id] = []
        
        key_map[user_id].append(k)

    message_text = ""

    for user_id, keys in key_map.items():
        text_items = []

        for k in keys:
            text_items.append(f"{k}: {db[k]}")
        
        user_text = '\n'.join(text_items)

        if len(message_text) + len(user_text) > MAX_MESSAGE_LENGTH - 2:
            update.message.reply_text(message_text)
            message_text = user_text
        else:
            message_text += "\n\n" + user_text

    if message_text:
        update.message.reply_text(message_text)
    
    # for k, v in db.items():
    #   update.message.reply_text(f"{k}: {v}")

def print_command(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id
    user_age = db[f"age:{user_id}"]
    update.message.reply_text(f"age: {user_age}")

#def unknown_command(update: Update, context: CallbackContext) -> None:
    #update.message.reply_text("Не понятно :(")

def main():
    updater = Updater("1749703925:AAFAYnEJKRZNTNhfx0FSX4YxHa5-QpVuvxA")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("reset", reset_command))
    dispatcher.add_handler(CommandHandler("list", list_command, pass_args=True))
    dispatcher.add_handler(CommandHandler("print", print_command))
    dispatcher.add_handler(MessageHandler(Filters.all, text_command))
    
      #dispatcher.add_handler(MessageHandler(Filters.all, unknown_command))
    # dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_error_handler(handler_error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()