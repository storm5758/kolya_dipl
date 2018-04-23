import requests
import json
import telebot
import config
from telebot import apihelper
from datetime import datetime


bot = telebot.TeleBot(config.token)


apihelper.proxy = {'https': '217.61.15.26:3128'} #прокси для обхода блокировки

@bot.message_handler(commands=["start"])

def start_help(message): 
	bot.send_message(message.chat.id,"Приветствуем, чтобы увидеть информацию введите /command_help") #чисто инфа, готово

@bot.message_handler(commands=["help"])

def command_help(message): 
	bot.reply_to(message,'Привет,первым делом зарегестрируйтесь в системе.Для этого введите /reg. Чтобы записаться на мойку, введите /entry. Чтобы посмотреть ваши записи введите команду /history') #чисто инфа, готово


@bot.message_handler(commands=["reg"])

def command_reg(message): 
	
	print(message.from_user.id)
	print(message.from_user.last_name)
	bot.reply_to(message, message.from_user.first_name+' ,вы успешно зарегистрированы в системе ')
	return message.from_user.id, message.from_user.last_name				#заносим в базу, чтобы потом сортировать записи на мойку

@bot.message_handler(commands=["entry"])

def command_entry(message): 
	bot.reply_to(message,'Чтобы записаться введите дату в формате ГОД.МЕСЯЦ.ЧИСЛО ')
	
	@bot.message_handler(regexp="([12]\d{3}.(0[1-9]|1[0-2]).(0[1-9]|[12]\d|3[01]))")
	def check_date(message):
		bot.reply_to(message,'На это число свободны следующие даты: ')
		#тут из базы будет тянутся день и доступное время и отсылаться в чат
		global _time
		_time = {id: id+10 for id in range(10)} #id нужен чтобы выбрать время и отослать его в бот, время тянется из базы, пока чисто рандомный словарь
		for key in _time.keys():
			bot.send_message(message.chat.id,"%s  %s" % (key, _time[key]))
		bot.send_message(message.chat.id,"Выберите время которое вам подходит и отправьте его номер")	
	@bot.message_handler(regexp="[0-9]+$")
	def select_time(message):
		print(message.text) #по номеру выбираем время и отправляем запрос в бд,тем самым забивая время
		bot.send_message(message.chat.id,"Напишите какие типы услуг вы хотите забронировать(например: мойка, пылесос )")	
	#сюда добавить карты
	@bot.message_handler(func=lambda m: True)
	def function(message):
		print(message.text)
		bot.send_message(message.chat.id,"Вы записаны на мойку, чтобы посомтреть ваши заказы введите /history")	


#оповещение о мойке

@bot.message_handler(commands=["history"])

def command_comments(message): 
	bot.reply_to(message,'Ваши записи: ')
	#здесь будет запрос из базы, который показывает все текущие записи



if __name__ == '__main__':
	bot.polling(none_stop=True)
	
