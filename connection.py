'''
Connecting to site
'''
import config
from time import sleep
import requests
from MyAdapter import MyAdapter

# Connects and logs in to to Chaturbate, then returns the logged in requests session
def Connection():
	#Connecting to server
	count = 0
	connected = 0

	while connected != 1:
		try:
			config.logging.info('Connecting to ' + config.URL)
			client = requests.session()
			client.mount('https://', MyAdapter())

			# Retrieve the CSRF token first
			request = client.get(config.URL)

			connected = 1
		except Exception, e:
			config.logging.error('Some error during connecting to ' + config.URL)
			config.logging.error(e)
			config.logging.error('Trying again after 60 seconds')
			count += 1

			if count > 5:
				config.logging.error('Performing delay for 1800 seconds')
				sleep(1740)

				count = 0
			sleep(60)

	csrfToken = request.cookies['csrftoken']

	# Set login data and perform submit
	login_data = dict(username = config.USER, password = config.PASS, csrfmiddlewaretoken=csrfToken, next='/')

	try:
		request = client.post(config.URL, data = login_data, headers = dict(Referer=config.URL))
	except Exception, e:
		config.logging.error('Some error during posting to ' + config.URL)
		config.logging.error(e)

	#config.logging.debug('Page Source for ' + config.URL + '\n' + request.text)
	page_source = 'Page Source for ' + config.URL + '\n' + request.text

	# if Debugging is enabled Page source goes to debug.log file
	if config.Debugging == True:
		Store_Debug(page_source, "connection.log")

	return client




