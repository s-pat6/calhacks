import os
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)
from groq import Groq
import pyaudio
import wave

def speak(txt="Hello and welcome to ForgetMeNot. I'm here to guide you through human emotions.", file='output.wav'):
    SPEAK_OPTIONS = {'text': txt}
    filename = file

    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key='d06a398656d51aa46a048e0e346314756189b101')

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-athena-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        chunk = 1024
        f = wave.open(r'./'+filename, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        data = f.readframes(chunk)
        while data:
            stream.write(data)
            data=f.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

def generate(content='Reaffirm the user', system='You are a voice assistant for an app called ForgetMeNot. You are assisting a user who forgot it was their anniversary with their significant other. Based on the emotions of the significant other, provide a course of action for the user to first identify how the other person is feeling, then make up for forgetting by presenting gifts.', tokens=30, assistant=''):
    client = Groq(
        api_key='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'
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': system,
            },
            {
                'role': 'user',
                'content': content,
            },
            {
                'role': 'assistant',
                'content': assistant
            }
        ],
        model='llama3-8b-8192',
        temperature=0.5,
        max_tokens=tokens,
    )

    return chat_completion.choices[0].message.content

def generate_and_speak(file='output.wav', content='Reaffirm the user', system='You are a voice assistant for an app called ForgetMeNot. You are assisting a user who forgot it was their anniversary with their significant other. Based on the emotions of the significant other, provide a course of action for the user to first identify how the other person is feeling, then make up for forgetting by presenting gifts.', tokens=30, assistant=''):
    print('context: ' + system)
    print('content: ' + content)
    text = generate(content, system, tokens, assistant)
    print('text: ' + text)
    speak(text, file)
    return text


def main():
    speak()
    generate()


if __name__ == "__main__":
    main()