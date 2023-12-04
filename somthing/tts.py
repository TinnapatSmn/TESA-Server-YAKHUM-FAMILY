from voicevox import Client
import asyncio
from pydub import AudioSegment
from pydub.playback import play
import re

strings = []

async def main():
            
        async with Client() as client:
            audio_query = await client.create_audio_query(text = ''.join(str(e+' ') for e in strings), speaker=1)
        with open(r"voice.wav", "wb") as f:
            f.write(await audio_query.synthesis(speaker=4))
        
def textreader():
    with open(r'tmp_answer.txt','r', encoding = 'utf-8') as f:
        for line in f:
            line = re.sub("\\u3000"," ",line).rstrip("\n\r")
            strings.append(line)
            #print(strings)

def speak():
    textreader()
    asyncio.run(main())
    play(AudioSegment.from_wav(r"voice.wav"))
    
speak()
        
        
    

    
    