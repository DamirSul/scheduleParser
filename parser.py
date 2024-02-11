import telebot
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

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
    time.sleep(2)
    our_cell = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/main/div/div[4]/div/div/div[3]/div/div[2]/div/div/input")  # находим поле с вводом
    user_input = message.text  # перменная содержащая в себе текст из бота тг
    time.sleep(2)
    our_cell.send_keys(user_input)
    time.sleep(3)
    group = driver.find_element(By.CLASS_NAME "text-start")  # поле с выводимыми группами
    time.sleep(2)
    group.click()  # заходим на группу

    full_page = driver.find_element(By.CSS_SELECTOR, "")
    print(full_page)



bot.polling()