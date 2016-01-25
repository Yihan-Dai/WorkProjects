# This part is completed by Sihan Wu, Yihan Dai, and Yitong Wang together
import urllib2

import json

import os
 

def recording(stuff):      #define a function called recording
    print "Start recording"
    os.system(stuff)

 
def stt_google(filename):  #define a function called stt_google
    f = open(filename, 'rb') #open the flac in 'rb' mode
    flac_cont = f.read()     
    f.close()
    
    GOOGLE_SPEECH_URL_V2 = "https://www.google.com/speech-api/v2/recognize?output=json&lang=en&key=AIzaSyBkR9o3L1nGPsEcq2S3ifT9fb_U7RhdNm4"

    # Headers. A common Chromium (Linux) User-Agent
    hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",
    'Content-type': 'audio/x-flac; rate=16000'}         
 
    req = urllib2.Request(GOOGLE_SPEECH_URL_V2, data=flac_cont, headers=hrs)
    print "Sending request to Google TTS"
    p = urllib2.urlopen(req)
    response = p.read()
    response = response.split('\n', 1)[1]
    
    # Try to get something out of the complicated json response:
    res = json.loads(response)['result'][0]['alternative'][0]['transcript']
    print res     #print the result
    return res    



 
