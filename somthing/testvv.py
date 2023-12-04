
from voicevox import Client
import asyncio
import re
from pydub import AudioSegment
from pydub.playback import play
strings = []
async def tts():
    async with Client() as client:
        audio_query = await client.create_audio_query(
            text = ''.join(str(e+' ') for e in strings), speaker=1
        )
        with open("voice.wav", "wb") as f:
            f.write(await audio_query.synthesis(speaker=4))

def textreader():
    
    with open(r'tmp_answer.txt','r', encoding = 'utf-8') as f:
        for line in f:
            line = re.sub("\\u3000"," ",line).rstrip("\n\r")
            strings.append(line)
            #print(strings)


def speak():
    textreader()
    asyncio.run(tts())
    play(AudioSegment.from_wav(r"C:\somthing\voice.wav"))

"""
if __name__ == "__main__":
    ## already in asyncio (in a Jupyter notebook, for example)
    # await main()
    ## otherwise
    textreader()
    asyncio.run(tts())

"""
speak()