api = "631f2e4b37f22f14bd3e66899d311e0ea900aa7b8bec6c021bb6b28927ad84960cb2e0a4e16e2214813aa"

import codecs
import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
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

errors = []

while True:
	try:
		vk_session = vk_api.VkApi(token=api)

		# get_random_id = lambda : rnd(10**8, 10**9 - 1)

		longpoll = VkLongPoll(vk_session)
		vk = vk_session.get_api()

		my_id = 184891897


		keyboard_menu = VkKeyboard(one_time=False)
		keyboard_menu.add_button('Когда сессия?', color=VkKeyboardColor.SECONDARY)
		keyboard_menu.add_button('Когда консультации?', color=VkKeyboardColor.PRIMARY)
		keyboard_menu.add_line()
		keyboard_menu.add_button('Подписаться', color=VkKeyboardColor.POSITIVE)
		keyboard_menu.add_button('Отписаться', color=VkKeyboardColor.NEGATIVE)
		keyboard_menu.add_line()
		keyboard_menu.add_button('Полезные ссылки, облока итд', color=VkKeyboardColor.SECONDARY)

		keyboard_admin = VkKeyboard(one_time=False)
		keyboard_admin.add_button('Когда сессия?', color=VkKeyboardColor.SECONDARY)
		keyboard_admin.add_button('Когда консультации?', color=VkKeyboardColor.PRIMARY)
		keyboard_admin.add_line()
		keyboard_admin.add_button('Подписаться', color=VkKeyboardColor.POSITIVE)
		keyboard_admin.add_button('Отписаться', color=VkKeyboardColor.NEGATIVE)
		keyboard_admin.add_line()
		keyboard_admin.add_button('Полезные ссылки, облока итд', color=VkKeyboardColor.SECONDARY)
		keyboard_admin.add_line()
		keyboard_admin.add_button('Текст Рассылки', color=VkKeyboardColor.SECONDARY)
		keyboard_admin.add_button('Изменить текст', color=VkKeyboardColor.SECONDARY)
		keyboard_admin.add_line()
		keyboard_admin.add_button('Разослать!', color=VkKeyboardColor.NEGATIVE)
		keyboard_admin.add_button('Кто подписался?', color=VkKeyboardColor.PRIMARY)
		keyboard_admin.add_line()
		keyboard_admin.add_button('ERRORS', color=VkKeyboardColor.NEGATIVE)
		keyboard_admin.add_button('ERRORS NUM', color=VkKeyboardColor.SECONDARY)

		keyboard_links = VkKeyboard(one_time=False)
		keyboard_links.add_button(label='Билеты по философии', color=VkKeyboardColor.SECONDARY)
		keyboard_links.add_button(label='Собрание по сессиям', color=VkKeyboardColor.SECONDARY)
		keyboard_links.add_line()
		keyboard_links.add_button(label='Курсач ВышМат', color=VkKeyboardColor.SECONDARY)
		keyboard_links.add_button(label='Курсач Агила', color=VkKeyboardColor.SECONDARY)
		keyboard_links.add_line()
		keyboard_links.add_button('Расписание занятий', color=VkKeyboardColor.PRIMARY)
		keyboard_links.add_button('Расписание секций', color=VkKeyboardColor.PRIMARY)
		keyboard_links.add_line()
		keyboard_links.add_button('Получить все ссылки разом', color=VkKeyboardColor.PRIMARY)
		keyboard_links.add_line()
		keyboard_links.add_button('Home', color=VkKeyboardColor.POSITIVE)
		keyboard_links.add_button('Облака', color=VkKeyboardColor.NEGATIVE)

		keyboard_clouds = VkKeyboard(one_time=False)
		keyboard_clouds.add_button(label='Институт', color=VkKeyboardColor.PRIMARY)
		keyboard_clouds.add_button(label='Тесты', color=VkKeyboardColor.PRIMARY)
		keyboard_clouds.add_line()
		keyboard_clouds.add_button(label='Курсы 1-2', color=VkKeyboardColor.PRIMARY)
		keyboard_clouds.add_button(label='Курсы 1-4', color=VkKeyboardColor.PRIMARY)
		keyboard_clouds.add_line()
		keyboard_clouds.add_button(label='Все предметы', color=VkKeyboardColor.PRIMARY)
		keyboard_clouds.add_button(label='MTUCI old', color=VkKeyboardColor.PRIMARY)
		keyboard_clouds.add_line()
		keyboard_clouds.add_button('Получить все облака разом', color=VkKeyboardColor.PRIMARY)
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

		def send_message(id, text, keyboard=None):
			vk.messages.send(
				keyboard=keyboard,
				random_id = get_random_id(),
				message= text,
				user_id = id
			)

		def get_name(user_id):
			data = vk.users.get(user_ids = user_id, name_case = 'nom')[0]
			return data['last_name'] + " " + data['first_name']

		for event in longpoll.listen():

			if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
				if event.from_user: #Если написали в ЛС
					command = event.text
					u_id = event.user_id

					kb = keyboard_admin.get_keyboard() if my_id == u_id else keyboard_menu.get_keyboard()

					if mail_text_change and my_id == u_id:
						mail_text = command
						mail_text_change = False
						update_stud_file_list()

						send_message(u_id, "New mail text:\n" + mail_text, kb)
					elif command.lower() in hello_messages:
						send_message(u_id, chs(my_hello), kb)
					elif command == 'Когда сессия?':
						send_message(u_id, session_time, kb)
					elif command == 'Когда консультации?':
						send_message(u_id, cons_time, kb)
					elif command == 'Полезные ссылки, облока итд' or command == 'Назад':
						send_message(u_id, "Открываю клавиатуру с ссылками", keyboard_links.get_keyboard())
					elif command == 'Home':
						send_message(u_id, "Открываю домашнюю клаиватуру", kb)
					elif command == 'Облака':
						send_message(u_id, "Открываю клаиватуру с облаками", keyboard_clouds.get_keyboard())
					elif command == 'Билеты по философии':
						send_message(u_id, fila, keyboard_links.get_keyboard())
					elif command == 'Собрание по сессиям':
						send_message(u_id, sobr_by_session, keyboard_links.get_keyboard())
					elif command == 'Курсач ВышМат':
						send_message(u_id, matan, keyboard_links.get_keyboard())
					elif command == 'Курсач Агила':
						send_message(u_id, agila, keyboard_links.get_keyboard())
					elif command == 'Расписание занятий':
						send_message(u_id, default_raspi, keyboard_links.get_keyboard())
					elif command == 'Расписание секций':
						send_message(u_id, dop_raspi, keyboard_links.get_keyboard())
					elif command == 'Институт':
						send_message(u_id, institute, keyboard_clouds.get_keyboard())
					elif command == 'Тесты':
						send_message(u_id, tests, keyboard_clouds.get_keyboard())
					elif command == 'Курсы 1-2':
						send_message(u_id, mtuci_courses_1_2, keyboard_clouds.get_keyboard())
					elif command == 'Курсы 1-4':
						send_message(u_id, mtuci_courses_1_4, keyboard_clouds.get_keyboard())
					elif command == 'Все предметы':
						send_message(u_id, all_subj, keyboard_clouds.get_keyboard())
					elif command == 'MTUCI old':
						send_message(u_id, mtuci_old, keyboard_clouds.get_keyboard())
					elif command == 'Получить все ссылки разом':
						text = "Философия: " + fila + "\n\nВышМат: " + matan + "\n\nАлгГеом: " + agila +\
							 "\n\nСобрание о сессиях: " + sobr_by_session + "\n\nРасписание занятий: " +\
							 default_raspi + "\n\nРасписание секций: " + dop_raspi
						send_message(u_id, text, keyboard_links.get_keyboard())
					elif command == 'Получить все облака разом':
						text = "Институт: " + institute + "\n\nТесты: " + tests + "\n\nМТУСИ курсы 1-2: " +\
							mtuci_courses_1_2 + "\n\nМТУСИ курсы 1-4: " + mtuci_courses_1_4 +\
							"\n\nВсе предметы: " + all_subj + "\n\nMTUCI old: " + mtuci_old
						send_message(u_id, text, keyboard_clouds.get_keyboard())

					elif command == 'Отписаться':
						user_name = get_name(event.user_id)
						if (user_name not in all_users["Names"]):
							send_message(event.user_id, "Вы еще подписались на нашу рассылку (((", kb)
						else:
							all_users["Names"].remove(user_name)
							all_users["Id"].remove(str(u_id) + "\n")

							update_stud_file_list()
							info = get_stud_list_from_file()
							send_message(event.user_id, "Вы успешно отписались от наших напоминаний(", kb)

					elif command == 'Подписаться':
						user_name = get_name(event.user_id)
						if (user_name in all_users["Names"]):
							send_message(event.user_id, "Вы уже подписались на нашу рассылку ;)", kb)
						else:
							all_users["Names"].append(user_name)
							all_users["Id"].append(event.user_id)

							update_stud_file_list()
							info = get_stud_list_from_file()
							send_message(event.user_id, "Теперь вы подписаны на напоминания!", kb)
					elif command == 'ERRORS' and my_id == u_id:
						text = "\n".join(errors) if errors else "None"
						send_message(u_id, text, kb)
					elif command == 'ERRORS NUM' and my_id == u_id:
						text = str(len(errors))
						send_message(u_id, text, kb)
					elif  command == 'Текст Рассылки' and my_id == u_id:
						send_message(u_id, mail_text, kb)
					elif command == 'Изменить текст' and my_id == u_id:
						send_message(u_id, "Введите новый текст", kb)
						mail_text_change = True
					elif command == 'Разослать!' and my_id == u_id:
						for i, ind in enumerate(all_users["Id"]):
							if (ind == my_id):
								send_message(int(ind), mail_text, keyboard_admin.get_keyboard())
							else:
								send_message(int(ind), mail_text, keyboard_menu.get_keyboard())
					elif command == 'Кто подписался?' and my_id == u_id:
						text = ""
						for i, ind in enumerate(all_users["Names"]):
							text += str(i + 1) + ") " + all_users["Names"][i] + "\n"
						send_message(u_id, text, kb)
					else:
						send_message(u_id, chs(dont_understand), kb)
	except Exception as err:
		print(err)
		errors.append(str(err))