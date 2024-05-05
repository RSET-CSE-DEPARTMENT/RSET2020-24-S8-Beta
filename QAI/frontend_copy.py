from tkinter import *
import mysql.connector as mcon
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

root = Tk()
root.geometry("1920x1080")
root.title("Q&AI")
cap = cv2.VideoCapture(0)
width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

con = mcon.connect(host="localhost", user="root", password="1234")
c = con.cursor()
c.execute("use bloodbank")
count=0
freq = 44100
duration = 5
def changeOnHover(button, colorOnHover, colorOnLeave):
 
    # adjusting background of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover))
 
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave))
def UploadAction(event=None):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
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
    

def interview():
    global interview_f,interview_c,resume,home_f,logo_i1,interview_i1,interview_l
    resume.destroy()
    home_f.destroy()
    interview_f = Frame(root, bg="#FAFAFA")
    interview_f.pack()
    interview_c=Canvas(interview_f,height=1080,width=1920,bg='#FAFAFA')
    interview_c.pack(fill = "both", expand = True)
    logo_i1=PhotoImage(file = "logo.png")
    interview_i1=PhotoImage(file = "interview_1.png")
    interview_c.create_rectangle(0, 0, 1920, 100, fill="#4EC261", outline="#4EC261")
    interview_c.create_image(100,15,image=logo_i1,anchor="nw")
    interview_c.create_image(340,180,image=interview_i1,anchor="nw")
    interview_l = Label(interview_c)
    interview_l.place(x=850,y=450)
    interview_b1=Button(interview_c,width=10,text="End",font=("Arial", 30),bg="#D83535",fg="white",relief="flat",activebackground="#D83535",activeforeground="white",cursor="hand2", command=result)
    interview_b1.place(x=880,y=650)
    interview_b2=Button(interview_c,width=16,text="Next Question",font=("Arial", 30),bg="#4EC261",fg="white",relief="flat",activebackground="#4EC261",activeforeground="white",cursor="hand2",command=process)
    interview_b2.place(x=350,y=650)
    update_frame()

def upload_resume():
    global  resume_f, resume_c, resume_b1,resume
    resume = Tk()
    resume.geometry("900x600")
    resume.title("Upload Resume")
    resume_f=Frame(resume,bg="#FAFAFA")
    resume_f.pack()
    resume_c=Canvas(resume_f,height=600,width=900,bg="#FAFAFA")
    resume_c.pack(fill="both",expand=True)
    resume_c.create_text(300, 50, text="Upload Resume", font=("Arial", 30))
    # resume_b1=Button(resume_c,text="Upload",font=("Arial", 30),relief="flat",cursor="hand2", command=UploadAction)
    resume_b1 = Frame(resume_c, highlightbackground = "black",  
                         highlightthickness = 1, bd=0) 
    bttn = Button(resume_b1,width=50,height=2, text = 'Upload', fg = '#BCBCBC', 
                    bg = '#FAFAFA',font = (("Times New Roman"),15),cursor="hand2", command=UploadAction) 
    bttn.pack() 
    resume_b1.place(x=150,y=100)
    resume_c.create_text(420, 200, text="Choose the number of questions", font=("Arial", 30))
    noq=Label(resume_c, text="5",bg="#FAFAFA", font=("Arial", 20))
    noq.place(x=400,y=250)
    val=IntVar()
    def sliding(val):
        noq.config(text=val)
    # resume_sliding=customtkinter.CTkSlider(resume_c,from_=5,to=12,number_of_steps=1,fg_color='white',progress_color='#4EC261',orient="horizontal",command=sliding)
    resume_sliding=Scale(resume_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",variable=val,length=550,command=sliding)
    resume_sliding.place(x=150,y=300)         
    resume_start_button=Button(resume_c,text="Start",font=("Arial", 30),bg="#4EC261",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2", command=interview)
    resume_start_button.place(x=350,y=400)
    resume.mainloop()
def landing_page():
    global home_i1, logo_i1, home_i2, home_f, home_c, home_b1, home_b2, home_b3, home_b4, interview_f,scrollable
    scrollable.destroy()
    interview_f.destroy()
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
    home_b2=Button(home_c,text="Interview Tips",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    home_b2.place(x=10,y=350)
    home_b3=Button(home_c,text="Edit Profile",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    home_b3.place(x=20,y=450)
    home_b4=Button(home_c,text="Take Your Interview",font=("Arial", 30),bg="#4EC261",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2", command=upload_resume)
    home_b4.place(x=550,y=550)
    changeOnHover(home_b1, "#4EC261", "#1F7D2E")
    changeOnHover(home_b2, "#4EC261", "#1F7D2E")
    changeOnHover(home_b3, "#4EC261", "#1F7D2E")
    changeOnHover(home_b4, "#1F7D2E", "#4EC261")

def past_scores():
    global home_f, logo_i1, scores_f, scores_c, home_b1, home_b2, home_b3, dates, clicked, past_date, time, past_time, scores_b1, score_sliding1, score_sliding2, score_sliding3, chart1,scrollable
    home_f.destroy()
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
    scores_b2=Button(scores_c,text="Back",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2",command=landing_page)
    scores_b2.place(x=330,y=150)
    scores_c.create_rectangle(0, 0, 1920, 100, fill="#4EC261", outline="#4EC261")
    scores_c.create_rectangle(0, 100, 300, 2080, fill="#1F7D2E", outline="#1F7D2E")
    scores_c.create_image(100,15,image=logo_i1,anchor="nw")
    home_b1=Button(scores_c,text="Past Scores",font=("Arial", 30),bg="#4EC261",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    home_b1.place(x=20,y=250)
    home_b2=Button(scores_c,text="Interview Tips",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    home_b2.place(x=10,y=350)
    home_b3=Button(scores_c,text="Edit Profile",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    home_b3.place(x=20,y=450)
    dates = [ 
    "              01/01/2021              ", 
    "              02/01/2021              ", 
    "              03/01/2021              ", 
    "              04/01/2021              ", 
    "              08/01/2021              ", 
    "              10/01/2021              ", 
    "              15/01/2021              "
    ] 
    
    # datatype of menu text 
    clicked = StringVar() 
    
    # initial menu text 
    clicked.set( "              01/01/2021              " ) 
    
    # Create Dropdown menu 
    past_date = OptionMenu( scores_c , clicked , *dates )
    past_date.place(x=800,y=220)
    scores_c.create_text(800, 200, text="Date", font=("Arial", 20))
    time=[
        "               01:00 PM               ",
        "               02:00 PM               ",
        "               03:00 PM               ",
        "               04:00 PM               "
    ]
    past_time = OptionMenu( scores_c , clicked , *time )
    past_time.place(x=800,y=320)
    scores_c.create_text(800, 280, text="Time", font=("Arial", 20))
    scores_b1=Button(scores_c,text="Choose",font=("Arial", 20),bg="#4EC261",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2")
    scores_b1.place(x=800,y=380)
    scores_c.create_text(600, 450, text="Confidence", font=("Arial", 20))
    score_sliding1=Scale(scores_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",length=550,state="disabled")
    score_sliding1.place(x=525,y=500)
    scores_c.create_text(650, 600, text="Language Proficiency", font=("Arial", 20))
    score_sliding2=Scale(scores_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",length=550,state="disabled")
    score_sliding2.place(x=525,y=650)
    scores_c.create_text(650, 750, text="Factual Accuracy", font=("Arial", 20))
    score_sliding3=Scale(scores_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",length=550,state="disabled")
    score_sliding3.place(x=525,y=800)
    stockListExp = ['Happy' , 'neutral', 'sad', 'angry', 'fear','disgust']
    stockSplitExp = [15,25,20,20,10,10]

    fig = Figure() # create a figure object
    ax = fig.add_subplot(111) # add an Axes to the figure

    ax.pie(stockSplitExp, radius=1, labels=stockListExp,autopct='%0.2f%%')
    ax.set_facecolor('#FAFAFA')

    chart1 = FigureCanvasTkAgg(fig,scores_c)
    scores_c.create_text(650, 1500, text="Sentiment", font=("Arial", 20))
    chart1.get_tk_widget().place(x=525,y=950)
    score_sliding4=Scale(scores_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",length=550,state="disabled")
    score_sliding4.place(x=525,y=1550)

def process():
    global freq,duration
    recording = sd.rec(int(duration * freq),samplerate=freq, channels=2)
    sd.wait()
    write("./data/recording0.wav", freq, recording)
    result()

def result():
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
    scores_c.create_text(600, 250, text="Result", font=("Arial", 30))
    scores_b2=Button(scores_c,text="Home",font=("Arial", 30),bg="#1F7D2E",fg="white",relief="flat",activebackground="#1F7D2E",activeforeground="white",cursor="hand2",command=landing_page)
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
    
    scores_c.create_text(600, 450, text="Confidence", font=("Arial", 20))
    score_sliding1=Scale(scores_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",length=550,state="disabled")
    score_sliding1.place(x=525,y=500)
    scores_c.create_text(650, 600, text="Language Proficiency", font=("Arial", 20))
    score_sliding2=Scale(scores_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",length=550,state="disabled")
    score_sliding2.place(x=525,y=650)
    scores_c.create_text(650, 750, text="Factual Accuracy", font=("Arial", 20))
    score_sliding3=Scale(scores_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",length=550,state="disabled")
    score_sliding3.place(x=525,y=800)
    stockListExp = ['Happy' , 'neutral', 'sad', 'angry', 'fear','disgust']
    stockSplitExp = [15,25,20,20,10,10]

    fig = Figure() # create a figure object
    ax = fig.add_subplot(111) # add an Axes to the figure

    ax.pie(stockSplitExp, radius=1, labels=stockListExp,autopct='%0.2f%%')
    ax.set_facecolor('#FAFAFA')

    chart1 = FigureCanvasTkAgg(fig,scores_c)
    scores_c.create_text(650, 1500, text="Sentiment", font=("Arial", 20))
    chart1.get_tk_widget().place(x=525,y=950)
    score_sliding4=Scale(scores_c,from_=5,to=12,fg="#FAFAFA",bg="#FAFAFA",troughcolor="#4EC261",orient="horizontal",length=550,state="disabled")
    score_sliding4.place(x=525,y=1550)

resume_i1=PhotoImage(file = "upload2.png")


interview_f = Frame(root, bg="#FAFAFA")
scrollable=Frame(root)
landing_page()
root.mainloop()
cap.release()
cv2.destroyAllWindows()