
import datetime
import os
import re
import smtplib
import time
import urllib.request
import webbrowser
from urllib.parse import *

import pafy
import pyttsx3
import speech_recognition as sr
import wikipedia
from bs4 import BeautifulSoup
from pydub import AudioSegment
from pydub.playback import play
from concurrent import futures
from howdoi import howdoi
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice',voice[0].id)
master="kishoor"

#speak function will pronuce your text which is passed
def speak(text_audio):
    engine.say(text_audio)
    engine.runAndWait()


def wishme():
    hour = datetime.datetime.now().hour
    if hour >=0 and hour <12:
        speak(f"Good Morning , I am assistant of {master}, hi how are you")
    elif hour >=12 and hour <=18:
        speak(f"Good Afternoon , I am assistant of {master}, hi how are you")
    else:    
        speak(f"Good Evening , I am assistant of {master}, hi how are you")
    #speak("how may i help you")

def song_cmd():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")              
        audio = r.listen(source) 
    try:
        print("Recongnizing..")
        query = r.recognize_google(audio,language='ta-en')
        print(f'user said {query}\n')
    except Exception as e:        
        speak("oh oh , Not able to catch you")
        query="wasted"     
    return query.lower()


def takecommand():
    r=sr.Recognizer()
    speak("say your command now")
    with sr.Microphone() as source:
        print("Listening...")              
        audio = r.listen(source) 
    try:
        print("Recongnizing..")
        query = r.recognize_google(audio,language='en-in')
        print(f'user said {query}\n')
    except Exception as e:        
        speak("oh oh , Not able to catch you")
        query="wasted"     
    return query.lower()

def number_command():
    r=sr.Recognizer()
    speak("say the song number")
    with sr.Microphone() as source:
        print("Listening...")              
        audio = r.listen(source) 
    try:
        print("Recongnizing..")
        query = r.recognize_google(audio,language='en-in')
        print(f'user said {query}\n')
    except Exception as e:        
        speak("oh oh , Not able to catch you")
        query="wasted"     
    return query.lower()

class Youtube_mp3():
    def __init__(self):
        self.lst = []
        self.dict = {}
        self.dict_names = {}
        self.playlist = []

    def url_search(self, search_string, max_search):
        print('checking songs for you')
        textToSearch = search_string
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        i = 1
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if len(self.dict) < max_search:
                self.dict[i] = 'https://www.youtube.com' + vid['href']
                i += 1
            else:
                break


    def get_search_items(self, max_search):
        print(self.dict)

        if self.dict != {}:
            i = 1
            for url in self.dict.values():
                try:
                    info = pafy.new(url)
                    self.dict_names[i] = info.title
                    print("{0}. {1}".format(i, info.title))
                    i += 1

                except ValueError:
                    pass

    def play_media(self, num):
        url = self.dict[int(num)]
        info = pafy.new(url)
        audio = info.getbestaudio(preftype="m4a")
        try:
            os.remove('song.mp3')
        except :
            print("no file")
        audio.download('song.mp3')        
        audio = AudioSegment.from_file('song.mp3')
        play(audio)    
        print("Playing: {0}.".format(self.dict_names[int(num)]))

def main():
    
    query = takecommand()

    try:

        if 'wikipedia' in query:
            speak("Searching in wikipedia")
            query = query.replace("in wikipedia", "")
            results = wikipedia.summary(query, sentences =2)
            speak(results)
            return 0
        elif 'browser' in query:
            url = re.search("([a-zA-Z0-9]*\.[a-zA-Z]*)",query)
            url = url.group() #f"https://{url.group()}"
            chromepath="C:/Users/kbalaraman/AppData/Local/Google/Chrome/Application/chrome.exe %s"
            webbrowser.get(chromepath).open(url)
            return 0
        elif 'time' in  query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"{master} the time is {strTime}")
            return 0
        elif "open code" in query:
            codepath="C:/Users/kbalaraman/AppData/Local/Programs/Microsoft VS Code/code.exe"
            os.startfile(codepath)
            return 0
        elif "check"  in query:
                query = query.replace("check", "")
                parser = howdoi.get_parser()
                args = vars(parser.parse_args(query.split(' ')))
                output = howdoi.howdoi(args)
                print("i hope this helps you \n {} ".format(output))
                return 0 
        elif "song" in query:
            try:
                x = Youtube_mp3()
                speak("Please say the song name")
                query = song_cmd()
                search = query
                max_search = 5
                x.dict = {}
                x.dict_names = {}
                x.url_search(search, max_search)
                x.get_search_items(max_search)                
                song_num = number_command()
                song_num = re.search("\d", song_num)
                song_num=int(song_num.group())
                with futures.ThreadPoolExecutor(3) as executor:
                    executor.submit(x.play_media(song_num))        

            except :
                print("error")
                return 0
            return 0
        elif "Good" or "fine" in query:
            speak("Sounds good")
            return 0 
        elif "hold" or "wait" in query:
            if "minutes" or "min" in query:
                w = re.search("\d",query)
                waits=int(w.group())
                waits = waits*60
                time.sleep(waits)
            elif "secs" or "seconds" in query:
                w = re.search("\d",query)
                waits=int(w.group())
                time.sleep(waits)
            return 0
        elif "wasted" in query:
            return 1        
    except :
        speak("sorry")
    return 1    


if __name__=="__main__":
    print("Initializing")
    speak("Initializing ")
    wishme()
    count=0
    while True:
        count +=main()  
        if count > 2:
            speak("I think you are busy, bye bye")     
            break        
        time.sleep(3)
        continue
