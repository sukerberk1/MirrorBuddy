# from django.shortcuts import render
# from chatbot.Voice_Assistant.model import BuddyBrain


# # Create your views here.

# def chatbot(message):
    
#     message = message.lower()
#     if message=="Hej":
#         return "No dzien dobry"
#     if message=='':
#         return "Zostałem zaprojektowany z myślą o pomocy uczniom takim jak ty. Zadaj mi pytanie i sprawdź, jak się spiszę."
#     if message.find("led") != -1:
#         return "Ledy znajdujące się w pokoju SU niedługo zostaną zerwane, wraz z tym samorząd obalony. Przygotujcie się na rewolucje - Liberté, égalité, fraternité!!"
#     if message.find("samorząd") != -1:
#         return "Członków samorządu możesz poznać korzystając z funkcji 'Znajdź' na pasku nawigacyjnym. Sam nie wiem o nich za dużo, więc lepiej sam z nimi pogadaj."
    
#     response = message
#     return response

# def chatbot_view(request):
#     assistant = BuddyBrain()
#     botresponse = "Cześć! Jestem MirrorBuddy, twój elektroniczny towarzysz, przewodnik po szkole, jednosobowa armia! Czego potrzebujesz?"
    
    

#     if request.method=="POST":
#         #botresponse = chatbot(request.POST.get('message'))
#         message = assistant.listen()
#         res, tag = assistant.answer(message)
#         assistant.say(res)
    


#     return render(request, 'chatbot.html', {'botresponse':botresponse})
