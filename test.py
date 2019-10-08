from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import time, threading
from pynput.keyboard import Controller
import keyboard
from queue import Queue
from textblob import TextBlob


class DictatorSlave:
    index = 0
    text = "Call Incoming. Call Incoming\n"
    phrase_aud = Queue()
    temp_phrase = ""
    r = sr.Recognizer()
    keyboard_press = Controller()

    def analyze_phrase(self, phrase):
        self.temp_phrase = phrase
        blob = TextBlob(self.temp_phrase)
        blob.correct()
        time.sleep(2)
        with open(f"next_anal_{self.file_index}.txt", 'a') as file:
            if blob.noun_phrases:
                print("User talking about subject:")
                file.write("User talking about subject: ")
                for np in blob.noun_phrases:
                    print(np)
                    file.write(np)
            file.write("\n")
            if blob.sentiment.polarity > 0:
                print("Positive Intent")
                file.write("Positive Intent\n")
            elif blob.sentiment.polarity == 0:
                print("Neutral Intent")
                file.write("Neutral Intent\n")
            else:
                print("Negative Intent")
                file.write("Negative Intent\n")
            if blob.subjectivity > .5:
                print("Seems to be a personal opinion or a judgement.")
                file.write("Seems to be a personal opinion or a judgement.\n")
            else:
                print("Seems like a fact is represented.")
                file.write("Seems like a fact is represented.\n")
        file.close()

    def __init__(self, flag_call):
        self.flag_call = flag_call
        tts = gTTS(text=self.text, lang='en')
        tts.save('speak_dict.mp3')
        self.index = 0
        self.file_index = 0
        self.phrase_dict = {}

    def phrase_detection(self):
        while True:
            phrase = self.phrase_aud.get()
            if phrase is None:
                break
            else:
                try:
                    with open(f'next{self.file_index}.txt', 'a') as f_out:
                        self.temp_phrase = self.r.recognize_google(phrase)
                        self.phrase_dict[self.index] = str(self.temp_phrase)
                        f_out.write(self.temp_phrase + ",\n")
                        f_out.close()
                        self.index += 1
                        self.analyze_phrase(self.temp_phrase)
                except sr.UnknownValueError:
                    print("Speech cannot be understood.")
                except sr.RequestError as e:
                    print("Could not request result. Error Connection"+str(e))
                self.phrase_aud.task_done()

    def inspect_call(self):
        # print("step 1")
        modulo = threading.Thread(target=self.phrase_detection)
        # print("step 1")
        modulo.daemon = True
        # print("step 1")
        modulo.start()
        # print("step 1")
        mic = sr.Microphone(device_index=1)
        # file = open(f'next{self.index}.txt', 'w')
        with mic as source:
            self.r.adjust_for_ambient_noise(source, duration=.5)
            self.r.energy_threshold = 1000
            self.r.pause_threshold = 5
            while True:
                if keyboard.is_pressed('/'):
                    print("The call ended.")
                    self.file_index += 1
                    break
                else:
                    print("trying to hear")
                    try:
                        self.temp_phrase = self.r.listen(mic, phrase_time_limit=5, timeout=5)
                        self.phrase_aud.put(self.temp_phrase)
                    except sr.WaitTimeoutError:
                        continue

        self.phrase_aud.put(None)

        # self.phrase_aud.join()
        print("Out of loop")
        self.flag_call = 0

    def incoming_call(self):
        print(self.text+'\n')
        playsound("speak_dict.mp3")
        self.inspect_call()


