from openpyxl import load_workbook
from datetime import datetime
import smtplib                                              # Импортируем библиотеку по работе с SMTP
import os                                                   # Функции для работы с операционной системой, не зависящие от используемой операционной системы

# Добавляем необходимые подклассы - MIME-типы
import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект


def send_otchet():
	try:
		cure_date = datetime.today().strftime('%d.%m.%Y')


		file = open("send_data.txt", "r")
		addr_to = file.readline().split(": ")[-1].replace("\n", "").replace(" ", "")

		file_name = file.readline().split(": ")[-1].replace("\n", "").replace(" ", "")

		# print("Sending {} \nto {}".format(file_name, addr_to))
		# n = input()

		# Load in the workbook
		wb = load_workbook(file_name)

		sheet = wb.get_sheet_by_name(wb.get_sheet_names()[0])
		# sheet['A1'] = "LOOOL"
		text = sheet['A1'].value
		text_arr = text.split(" ")

		text_arr[6] = cure_date

		res_text = " ".join(k for k in text_arr)

		sheet['A1'] = res_text

		wb.save(file_name)





		def send_email(addr_to, msg_subj, msg_text, files):
		    addr_from = "igrok332233@gmail.com"                         # Отправитель
		    password  = "Moscow2001"                                  # Пароль

		    msg = MIMEMultipart()                                   # Создаем сообщение
		    msg['From']    = addr_from                              # Адресат
		    msg['To']      = addr_to                                # Получатель
		    msg['Subject'] = msg_subj                               # Тема сообщения

		    body = msg_text                                         # Текст сообщения
		    msg.attach(MIMEText(body, 'plain'))                     # Добавляем в сообщение текст

		    process_attachement(msg, files)

		    #======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
		    server = smtplib.SMTP('smtp.gmail.com', 587)        # Создаем объект SMTP
		    server.starttls()                                   # Начинаем шифрованный обмен по TLS
		    server.login(addr_from, password)                   # Получаем доступ
		    server.send_message(msg)                            # Отправляем сообщение
		    server.quit()                                       # Выходим
		    #==========================================================================================================================

		def process_attachement(msg, files):                        # Функция по обработке списка, добавляемых к сообщению файлов
		    for f in files:
		        if os.path.isfile(f):                               # Если файл существует
		            attach_file(msg,f)                              # Добавляем файл к сообщению
		        elif os.path.exists(f):                             # Если путь не файл и существует, значит - папка
		            dir = os.listdir(f)                             # Получаем список файлов в папке
		            for file in dir:                                # Перебираем все файлы и...
		                attach_file(msg,f+"/"+file)                 # ...добавляем каждый файл к сообщению

		def attach_file(msg, filepath):                             # Функция по добавлению конкретного файла к сообщению
		    filename = os.path.basename(filepath)                   # Получаем только имя файла
		    ctype, encoding = mimetypes.guess_type(filepath)        # Определяем тип файла на основе его расширения
		    if ctype is None or encoding is not None:               # Если тип файла не определяется
		        ctype = 'application/octet-stream'                  # Будем использовать общий тип
		    maintype, subtype = ctype.split('/', 1)                 # Получаем тип и подтип
		    if maintype == 'text':                                  # Если текстовый файл
		        with open(filepath) as fp:                          # Открываем файл для чтения
		            file = MIMEText(fp.read(), _subtype=subtype)    # Используем тип MIMEText
		            fp.close()                                      # После использования файл обязательно нужно закрыть
		    elif maintype == 'image':                               # Если изображение
		        with open(filepath, 'rb') as fp:
		            file = MIMEImage(fp.read(), _subtype=subtype)
		            fp.close()
		    elif maintype == 'audio':                               # Если аудио
		        with open(filepath, 'rb') as fp:
		            file = MIMEAudio(fp.read(), _subtype=subtype)
		            fp.close()
		    else:                                                   # Неизвестный тип файла
		        with open(filepath, 'rb') as fp:
		            file = MIMEBase(maintype, subtype)              # Используем общий MIME-тип
		            file.set_payload(fp.read())                     # Добавляем содержимое общего типа (полезную нагрузку)
		            fp.close()
		            encoders.encode_base64(file)                    # Содержимое должно кодироваться как Base64
		    file.add_header('Content-Disposition', 'attachment', filename=filename) # Добавляем заголовки
		    msg.attach(file)                                        # Присоединяем файл к сообщению



		# Использование функции send_email()
		# addr_to   = "it_reports@bk.ru"                                # Получатель
		# addr_to   = "igrok332233@mail.ru"                                # Получатель
		files = [file_name]                                       # Если нужно отправить все файлы из заданной папки, нужно указать её

		send_email(addr_to, "Отчет БВТ2003 за " + cure_date, "", files)
		return "None"
	except:
		return "File openning ERROR"