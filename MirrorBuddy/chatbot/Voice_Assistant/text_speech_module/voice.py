



from google.oauth2 import service_account
from google.cloud import texttospeech
import os
import speech_recognition as sr




class Google_VoiceModule():
    def __init__(self):
        
        # Instantiates a client
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './chatbot/Voice_Assistant/text_speech_module/key.json'
        print("Inicjalizacja klienta mowy...")
        self.client = texttospeech.TextToSpeechClient()

        
      
    def say(self, message):

        #Voice gender
        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="pl-PL", ssml_gender=texttospeech.SsmlVoiceGender.MALE	
        )

        # Set the text input to be synthesized
        try:
            
            # The response's audio_content is binary.
            synthesis_input = texttospeech.SynthesisInput(text=message)


            # Select the type of audio file you want returned
            audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3)

             # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        except TypeError:
            print("Type Error")
        

       
       


        with open("output.mp3", "wb") as out:
            try:
                # Write the response to the output file.
                out.write(response.audio_content)
                print('Audio content written to file "output.mp3"')
            except UnboundLocalError as e:
                # I don't know why, but sometimes it tries get response again
                print(e)
                print("Error: response nie zostało zdefiniowane")
                return True

        os.system("mpg123 " + "output.mp3")
        os.system("rm output.mp3")
        return True
    
    def listen(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2, language='pl-PL')
                MyText = MyText.lower()
                print("Did you say " + MyText)
            return MyText
        except:
            return "Wystąpił błąd"

        
        


