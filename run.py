'''
Run each models rtmpdump script
'''
import config
import os, subprocess

def Run_scripts():
	# Run all scripts from Scripts folder
	config.logging.info('[Run_scripts] Running scripts:')
	Scripts = os.listdir('Scripts/')
	config.logging.debug(Scripts)
	#print len(Scripts)
	if (len(Scripts) != 0):
		for script in Scripts:
			config.logging.info('[Run_scripts] Run: '+ script)
			subprocess.Popen('./' + script, cwd='Scripts/')
	else:
		config.logging.warning('[Run_scripts] There is nothing to execute!')
