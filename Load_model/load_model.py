import json, tflearn, random, deepcut, time, tensorflow as tf, numpy as np, datetime

with open('Data/training_data.json',encoding='utf8') as json_data:
    data = json.load(json_data)
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']
with open('Data/corpus.json', encoding='utf8') as json_data:
    intents = json.load(json_data)

tf.reset_default_graph()
graph = tf.get_default_graph()
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='../Data/tflearn_logs')
model.load('../Alan/Data/./model.tflearn')

list_words = []
kumyabs = ['แพศยา','กู','มึง','กระจู๋', 'กระดอ', 'กระทวย', 'กระสัน', 'กระสัน', 'กระหรี่', 'กระเจี้ยว', 'กระเจี๊ยว', 'กระเด้า', 'กะดอ', 'กะสัน', 'กะหรี่', 'กะเจี๊ยว', 'กะเจี๊ยว', 'กะโปก', 'กาจู๋', 'กาดอ', 'กาหรี่', 'กาเจี้ยว', 'ควย', 'จัญไร', 'จู๋', 'ชักว่าว', 'ชั่วช้า', 'ชาติชั่ว', 'ชาติหมา', 'ชิงหมาเกิด', 'ชิบหาย', 'ดอกทอง', 'ตูด', 'ตอแหล', 'ตีน', 'ถุย', 'ถ่อย', 'ทุเรศ', 'บัดซบ', 'มึง', 'พ่อตาย', 'พ่อง', 'ฟักยู', 'ร่าน', 'ลาวสัตว์', 'ลูกอีกะหรี่', 'ลูกอีดอกทอง', 'ลูกอีสัตว์', 'สถุน', 'สถุล', 'สันดาน', 'สาระเลว', 'อีควาย', 'หน้าควาย', 'หน้าควาย', 'หน้าตัวเมีย', 'หี', 'หำ', 'หน้าหมา', 'หมอย', 'แดก', 'หอกหัก', 'หัวดอ', 'เหี้ย', 'เชี่ย', 'ชาติหมา', 'ไอ้', 'อีตัว', 'อีตุ๊ด', 'อีบ้า', 'อีวอก', 'อีสัตว์', 'อีหอย', 'อีหอยดอง', 'อีห่า', 'ห่า', 'อีห่าราก', 'อีอับปรี', 'อีเปรต', 'อีเลว', 'อีเวร', 'อีเห็ดสด', 'แตด', 'อีไพร่', 'เสือก', 'แม่ง', 'เงี่ยน', 'เลวมาก', 'เลวสัด', 'เลว', 'เวรตะไล', 'เฮงซวย', 'โครตพ่อ', 'โครตแม่', 'ไปตายซะ', 'ไปตายห่า', 'นายชาติชั่ว', 'นายชาติหมา', 'นายชิงหมาเกิด', 'ปากหมา', 'นายชิบหาย', 'นายดอก', 'นายทุเรศ', 'นายนรก', 'นายบัดซบ', 'นายปากหมา', 'นายลาว', 'นายลูกกระหรี่', 'นายสันดาน', 'หน้าหี', 'หน้าด้าน', 'นายหน้าโง่']   
def replace_wordAtoB(text,target, word):
    text = text.replace(target,word)
    return text
def replace_word(text):
    text = text.replace("สาขาวิทยาการคอมพิวเตอร์","วิทย์คอม")
    text = text.replace("วิทยาการคอมพิวเตอร์","วิทย์คอม")
    text = text.replace("สาขาวิทยาการคอม","วิทย์คอม")
    text = text.replace("วิทยาการคอม","วิทย์คอม")
    text = text.replace("สาขานี้","วิทย์คอม")
    text = text.replace("สาขาวิทย์คอม","วิทย์คอม")
    return text

def kumyab(text):
    for kumyab in kumyabs:
        if kumyab in text:
            return True
    return False

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

def bow(sentence, words, show_details=False):
    sentence_words = remove_stopwords(word_tokenize(sentence))
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))

def classify(sentence,ERROR_THRESHOLD = 0.25):
    results = model.predict([bow(sentence, words)])[0]

    results = [[i,r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def response(sentence,show_tag=False, show_details=False):
    if kumyab(sentence):
        sentence = "คำหยาบ"
    replace_wordAtoB(sentence,"เธอ","คุณ")
    results = classify(replace_word(sentence))
    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    if show_tag:
                        return results[0],random.choice(i['responses'])
                    else:
                        return random.choice(i['responses'])
            results.pop(0)