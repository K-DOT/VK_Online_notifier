#!/usr/bin/python
import os
import sys
import json
import time
import configparser
import urllib.request as urllib
from multiprocessing import Process

last_status = 1
last_status_mobile = 1

def parse_config(config_file):
    config = configparser.ConfigParser(inline_comment_prefixes='#')
    config.read_file(open(config_file))
    items = dict(config.items('MAIN'))
    return items    

def status_message(online, mobile, name, modes):
    if (online and not mobile) and modes['check_online'] == 'yes':
        os.system('notify-send --icon=gtk-info VK_Online_notifier "User %s is now online"' % name) 
        return 'User %s is now online' % name
    elif (online and mobile) and modes['check_online_from_mobile'] == 'yes':
        os.system('notify-send --icon=gtk-info VK_Online_notifier "User %s is now online from mobile"' % name)
        return 'User %s is now online from mobile' % name
    elif modes['check_offline'] == 'yes':
        os.system('notify-send --icon=gtk-info VK_Online_notifier "User %s is now offline"' % name)
        return 'User %s is now offline' % name
    

def check_status(address, interval, modes):
    while True:       
        url = 'https://api.vk.com/method/users.get?user_ids=%s&fields=online' % address
        response = urllib.urlopen(url).read()
        response_dict = json.loads(response.decode('utf-8'))['response']
        global last_status, last_status_mobile        
        user_name = '%s %s' % (response_dict[0].get('first_name', 0), response_dict[0].get('last_name', 0))
        is_online = response_dict[0].get('online', 0)
        is_online_mobile = response_dict[0].get('online_mobile', 0) 
        #print(last_status, is_online, last_status_mobile, is_online_mobile) 
        if last_status != is_online or last_status_mobile != is_online_mobile:
            print(status_message(is_online, is_online_mobile, user_name, modes))
            last_status, last_status_mobile = is_online, is_online_mobile 
        time.sleep(interval) if interval >= 10 else time.sleep(10)


if __name__ == '__main__':    
     if len(sys.argv) == 3 and sys.argv[1] in ('-c', '--conf'):
         config = parse_config(sys.argv[2])
     else:
         config = parse_config('config.cfg')
     addresses = config['users'].split(',')
     interval = int(config['check_interval'])
     modes = {
         'check_online' : config['online'],  
         'check_online_from_mobile' : config['online_from_mobile'],
         'check_offline' : config['offline']
     }
     
     for address in addresses:
         process = Process(target=check_status, args=(address,interval,modes))
         process.start()              
