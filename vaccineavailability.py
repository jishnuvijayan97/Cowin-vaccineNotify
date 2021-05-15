import requests
import time
from datetime import date
browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
chat_id = "replace with chat id of telegram group"
pincode1 = "replace with pincode"
pincode2 = "replace with pincode"


token = "replace with telegram bot token"

def getUrl(pincode, date):
    return "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+ pincode + "&date=" + date
def postUrl():
    return "https://api.telegram.org/bot"+token+"/sendMessage"

def getMessageBody(details):
    return {'chat_id': chat_id, 'text': getMessageText(details), 'parse_mode': 'HTML'}

def getMessageText(details):
    return ('<b>Name : </b><b>'+details["name"]+'</b>'+'\n'
           'Avail. Capacity :' +details["avail_capacity"] + '\n'
           'Min. Age : ' + details['min_age'] +'\n'
           'Date : ' + details['date'])

def checkAvailabilityAndSendMessage(available_centers):
    for center in available_centers:
        name = center["name"]
        sessions = center["sessions"]
        for session in sessions:
            if session["available_capacity"] > 0:
                sendMessage( {'name': name,'date': session["date"],'avail_capacity': str(session["available_capacity"]),'min_age': str(session["min_age_limit"]) })

def checkCenters(pincode, date):
    url = getUrl(pincode, date)
    response = requests.get(url ,headers=browser_header)
    if response.ok:
        available_centers = response.json()["centers"]
        if len(available_centers)> 0:
            checkAvailabilityAndSendMessage(available_centers)

def sendMessage( details ):
    requests.post( postUrl(), data= getMessageBody(details))



while 1:
    today = date.today().strftime("%d-%m-%Y")
    print(today)
    checkCenters(pincode1,today)
    checkCenters(pincode2,today)
    time.sleep(10)




