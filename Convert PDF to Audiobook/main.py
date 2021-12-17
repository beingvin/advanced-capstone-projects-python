
#file = open ("sample.pdf", 'rb')
#read = file.read()
#print(read)

import pyttsx3
import PyPDF2


file = open ("sample.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(file)
pages = pdfReader.numPages

speaker = pyttsx3.init()
for num in range(7, pages):
    page = pdfReader.getPage(num)
    text = page.extractText()
    speaker.say(text)
    speaker.runAndWait()