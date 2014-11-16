'''
Functions such as getting models list, details for rtmpdump, etc.
'''
from config import *
from bs4 import BeautifulSoup
import re
import time, datetime
import signal, os

def Models_list(client):
	# Moving to followed models page
	try:
		logging.info("Redirecting to " + URL_follwed)
		r2 = client.get(URL_follwed)
	except Exception, e:
		logging.error('Some error during connecting to '+URL)
		logging.error(e)
	soup = BeautifulSoup(r2.text)
	#logging.debug('Page Source for ' + URL_follwed + '\n' + r2.text)
	page_source = 'Page Source for ' + URL_follwed + '\n' + r2.text
	if Debugging == True:
		Store_Debug(page_source, "modellist.log")
	ul_list = soup.find('ul', class_="list")
	li_list = soup.findAll('li', class_="cams")
	#logging.debug(li_list)
	if Debugging == True:
		Store_Debug(li_list, "li_list.log")
	## Finding who is not offline
	online_models = []	
	for n in li_list:
		if n.text != "offline":
			if n.parent.parent.parent.div.text == "IN PRIVATE":
				logging.warning(n.parent.parent.a.text[1:] + ' model is now in private mode')
			else:
				online_models.append(n.parent.parent.a.text[1:])			
	logging.info('[Models_list] %s models are online: %s'  %(len(online_models),str(online_models)))
	return online_models

def Select_models(Models_list):
    # Select models that we need
    Wish_list = Wishlist()
    Model_list_approved = []
    logging.info('[Select_models] Which models are approved?')
    for model in Models_list:
        if model in Wish_list:
            logging.info("[Select_models] " + model+ ' is approved')
            Model_list_approved.append(model)
    if len(Model_list_approved) == 0:
        logging.warning('[Select_models]  No models for approving')
    return Model_list_approved

def Get_links(client, Models_list_store):
	## Get the models options for creating rtmpdump string
    if (len(Models_list_store) != 0):
        for model in Models_list_store:
            r3 = client.get("https://chaturbate.com/"+model+"/")
            soup = BeautifulSoup(r3.text)        
            script_list =  soup.findAll('script')
            #logging.debug('[Get_links] Script Source for ' + "https://chaturbate.com/" + model + "/\n" + str(script_list))        
            page_source = '[Get_links] Script Source for ' + "https://chaturbate.com/" + model + "/\n" + str(script_list)
            if Debugging == True:
            	Store_Debug(page_source, model + "_source.log")
            ## Put model_page_source in the temporary file
            regex = re.compile(r""".*EmbedViewerSwf""", re.VERBOSE)
            #print str(script_list).splitlines()
            script_list_lines = str(script_list).splitlines()
            for i,line in enumerate(script_list_lines):
                match = regex.match(line)
                if match:          
                    flash_pl_ver = re.sub(',', '', re.sub(' ', '', re.sub('"', '', script_list_lines[i+1])))                
                    model_name = re.sub('\'', '', re.sub(',', '', re.sub(' ', '', re.sub('"', '', script_list_lines[i+2])))) 
                    stream_server = re.sub('\'', '', re.sub(',', '', re.sub(' ', '', re.sub('"', '', script_list_lines[i+3]))))
                    logging.debug('Extracted:\n'+flash_pl_ver+'\n'+model_name+'\n'+stream_server)
                    # write models rtmpdump string to file
                    flinks = open(Script_folder+'/'+model+'.sh', 'w')
                    flinks.write('#!/bin/sh\n')        
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y.%d.%m_%H:%M')
                    flinks.write('rtmpdump -r "rtmp://%s/live-edge" -a "live-edge" -f "WIN 11,1,102,63" -W "http://chaturbate.com/%s" -p "http://chaturbate.com/%s/" -C S:testingallthethings -C S:%s -C S:2.645 -C S:pbkdf2_sha256\$12000\$QwwcaxjaV3Ik\$cZHXVde52w+Fl6In54Ay5ZeMQMAFueQgwnnLbkTWT5g\= -T "m9z#$dO0qe34Rxe@sMYxx" --live -y "mp4:%s-sd-2c42ecd59c03850eaee04fd89924ee5c3a24b1a41b56711cf3c0176135569ad8" -q -o "%s/Chaturbate_%s_%s.flv"' %(stream_server, flash_pl_ver, model_name, model_name, model_name,Video_folder , st, model_name))
                    flinks.write('\n')
                    flinks.close()
                    os.chmod(Script_folder+'/'+model+'.sh', 0777)
                    logging.info('[Get_links] ' + model+'.sh is created')
    else:
        logging.warning('[Get_links] No models to get!')

def Rtmpdump_models():
	models = []
	for line in os.popen("ps xa | grep rtmpdump"):
		fields = line.split()
		pid = fields[0]
		process = fields[4]
		if process == "rtmpdump":
			#print process + pid
			#print fields[19][2:]	
			models.append(fields[19][2:])
	logging.debug('Rtmpdump shows the following models: \n' + str(models))
	return models

def Compare_lists(ml, mlr):
	# Comparing old models list(Main list) to new(updated) models list
    # This loop is used for removing offline models from main list
    ml_new = []
    logging.info('[Compare_lists] Checking model list:')
    for model in ml:
    	if model in mlr:
    		logging.info("[Compare_lists] " + model + " is still being recorded")
    		logging.debug("[Compare_lists] Removing " + model + " model")    		
    	else:
    		logging.debug("[Compare_lists] " + model + " is online")
    		ml_new.append(model)
    logging.debug("[Compare_lists] List of models after comparing:" + str(ml_new))
    return ml_new
