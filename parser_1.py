import telebot
import requests
import json
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime

bot = telebot.TeleBot('6715780052:AAHLF3BSwdfTIrOXfPlADPLJ5Qup6at5xr4')
driver = webdriver.Chrome()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, я рад тебя видеть. У меня ты сможешь получить расписание своей группы.")

@bot.message_handler(commands=['search_timetable'])
def search_timetable(message):
    msg = bot.send_message(message.chat.id, "Введите группу, расписание которой вы хотите найти.")
    bot.register_next_step_handler(msg, search)

@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, "Уточни, что ты хотел?")
def search(message):
    bot.send_message(message.chat.id, "Начинаю поиск")
    driver.get("https://umu.sibadi.org/WebApp/#/Rasp/List")
    time.sleep(4)
    our_cell = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/main/div/div[4]/div/div/div[3]/div/div[2]/div/div/input")  # находим поле с вводом
    user_input = message.text  # перменная содержащая в себе текст из бота тг
    time.sleep(1)
    our_cell.send_keys(user_input)
    time.sleep(1)
    group = driver.find_element(By.CLASS_NAME, "text-start")  # поле с выводимыми группами
    time.sleep(1)
    group.click()  # заходим на группу


    now_time = datetime.utcnow().strftime('%Y-%m-%d')
    some_url = 'https://umu.sibadi.org/api/Rasp?idGroup=13688&sdate='
    res_url = some_url + now_time
    r = requests.get(res_url).text
    data = json.loads(r)

    schedule_by_day = {}

    # Извлекаем нужные данные из словаря
    rasp = data["data"]["rasp"]
    for item in rasp:
        day = item["день_недели"]
        subject = item["дисциплина"]
        teacher = item["преподаватель"]
        if day not in schedule_by_day:
            schedule_by_day[day] = []
        schedule_by_day[day].append({"предмет": subject, "преподаватель": teacher})

    # Выводим результат
    bot.send_message(message.chat.id, 'Расписание на этой неделе: \n')
    for day, schedule in schedule_by_day.items():
        bot.send_message(message.chat.id, f'{day}:')
        
        for item in schedule:
            str_1 = f'Предмет: {item["предмет"]}\n'
            str_2 = f'Преподаватель: {item["преподаватель"]}'
            bot.send_message(message.chat.id, str_1 + str_2)

    ''' Подумать над тем, как отправлять сообщение пользователю в виде:
                Понедельник:
                    lesson
                    lesson
                    lesson
                    ....
                Вторник:
                    lesson
                    lesson
                    lesson
                    ....
                ...
                '''



bot.polling()