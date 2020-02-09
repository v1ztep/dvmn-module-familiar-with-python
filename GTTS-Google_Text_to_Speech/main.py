from gtts import gTTS

text = input('Введи текст на русском и нажми enter: ')
tts = gTTS(text, lang='ru')
tts.save('text.mp3')
