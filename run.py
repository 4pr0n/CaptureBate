'''
Run each models rtmpdump script
'''
from config import *
import os, subprocess

def Run_scripts():
    # Run all scripts from Scripts folder
    logging.info('[Run_scripts] Running scripts:')
    Scripts = os.listdir('Scripts/')
    logging.debug(Scripts)
    #print len(Scripts)
    if (len(Scripts) != 0):
        for script in Scripts:
            logging.info('[Run_scripts] Run: '+ script)
            subprocess.Popen('./'+script, cwd='Scripts/')
    else:
        logging.warning('[Run_scripts] There is nothing to execute!')
