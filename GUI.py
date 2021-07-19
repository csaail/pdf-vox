from tkinter import *
import tkinter as tk
import PyPDF2
from tkinter import filedialog
from pygame import mixer
from gtts import gTTS


root = tk.Tk()
root.title('Pdf Reader')
root.iconbitmap('images/icon.ico')
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

#bg image
bg = PhotoImage(file ="images/bg.png")

#label for bg image
bglabel = Label(root, image= bg)
bglabel.place(x=0, y=0, relwidth= 1, relheight= 1)

cp = 0
#func to add pdf
def add_pdf():
  #initializing value of current page as 0
  add_pdf.cp = cp
  
  #adding pdf from computer
  add_pdf.pdf = filedialog.askopenfilename(initialdir='pdfs/', title="choose a pdf", filetypes =(("pdf files", "*.pdf"), )) 
  add_pdf.pdf_file= PyPDF2.PdfFileReader(add_pdf.pdf)
  
  #extracting total number of pages in pdf 
  add_pdf.lpg = add_pdf.pdf_file.numPages
  add_pdf.nlpg = add_pdf.lpg - 1
  extract()
  
  # removing unwanted names
  pdf = add_pdf.pdf.replace("C:/Users/SAAIL/Desktop/projects/pdf to audio/pdfs/", "")
  pdf = pdf.replace(".pdf", "")  
  
  
  #insert pdf in pdf list box
  pdf_list.insert(END, pdf)
  
  #insert pdf text in text box
  text.insert(1.0,add_pdf.content)
  
  
def extract():
  #extracting text from pdf
  add_pdf.page= add_pdf.pdf_file.getPage(add_pdf.cp)
  add_pdf.content=add_pdf.page.extractText()   


def del_insert():
  text.delete('1.0', END)
  text.insert(1.0,add_pdf.content)
  

#first page
def first_pg():
  add_pdf.cp = 0
  extract()
  del_insert()
 
  
#prvious page 
def prev_pg():
  add_pdf.cp = add_pdf.cp - 1
  extract()
  del_insert() 
  
#last page
def last_pg():
  add_pdf.cp = add_pdf.lpg - 1
  extract()
  del_insert()
#change page number 

def jump():
  inp=text2.get()
  inp2 = int(inp) 
  lbl.config(text = "on"+inp)
  add_pdf.cp = inp2
  extract()
  del_insert()


def talk():
    tts = gTTS(text=add_pdf.content, lang='en')
    tts.save("temp.mp3")

def play():
    talk()
    mixer.init()
    mixer.music.load("temp.mp3")
    mixer.music.play()
  
  
#stop button
def stop():
  mixer.music.stop()
  
#pause button
def pause():
  mixer.music.pause()

#unpause button
def unpause():
  mixer.music.unpause()


#next page 
def nxt_pg():
  add_pdf.cp = add_pdf.cp +1
  if mixer.music.get_busy() == True:
    mixer.music.stop()
    mixer.music.unload()
    extract() 
    del_insert() 
    talk() 
  else:  
    print("nope")
    
    
#function to hover 
def button_hover(button, color_on_hover, color_on_leave):
  button.bind("<Enter>", func = lambda e: button.config(background=color_on_hover))
  button.bind("<Leave>", func = lambda e: button.config(background=color_on_leave))

#control button images
fpg_btn_img = PhotoImage(file='images/fpg.png')
prev_btn_img = PhotoImage(file='images/next2.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
unpause_btn_img = PhotoImage(file='images/unpause.png')
stop_btn_img = PhotoImage(file='images/stop.png') 
nxt_btn_img = PhotoImage(file='images/next.png')
lpg_btn_img = PhotoImage(file='images/lpg.png')

#frame for control button
master_frame = Frame(root)
master_frame.pack(pady=20)

#control frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

#control button
fpg_btn =   Button(controls_frame, image = fpg_btn_img, width=50, height=50, 
                  command= first_pg)
prev_btn =  Button(controls_frame, image = prev_btn_img, width=50, height=50, 
                  command= prev_pg)
play_btn =  Button(controls_frame, image = play_btn_img, width=50, height=50, 
                  command= play)
pause_btn = Button(controls_frame, image = pause_btn_img, width=50, height=50, 
                  command= pause)
up_btn =    Button(controls_frame, image = unpause_btn_img, width=50, height=50, 
                  command= unpause)
stop_btn =  Button(controls_frame, image = stop_btn_img, width=50, height=50, 
                  command= stop)
nxt_btn =   Button(controls_frame, image= nxt_btn_img, width=50, height=50, 
                  command= nxt_pg)
lpg_btn =   Button(controls_frame, image = lpg_btn_img, width=50, height=50, 
                  command=last_pg)

#control grid
fpg_btn.grid(row=0,column=0,padx=10)
prev_btn.grid(row=0,column=1,padx=10)
play_btn.grid(row=0,column=3,padx=10)
pause_btn.grid(row=0,column=4,padx=10)
up_btn.grid(row=0,column=5,padx=10)
stop_btn.grid(row=0,column=6,padx=10)
nxt_btn.grid(row=0,column=7,padx=10)
lpg_btn.grid(row=0,column=8,padx=10)

#button hover
button_hover(fpg_btn, "white", "SystemButtonFace")
button_hover(prev_btn, "white", "SystemButtonFace")
button_hover(play_btn, "white", "SystemButtonFace")
button_hover(pause_btn, "white", "SystemButtonFace")
button_hover(up_btn, "white", "SystemButtonFace")
button_hover(stop_btn, "white", "SystemButtonFace")
button_hover(nxt_btn, "white", "SystemButtonFace")
button_hover(lpg_btn, "white", "SystemButtonFace")


#pdf list
pdf_list = Listbox(root, bg="black", 
                  fg="green", 
                  width=60, 
                  selectbackground= "gray", 
                  selectforeground="black")
pdf_list.pack()

#frame for text box and page number
pg_frame = Frame(root)
pg_frame.pack(pady=20)

#frame for pg no
pg_frame1 = Frame(pg_frame)
pg_frame1.pack()

#frame for text box
pg_frame2 = Frame(pg_frame)
pg_frame2.pack()

#frames pg no + txt box
page_change1 = Frame(pg_frame1)
page_change2 = Frame(pg_frame2)

#grid pg no + txt box
page_change1.grid(row=0, column=0, pady=5)
page_change2.grid(row=1, column=0, pady=2)

lbl = tk.Label(root, text = "")
lbl.pack()

# Label Creation
#printt()
text1 = "0"
text21 = "0"
lbl = tk.Label(page_change1, text =  text1 + " of " + text21)
lbl2 = tk.Label(page_change1, text = "enter pg no")

#text box for page number 
text2= Text(page_change1,
            height=1,
            width=5)
#btn to jump to that page
jump_btn =   Button(page_change1, text="jump", 
                    width=5, 
                    height=1, 
                    command= jump)


lbl.grid(row=0,column=0,padx=10)
text2.grid(row=0,column=1,padx=10)

lbl2.grid(row=1,column=1,padx=10)

jump_btn.grid(row=0,column=2,padx=10)
button_hover(jump_btn, "white", "SystemButtonFace")


#text box  
text= Text(page_change2,
           height=23,
           width=80)
text.pack(pady=5) 


#menu
my_menu = Menu(root)
root.config(menu = my_menu)

#adding menu
add_pdf_menu = Menu(my_menu)

my_menu.add_cascade(label="Add pdf", 
                    menu = add_pdf_menu)
add_pdf_menu.add_command(label="add pdf in box", 
                         command= add_pdf)


root.mainloop()
