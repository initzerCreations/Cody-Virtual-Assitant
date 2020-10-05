import cv2
import pyttsx3
import speech_recognition as sr
import time
import winsound
import os
import wikipedia
from _thread import start_new_thread
from googletrans import Translator
import sys
import urllib.request
import urllib.parse
import re
import webbrowser

engine = pyttsx3.init()
translator = Translator()
r = sr.Recognizer()
adjustedSound = False

def process_command(t):
	try:
		text = t
		if 'parar' in text:
			engine.stop()
		if 'ver' in text:
			concepto = text.split(' ',1)[1]
			query_string = urllib.parse.urlencode({"search_query" : concepto})
			html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
			search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
			url = "http://www.youtube.com/watch?v=" + search_results[0]
			webbrowser.open(url)
			#listen_commands()
		if text == 'quién eres' or 'identifícate' in text or 'nombre' in text or 'cómo te llamas' in text:
			engine.say('Soy Null, mi creador es Samuel Huesca y me dedico a proporcionar servicios de asistencia. Prueba a pedirme algo')
			engine.runAndWait()
			
		if 'música clásica' in text:
			engine.say('Activando musica')
			engine.runAndWait()
			os.system("nocturne.wav")
			listen_commands()
			return
			
		if 'vigilar' in text or 'vigilancia' in text:
			engine.say('Vigilare la actividad en la sala')
			engine.runAndWait()
			# Load the cascade
			face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

			# To capture video from webcam. 
			cap = cv2.VideoCapture(1)
			while True:
				# Read the frame
				_, img = cap.read()

				# Convert to grayscale
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

				# Detect the faces
				faces = face_cascade.detectMultiScale(gray, 1.1, 4)

				# Draw the rectangle around each face
				for (x, y, w, h) in faces:
					cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
					print('face detected')

				# Display
				cv2.imshow('img', img)

				# Stop if escape key is pressed
				k = cv2.waitKey(30) & 0xff
				if k==27:
					break
			# Release the VideoCapture object
			cap.release()
			
			listen_commands()
			return
			
		if 'explica' in text or 'explícame' in text:
			concepto = text.split(' ',1)[1]
			concepto_traducido = translator.translate(str(concepto), dest='en').text
			print(concepto_traducido)
			concepto_encontrado = wikipedia.search(concepto_traducido, results=5, suggestion=False)
			respuesta = wikipedia.summary(concepto_encontrado[0] , sentences = 5 , chars = 0 , auto_suggest = True , redirect = True)
			traducida = translator.translate(respuesta, dest='es')
			print(traducida.text)
			engine.say(traducida.text)
			engine.runAndWait()
			listen_commands()
		
		if 'calcula' in text:
			text = text.replace('mas', '+')
			text = text.replace('más', '+')
			text = text.replace('menos', '-')
			text = text.replace('por', '*')
			text = text.replace('x', '*')
			text = text.replace('dividido entre', '/')
			resultado = eval(text.split(' ',1)[1])
			print(resultado)
			engine.say("El resultado es "+str(resultado))
			engine.runAndWait()
		
		if 'buenas noches' in text:
			engine.say("Hasta pronto amigo")
			engine.runAndWait()
			sys.exit()
		listen_commands()
		
		
		
	except:
		listen_commands()
		
def listen_commands():
	with sr.Microphone(1) as source:
		print('Escuchando...')
		if not adjustedSound:
			r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		print('listened')
		try:
			text = r.recognize_google(audio, language='es-ES')
			print('Comando recibido: {}'.format(text))
			#engine.say('Te he escuchado correctamente')
			#engine.runAndWait()
			process_command(text)
		except:
			print('Lo siento no pude reconocer su voz, espere y vuelva a intentarlo')
			#engine.say('Lo siento no pude entenderle')
			#engine.runAndWait()
			time.sleep(2)
			listen_commands()
			
listen_commands()

#r = sr.Recognizer()
#*with sr.Microphone(1) as source:
#	audio = r.listen(source)
#	try:
#		text = r.recognize_google(audio)
#		print('Comando recibido: {}'.format(text))
#		engine.say('Te he escuchado correctamente')
#		engine.runAndWait()
#	except:
#		print('Lo siento no pude reconocer su voz')
#		engine.say('Lo siento no pude entenderle')
#		engine.runAndWait()
#
#time.sleep(3)
