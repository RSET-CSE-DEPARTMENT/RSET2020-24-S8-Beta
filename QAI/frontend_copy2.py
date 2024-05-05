from tkinter import *
import mysql.connector as mcon
import tkinter.messagebox
import datetime
import json
from customtkinter import *
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sounddevice as sd
import scipy.io.wavfile  as wav
# import wavio as wav
from emo import *
from stt import *
from gram import *
from qg import *
from fact import *
from sentiment_analysis import *
import time
from voice_analysis import *

recording = False
recording_count=0
count=0
frames = []
start_time=None
root = Tk()
root.geometry("1920x1080")
root.title("Q&AI")
cap = cv2.VideoCapture(0)
width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

con = mcon.connect(host="localhost", user="root", password="1234")
c = con.cursor()
c.execute("use QAI")

def interview_tips():
    global home_f, logo_i1, scores_f, scores_c, home_b1, home_b2, home_b3, dates, clicked, past_date, time, past_time, scores_b1, score_sliding1, score_sliding2, score_sliding3, chart1,scrollable1,scrollable
    home_f.destroy()
    scrollable.destroy()
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable1=Frame(root)
    scrollable1.pack()
# Create a scrollable frame
    canvas = Canvas(scrollable1, height=2080, width=1920, bg="#FAFAFA")
    # scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    logo_i1=PhotoImage(file = "logo.png")
    scores_f=Frame(scrollable_frame,bg="#FAFAFA")
    scores_f.pack()
    scores_c=Canvas(scores_f,height=2080,width=1920,bg='#FAFAFA')
    scores_c.pack(fill = "both", expand = True)
    scores_b2=CTkButton(scores_c,text="Back",font=("Arial", 30),height=50,fg_color="#4EC261",border_color="#4EC261",text_color="white",cursor="hand2",hover_color='#1F7D2E', command=landing_page)
    scores_b2.place(x=330,y=150)
    scores_c.create_rectangle(0, 0, 1920, 100, fill="#4EC261", outline="#4EC261")
    scores_c.create_rectangle(0, 100, 300, 2080, fill="#1F7D2E", outline="#1F7D2E")
    scores_c.create_image(100,15,image=logo_i1,anchor="nw")
    home_b1=Button(scores_c,text="Past Scores",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2",command=past_scores)
    home_b1.place(x=20,y=250)
    home_b2=Button(scores_c,text="Interview Tips",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    home_b2.place(x=10,y=350)
    scores_c.create_text(960, 180, fill="#4EC261",text="The impression you make on the interviewer \noften can outweigh your actual credentials. ", font=("Arial", 34,"bold"))
    scores_c.create_text(725, 300, fill="black",text="Your poise, attitude, basic social skills, and ability to communicate\nare evaluated along with your experience and education. ", font=("Arial", 15,"normal"))
    scores_c.create_text(650, 400, fill="black",text="Here are some interview tips that may guide you:", font=("Arial", 15))
    scores_c.create_text(800, 720, fill="black",text="1. Be on time\n\n2. Have some questions of your own prepared in advance\n\n3. Greet the interviewer with a handshake and a smile\n\n4. Expect to spend some time developing rapport.\n\n5. Focus on your attributes, your transferable skills, and your willingness to learn\n\n6. Tell the truth\n\n7. Listen carefully to the interviewer.\n\n8. Never slight a teacher, friend, employer, or your university.\n\n9. Watch your grammar.\n\n10. Be prepared for personal questions.\n\n11. Wait for the interviewer to mention salary and benefits.\n\n12. Close on a positive, enthusiastic note.\n\n13. No interview is complete until you follow up with a thank-you note.", font=("Arial", 15))



def changeOnHover(button, colorOnHover, colorOnLeave):
 
    # adjusting background of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))
 
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))
def UploadAction(event=None):
        global filename
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        # print('Selected:', filename)
def update_frame():
    ret, frame = cap.read()
    global count
    if ret:
        name = './data/frame' + str(count) + '.jpg'
        count=count+1
        if(count%50==0):
            cv2.imwrite(name, frame)
            print ('Creating...' + name)  
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (width//3, height//3))
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        interview_l.config(image=photo)
        interview_l.image = photo
    interview_l.after(10, update_frame)
    
def start_recording():
    global start_time,fs,recording1
    start_time= time.time()
    fs = 44100  # Sample rate
    recording1 = sd.rec(int(180 * fs), samplerate=fs, channels=2, dtype='int16')
def stop_recording():
    global start_time,fs,recording1,recording_count,questions,current_question,show_q
    current_question+=1
    if(current_question==len(questions)):
        final_recording()
    else:
        show_q.configure(text=questions[current_question])
    sd.stop()
    end_time = time.time()
    duration = end_time - start_time
    print("Recording duration:", duration, "seconds")
        
        # Cut the audio to the specified duration
    recording1 = recording1[:int(duration * fs)]
        # Save the cut audio
    filename = f"data/recording_{recording_count}.wav"
    recording_count += 1
    wav.write(filename,fs,recording1)
    start_recording()

def final_recording():
    global start_time,fs,recording1,recording_count
    sd.stop()
    end_time = time.time()
    duration = end_time - start_time
    print("Recording duration:", duration, "seconds")
        
        # Cut the audio to the specified duration
    recording1 = recording1[:int(duration * fs)]
        # Save the cut audio
    filename = f"data/recording_{recording_count}.wav"
    wav.write(filename,fs,recording1)
    result()

def interview():
    global interview_f,interview_c,resume,home_f,logo_i1,interview_i1,interview_l,filename,val,questions,current_question,show_q
    resume.destroy()
    home_f.destroy()
    val=val-1
    print(filename,val)
    current_question=0
    questions=['Tell me about yourself']
    questions+=get_questions(filename,val)
    interview_f = Frame(root, bg="#FAFAFA")
    interview_f.pack()
    interview_c=Canvas(interview_f,height=1080,width=1920,bg='#FAFAFA')
    interview_c.pack(fill = "both", expand = True)
    logo_i1=PhotoImage(file = "logo.png")
    interview_i1=PhotoImage(file = "interview_1.jpg")
    interview_c.create_rectangle(0, 0, 1920, 100, fill="#4EC261", outline="#4EC261")
    interview_c.create_image(100,15,image=logo_i1,anchor="nw")
    interview_c.create_image(340,180,image=interview_i1,anchor="nw")
    show_q = CTkLabel(interview_c, text=questions[0], text_color="black",corner_radius=20,width=300,font=("Arial", 15),fg_color="#D9D9D9",height=150,wraplength=280)
    show_q.place(x=380,y=450)
    interview_l = Label(interview_c)
    interview_l.place(x=850,y=450)
    interview_b1=CTkButton(interview_c,text="End",font=("Arial", 30),height=100,width=300,fg_color="#D83535",border_color="#D83535",text_color="white",cursor="hand2",hover_color='red', command=final_recording)
    interview_b1.place(x=830,y=650)
    interview_b2=CTkButton(interview_c,text="Next Question",font=("Arial", 30),height=100,width=300,fg_color="#4EC261",border_color="#4EC261",text_color="white",cursor="hand2",hover_color='#1F7D2E', command=stop_recording)
    interview_b2.place(x=350,y=650)
    start_recording()
    update_frame()

def upload_resume():
    global  resume_f, resume_c, resume_b1,resume,val,filename
    resume = Toplevel()
    filename='Joel_resume.pdf'
    resume.geometry("900x600")
    resume.title("Upload Resume")
    resume_f=Frame(resume,bg="#FAFAFA")
    resume_f.pack()
    resume_c=Canvas(resume_f,height=600,width=900,bg="#FAFAFA")
    resume_c.pack(fill="both",expand=True)
    resume_c.create_text(300, 50, text="Upload Resume", font=("Arial", 30))
    # resume_b1=Button(resume_c,text="Upload",font=("Arial", 30),relief="flat",cursor="hand2", command=UploadAction)
    # resume_b1 = Frame(resume_c, highlightbackground = "black",  
    #                      highlightthickness = 1, bd=0) 
    resume_b1 = CTkButton(resume_c,width=600,height=60, text = 'Upload', text_color = '#BCBCBC',border_width=1, hover_color="gray",
                    fg_color = '#FAFAFA',font = (("Times New Roman"),25),cursor="hand2", command=UploadAction) 
    # bttn.pack() 
    resume_b1.place(x=150,y=100)
    resume_c.create_text(420, 200, text="Choose the number of questions", font=("Arial", 30))
    noq=Label(resume_c, text="5",bg="#FAFAFA", font=("Arial", 20))
    noq.place(x=400,y=250)
    val=IntVar()
    val=5
    def sliding(value):
        global val
        val=int(value)
        noq.config(text=int(value))
    # resume_sliding=customtkinter.CTkSlider(resume_c,from_=5,to=12,number_of_steps=1,fg_color='white',progress_color='#4EC261',orient="horizontal",command=sliding)
    resume_sliding=CTkSlider(resume_c,from_=5,to=12,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=7,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,command=sliding)
    resume_sliding.place(x=150,y=300)  
    resume_sliding.set(5)       
    resume_start_button=CTkButton(resume_c,text="Start",font=("Arial", 30),height=50,fg_color="#4EC261",border_color="#4EC261",text_color="white",cursor="hand2",hover_color='#1F7D2E', command=interview)
    resume_start_button.place(x=350,y=400)
    # resume.mainloop()
def empty_data():
    folder_path = "data"
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
def landing_page():
    empty_data()
    global home_i1, logo_i1, home_i2, home_f, home_c, home_b1, home_b2, home_b3, home_b4, interview_f,scrollable,scrollable1
    scrollable.destroy()
    interview_f.destroy()
    scrollable1.destroy()
    home_i1=PhotoImage(file = "home1.png")
    logo_i1=PhotoImage(file = "logo.png")
    home_i2=PhotoImage(file = "home2.png")
    home_f = Frame(root, bg="#FAFAFA")
    home_f.pack()
    home_c=Canvas(home_f,height=1080,width=1920,bg='#FAFAFA')
    home_c.pack(fill = "both", expand = True)
    home_c.create_rectangle(0, 0, 1920, 100, fill="#4EC261", outline="#4EC261")
    home_c.create_rectangle(0, 100, 300, 1080, fill="#1F7D2E", outline="#1F7D2E")
    home_c.create_image(480,160,image=home_i2,anchor="nw")
    home_c.create_image(900,360,image=home_i1,anchor="nw")
    home_c.create_image(100,15,image=logo_i1,anchor="nw")
    home_c.create_text(800, 300, text="Navigate the Interview\nLandscape with confidence", font=("Arial", 30))
    home_b1=Button(home_c,text="Past Scores",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2",command=past_scores)
    home_b1.place(x=20,y=250)
    home_b2=Button(home_c,text="Interview Tips",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2",command=interview_tips)
    home_b2.place(x=10,y=350)
    # home_b3=Button(home_c,text="Edit Profile",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    # home_b3.place(x=20,y=450)
    home_b4=CTkButton(home_c,text="Take Your Interview",font=("Arial", 30),height=50,fg_color="#4EC261",border_color="#4EC261",text_color="white",cursor="hand2",hover_color='#1F7D2E', command=upload_resume)
    home_b4.place(x=550,y=550)
    changeOnHover(home_b1, "#4EC261", "#1F7D2E")
    changeOnHover(home_b2, "#4EC261", "#1F7D2E")
    # changeOnHover(home_b3, "#4EC261", "#1F7D2E")
    # changeOnHover(home_b4, "#1F7D2E", "#4EC261")

def past_scores():
    global scrollable1,home_f, logo_i1, scores_f, scores_c, home_b1, home_b2, home_b3, dates, clicked, past_date, time, past_time, scores_b1, score_sliding1, score_sliding2, score_sliding3, chart1,scrollable
    home_f.destroy()
    scrollable1.destroy()
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable=Frame(root)
    scrollable.pack()
# Create a scrollable frame
    canvas = Canvas(scrollable, height=2080, width=1920, bg="#FAFAFA")
    # scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    logo_i1=PhotoImage(file = "logo.png")
    scores_f=Frame(scrollable_frame,bg="#FAFAFA")
    scores_f.pack()
    scores_c=Canvas(scores_f,height=2080,width=1920,bg='#FAFAFA')
    scores_c.pack(fill = "both", expand = True)
    scores_b2=CTkButton(scores_c,text="Back",font=("Arial", 30),height=50,fg_color="#4EC261",border_color="#4EC261",text_color="white",cursor="hand2",hover_color='#1F7D2E', command=landing_page)
    scores_b2.place(x=330,y=150)
    scores_c.create_rectangle(0, 0, 1920, 100, fill="#4EC261", outline="#4EC261")
    scores_c.create_rectangle(0, 100, 300, 2080, fill="#1F7D2E", outline="#1F7D2E")
    scores_c.create_image(100,15,image=logo_i1,anchor="nw")
    home_b1=Button(scores_c,text="Past Scores",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    home_b1.place(x=20,y=250)
    home_b2=Button(scores_c,text="Interview Tips",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2",command=interview_tips)
    home_b2.place(x=10,y=350)
    # home_b3=Button(scores_c,text="Edit Profile",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    # home_b3.place(x=20,y=450)
    c.execute("select date from past_scores")
    dates=list(c.fetchall())
    dates = [item[0] for item in dates]
    # print(x)

    # dates = [ 
    # "              01/01/2021              ", 
    # "              02/01/2021              ", 
    # "              03/01/2021              ", 
    # "              04/01/2021              ", 
    # "              08/01/2021              ", 
    # "              10/01/2021              ", 
    # "              15/01/2021              "
    # ] 
    
    # datatype of menu text 
    clicked = StringVar() 
    clicked2 = StringVar() 
    
    # initial menu text 
    
    # Create Dropdown menu 
    def d(x):
        # global times
        print(x)
        print(clicked.get())
        c.execute("select time from past_scores where date='"+clicked.get()+"'")
        times=list(c.fetchall())
        times = [item[0] for item in times]
        print(times)
        past_time = CTkOptionMenu( scores_c ,width=200, variable=clicked2, fg_color="#1F7D2E",button_color="#1F7D2E",dropdown_fg_color="#FAFAFA",text_color="white",dynamic_resizing=False,dropdown_text_color="#4EC261" , values=times )
        past_time.place(x=700,y=320)
    past_date = CTkOptionMenu( scores_c ,width=200, variable=clicked, fg_color="#1F7D2E",button_color="#1F7D2E",dropdown_fg_color="#FAFAFA",text_color="white",dynamic_resizing=False,dropdown_text_color="#4EC261",command=d , values=dates )
    past_date.place(x=700,y=220)
    scores_c.create_text(800, 200, text="Date", font=("Arial", 20))
    if(clicked.get()==''):
        clicked.set(dates[0])
    print(clicked.get())
    c.execute("select time from past_scores where date='"+clicked.get()+"'")
    times=list(c.fetchall())
    times = [item[0] for item in times]
    print(times)
    # times=[
    #     "               01:00 PM               ",
    #     "               02:00 PM               ",
    #     "               03:00 PM               ",
    #     "               04:00 PM               "
    # ]
    past_time = CTkOptionMenu( scores_c ,width=200, variable=clicked2, fg_color="#1F7D2E",button_color="#1F7D2E",dropdown_fg_color="#FAFAFA",text_color="white",dynamic_resizing=False,dropdown_text_color="#4EC261" , values=times )
    past_time.place(x=700,y=320)
    scores_c.create_text(800, 280, text="Time", font=("Arial", 20))
    score1=    tkinter.IntVar()
    score1.set(0)
    score2=	tkinter.IntVar()
    score2.set(0)
    score3=	tkinter.IntVar()
    score3.set(0)
    score4=	tkinter.IntVar()
    score4.set(0)
    def update():
        c.execute("select * from past_scores where date='"+clicked.get()+"' and time='"+clicked2.get()+"'")
        val=c.fetchall()
        print(val)
        o1 = json.loads(val[0][2])
        fig = Figure() # create a figure object
        ax = fig.add_subplot(111) # add an Axes to the figure
        ax.pie(list(o1.values()), radius=1, labels=list(o1.keys()),autopct='%0.2f%%')
        ax.set_facecolor('#FAFAFA')

        chart1 = FigureCanvasTkAgg(fig,scores_c)
        chart1.get_tk_widget().place(x=525,y=950)
        score1.set(val[0][4])
        score2.set(val[0][6])
        score3.set(val[0][3])
        score4.set(val[0][5])

    scores_b1=CTkButton(scores_c,text="Choose",font=("Arial", 30),height=50,fg_color="#4EC261",border_color="#4EC261",text_color="white",cursor="hand2",hover_color='#1F7D2E',command=update)
    scores_b1.place(x=725,y=380)
    scores_c.create_text(600, 450, text="Confidence", font=("Arial", 20))
    score_sliding1=CTkSlider(scores_c,from_=1,to=5,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=5,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,state="disabled",variable=score1)
    score_sliding1.place(x=525,y=500)
    scores_c.create_text(650, 600, text="Language Proficiency", font=("Arial", 20))
    score_sliding2=CTkSlider(scores_c,from_=1,to=5,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=5,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,state="disabled",variable=score2)
    score_sliding2.place(x=525,y=650)
    scores_c.create_text(650, 750, text="Factual Accuracy", font=("Arial", 20))
    score_sliding3=CTkSlider(scores_c,from_=1,to=5,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=5,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,state="disabled",variable=score3)
    score_sliding3.place(x=525,y=800)
    scores_c.create_text(500, 500, text="1", font=("Arial", 20))
    scores_c.create_text(1100, 500, text="5", font=("Arial", 20))
    scores_c.create_text(500, 650, text="1", font=("Arial", 20))
    scores_c.create_text(1100, 650, text="5", font=("Arial", 20))
    scores_c.create_text(500, 800, text="1", font=("Arial", 20))
    scores_c.create_text(1100, 800, text="5", font=("Arial", 20))
    stockListExp = ['Happy' , 'neutral', 'sad', 'angry', 'fear','disgust']
    stockSplitExp = [20,20,20,20,10,10]

    fig = Figure() # create a figure object
    ax = fig.add_subplot(111) # add an Axes to the figure

    ax.pie(stockSplitExp, radius=1, labels=stockListExp,autopct='%0.2f%%')
    ax.set_facecolor('#FAFAFA')

    chart1 = FigureCanvasTkAgg(fig,scores_c)
    chart1.get_tk_widget().place(x=525,y=950)
    score_sliding4=CTkSlider(scores_c,from_=0,to=2,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=5,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,state="disabled",variable=score4)
    score_sliding4.place(x=525,y=1550)
    scores_c.create_text(450, 1550, text="negative", font=("Arial", 20))
    scores_c.create_text(1150, 1550, text="positive", font=("Arial", 20))

def result():
    global questions
    o1=emotion()
    speact_to_text()
    o2=sentiment_analysis()
    o3=grammar()
    o4=confidence()
    o5=fact(questions)
    print(o1)
    print(o2)
    print(o4)
    global home_f, logo_i1, scores_f, scores_c, home_b1, home_b2, home_b3, dates, clicked, past_date, time, past_time, scores_b1, score_sliding1, score_sliding2, score_sliding3, chart1,scrollable,interview_f
    home_f.destroy()
    interview_f.destroy()
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable=Frame(root)
    scrollable.pack()
# Create a scrollable frame
    canvas = Canvas(scrollable, height=2080, width=1920, bg="#FAFAFA")
    # scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    logo_i1=PhotoImage(file = "logo.png")
    scores_f=Frame(scrollable_frame,bg="#FAFAFA")
    scores_f.pack()
    scores_c=Canvas(scores_f,height=2080,width=1920,bg='#FAFAFA')
    scores_c.pack(fill = "both", expand = True)
    scores_c.create_text(800, 250, text="Result", font=("Arial", 60))
    # border=CTkFrame(scores_c,fg_color="#FAFAFA",height=1580,width=1020,border_width=2)
    # border.place(x=300,y=200)
    scores_b2=CTkButton(scores_c,text="Home",font=("Arial", 30),height=50,fg_color="#4EC261",border_color="#4EC261",text_color="white",cursor="hand2",hover_color='#1F7D2E',command=landing_page)
    scores_b2.place(x=730,y=1750)
    scores_c.create_rectangle(0, 0, 1920, 100, fill="#4EC261", outline="#4EC261")
    # scores_c.create_rectangle(0, 100, 300, 2080, fill="#1F7D2E", outline="#1F7D2E")
    scores_c.create_image(100,15,image=logo_i1,anchor="nw")
    # home_b1=Button(scores_c,text="Past Scores",font=("Arial", 30),bg="#4EC261",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    # home_b1.place(x=20,y=250)
    # home_b2=Button(scores_c,text="Interview Tips",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    # home_b2.place(x=10,y=350)
    # home_b3=Button(scores_c,text="Edit Profile",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    # home_b3.place(x=20,y=450)
    
    score1=    tkinter.IntVar()
    score1.set(o4)
    score2=	tkinter.IntVar()
    score2.set(o3)
    score3=	tkinter.IntVar()
    score3.set(o5)
    score4=	tkinter.IntVar()
    score4.set(o2)
    scores_c.create_text(600, 450, text="Confidence", font=("Arial", 20))
    score_sliding1=CTkSlider(scores_c,from_=1,to=5,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=5,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,state="disabled",variable=score1)
    score_sliding1.place(x=525,y=500)
    scores_c.create_text(650, 600, text="Language Proficiency", font=("Arial", 20))
    score_sliding2=CTkSlider(scores_c,from_=1,to=5,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=5,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,state="disabled",variable=score2)
    score_sliding2.place(x=525,y=650)
    scores_c.create_text(650, 750, text="Factual Accuracy", font=("Arial", 20))
    score_sliding3=CTkSlider(scores_c,from_=1,to=5,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=5,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,state="disabled",variable=score3)
    score_sliding3.place(x=525,y=800)
    scores_c.create_text(500, 500, text="1", font=("Arial", 20))
    scores_c.create_text(1100, 500, text="5", font=("Arial", 20))
    scores_c.create_text(500, 650, text="1", font=("Arial", 20))
    scores_c.create_text(1100, 650, text="5", font=("Arial", 20))
    scores_c.create_text(500, 800, text="1", font=("Arial", 20))
    scores_c.create_text(1100, 800, text="5", font=("Arial", 20))
    stockListExp = ['Happy' , 'neutral', 'sad', 'angry', 'fear','disgust']
    stockSplitExp = [15,25,20,20,10,10]

    fig = Figure() # create a figure object
    ax = fig.add_subplot(111) # add an Axes to the figure
    ax.pie(list(o1.values()), radius=1, labels=list(o1.keys()),autopct='%0.2f%%')
    ax.set_facecolor('#FAFAFA')

    chart1 = FigureCanvasTkAgg(fig,scores_c)
    scores_c.create_text(650, 1500, text="Sentiment", font=("Arial", 20))
    chart1.get_tk_widget().place(x=525,y=950)
    score_sliding4=CTkSlider(scores_c,from_=0,to=2,button_corner_radius=10,button_hover_color="#4EC261",border_color="black",border_width=1,number_of_steps=3,button_color="#4EC261",fg_color="#FAFAFA",progress_color="#4EC261",orientation="horizontal",width=550,state="disabled",variable=score4)
    score_sliding4.place(x=525,y=1550)
    scores_c.create_text(450, 1550, text="negative", font=("Arial", 20))
    scores_c.create_text(1150, 1550, text="positive", font=("Arial", 20))
    c.execute("insert into past_scores values('"+str(datetime.date.today())+"','"+str(datetime.datetime.now().strftime("%H:%M:%S"))+"','"+json.dumps(o1)+"','"+str(o5)+"','"+str(o4)+"','"+str(o2)+"','"+str(o3)+"')")
    con.commit()

resume_i1=PhotoImage(file = "upload2.png")


interview_f = Frame(root, bg="#FAFAFA")
scrollable=Frame(root)
scrollable1=Frame(root)
landing_page()
root.mainloop()
cap.release()
cv2.destroyAllWindows()