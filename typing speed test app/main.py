from time import time
from tkinter import *
from tkinter import messagebox


class Game():
    def __init__(self):
        self.string = paragraph["text"]
        self.word_lenght = len(self.string.split())
        self.start_time = time()
        self.end_time = time()

    def start(self):
        root.withdraw()
        window.wm_deiconify()
        self.start_time = time()

    def submit(self):

        input_text = textInput.get("1.0","end-1c")
        # input_text = str(input('Enter the Sentence :'))
        self.end_time= time()

        # calculate  accuracy
        accuracy = len(set(input_text.split()) & set(self.string.split()))
        accuracy = accuracy/self.word_lenght

        # calculate time
        timetaken = self.end_time - self.start_time
        
        # calculate word per minut
        wpm = len(input_text)*60/(5*timetaken)

        messagebox.showinfo(
            title="result", message=f"WPM : {round(wpm)} \nAccuracy : {round(accuracy, 2)}% \nTimetaken : {round(timetaken, 2)}sec")

        # messagebox.showinfo(
        #     title="result", message=f"lenght : {input_lenght} \ntext : {input_text} wpm \nTimetaken : {round(timetaken, 2)}sec ")

########################## GUI #######

root = Tk()
root.title("Typing speed test")
root.geometry("500x400+250+100")
root.configure(bg="grey")

window = Tk()
window.title("Typing speed test")
window.geometry("800x500+250+100")
window.minsize(800, 500)
window.maxsize(900, 550)
window.configure(bg="grey")
window.withdraw()



########################## window #######


####### paragraph to type #######
paragraph = Label(window, text="Python is an amazing programming language. It can be applied to almost any programming task, allows for rapid development and debugging, and brings the support of what is arguably the most welcoming user community.",
                  font=("arial", 15, 'italic bold'), bg="grey", fg='yellow', wraplength=700, justify="center")
paragraph.place(x=50, y=50)
paragraph.pack(padx=10, pady=20)


####### text input #######
textInput = Text(window, height=10, width=80, font=("arial", 15), cursor="circle")
textInput.pack(padx=10, pady=20)


####### submit button #######
submit = Button(window, text="SUBMIT", width=50, height=20, font=("arial", 20, "bold"), bg='yellow', command=Game().submit)
submit.pack(padx=10, pady=20)

########################## root #######


####### heading text #######
heading = Label(root, text="TYPING SPEED TEST", font=(
    "arial", 25, 'italic bold'), bg="grey", fg='white')
heading.pack(padx=10, pady=20)

####### start button #######
start = Button( text="START", width=40, height=10, font=("arial", 30, "bold"), bg='yellow', command= Game().start)
start.pack(padx=10, pady=20)

window.mainloop()
