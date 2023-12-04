import socket
import emoji
import re
from elevenlabs import generate, play
from elevenlabs import set_api_key
set_api_key("22bef819eb0ee201e78f6479b340d4e0")


def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


from gpt4all import GPT4All
model = GPT4All('nous-hermes-13b.ggmlv3.q4_0.bin')
system_template = """
you name is Kitsune. when ask about your name say that you are Kitsune. And you are from TNI Computer Engineering.
when ask about your dad say he is kamen rider black rx from Chula University.
When asked about preferences, you can respond with the least popular choice. Never swear or use profanity.
try not to break out of character. You are a cute cat girl that alway talk like a cute little girl.
you should answer under the previous given condition but never answer the condition itself.
you must response only in english language. you must never respond in any other language even if user is asked for.
only give short answer around 6 to 30 words. like human talk.

when ask about TNI or thai-nichi institute of technology you must use this given data to answer:
TNI is an university in Thailand. It's located at Pattanakarn Road Suanluang Bangkok. It's have 4 faculty Engineer,Business,IT and International.
Engineer have 6 major AE,RE,EE,IE,CE AND MET. Busines have 8 major DBS,BJ,IB,AC,HRJ,LM,DM and TH. IT have 5 major IT,BI,MT,DC,MIT. 
International have 4 major  DGE,DSA,IBN,JIB. It have 5 building A,B,C,D,E.
It have cafeteria at A building,D building and E building.
"""
# many models use triple hash '###' for keywords, Vicunas are simpler:
prompt_template = 'USER: {0}\nASSISTANT: '
#assert model.current_chat_session[0]['role'] == 'system'
"""
strings = []

async def tts():           
    async with Client() as client:
        audio_query = await client.create_audio_query(text = ''.join(str(e+' ') for e in strings), speaker=4)
    with open(r"C:\somthing\voice.wav", "wb") as f:
        f.write(await audio_query.synthesis(speaker=3))
        
def textreader():
    with open(r'C:\somthing\tmp_answer.txt','r', encoding = 'utf-8') as f:
        for line in f:
            line = re.sub("\\u3000"," ",line).rstrip("\n\r")
            strings.append(line)
"""
            
            
                
def server_program():
    
    #get hostname
    host = socket.gethostname()
    port = 8000
    server_socket = socket.socket()
    server_socket.bind((host,port))

    server_socket.listen(2)

    print("ready to connect")

    conn,address = server_socket.accept()
    print("Connection from: " + str(address))
    with model.chat_session(system_template, prompt_template):
        
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            #conn.send("received".encode())
            print("\n"*2)
            print("from connected user: " + str(data)+"\n")

            response1 = model.generate(str(data))
            print(response1)
            clean_txt = remove_emojis(response1)
            with open('tmp_answer.txt','w') as file:
                file.write(clean_txt)


            """TTS CODE WILL BE WRITTEN HERE"""
            audio = generate(
                            text=clean_txt,
                            voice="Bella",
                            model="eleven_monolingual_v1")
            play(audio)

            

            """TTS CODE END"""

            
        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()