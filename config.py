'''
Config functions such as read settings from file, logging, etc.
'''
import logging
import shutil
import os, sys
from ConfigParser import SafeConfigParser
import ast

def Config_file(section, option):
	config = SafeConfigParser()
	config.read('config.conf')
	try:
		value = config.get(section, option)
	except Exception, e:
		logging.error('Error reading config file!')
		logging.error(e)
		sys.exit(1)
	return value

def Logging():
	if Debugging == True:
		Logging_level = logging.DEBUG
	else:
		Logging_level = logging.INFO
	logging.basicConfig(filename=Log_file,level=Logging_level, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
	logging.info('Starting application: version %s' %Version)

def Remove_folder(folder):
    if (os.path.exists(folder) == True):
        try:
            shutil.rmtree(folder)
            logging.debug("Removing folder: " + folder)
        except IOError as e:
            logging.error(e)

def Preconditions(folder):
	if (os.path.exists(folder) == False):
		try:
			os.mkdir(folder)
			logging.debug("Creating folder: " + folder)
		except IOError as e:
			logging.error(e)

def Wishlist():
	# Wishlist has a list of models that should be recorded
    try:
        with open(wishlist_file, 'r') as f:
                data = [line.strip() for line in f]
        f.close()
    except IOError, e:
        logging.info("Error: %s file does not appear to exist." % wishlist_file)
        logging.debug(e)
        sys.exit(1)
    return data

def Store_Debug(lines, filename):
	# Store html to debug.log file
	if (os.path.exists('Debug') == False):
		try:
			os.mkdir('Debug')
			logging.debug("Creating folder: Debug")
		except IOError as e:
			logging.error(e)
	try:
		f = open('Debug/' + filename, 'a')
		for line in lines:
			f.write(line.encode("utf-8"))
		f.close()
	except IOError, e:
		logging.info("Error: debug.log file does not appear to exist.")

# Setup options
URL = Config_file('url','URL')
URL_follwed = Config_file('url', 'URL_follwed')
USER = Config_file('credentials','USER')
PASS = Config_file('credentials','PASS')
Video_folder = Config_file('folders','Video_folder')
Script_folder = Config_file('folders','Script_folder')
Log_file = Config_file('files','Log_file')
wishlist_file = Config_file('files','wishlist_file')
Time_delay = int(Config_file('delays','Time_delay'))
Version = Config_file('version','Version')
RTMPDUMP = Config_file('advanced','RTMPDUMP')
# Enable storing html to debug.log file + set logging level
Debugging = ast.literal_eval(Config_file('debug','Debugging'))
