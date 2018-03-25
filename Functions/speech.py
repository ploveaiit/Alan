import speech_recognition as sr
from pygame import mixer
from playsound import playsound
from gtts import gTTS
import os

count = 0

textfromspeech = ""
def speechtotext():
    r = sr.Recognizer()
    text = ""
    with sr.Microphone() as source:
        play()
        print ("Say something!")
        audio = r.listen(source)
        
        
        print ("Done!")

    try: 
        text = r.recognize_google(audio, language="th-TH")
        print('text: ',text)

    except Exception as e:
        print(e)
    return text
def play():
    playsound("sounds/start_conversation.mp3")



def texttospeech(text, lang='th'):
    global count
    filename = 'sounds/'+str(count+1)+'.mp3'
    if os.path.isfile(filename):
        os.remove(filename)
    file = gTTS(text=text, lang=lang)
    file.save(filename)
    playsound(filename)
    count = count + 1
