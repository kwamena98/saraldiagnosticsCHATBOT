from flask import Flask,request, render_template,request
import json
import random
import random
import numpy as np
import json 
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model




lemmatizer=WordNetLemmatizer()

intents= json.loads(open("dataset.json").read())

words=pickle.load(open('words.pkl','rb'))
classes=pickle.load(open('classes.pkl','rb'))

model=load_model('chat_bot.model')


def clean_up_sentence(sentence):
   
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[lemmatizer.lemmatize(word) for word in sentence_words]
    print(sentence_words)
    return sentence_words

def bag_of_words(sentence):
    sentence_words=clean_up_sentence(sentence)
    bag=[0]*len(words)

    for w in sentence_words:
        for i, word in enumerate(words):
            if word==w:
                bag[i]=1

    return np.array(bag)


def predict_class(sentence):
    bow=bag_of_words(sentence)
    res=model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD=0.25

    results=[[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    return_list=[]

    for r in results:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})

    return return_list

def get_response(intents_list,intents_json):
    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag']  == tag:
                result = random.choice(i['responses'])
                return result
                break
    except:
        result = "I don't understand!"
        return result


app=Flask(__name__)
@app.route("/")
@app.route("/messaging",methods=['GET','POST'])
def message():
    data="Hi there, I\'m SARLA DIAGNOSTICS, what\'s on your mind today?"

    if request.method == 'POST':
        message = request.json["message"]
        print(message)


        if "Delhi" in message:
            res="""
            Weekdays: 08:00 AM - 07:00 PM
            Sundays: 08:00 AM - 01:00 PM
            LAB (every sunday's): 08:00 AM - 011:00 AM
            CT & MRI: 24*7( Round The Clock)
            """
        
        elif "Noida" in message:
            res="""
            Weekdays: 07:00 AM - 08:00 PM
            Sundays: 08:00 AM - 01:00 PM
            Lab (Every sunday's): 08:00 AM - 01:00 PM
            CT & MRI: 24*7( Round The Clock)
            """

        else:
            ints=predict_class(message)
            res=get_response(ints,intents)



        return {"message": res}

    return render_template("message.html",Koto=data)


if __name__=='__main__':
    app.run(debug=True)

    

 

