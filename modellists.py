'''
Functions such as getting models list, details for rtmpdump, etc.
'''
import config
from bs4 import BeautifulSoup
import re
import time, datetime
import signal, os

def Models_list(client):
	# Moving to followed models page
	soup = None

	try:
		config.logging.info("Redirecting to " + config.URL_follwed)
		request = client.get(config.URL_follwed)
		soup = BeautifulSoup(request.text)
	except Exception, e:
		config.logging.error('Some error during connecting to ' + config.URL)
		config.logging.error(e)

	#config.logging.debug('Page Source for ' + config.URL_follwed + '\n' + request.text)
	page_source = 'Page Source for ' + config.URL_follwed + '\n' + request.text

	if config.Debugging == True:
		Store_Debug(page_source, "modellist.log")

	ul_list = soup.find('ul', class_ = "list")
	li_list = soup.findAll('li', class_ = "cams")

	#config.logging.debug(li_list)
	if config.Debugging == True:
		Store_Debug(li_list, "li_list.log")

	## Finding who is not offline
	online_models = []

	for li in li_list:
		if li.text != "offline":
			if li.parent.parent.parent.div.text == "IN PRIVATE":
				config.logging.warning(li.parent.parent.a.text[1:] + ' model is now in private mode')
			else:
				online_models.append(li.parent.parent.a.text[1:])

	config.logging.info('[Models_list] %s models are online: %s'  %(len(online_models), str(online_models)))

	return online_models

def Select_models(Models):
	# Select models that we need
	Wish_list = config.Wishlist()
	Model_list_approved = []
	config.logging.info('[Select_models] Which models are in the wishlist?')

	for model in Models:
		if model in Wish_list:
			config.logging.info("[Select_models] " + model + ' is in the wishlist')
			Model_list_approved.append(model)

	if len(Model_list_approved) == 0:
		config.logging.warning('[Select_models] No new models from the wishlist')

	return Model_list_approved

def Password_hash(string):
	#replace special chars for unix shell! \$ and \/ and \= mostly
	string = string.replace("\u003D","\=")
	string = string.replace("$", "\$")
	string = string.replace("/", "\/")

	return string

def Get_links(client, Models_list_store):
	## Get the models options for creating rtmpdump string
	if (len(Models_list_store) != 0):
		for model in Models_list_store:
			r3 = client.get("https://chaturbate.com/" + model + "/")
			soup = BeautifulSoup(r3.text)
			script_list =  soup.findAll('script')
			#config.logging.debug('[Get_links] Script Source for ' + "https://chaturbate.com/" + model + "/\n" + str(script_list))
			page_source = '[Get_links] Script Source for ' + "https://chaturbate.com/" + model + "/\n" + str(script_list)

			if config.Debugging == True:
				Store_Debug(page_source, model + "_source.log")

			## Put model_page_source in the temporary file
			regex = re.compile(r""".*EmbedViewerSwf""", re.VERBOSE)

			#print str(script_list).splitlines()
			script_list_lines = str(script_list).splitlines()

			for i,line in enumerate(script_list_lines):
				match = regex.match(line)
				pw_match = re.search(r"password:\s'(pbkdf2_sha256.*[\\u003D|=])", line)

				if pw_match:
					config.logging.debug('[Get_Links] found hashed password: %s' % pw_match.group(1))
					pw = Password_hash(pw_match.group(1))

				if match:
					flash_pl_ver = re.sub(',', '', re.sub(' ', '', re.sub('"', '', script_list_lines[i + 1])))
					model_name = re.sub('\'', '', re.sub(',', '', re.sub(' ', '', re.sub('"', '', script_list_lines[i + 2]))))
					stream_server = re.sub('\'', '', re.sub(',', '', re.sub(' ', '', re.sub('"', '', script_list_lines[i + 3]))))
					config.logging.debug('Extracted:\n' + flash_pl_ver + '\n' + model_name + '\n' + stream_server)
					# write models rtmpdump string to file
					flinks = open(config.Script_folder + '/' + model + '.sh', 'w')
					flinks.write('#!/bin/sh\n')
					ts = time.time()
					currentTime = time.strftime("%Y-%m-%d_%H:%M:%S")

					form_dict = {
						"stream_server": stream_server,
						"model_name": model_name,
						"username": config.USER.lower(),
						"flash_ver": "2.645",
						"pw_hash": pw,
						"video_folder": config.Video_folder,
						"date_string": currentTime
					}

					flinks.write('/usr/bin/env rtmpdump --quiet --live --rtmp "rtmp://%(stream_server)s/live-edge" --pageUrl "http://chaturbate.com/%(model_name)s" --conn S:%(username)s --conn S:%(model_name)s --conn S:%(flash_ver)s --conn S:%(pw_hash)s --token "m9z#$dO0qe34Rxe@sMYxx" --playpath "playpath" --flv "../%(video_folder)s/Chaturbate_%(date_string)s_%(model_name)s.flv"' % form_dict)
					flinks.write('\n')
					flinks.close()
					os.chmod(config.Script_folder + '/' + model + '.sh', 0777)
					config.logging.info('[Get_links] ' + model + '.sh is created')
	else:
		config.logging.warning('[Get_links] No models to get!')

def Rtmpdump_models():
	models = []

	for line in os.popen("ps xa | grep rtmpdump"):
		fields = line.split()
		pid = fields[0]
		process = fields[4]

		if process == config.RTMPDUMP:
			#print process + pid
			#print fields[19][2:]
			models.append(fields[14][2:])

	config.logging.debug('Rtmpdump shows the following models: \n' + str(models))

	return models

def Compare_lists(ml, mlr):
	# Comparing old models list(Main list) to new(updated) models list
	# This loop is used for removing offline models from main list
	ml_new = []
	config.logging.info('[Compare_lists] Checking model list:')

	for model in ml:
		if model in mlr:
			config.logging.info("[Compare_lists] " + model + " is still being recorded")
			config.logging.debug("[Compare_lists] Removing " + model + " model")
		else:
			config.logging.debug("[Compare_lists] " + model + " is online")
			ml_new.append(model)

	config.logging.debug("[Compare_lists] List of models after comparing:" + str(ml_new))

	return ml_new
