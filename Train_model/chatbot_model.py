# coding: utf-8
import random
import numpy as np
import tensorflow as tf
import tflearn
import deepcut
import json, datetime

start = datetime.datetime.now()

with open('../Data/corpus.json', encoding='utf8') as json_data:
    intents = json.load(json_data)

list_words = [] 
def remove_stopwords(list_words):
    stopwords = ["ไว้","เปล่า","ไป""ได้","ให้","ใน","โดย","แห่ง","แล้ว","และ","แรก","แบบ","แต่","เอง","เห็น","เลย","เริ่ม","เรา","เมื่อ","เพื่อ","เพราะ","เป็นการ","เป็น","เปิดเผย","เปิด","เนื่องจาก","เดียวกัน","เดียว","เช่น","เฉพาะ","เคย","เข้า","เขา","อีก","อาจ","อะไร","ออก","อย่าง","อยู่","อยาก","หาก","หลาย","หลังจาก","หลัง","หรือ","หนึ่ง","ส่วน","ส่ง","สุด","สําหรับ","ว่า","วัน","ลง","ร่วม","ราย","รับ","ระหว่าง","รวม","ยัง","มี","มาก","มา","พร้อม","พบ","ผ่าน","ผล","บาง","น่า","นี้","นํา","นั้น","นัก","นอกจาก","ทุก","ที่สุด","ที่","ทําให้","ทํา","ทาง","ทั้งนี้","ทั้ง","ถ้า","ถูก","ถึง","ต้อง","ต่างๆ","ต่าง","ต่อ","ตาม","ตั้งแต่","ตั้ง","ด้าน","ด้วย","ดัง","ซึ่ง","ช่วง","จึง","จาก","จัด","จะ","คือ","ความ","ครั้ง","คง","ขึ้น","ของ","ขอ","ขณะ","ก่อน","ก็","การ","กับ","กัน","กว่า","กล่าว"]
    cleaned_words = []
    for stopword in stopwords:
        if stopword in list_words:
            list_words.remove(stopword)
    return list_words
def word_tokenize(list_words):
    list_words = deepcut.tokenize(list_words)
    return list_words

words = []
classes = []
documents = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = remove_stopwords(word_tokenize(pattern))
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))




training = []
output = []
output_empty = [0]*len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])


tf.reset_default_graph()
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='../Data/tflearn_logs')
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('../Data/model.tflearn')

with open("../Data/training_data.json","w")as file:
    json.dump({'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, file)
#json.dumps({'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open("training_data.json","wb"))
end = datetime.datetime.now()
print("End time: %s" %(end))
print("Total time: %s" %(end-start))

