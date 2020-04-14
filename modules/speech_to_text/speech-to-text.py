import speech_recognition as sr
import threading
import sys
from datetime import datetime

NOW=datetime.now()
DATE_TIME=NOW.strftime("%d-%m-%Y-%H-%M-%S")
SAVE_PATH='../saved_data/saved_transcripts/'

if len(sys.argv)>1:
	TOPIC_NAME=sys.argv[1]
else:
	TOPIC_NAME=""


r = sr.Recognizer()


def disp(text):
	#print(text + '.')
	print ('press enter to continue speaking or q and then enter to quit')
	return

with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source, duration=3)
	transcript = open(SAVE_PATH+TOPIC_NAME+'_'+DATE_TIME+'_transcript.txt', 'w')
	#transcript = open('transcript.txt', 'w')
	print('Start speaking')
	while(True):
		audio = r.listen(source)

		try:
			text = r.recognize_google(audio)
			print(text)
			transcript.writelines(text + '.')

		except:
			print('Inaudible. Try again.')

		timer = threading.Timer(2.0, disp, args = (text, ))
		timer.start()

		q = input()

		try:

			if q == 'q' or q == 'Q':
				print('Ending transcript')
				timer.cancel()
				break

		except NoneType:
			continue


transcript.close()
