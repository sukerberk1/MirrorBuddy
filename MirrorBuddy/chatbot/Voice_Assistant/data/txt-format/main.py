import json
from datetime import datetime, timedelta


with open('/home/pete/Coding/Python/Artificial_Inteligence/Intelligent Chatbot/txt-format/message_1.json',"r") as json_data:
    data = json.load(json_data)
    main_list = []
    for i in data["messages"]:
        
        #trzy linijki, które zwracają w ładnym formacie czas danej wiadomości

        time = i["timestamp_ms"]
        date = datetime.fromtimestamp(time/1000.0)
        time = str(date).replace(" ", ", ")
        
        name = i["sender_name"]
        try:
            content = i["content"]
        except KeyError:
            continue 

        l = [time,name,content]
        
        main_list.append(l)
        l = []

    json_data.close()

import sys

with open('words_databse.txt','w') as f:
    for i in main_list:
        print("")
        
        time = i[0].encode("latin1").decode('utf-8')
        name = i[1].encode("latin1").decode('utf-8')
        content = i[2].encode("latin1").decode('utf-8')

        f.write(f"[{time}] {name}: {content}\n")
        

        

  
    



