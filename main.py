from Load_model import load_model as model
from Functions import get_temp, speech
import datetime, time
latestCall = time.time()
res = ""
def res_temp():
    global latestCall
    latestCall = time.time()
    return get_temp.res()

if True:
    while(True):
        if (res != "") and (time.time() - latestCall > 120*60):
            res = res_temp()
            print("call res")
        elif res == "":
            res = res_temp()
            print("call res")
            
        textfrom = input("Enter text: ")
        #textfrom = speech.speechtotext()
        start = datetime.datetime.now()
        tag, responses = model.response(textfrom,True)
        finish = datetime.datetime.now()
        print ("เวลาประมวลผลคำตอบ: ",finish-start)

        if textfrom == "":
            print ("อะไรนะ ผมฟังไม่ทัน")
            speech.texttospeech("อะไรนะ ผมฟังไม่ทัน")
        elif tag[0] == "psycho question" or tag[0] =="ภาพยนตร์" or tag[0] =="emotion ความรู้สึก":
            print(responses)
            speech.texttospeech(responses)
        else:
            
            if responses in res:
                print (res[responses])
                speech.texttospeech(res[responses])
            else:
                if responses == None:
                    print("ผมไม่เข้าใจที่คุณพูด")
                    speech.texttospeech("ผมไม่เข้าใจที่คุณพูด")
                else:
                    print (responses)
                    speech.texttospeech(responses)
            break
