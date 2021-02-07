api = "45a352f4db1999a3605cb35805c5a00a86411222539a38a1a2ee2b82f34d90363b37d1c0c140218b0f3ce"

import codecs
import vk_api
import json
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint as rnd
from random import choice as chs

dont_understand = ["Hmm...", "Хммммм....", "What are you talking about?", "Whaaaaaat?", "Не понимаю",
					"Что что что?", "Тебя не понять", "Попробуй что-ниудь другое", "Мне такое не понять"]
hello_messages = ["привет", "прив", "ку", "салам", "шалом", "пис", "start", 
					"/start", "хай", "начать", "здравствуй", "здравствуйте", "приветик", "hello", "hello world"]
my_hello = ["Привет, просто привет", "Саламчик пополамчик", "Дратути", "Наблюдаю не готовых к сессии",
				"Доброе утро! И на случай, если я вас больше не увижу — добрый день, добрый вечер и доброй ночи!",
				"Давно не виделись! Как твои старые кости, друг?", "Рад видеть Его Величество (Её Величество) в добром здравии!"]

fila = "https://www.notion.so/8a285c0be03b4078a88d9e9fa4bc4c6d"
matan = "https://vk.com/doc71883084_578470968?hash=99c5ea81426d40fcf4&dl=3877ed1f352b737778"
agila = "https://vk.com/doc71883084_578470971?hash=c14dd1e2261580335a&dl=71e676b5f347a95abd"
sobr_by_session = "https://vk.com/doc71883084_577720531?hash=c371f85af56ef5931b&dl=70d59bd705e37885a8"

default_raspi = "https://sun9-65.userapi.com/impg/afkLS8MK7drz0ABDJuk7t0nWSi4wZOZQKOiPnA/YIyaqOQyLJU.jpg?size=1280x350&quality=96&proxy=1&sign=e122ce2401f9ec1f05e8b656170b5ef9&type=album"
dop_raspi = "https://sun9-56.userapi.com/impg/4Koofa9WHVzkPWYT3TtXP8QoCfEQL_hCZNTC6Q/nJXixuI4pEs.jpg?size=1080x810&quality=96&proxy=1&sign=0fb40ef462f0b7a5d7c6b23c0c28a52e&type=album"

institute = "https://drive.google.com/file/d/0B4Cl9AB9m1p6ZWl5NmMtMGZKS00/view"
tests = "https://yadi.sk/d/K7vQsjFvdqd26"
mtuci_courses_1_2 = "https://cloud.mail.ru/public/4aVf/wj8n1ZxGV/"
mtuci_courses_1_4 = "https://www.dropbox.com/sh/3sr3iq94xzhk071/AABmA1eh8KCVdU5SmE1DyMlma?dl=0"
all_subj = "https://cloud.mail.ru/public/4c0dc7a2dff7/1%20%D0%BA%D1%83%D1%80%D1%81/"
mtuci_old = "https://www.dropbox.com/sh/7tznxodz8zck1np/AADvxA7uRZmpvdguQrpIiRt7a?dl=0&m="


while True:
	try:
		# vk_session = vk_api.VkApi(token=api)

		# get_random_id = lambda : rnd(10**8, 10**9 - 1)

		API_VERSION = '5.120'

		vk_session = VkApi(token=api, api_version=API_VERSION)
		vk = vk_session.get_api()
		longpoll = VkBotLongPoll(vk_session, group_id='198357020')

		# longpoll = VkLongPoll(vk_session)
		# vk = vk_session.get_api()

		my_id = 184891897


		keyboard_menu = VkKeyboard(one_time=False)
		keyboard_menu.add_button('Когда сессия?', color=VkKeyboardColor.POSITIVE)
		keyboard_menu.add_button('Когда консультации?', color=VkKeyboardColor.PRIMARY)
		keyboard_menu.add_line()
		keyboard_menu.add_button('Подписаться на напоминания', color=VkKeyboardColor.SECONDARY)
		keyboard_menu.add_button('Отписаться', color=VkKeyboardColor.NEGATIVE)
		keyboard_menu.add_line()
		keyboard_menu.add_button('Полезные ссылки, облока итд', color=VkKeyboardColor.POSITIVE)

		keyboard_admin = VkKeyboard(one_time=False)
		keyboard_admin.add_button('Когда сессия?', color=VkKeyboardColor.POSITIVE)
		keyboard_admin.add_button('Когда консультации?', color=VkKeyboardColor.PRIMARY)
		keyboard_admin.add_line()
		keyboard_admin.add_button('Подписаться на напоминания', color=VkKeyboardColor.SECONDARY)
		keyboard_admin.add_button('Отписаться', color=VkKeyboardColor.NEGATIVE)
		keyboard_admin.add_line()
		keyboard_admin.add_button('Полезные ссылки, облока итд', color=VkKeyboardColor.POSITIVE)
		keyboard_admin.add_line()
		keyboard_admin.add_button('Текст Рассылки', color=VkKeyboardColor.SECONDARY)
		keyboard_admin.add_button('Изменить текст', color=VkKeyboardColor.SECONDARY)
		keyboard_admin.add_line()
		keyboard_admin.add_button('Разослать!', color=VkKeyboardColor.SECONDARY)
		keyboard_admin.add_button('Кто подписался?', color=VkKeyboardColor.SECONDARY)

		keyboard_links = VkKeyboard(one_time=False)
		keyboard_links.add_callback_button(label='Билеты по философии', color=VkKeyboardColor.SECONDARY, payload={"type": "open_link", "link": fila})
		keyboard_links.add_callback_button(label='Собрание по сессиям', color=VkKeyboardColor.SECONDARY, payload={"type": "open_link", "link": sobr_by_session})
		keyboard_links.add_line()
		keyboard_links.add_callback_button(label='Курсач ВышМат', color=VkKeyboardColor.PRIMARY, payload={"type": "open_link", "link": matan})
		keyboard_links.add_callback_button(label='Курсач Агила', color=VkKeyboardColor.PRIMARY, payload={"type": "open_link", "link": agila})
		keyboard_links.add_line()
		keyboard_links.add_button('Расписание занятий', color=VkKeyboardColor.SECONDARY)
		keyboard_links.add_button('Расписание секций', color=VkKeyboardColor.SECONDARY)
		keyboard_links.add_line()
		keyboard_links.add_button('Home', color=VkKeyboardColor.POSITIVE)
		keyboard_links.add_button('Облака', color=VkKeyboardColor.PRIMARY)

		keyboard_clouds = VkKeyboard(one_time=False)
		keyboard_clouds.add_callback_button(label='Институт', color=VkKeyboardColor.PRIMARY, payload={"type": "open_link", "link": institute})
		keyboard_clouds.add_callback_button(label='Тесты', color=VkKeyboardColor.PRIMARY, payload={"type": "open_link", "link": tests})
		keyboard_clouds.add_line()
		keyboard_clouds.add_callback_button(label='Курсы 1-2', color=VkKeyboardColor.SECONDARY, payload={"type": "open_link", "link": mtuci_courses_1_2})
		keyboard_clouds.add_callback_button(label='Курсы 1-4', color=VkKeyboardColor.SECONDARY, payload={"type": "open_link", "link": mtuci_courses_1_4})
		keyboard_clouds.add_line()
		keyboard_clouds.add_callback_button(label='Все предметы', color=VkKeyboardColor.PRIMARY, payload={"type": "open_link", "link": all_subj})
		keyboard_clouds.add_callback_button(label='MTUCI old', color=VkKeyboardColor.PRIMARY, payload={"type": "open_link", "link": mtuci_old})
		keyboard_clouds.add_line()
		keyboard_clouds.add_button('Назад', color=VkKeyboardColor.POSITIVE)



		session_time = "Расписание сессий:\n\nВышМат:\t 12.01.2021 в 9.30\nФилософия:\t 19.01.2021 в 14.00\nАлгГеом:\t 23.01.2021 в 9.30"
		cons_time = "Расписание консультаций:\n\nВышМат:\t 11.01.2021 в 13.00\nФилософия:\t 18.01.2021 в 17.00\nАлгГеом:\t 22.01.2021 в 15.00"

		mail_text = "Lol"
		mail_text_change = False

		clear_line = lambda x: x.replace("\n", "").replace(" ", "")

		filename = "students_id.txt"
		def get_stud_list_from_file():
			global mail_text
			mail_text = ""
			info = {"Names": [], "Id": []}
			save_mail = False
			with codecs.open(filename, encoding = 'utf-8', mode = 'r') as file:
				line = file.readline()
				while line:
					s_line = line.split(" ")
					
					if save_mail:
						mail_text += line

					if len(s_line) == 3 and not save_mail:
						info["Names"].append(s_line[0] + " " + s_line[1])
						info["Id"].append(s_line[2])
					else:
						save_mail = True

					line = file.readline()

			return info

		def sorting_info():
			arr = [*zip(all_users["Names"], all_users["Id"])]
			arr = sorted(arr, key=lambda i:i[0])
			all_users["Names"] = [x[0] for x in arr]
			all_users["Id"] = [x[1] for x in arr]

		def update_stud_file_list():
			sorting_info()
			with codecs.open(filename, encoding = 'utf-8', mode = 'w') as file:
				for i in range(len(all_users["Names"])):
					line = str(all_users["Names"][i]) + " " + str(all_users["Id"][i])
					file.write(line.replace("\n", "") + "\n")
				file.write("-\n")
				file.write(mail_text)

		all_users = get_stud_list_from_file()
		update_stud_file_list()

		def send_message(id, peer, text, keyboard=None):
			vk.messages.send(
				keyboard=keyboard,
				peer_id=peer,
				random_id = get_random_id(),
				message= text,
				user_id = id
			)

		def get_name(user_id):
			data = vk.users.get(user_ids = user_id, name_case = 'nom')[0]
			return data['last_name'] + " " + data['first_name']

		for event in longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				if event.from_user: #Если написали в ЛС
					command = event.obj.message['text']
					u_id = event.object.user_id
					peer = event.obj.message['from_id']

					kb = keyboard_admin.get_keyboard() if my_id == u_id else keyboard_menu.get_keyboard()

					if 'callback' not in event.obj.client_info['button_actions']:
						print(f'Клиент {event.obj.message["from_id"]} не поддерж. callback')

					if mail_text_change and my_id == u_id:
						mail_text = command
						mail_text_change = False
						update_stud_file_list()

						send_message(u_id, "New mail text:\n" + mail_text, kb)
					elif command.lower() in hello_messages:
						send_message(u_id, peer, chs(my_hello), kb)
					elif command == 'Когда сессия?':
						send_message(u_id, pper, session_time, kb)
					elif command == 'Когда консультации?':
						send_message(u_id, peer, cons_time, kb)
					elif command == 'Полезные ссылки, облока итд' or command == 'Назад':
						send_message(u_id, peer, "Открываю клавиатуру с ссылками", keyboard_links.get_keyboard())
					elif command == 'Home':
						send_message(u_id, peer, "Открываю домашнюю клаиватуру", kb)
					elif command == 'Облака':
						send_message(u_id, peer, "Открываю клаиватуру с облаками", keyboard_clouds.get_keyboard())
					elif command == 'Отписаться':
						user_name = get_name(u_id)
						if (user_name not in all_users["Names"]):
							send_message(u_id, peer, "Вы еще подписались на нашу рассылку (((", kb)
						else:
							all_users["Names"].remove(user_name)
							all_users["Id"].remove(str(u_id) + "\n")

							update_stud_file_list()
							info = get_stud_list_from_file()
							send_message(u_id, peer, "Вы успешно отписались от наших напоминаний(", kb)

					elif command == 'Подписаться на напоминания':
						user_name = get_name(u_id)
						if (user_name in all_users["Names"]):
							send_message(u_id, peer, "Вы уже подписались на нашу рассылку ;)", kb)
						else:
							all_users["Names"].append(user_name)
							all_users["Id"].append(u_id)

							update_stud_file_list()
							info = get_stud_list_from_file()
							send_message(u_id, peer, "Теперь вы подписаны на напоминания!", kb)

					elif  command == 'Текст Рассылки' and my_id == u_id:
						send_message(u_id, peer, mail_text, kb)
					elif command == 'Изменить текст' and my_id == u_id:
						send_message(u_id, peer, "Введите новый текст", kb)
						mail_text_change = True
					elif command == 'Разослать!' and my_id == u_id:
						for i, ind in enumerate(all_users["Id"]):
							#print("Sending to {}".format(all_users["Names"][i]))
							send_message(int(ind), mail_text, kb)
					elif command == 'Кто подписался?' and my_id == u_id:
						text = ""
						for i, ind in enumerate(all_users["Names"]):
							text += str(i + 1) + ") " + all_users["Names"][i] + "\n"
						send_message(u_id, peer, text, kb)
					else:
						send_message(u_id, peer, chs(dont_understand), kb)
			elif event.type == VkBotEventType.MESSAGE_EVENT:
				if event.object.payload.get('type') in CALLBACK_TYPES:
					r = vk.messages.sendMessageEventAnswer(
						event_id=event.object.event_id,
						user_id=event.object.user_id,
						peer_id=event.object.peer_id,                                                   
						event_data=json.dumps(event.object.payload))
	except Exception as err:
		print(err)