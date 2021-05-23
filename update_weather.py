from selenium import webdriver
from PIL import Image
# from translate import Translator
from datetime import datetime
from deep_translator import GoogleTranslator

# https://sites.google.com/a/chromium.org/chromedriver/downloads
def update_img(city):
	try:
		to_translate = city
		t_city = GoogleTranslator(source='auto', target='en').translate(to_translate)

		# translator= Translator(from_lang="russian",to_lang="english")
		# t_city = translator.translate(city)

		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument(f'window-size={2000},{1080}')
		options.add_argument('hide-scrollbars')

		url = 'https://yandex.ru/pogoda/' + t_city.lower()
		print("\n\n<<", url, ">>\n\n")

		browser = webdriver.Chrome(chrome_options=options)
		browser.get(url)
		browser.save_screenshot('data/weather.png')

		img = Image.open("data/weather.png")
		area = (305, 105, 1388, 675)
		cropped_img = img.crop(area)
		# cropped_img.show()
		cropped_img.save("data/weather.png")

		return ""
	except Exception as e:
		print(e)
		return "City Error"