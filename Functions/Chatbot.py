from groq import Groq
from json import load , dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values('D:\jarvis\Jarvis\.env')

Username = env_vars.get('Username')
Assistantname = env_vars.get('Assistant')
GroqAPI = env_vars.get('GroqAPI')

client = Groq(api_key= GroqAPI)

messages =[]

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatbot = [
    {'role' : 'system' ,'content':System}
]

try:
    with open(r"D:\jarvis\Jarvis\Data\Chatlog.json","r") as f:
        messages=load(f)
except FileNotFoundError:
    with open(r"D:\jarvis\Jarvis\Data\Chatlog.json","w") as f:
        dump([],f)

def RealtimeInfo():
    current_date_time =  datetime.datetime.now()
    date = current_date_time.strftime("%A")
    day = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this information if needed,\n"
    data+=f"Day :{day} \nDate :{date}\nMonth :{month}\nYear :{year}"
    data+=f"Hours:{hour}\nMinute:{minute}\nSecond:{second}"

    return data


def AnswerModifier(Answer):
    lines=Answer.split('\n')
    non_empty_lines =[line for line in lines if line.strip()]
    moodified_answer = '\n'.join(non_empty_lines)
    return moodified_answer

def Chatbot(query):
    try:
        with open(r"D:\jarvis\Jarvis\Data\Chatlog.json",'r') as f:
            messages=load(f)

        messages.append({"role":"user","content":f"{query}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages = SystemChatbot+[{"role":"system","content":RealtimeInfo()}]+messages,
            max_tokens=1024,
            temperature=0.7,
            top_p= 1,
            stream = True,
            stop=None
        )

        Answer=""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer+=chunk.choices[0].delta.content

        Answer = Answer.replace("</s>","")

        messages . append({"role":"assistant","content":Answer})

        with open(r"D:\jarvis\Jarvis\Data\Chatlog.json","w") as f:
            dump(messages,f,indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"Error :{e}")
        with open(r"D:\jarvis\Jarvis\Data\Chatlog.json","w") as f:
            dump([],f,indent=4)

        return Chatbot(query)

if __name__ =="__main__":
    while True :
        user_input = input("Enter the Question: ")
        print(Chatbot(user_input))


