from typing import Self
import telebot # сама библиотека telebot
import time # необходим для cрока /mute и автоматического размута после срока мута
from datetime import datetime, timedelta
import settings


bot = telebot.TeleBot(settings.API_KEY) # в TOKEN мы вводим непосредственно сам полученный токен.

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я Чат-Менеджер COSPAY")

@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно кикнуть администратора.")
        else:
            bot.kick_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} был кикнут.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator' or user_status == 'moderator':
            bot.reply_to(message, "Невозможно замутить администратора.")
        else:
            duration = 60 # Значение по умолчанию - 1 минута
            args = message.text.split()[1:]
            if args:
                try:
                    duration = int(args[0])
                except ValueError:
                    bot.reply_to(message, "Неправильный формат времени.")
                    return
                if duration < 1:
                    bot.reply_to(message, "Время должно быть положительным числом.")
                    return
                if duration > 20160:
                    bot.reply_to(message, "Максимальное время - 14 деней.")
                    return
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} размучен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.")

# Функция для проверки, является ли пользователь администратором чата
def is_admin(message: telebot.types.Message) -> bool:
    chat_id = message.chat.id
    user_id = message.from_user.id
    # Получаем список администраторов чата
    admins = bot.get_chat_administrators(chat_id)
    # Проверяем, есть ли пользователь среди них
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False

# Функция для проверки, является ли пользователь администратором чата
def is_admin(message: telebot.types.Message) -> bool:
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Получаем список администраторов чата
    admins = bot.get_chat_administrators(chat_id)
    
    # Проверяем, есть ли пользователь среди них
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False




# Функция для проверки, является ли пользователь администратором чата
def is_admin(message: telebot.types.Message) -> bool:
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Получаем список администраторов чата
    admins = bot.get_chat_administrators(chat_id)
    
    # Проверяем, есть ли пользователь среди них
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False

# Обработчик команды /ban
@bot.message_handler(commands=['ban'])
def ban_user(message: telebot.types.Message):
    if is_admin(message):
        # Проверяем, что команда используется в ответ на сообщение пользователя
        if message.reply_to_message is not None:
            # Получаем пользователя, которого нужно забанить
            user_to_ban = message.reply_to_message.from_user
            
            # Разбиваем текст команды на аргументы
            args = message.text.split()
            
            # Проверяем наличие необходимого количества аргументов
            if len(args) >= 2:
                # Получаем время бана в минутах
                ban_duration = int(args[1])
                
                # Вычисляем время окончания бана
                ban_end_time = time.time() + ban_duration * 60
                
                # Теперь можем применить бан
                bot.restrict_chat_member(message.chat.id, user_to_ban.id, until_date=ban_end_time)
                
                bot.reply_to(message, f"Пользователь {user_to_ban.username} забанен на {ban_duration} минут.")
            else:
                bot.reply_to(message, "Неверное количество аргументов. Используйте /ban <duration_minutes>")
        else:
            bot.reply_to(message, "Используйте команду в ответ на сообщение пользователя.")
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")


# Функция для проверки, является ли пользователь администратором чата
def is_admin(message: telebot.types.Message) -> bool:
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Получаем список администраторов чата
    admins = bot.get_chat_administrators(chat_id)
    
    # Проверяем, есть ли пользователь среди них
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False

# Обработчик команды /unban
@bot.message_handler(commands=['unban'])
def unban_command(message: telebot.types.Message):
    # Проверяем, является ли отправитель команды администратором чата
    if not is_admin(message):
        bot.reply_to(message, "Вы не являетесь администратором чата.")
        return
    
    # Получаем информацию о пользователе, которого нужно разбанить
    reply_to_message = message.reply_to_message
    if reply_to_message is None or not reply_to_message.from_user:
        bot.reply_to(message, "Необходимо ответить на сообщение пользователя, которого нужно разбанить.")
        return
    
    user_to_unban_id = reply_to_message.from_user.id
    
    # Разбан пользователя
    bot.unban_chat_member(message.chat.id, user_to_unban_id)
    
    # Отправляем уведомление об успешном разбане
    bot.reply_to(message, f"Пользователь {user_to_unban_id} разблокирован.")

# создаем словарь для хранения правил для каждого чата
rules = {}

# обрабатываем команду /setrules
@bot.message_handler(commands=["setrules"])
def set_rules(message):
    # проверяем, является ли отправитель администратором чата
    chat_id = message.chat.id
    user_id = message.from_user.id
    admins = bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]
    if user_id not in admin_ids:
        # если нет, то отправляем сообщение об ошибке
        bot.reply_to(message, "Вы должны быть администратором, чтобы установить правила.")
        return
    # получаем текст правил из сообщения
    text = message.text
    # проверяем, есть ли текст после команды
    if len(text.split()) == 1:
        # если нет, то отправляем сообщение с инструкцией
        bot.reply_to(message, "Пожалуйста, укажите правила после команды. Например:\n/setrules Не ругайтесь и не спамьте.")
        return
    # удаляем команду из текста
    rules_text = text.replace("/setrules", "").strip()
    # сохраняем правила в словаре
    rules[chat_id] = rules_text
    # отправляем сообщение с подтверждением
    bot.reply_to(message, f"Правила для этого чата установлены:\n{rules_text}")

# обрабатываем команду /rules
@bot.message_handler(commands=["rules"])
def show_rules(message):
    # получаем идентификатор чата
    chat_id = message.chat.id
    # проверяем, есть ли правила для этого чата в словаре
    if chat_id not in rules:
        # если нет, то отправляем сообщение с уведомлением
        bot.reply_to(message, "Для этого чата не установлены правила.")
        return
    # получаем правила из словаря
    rules_text = rules[chat_id]
    # отправляем правила в ответ на сообщение
    bot.reply_to(message, f"Правила для этого чата:\n{rules_text}")

# Запуск бота
bot.polling()