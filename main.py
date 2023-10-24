import speech_recognition as sr
from config import apiKey
import os
import webbrowser
import openai
import datetime
import random

#research on web driver module
chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apiKey
    chatStr += f"Rahim: {query}\n Jarvis: "

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": query}],
        max_tokens=150,
    )

    # todo: Wrap this inside a try-except block
    say(response.choices[0].message['content'])
    chatStr += f"{response.choices[0].message['content']}\n"
    return response.choices[0].message['content']

def ai(prompt):
    openai.api_key = apiKey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)
def say(text):
    os.system(f"say {text}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing....")
            query = r.recognize_google(audio , language= "en-in")
            print(f"User said {query}")
            return query
        except Exception as e:
            return "Some Unknown Error Ocurred. Sorry from Cipher"


if __name__ == '__main__':
    print("Sypher")
    say("Cipher A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        #To open websites
        sites = [["youtube" , "https://youtube.com"] ,
                 ["facebook" , "https://facebook.com"] ,
                 ["tcb scans" , "https://tcbscans.com"],
                 ["instagram" , "https://instagram.com"],
                 ["google" , "https://google.com"],
                 ["classroom" , "https://classroom.google.com"],
                 ["gmail" , "https://gmail.com"]]

        #To open Applications
        application = [["VS Code" , "/Applications/Visual Studio Code.app"],    #check vs code not opening error
                       ["Xcode" , "/Applications/Xcode.app"],
                       ["Facetime" , "/System/Applications/FaceTime.app"],
                       ["Spotify" , "/Applications/Spotify.app"],
                       ["Opera" , "/Applications/Opera.app"]]

        #for websites
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Sir")
                webbrowser.open(site[1])
        #for application
        for app in application:
            if f"Open {app[0]}".lower() in query.lower():
                say(f"Opening {app[0]} Sir")
                os.system(f"open {app[1]}")
        #for music
        if "open music" in query:
            musicPath = "/Users/rahimabbas/Downloads/music.mp3"
            os.system(f"open {musicPath}")
        #for time
        elif "time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {min} minutes.")

        elif "Cipher Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
