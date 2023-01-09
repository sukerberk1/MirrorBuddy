import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

try:
    from text_speech_module.voice import Google_VoiceModule
except:
    from chatbot.Voice_Assistant.text_speech_module.voice import Google_VoiceModule

try:
    import get_data.get_data as g_data
except:
    import chatbot.Voice_Assistant.get_data.get_data as g_data


#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
        

class BuddyBrain():
    def __init__(self):
        print("Inicjalizacja modelu...")
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open('./chatbot/Voice_Assistant/data/wordsList.json').read())

        self.words = pickle.load(open('./chatbot/Voice_Assistant/model_a/words.pkl', 'rb'))
        self.classes = pickle.load(open('./chatbot/Voice_Assistant/model_a/classes.pkl','rb'))

        self.model = load_model('./chatbot/Voice_Assistant/model_a')

        

    #tokenizacja i lemantyzacja
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    #zwraca liste tokenów i zlemantyzwoanych słów
    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    #klasa, która używa gotowego modelu do predykcji
    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = .25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)

        return_list = []
        for r in results:
            return_list.append({'intent':self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    
    def get_response(self, message, intents_list, intents_json):
        list_of_intents = intents_json['Model_A']
    
        try:
            tag = intents_list[0]['intent']
            print(f"Wyjątek: {intents_list[0]['intent']}")
        except IndexError as e:
            print(e)
            print("I'm giving random asnwer.....")
            for i in list_of_intents:
                tag = random.choice(i['tag'])

        res = message
        
        for i in list_of_intents:
            if i['tag'] == tag:
                res = random.choice(i['responses'])
                break
        
        
        if res == 1:
            list_of_words = self.clean_up_sentence(message)
            count = 1
            for word in list_of_words:
                if len(word) > 4:
                    word = word[:-2]

                is_teacher = g_data.find_teacher(word)
                if is_teacher[0] != 0:
                    word = g_data.schedule_of_teacher(word)
                    
                    if str(word[1]) == "nan":
                        print("Ten nauczyciel nie ma teraz lekcji")
                        self.say("Ten nauczyciel nie ma teraz lekcji")
                        break
                    else:
                        n_of_class = g_data.clean_up_string_and_get_num_of_classroom(word[1])
                    print(f"Tego nauczyciela powinieneś znaleźć w {n_of_class}")
                    self.say(f"Tego nauczyciela powinieneś znaleźć w {n_of_class}")
                else:
                    symbol = "." * count
                    count += 1
                    print(f"Searching: {symbol}")
            return True, True 

        elif res == 2:
            print("Aktualnie nie posiadam takich informacji")
            self.say("Aktualnie nie posiadam takich informacji")
            return True, True 
            

        elif res == 3:
            self.say("Z której jesteś klasy?:")
            q = input("Z której jesteś klasy?:")
            

            try:
                nth_lesson, name_of_lesson = g_data.find_where_i_have_lesson(q)
            except:
                nth_lesson = 0
                
            if nth_lesson == 0 or str(name_of_lesson) == "nan":
               print("Wygląda na to, że nie masz teraz lekcji")
               self.say("Wygląda na to, że nie masz teraz lekcji")
            else:
                print(f"To jest {nth_lesson}. lekcja, jest to {name_of_lesson}")
                self.say(f"To jest {nth_lesson}. lekcja, jest to {name_of_lesson}")
            
            return True, True 

        return res, tag

    def answer(self, message):
        ints = self.predict_class(message)
        res, tag = self.get_response(message, ints,self.intents)
        return res, tag
    
    def listen(self):
        message = Google_VoiceModule.listen(self)
        return message

    def say(self,answer):
        self.google_voice = Google_VoiceModule()
        self.google_voice.say(answer) 

    def all_in_one(self):
        message = self.listen()
        answer, tag = self.answer(message)
        self.say(answer)
        return message, answer, tag




if __name__ == "__main__":

    model_a = BuddyBrain()

    while True:
        message = model_a.listen()
        res, tag = model_a.answer(message)
        model_a.say(res)
        
        print("\n")
        print(f"res = {res} tag = {tag}")
        
        

        
        