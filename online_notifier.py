#!/usr/bin/python
import os
import json
import time
import urllib.request as urllib
from multiprocessing import Process

addresses = ['rub_1998', 'id269609110']

last_status = 1
last_status_mobile = 1


def status_message(online, mobile, name):
    if online and not mobile:
        os.system('notify-send --icon=gtk-info VK_Online_notifier "User %s is now online"' % name) 
        return 'User %s is now online' % name
    elif online and mobile:
        os.system('notify-send --icon=gtk-info VK_Online_notifier "User %s is now online from mobile"' % name)
        return 'User %s is now online from mobile' % name
    else:
        os.system('notify-send --icon=gtk-info VK_Online_notifier "User %s is now offline"' % name)
        return 'User %s is now offline' % name
    

def check_status(address):
    while True:
        print('here')
        url = 'https://api.vk.com/method/users.get?user_ids=%s&fields=online' % address
        response = urllib.urlopen(url).read()
        response_dict = json.loads(response.decode('utf-8'))['response']
        global last_status, last_status_mobile        
        user_name = '%s %s' % (response_dict[0].get('first_name', 0), response_dict[0].get('last_name', 0))
        is_online = response_dict[0].get('online', 0)
        is_online_mobile = response_dict[0].get('online_mobile', 0) 
        print(last_status, is_online, last_status_mobile, is_online_mobile) 
        if last_status != is_online or last_status_mobile != is_online_mobile:
            print(status_message(is_online, is_online_mobile, user_name))
            last_status, last_status_mobile = is_online, is_online_mobile 
        time.sleep(10)


if __name__ == '__main__':
     for address in addresses:
         process = Process(target=check_status, args=(address,))
         process.start()
         #process.join()
     #check_status()
