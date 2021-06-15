import requests
#import pygame , sys, time
from pygame import mixer
#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
from datetime import datetime,timedelta
import time
import json
import webbrowser
from win10toast_click import ToastNotifier

age = 21
pincodes = ["700054","462003"]
print_flag = 'Y'
num_days = 2

print("Starting search for Covid vaccine slots!")

actual = datetime.today()
list_format = [actual+ timedelta(days=i) for i in range(0,num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
print(actual_dates)

while (True):
    counter = 0   

    for pincode in pincodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
            
            result = requests.get(URL, headers=header)

            if (result.ok):
                response_json = result.json()
                flag=False
                
                if response_json["centers"]:
                   if(print_flag.lower() =='y'):
                       
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 and session["date"] == given_date) :
                                        print("Vaccine type:", session["vaccine"])
                                        print('Pincode: ' + pincode)
                                        print("Available on: {}".format(given_date))
                                        print("\t", center["name"])
                                        print("\t", center["block_name"])
                                        print("\t Price: ", center["fee_type"])
                                        print("\t Availablity : ", session["available_capacity"])

                                        if(session["vaccine"] != ''):
                                           print("\t Vaccine type: ", session["vaccine"])
                                        print("\n")
                                        counter = counter + 1
                                else:
                                        pass
                else:
                    pass
            else:
                 print("No Response!")
                
    if  (counter == 0):
        
        toaster = ToastNotifier()
        toaster.show_toast("NO SLOT TILL NOW", # title
                           "Checking after few minutes", # message 
                           icon_path=r"C:\Users\HP\Desktop\vaccine.ico", # 'icon_path' 
                           duration=None, # for how many seconds toast should be visible
                           threaded=True,)# True = run other code in parallel
        
        time.sleep(60)
        
    else:
        mixer.init()
        mixer.music.load('sound_dingdong.wav')
        mixer.music.play()
        print("Search Completed!")

        def open_url():
             webbrowser.open('https://cowin.gov.in',new=2)

        toaster = ToastNotifier()
        toaster.show_toast("VACANT SLOTS AVAILABLE", # title
                           "Click to book your slot from Cowin! >>", # message 
                           icon_path=r"C:\Users\HP\Desktop\vaccine.ico", # 'icon_path' 
                           duration=None, # for how many seconds toast should be visible
                           threaded=True, # True = run other code in parallel 
                           callback_on_click=open_url)
        
        time.sleep(60*30)
       
        
        
        
   
        
