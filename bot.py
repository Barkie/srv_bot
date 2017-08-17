# -*- coding: utf-8 -*-
import telebot
import config
import os
import time
import requests
import re
import json

bot = telebot.TeleBot(config.tgtoken)

@bot.message_handler(commands=['start'])
def start(message):

    """
    The first command
    """

    bot.send_message(message.chat.id, '''
    Hello! This is really secret bad motherfucker.
    ''') 

@bot.message_handler(commands=['help'])
def start(message):

    """
    The help command
    """

    bot.send_message(message.chat.id, '''
    Can't tell you anything, sorry.
    ''') 

@bot.message_handler(commands=['show_vpn_users'])
def current_vpn_users(message):
	try:
		user = (message.chat.username, message.chat.id)
		print(user)
		if user != ('Barkie', 3314252):
			answer = 'Sorry, ' + str(message.chat.username) + ', access denied for you.'
			bot.send_message(message.chat.id, answer)
		else:
			f = open('/var/log/openvpn/openvpn-status.log', 'r')
			some_str = f.read()
			f.close()
			current_users = re.findall(r'(.*?),(.*?),(\d*),(\d*),(.*)\n', some_str)
			update_datetime = re.findall(r'Updated,(.*)\n', some_str)
			users_summ = 'OpenVPN users list. \n' + 'Updated: ' + str(update_datetime[0]) + '\n\n'
			for item in current_users:
				username = item[0]
				address = item[1]
				bytes_received = item[2]
				bytes_sent = item[3]
				connected_since = item[4]
				users_summarized = ('Username: ' + str(username) + '\n' + 'IP Address: ' + str(address) + '\n' \
					+ 'Bytes Received: ' + str(bytes_received) + '\n' + 'Bytes Sent: ' + str(bytes_sent) \
					+ '\n' + 'Connected since: ' + str(connected_since) + '\n\n')
				users_summ += users_summarized

			bot.send_message(message.chat.id, users_summ)
	except Exception as e:
		log.error(
			'! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
															sys.exc_info()[2].tb_lineno,
															os.path.basename(
																sys.exc_info()[2].tb_frame.f_code.co_filename),
															sys._getframe().f_code.co_name,
															e))

@bot.message_handler(commands=['show_btc_value'])
def current_btc_value(message):
	try:
		user = (message.chat.username, message.chat.id)
		print(user)
		if user != ('Barkie', 3314252):
			answer = 'Sorry, ' + str(message.chat.username) + ', access denied for you.'
			bot.send_message(message.chat.id, answer)
		else:
			res = requests.get('https://blockchain.info/ru/ticker')
			if res.status_code == 200:  # HTTP OK
				resmap = json.loads(res.text)
				USD_value = resmap['USD']['last']
				EUR_value = resmap['EUR']['last']
				RUB_value = resmap['RUB']['last']
				answer = ('1 BTC = ' + str(USD_value) + ' USD\n' \
					+ '1 BTC = ' + str(EUR_value) + ' EUR\n' \
					+ '1 BTC = ' + str(RUB_value) + ' RUB')
				bot.send_message(message.chat.id, answer)
			else:
				bot.send_message(message.chat.id, 'Sorry, \
					https://blockchain.info is not answering. Try again later')
	except Exception as e:
		log.error(
			'! {} exception in row #{} ({}, {}): {}'.format(sys.exc_info()[0].__name__,
															sys.exc_info()[2].tb_lineno,
															os.path.basename(
																sys.exc_info()[2].tb_frame.f_code.co_filename),
															sys._getframe().f_code.co_name,
															e))	


if __name__ == '__main__':
	bot.polling(none_stop=True)



