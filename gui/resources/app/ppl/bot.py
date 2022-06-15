# from googlesearch import search
import random
from modules import *
from tkinter import *
import tkinter.messagebox
import tkinter as tk
from tkinter import *
from tkinter import filedialog  # from googlesearch import search
from tkinter import filedialog
import wolframalpha
import shutil
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image


# print(1)
# print(1)
# print(1)
# print(os.path.join(os.getcwd(), "resources/app/ppl/drivers/chromedriver.exe"))
# sys.exit(0)

# print(1)
# print(1)
# print(1)
# print(os.getcwd())
# sys.exit(0)


def image_conversion():
    root = tk.Tk()

    def my_function():
        current_id = variable.get()
        output_format = str(current_id)
        inside = root.filename
        for i in range(len(inside)):
            if inside[i] == '/':
                index = i
            if inside[i] == '.':
                index2 = i
        output = inside[:index]
        outside = inside[:index2]
        outside += output_format
        inside = r"{}".format(inside)
        outside = r"{}".format(outside)
        img = Image.open(inside)
        new_i = img.convert('RGB')
        new_i.save(outside)
        root.destroy()
        os.startfile(output)

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    root.filename = filedialog.askopenfilename(
        initialdir=desktop, title="Select A File")
    print(root.filename)
    my_label = tk.Label(root, text="Select output image format")
    my_label.config(width=25, font=('Helvetica,12'))
    my_label.grid(row=0, column=0)

    OptionList = [".jpg", ".png", ".tiff", ".bmp", ".eps"]
    variable = tk.StringVar(root)
    variable.set(OptionList[0])
    opt = tk.OptionMenu(root, variable, *OptionList)
    opt.config(width=50, font=('Helvetica', 12))
    opt.grid(row=2, column=0)

    my_button = tk.Button(root, text="Submit", command=my_function)
    my_button.config(width=10, font=('Helvetica,12'))
    my_button.grid(row=4, column=0)

    root.mainloop()


class ttt(object):
    def __init__(self, tk):
        self.tk = tk
        self.tk.title("Tic-Tac-Toe")

        self.playera = StringVar()
        self.playerb = StringVar()
        self.p1 = StringVar(value="Player 1")
        self.p2 = StringVar(value="Player 2")

        self.player1_name = Entry(self.tk, textvariable=self.p1, bd=2)
        self.player1_name.grid(row=1, column=1, columnspan=8)
        self.player2_name = Entry(self.tk, textvariable=self.p2, bd=2)
        self.player2_name.grid(row=2, column=1, columnspan=8)

        self.cross = PhotoImage(file='cross.png')
        self.zero = PhotoImage(file='zero.png')

        self.bclick = True
        self.flag = 0
        self.buttons = StringVar()

        self.label = Label(self.tk, text="Player 1:", font='Comic 15 bold', fg='black', height=1, width=8)
        self.label.grid(row=1, column=0)

        self.label = Label(self.tk, text="Player 2:", font='Comic 15 bold', fg='black', height=1, width=8)
        self.label.grid(row=2, column=0)

        self.button1 = Button(self.tk, text=' ', font='Times 20 bold', bg='#00bfff', height=4, width=8,
                              command=lambda: self.btnClick(self.button1))
        self.button1.grid(row=3, column=0)

        self.button2 = Button(self.tk, text=' ', font='Times 20 bold', bg='#ffff66', height=4, width=8,
                              command=lambda: self.btnClick(self.button2))
        self.button2.grid(row=3, column=1)

        self.button3 = Button(self.tk, text=' ', font='Times 20 bold', bg='#00bfff', height=4, width=8,
                              command=lambda: self.btnClick(self.button3))
        self.button3.grid(row=3, column=2)

        self.button4 = Button(self.tk, text=' ', font='Times 20 bold', bg='#ffff66', height=4, width=8,
                              command=lambda: self.btnClick(self.button4))
        self.button4.grid(row=4, column=0)

        self.button5 = Button(self.tk, text=' ', font='Times 20 bold', bg='#00bfff', height=4, width=8,
                              command=lambda: self.btnClick(self.button5))
        self.button5.grid(row=4, column=1)

        self.button6 = Button(self.tk, text=' ', font='Times 20 bold', bg='#ffff66', height=4, width=8,
                              command=lambda: self.btnClick(self.button6))
        self.button6.grid(row=4, column=2)

        self.button7 = Button(self.tk, text=' ', font='Times 20 bold', bg='#00bfff', height=4, width=8,
                              command=lambda: self.btnClick(self.button7))
        self.button7.grid(row=5, column=0)

        self.button8 = Button(self.tk, text=' ', font='Times 20 bold', bg='#ffff66', height=4, width=8,
                              command=lambda: self.btnClick(self.button8))
        self.button8.grid(row=5, column=1)

        self.button9 = Button(self.tk, text=' ', font='Times 20 bold', bg='#00bfff', height=4, width=8,
                              command=lambda: self.btnClick(self.button9))
        self.button9.grid(row=5, column=2)

    def disableButton(self):
        self.button1.configure(state=DISABLED)
        self.button2.configure(state=DISABLED)
        self.button3.configure(state=DISABLED)
        self.button4.configure(state=DISABLED)
        self.button5.configure(state=DISABLED)
        self.button6.configure(state=DISABLED)
        self.button7.configure(state=DISABLED)
        self.button8.configure(state=DISABLED)
        self.button9.configure(state=DISABLED)

    def btnClick(self, buttons):
        if buttons['text'] == " " and self.bclick == True:
            buttons['image'] = self.zero
            buttons['text'] = 'X'
            buttons['height'] = 141
            buttons['width'] = 131
            self.bclick = False
            self.playerb = self.p2.get() + " Won!"
            self.playera = self.p1.get() + " Won!"
            self.checkForWin()
            self.flag += 1

        elif buttons['text'] == " " and self.bclick == False:
            buttons['image'] = self.cross
            buttons['text'] = 'O'
            buttons['height'] = 141
            buttons['width'] = 131
            self.bclick = True
            self.checkForWin()
            self.flag += 1
        else:
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "Button already clicked!")

    def checkForWin(self):
        if (self.button1['text'] == 'X' and self.button2['text'] == 'X' and self.button3['text'] == 'X' or
                self.button4['text'] == 'X' and self.button5['text'] == 'X' and self.button6['text'] == 'X' or
                self.button7['text'] == 'X' and self.button8['text'] == 'X' and self.button9['text'] == 'X' or
                self.button1['text'] == 'X' and self.button5['text'] == 'X' and self.button9['text'] == 'X' or
                self.button3['text'] == 'X' and self.button5['text'] == 'X' and self.button7['text'] == 'X' or
                self.button1['text'] == 'X' and self.button4['text'] == 'X' and self.button7['text'] == 'X' or
                self.button2['text'] == 'X' and self.button5['text'] == 'X' and self.button8['text'] == 'X' or
                self.button3['text'] == 'X' and self.button6['text'] == 'X' and self.button9['text'] == 'X'):
            self.disableButton()
            tkinter.messagebox.showinfo("Tic-Tac-Toe", self.playera)

        elif (self.flag == 8):
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "It's a Tie!")

        elif (self.button1['text'] == 'O' and self.button2['text'] == 'O' and self.button3['text'] == 'O' or
              self.button4['text'] == 'O' and self.button5['text'] == 'O' and self.button6['text'] == 'O' or
              self.button7['text'] == 'O' and self.button8['text'] == 'O' and self.button9['text'] == 'O' or
              self.button1['text'] == 'O' and self.button5['text'] == 'O' and self.button9['text'] == 'O' or
              self.button3['text'] == 'O' and self.button5['text'] == 'O' and self.button7['text'] == 'O' or
              self.button1['text'] == 'O' and self.button4['text'] == 'O' and self.button7['text'] == 'O' or
              self.button2['text'] == 'O' and self.button5['text'] == 'O' and self.button8['text'] == 'O' or
              self.button3['text'] == 'O' and self.button6['text'] == 'O' and self.button9['text'] == 'O'):
            self.disableButton()
            tkinter.messagebox.showinfo("Tic-Tac-Toe", self.playerb)


if not os.path.exists("audio"):
    os.mkdir("audio")
if not os.path.exists("./images"):
    os.mkdir("./images")

path, dirs, files = next(os.walk("./images"))
image_count = len(files)

r = sr.Recognizer()
with sr.Microphone() as source:
    playsound.playsound("./ppl/audio/init_beep.mp3", True)
    print("Say something")
    audio = r.listen(source)
    print("Time over")
    playsound.playsound("./ppl/audio/end_beep.mp3", True)
try:
    text = r.recognize_google(audio)
    text = text.lower()
except:
    print("Something went wrong")
    sys.exit(0)
print("Text :" + text)


    # driver = webdriver.Chrome("./drivers/chromedriver.exe"),
    #                           chrome_options=chrome_options)
    def method1():
        try:
            # webbrowser.open_new_tab(URL)
            data = soup.find(
                'div', attrs={'class': 'ayqGOc kno-fb-ctx KBXm4e'})
            print(data.text)
            speak = gTTS(text=data.text, lang='en', slow=False)
            speak.save("./ppl/audio/gogole.mp3")
            playsound.playsound("./ppl/audio/gogole.mp3", True)
            driver.quit()
        except:
            return False
        return True


    def method2():
        try:
            data = soup.findAll('div', attrs={'class': 'thODed Uekwlc XpoqFe'})
            # res=(data.text).split(" ")
            count = 0
            for i in data:
                if count > 2:
                    break
                for j in range(2, len(i.text)):
                    if i.text[j] == '.':
                        break
                # if i.text[0] not in ['1', '2', '3']:
                #     print((count+1), end="")
                #     print(". ", end="")
                if i.text[:j + 1] != "":
                    print(i.text[:j + 1])
                    speak = gTTS(text=i.text[:j + 1], lang='en', slow=False)
                    speak.save("./ppl/audio/google.mp3")
                    playsound.playsound("./ppl/audio/google.mp3", True)
                    os.remove('./ppl/audio/google.mp3')
                    flag = False
                else:
                    flag = True
                count += 1
                driver.quit()
                sys.exit(0)
            if flag == False:
                driver.quit()
                sys.exit(0)
            else:
                return True
        except:
            return False


    def method3():
        try:
            data = soup.find('div', attrs={'class': 'z7BZJb XSNERd'})
            res = (data.text).split(" ")
            print(res[1])
            speak = gTTS(text=res[1], lang='en', slow=False)
            speak.save("./ppl/audio/google.mp3")
            playsound.playsound("./ppl/audio/google.mp3", True)
            os.remove('./ppl/audio/google.mp3')
            driver.quit()
        except:
            return False
        return True


    def method4():
        try:
            data = soup.find('div', attrs={'class': 'Z0LcW XcVN5d'})
            print(data.text)
            speak = gTTS(text=data.text, lang='en', slow=False)
            speak.save("./ppl/audio/google.mp3")
            playsound.playsound("./ppl/audio/google.mp3", True)
            os.remove('./ppl/audio/google.mp3')
            driver.quit()
        except:
            return False
        return True


    def method5():
        try:
            data = soup.find('div', attrs={'class': 'Z0LcW XcVN5d AZCkJd'})
            print(data.text)
            speak = gTTS(text=data.text, lang='en', slow=False)
            speak.save("./ppl/audio/google.mp3")
            playsound.playsound("./ppl/audio/google.mp3", True)
            os.remove('./ppl/audio/google.mp3')
            driver.quit()
        except:
            return False
        return True


    text = text.replace('+', '%2B')
    text = text.replace(' ', '+')
    URL = f"https://google.com/search?q={text}"
    data = []
    driver.get(URL)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')
    if method1() or method2() or method3() or method4() or method5():
        pass
    else:
        webbrowser.open_new_tab(URL)
        driver.quit()
