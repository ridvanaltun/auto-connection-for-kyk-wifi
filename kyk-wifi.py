#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import sys

username = 'YOUR-USERNAME'
password = 'YOUR-PASSWORD'

url = 'https://wifi.kyk.gov.tr/'

if __name__ == "__main__":
	main()

def status(page):

	if page.status_code == 200:

		soup = bs(page.content,'html.parser')

		if 'Location' in page.text:
			return True

		elif 'Welcome. Enter your login information' in page.text:
			return False

		elif 'Maksimum giriş hakkınız doldu' in page.text:
			print("Maksimum giriş hakkınız doldu!")
			sys.exit()

		else:
			print("Not Found, probably wrong page!")
			sys.exit()

	else:
		print('Website respond is not correct.')
		print('HTTP CODE : ' + page.status_code)



def login(username, password):

	login_payload = {
	'j_username': username,
	'j_password': password,
	'submit': 'Giriş'
	}

	login = HTMLSession()

	with login as l:

		try:

			page = l.get(url)

			if not status(page):

				l.post(url + 'j_spring_security_check',data=login_payload)
				page = l.get(url)

				if status(page):
					print('Login successful.')
				else:
					print('Login unsuccessful.')

			else:
				print('You are already logined.')

		except:
			print('Host has failed to respond.')
			sys.exit()



def logout():

	logout = HTMLSession()

	with logout as out:

		try:
			page = out.get(url)

			if status(page):

				soup = bs(page.content,'html.parser')
				token = soup.find(attrs={'name':'javax.faces.ViewState'}).get('value')

				logout_payload = {
				'javax.faces.partial.ajax': 'true',
				'javax.faces.source': 'servisUpdateForm:j_idt139',
				'javax.faces.partial.execute': '@all',
				'servisUpdateForm:j_idt139': 'servisUpdateForm:j_idt139',
				'servisUpdateForm': 'servisUpdateForm',
				'javax.faces.ViewState': token
				}

				result = out.post(url+'logout',data=logout_payload)
				result.html.render()

				page = out.get(url)

				if not status(page):
					print('Logout successful.')
				else:
					print('Logout unsuccessful.')

			else:
				print('You are already logged out.')

		except:
			print('Host has failed to respond.')
			sys.exit()

def main():
	#login(username,password)
	#logout()