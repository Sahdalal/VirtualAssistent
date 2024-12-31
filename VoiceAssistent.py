import speech_recognition as sr
import pyttsx3
import openai
from config import API_KEY


openai.api_key = API_KEY

class VoiceAssistent:
    def __init__(self):
        #Initialize text to speech
        self.engine = pyttsx3.init()

        #Speech Recognizer
        self.recognizer = sr.Recognizer()

        #Configure voice settings
        self.engine.setProperty('rate', 225)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

    def speak(self, text):
        #Make assistent read given text
        print(f'Assistent: {text}')
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        #Listen to user input
        with sr.Microphone() as source:
            print("\nListening...")

            #Adjust Microphone
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            #Listen for user voice
            audio = self.recognizer.listen(source)

        try:
            #Try to recognize speech
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            #If speech is unclear
            self.speak("Sorry, I did not catch that, Please Repeat")
            return None
        except sr.RequestError:
            #If there is an issue with speech recognizition
            self.speak("Sorry, there seems to be an issue with the speech recognition")
            return None
        
    def get_ai_response(self, user_input):
        #Get Reply from OpenAI
        try:
            #Send User input to openAI and get reply
            reponse = openai.chat.completions.create(
                model= "gpt-4o",
                messages=[
                    {"role": 'system', 'content': "You are a helpful virtual asssitent. Keep responses clear and concise."},
                    {"role": "user", "content": user_input}
                ]
            )
            return reponse.choices[0].message.content
        except Exception as e:
            return f'Sorry, I ran into an error: {str(e)}'
        
    def run(self):
        #Main program loop
        #Welcome message
        self.speak("Hello, I am your virtual assistant. How can I help you today")

        #keep running until user says exit
        while True:
            user_input = self.listen()

            if user_input:
            #Check if user wants to exit
                if 'exit' in user_input.lower():
                    self.speak("Goodbye, Have a good day")
                    break

            #Get and speak AI Reply
            response = self.get_ai_response(user_input)
            self.speak(response)


#This is where program starts
if __name__ == '__main__':
    assistant = VoiceAssistent()
    assistant.run()


