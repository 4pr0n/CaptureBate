#!/usr/bin/env python
'''
Main file that includes all functions in appropriate order
'''
import config
from time import sleep
import connection
import modellists
import run

if __name__ == '__main__':
	## Main section
	# Set logging
	config.Logging()

	# Create directories
	config.Remove_folder(config.Script_folder)
	config.Create_folder(config.Script_folder)
	config.Create_folder(config.Video_folder)

	# Connecting to server
	client = connection.Connection()

	# Get the models list and create main list
	Models_list_store = modellists.Models_list(client)

	# Select models for recording according to wishlist
	Selected_models = modellists.Select_models(Models_list_store)

	# Parse page for each model and creatr links for rtmpdump
	modellists.Get_links(client, Selected_models)

	# Run scripts
	run.Run_scripts()

	# First delay before loop
	config.logging.info('Waiting for %d seconds' %config.Time_delay)
	sleep(config.Time_delay)

	while True:
		## Reassign updated main models list
		# Connecting to server
		client = connection.Connection()

		# Models_list_store = Compare_lists(Models_list_store, Models_list(client))
		config.logging.info(str(len(Models_list_store)) + ' Models in the list before checking: ' + str(Models_list_store))

		# Models_list_store_new is a list of new models
		Models_list_store = modellists.Compare_lists(modellists.Models_list(client), modellists.Rtmpdump_models())
		config.logging.info('[Loop] List of new models for adding: ' + str(Models_list_store))
		Selected_models = modellists.Select_models(Models_list_store)

		# Remove old and create new script folder if we have someone to add
		if len(Selected_models) != 0:
			config.Remove_folder(config.Script_folder)
			config.Create_folder(config.Script_folder)

			# Parse page for each model and creatr links for rtmpdump
			modellists.Get_links(client, Selected_models)

			# Run scripts
			run.Run_scripts()

		config.logging.info('[Loop] Model list after check looks like: %d models:\n %s \n and models currently being recorded are:\n %s' %(len(Models_list_store), str(Models_list_store), str(modellists.Rtmpdump_models())))
		config.logging.info('[Sleep] Waiting for next check (%d seconds)' %config.Time_delay)
		sleep(config.Time_delay)
