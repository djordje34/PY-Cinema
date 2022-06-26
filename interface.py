from asyncio.windows_events import NULL
import tkinter as tk
from turtle import bgcolor
import webbrowser
from matplotlib.pyplot import fill, text
import pandas as pd
import tkinter.messagebox
from tkinter import Entry, Label, ttk
import urllib.request
import urllib3
import re
from adminMenu import adminMenu
from korisnik import Korisnik
from zaposleni import Zaposleni
from film import Film
from bioskopska_sala import BioskopskaSala
from termin import Termin
from korisnickiInterfejs import KorisnickiInterfejs
from osoba import Osoba
from admin import Admin
#paleta
YELLOW="#E7BB41"
GREY="#393E41"
LIGHT_GREY="#D3D0CB"
PLATINUM="#E7E5DF"
BLUE="#44BBA4"
#global indicators and vars
global currentUser
global username
global login
global reg
global existingLogs
global allUsers
existingLogs=pd.read_csv("data/zaposleni.txt",sep=" ",header=None)
existingLogs.columns=["id","ime","prezime","username","password"]
allUsers=pd.read_csv("data/sviKorisnici.txt",sep=" ",header=None)
allUsers.columns=["id","ime","prezime","username","password"]
#string checker for tk StringVars
def character_limit(text,x):
    if len(text.get()) > 0:
        text.set(text.get()[:x])

def loggingin():
    global currentUser
    global existingLogs
    global allUsers
    uname=username.get()
    passw=password.get()
    
    if uname=="admin" and passw=="administrator":
        
        login.destroy()
        currentUser=Admin()
        adminMenu()
    else:
    
        if uname not in allUsers["username"].values:        
            tkinter.messagebox.showinfo("Greška","Korisničko ime ne postoji")
        else:
            if passw!=allUsers[allUsers["username"]==uname]["password"].values[0]:
                tkinter.messagebox.showinfo("Greška","Pogrešna lozinka")
            else:
                currentUser=Osoba(allUsers[allUsers["username"]==uname]["ime"].values[0],allUsers[allUsers["username"]==uname]["prezime"].values[0],allUsers[allUsers["username"]==uname]["username"].values[0],allUsers[allUsers["username"]==uname]["password"].values[0],isIt="log")
                tkinter.messagebox.showinfo("Uspešna prijava","Uspešno ste se prijavili")
                login.destroy()

                if currentUser.isOsobaAZaposleni():
                    currentUser=Zaposleni(currentUser.im,currentUser.prez,currentUser.username,currentUser.password)
                    mainmenu()
                else:
                    currentUser=Korisnik(currentUser.im,currentUser.prez,currentUser.username,currentUser.password,isIt="log")
                    currentUser.pristup()
                #redirect to korisnik menu->napravi posebnu klasu sa GUI za korisnika 
def registering():
    global existingLogs
    global allUsers
    uname=username.get()
    passw=password.get()
    im=ime.get()
    ime1=im.split(" ")
    if uname in allUsers["username"].values:
        tkinter.messagebox.showinfo("Greška","Korisničko ime već postoji")
    else:
        if ime1 == [''] or len(ime1)!=2:
            tk.messagebox.showinfo("Greška","Molimo Vas unesite Vaše ime i prezime u ispravnom formatu (ime prezime)")
        else:
            ime2=ime1[0]
            prez=ime1[1]
            korisnik=Korisnik(ime2,prez,uname,passw)
        if uname=="" or passw=="" or len(uname)<6 or len(passw)<6:
            tk.messagebox.showinfo("Greška","Molimo Vas unesite Vaše korisničko ime i lozinku koje sadrže minimalno 6 karaktera")
        else:
            korisnik.exportKorisnik()
            tk.messagebox.showinfo("Uspešna registracija","Uspešno ste se registrovali")
            #redirect from registration to login
            existingLogs=pd.read_csv("data/zaposleni.txt",sep=" ",header=None)
            existingLogs.columns=["id","ime","prezime","username","password"]
            allUsers=pd.read_csv("data/sviKorisnici.txt",sep=" ",header=None)
            allUsers.columns=["id","ime","prezime","username","password"]
            redirectToLoginFromReg()
            
def redirectToLoginFromReg():
    reg.destroy()
    loginNew()
    
def registration():
    global reg
    reg=tk.Tk()
    
    global username
    username= tk.StringVar() 
    global password
    password=tk.StringVar()
    global ime
    ime=tk.StringVar()
    
    
    username.trace("w", lambda *args: character_limit(username,15))
    password.trace("w", lambda *args: character_limit(password,15))
    ime.trace("w", lambda *args: character_limit(ime,35))
    
    reg.title("Registracija")
    reg.config(bg=PLATINUM)
    reg.geometry("1080x720")
    reg.resizable(height = None, width = None)
    
    tk.Label(reg,bg=PLATINUM,font="Helvetica 12 bold").pack(anchor="center",fill="x",pady=80)
    
    imeText=tk.StringVar()
    imeText.set("Uneti Vaše ime i prezime")
    imeDir=tk.Label(reg, textvariable=imeText, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
    imeDir.pack(side="top", fill="x", pady=10)
    imeField=tk.Entry(reg,width=35,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,textvariable=ime,justify="center")
    imeField.pack(anchor="center",pady=0,ipadx=10,ipady=5)
    
    usernameText=tk.StringVar()
    usernameText.set("Uneti željeno korisničko ime")
    usernameDir=tk.Label(reg, textvariable=usernameText, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
    usernameDir.pack(side="top", fill="x", pady=10)
    usernameField=tk.Entry(reg,width=15,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,textvariable=username,justify="center")
    usernameField.pack(anchor="center",pady=0,ipadx=10,ipady=5)
    
    passwordText=tk.StringVar()
    passwordText.set("Uneti željenu korisničku lozinku")
    passwordDir=tk.Label(reg, textvariable=passwordText, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
    passwordDir.pack(side="top", fill="x", pady=10)
    passwordField=tk.Entry(reg,width=15,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,show="*",textvariable=password,justify="center")
    passwordField.pack(anchor="center",pady=0,ipadx=10,ipady=5)
    
    registracija=tk.Button(reg,text="Registruj se",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=registering,activebackground=BLUE,activeforeground=YELLOW)
    registracija.pack(anchor="center",pady=60)
    frame3=tk.Frame(reg,bg=PLATINUM)
    
    redirect=tk.Button(frame3,text="Prijava",width=15,height=2,font=("Helvetica",15),bg=PLATINUM,fg=BLUE,border=0,command=redirectToLoginFromReg,activebackground=PLATINUM,activeforeground=YELLOW)
    redirect.pack(anchor="se",pady=20,padx=10)
    frame3.pack(anchor="se",pady=0,padx=10,side="bottom")
    reg.mainloop()
    
    
    
def loginNew():        #napravi za prijavu!!!!
    global login
    login=tk.Tk()
    def redirectToRegFromLogin():
        login.destroy()
        registration()
    
    global username
    username= tk.StringVar() 
    global password
    password=tk.StringVar()
    
    username.trace("w", lambda *args: character_limit(username,15))
    password.trace("w", lambda *args: character_limit(password,15))
    
    login.title("Prijava")
    login.config(bg=PLATINUM)
    login.geometry("1080x720")
    login.resizable(height = None, width = None)
    frame1=tk.Frame(login,bg=PLATINUM)
    usernameText=tk.StringVar()
    usernameText.set("Uneti korisničko ime")
    usernameDir=tk.Label(frame1, textvariable=usernameText, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
    usernameDir.pack(side="top", fill="x", pady=10)
    usernameField=tk.Entry(frame1,width=15,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,textvariable=username,justify="center")
    usernameField.pack(anchor="center",pady=0,ipadx=10,ipady=5)
    
    passwordText=tk.StringVar()
    passwordText.set("Uneti korisničku lozinku")
    passwordDir=tk.Label(frame1, textvariable=passwordText, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
    passwordDir.pack(side="top", fill="x", pady=10)
    passwordField=tk.Entry(frame1,width=15,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,show="*",textvariable=password,justify="center")
    passwordField.pack(anchor="center",pady=0,ipadx=10,ipady=5)
    
    logbutton=tk.Button(frame1,text="Uloguj se",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=loggingin,activebackground=BLUE,activeforeground=YELLOW)
    logbutton.pack(anchor="center",pady=80)
    frame1.pack(anchor="center",pady=120,padx=10)
    frame2=tk.Frame(login,bg=PLATINUM)
    back=tk.Button(frame2,text="Registracija",width=15,height=2,font=("Helvetica",15),bg=PLATINUM,fg=BLUE,border=0,command=redirectToRegFromLogin,activebackground=PLATINUM,activeforeground=YELLOW)
    back.pack(anchor="se",pady=20,padx=10)
    frame2.pack(anchor="se",pady=0,padx=10,side="bottom")
    login.mainloop()


   
def pregledsala():  #napravi kao za filmove, get id sale i prikaz termina gde sala.id==termin.sID,slob mesta,termin.vreme
    global frame
    global tableFrame
    global currentUser
    global j
        
    j=-1
    
    def sledecasala():
        def deleteTermin(j,i):
                df=pd.read_csv("data/termini.txt",sep=" ",header=None)
                df.columns=["salaID","filmID","vreme","slobMesta"]
                temp=df.loc[df["salaID"]!=j]
                df=df.loc[df["salaID"]==j]
                df.reset_index(drop=True,inplace=True)
                idF=df.loc[df.index==i]["filmID"].values[0]
                imeF=Film.naOsnovuID(idF)
                ime=imeF["naziv"].values[0]
                df=df.loc[df.index!=i];
                df3=temp.append(df)
                df3.reset_index(drop=True,inplace=True)
                df3.to_csv("data/termini.txt",sep=" ",header=None,index=False)

                tkinter.messagebox.showinfo("Uspešno","Uspešno ste obrisali termin filma "+ime)
                
                
                
        global xyz,yzx,xzy,zyx,zxy,yxz,j,check,tableFrame,frame,delTermin
        check=False
        df=pd.read_csv("data/bioskopskasala.txt",sep=" ",header=None)
        if j==len(df)-1:
            j=-1
   #proveri da ne dolazi do loopa
        if tableFrame is not None:
            tableFrame.destroy()
            tableFrame=tk.Frame(bg=PLATINUM)
          
        filmovi=Film.returnAllMovies()
        j+=1
        sala=BioskopskaSala.loadSala(j)
        if(sala==None): 
            check=True
            sledecasala()
        else:
            check=False
        print("sala loaded")
        terminiJ=pd.DataFrame()
        terminiJ=sala.vratiTermine()    #dodaj da ih spaja sve u 1 row kao u svesci i mogucnost vise rowova
        if terminiJ.empty:
            tk.Label(tableFrame,text=("Nema rezervisanih termina za salu broj "+str(sala.id)),bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=11,column=0,columnspan=5,pady=10)
        else:
            xyz=tk.Label(tableFrame,text="Sala broj "+str(sala.id),bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=11,column=0,columnspan=10)
        counter=1;
        tk.Label(tableFrame,text="ID filma",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=1)
        tk.Label(tableFrame,text="Naziv",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=2)
        tk.Label(tableFrame,text="Vreme početka",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=3)
        tk.Label(tableFrame,text="Slobodnih mesta",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=4)
        tk.Label(tableFrame,text="Ukupno mesta",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=5)
        tk.Label(tableFrame,text="Opcije",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=6)
        for i in range(len(terminiJ)):  #namesti da se vidi ime filma kad i koliko

            print("Counter:",counter)
            xzy=tk.Label(tableFrame,text=terminiJ.iloc[i,1],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=counter,column=1,padx=10,pady=10)
            zyx=tk.Label(tableFrame,text=filmovi.loc[filmovi["id"]==terminiJ.iloc[i,1],"naziv"].values[0],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=counter,column=2,padx=10,pady=10)
            zxy=tk.Label(tableFrame,text=terminiJ.iloc[i,2],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=counter,column=3,padx=10,pady=10)
            yxz=tk.Label(tableFrame,text=terminiJ.iloc[i,3],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=counter,column=4,padx=10,pady=10)
            yzx=tk.Label(tableFrame,text=sala.mesta,bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=counter,column=5,padx=10,pady=10)
            delTermin=tk.Button(tableFrame,text=("Obriši"),bg=BLUE,fg=YELLOW,activebackground=PLATINUM,font=("Helvetica",15),command=lambda i=i:deleteTermin(j,i),border=0,width=8)
            delTermin.grid(row=counter,column=6,padx=10,pady=10)
            counter+=1
        tableFrame.pack(anchor="center",pady=0)
        print("termin loaded")
        
    
    if tableFrame is not None:
        tableFrame.destroy()
    if frame is not None:
        frame.destroy()   
    tableFrame=tk.Frame(bg=PLATINUM) 
    frame=tk.Frame(bg=PLATINUM)   
    sledecasala()
    sledecaSala=tk.Button(frame,text="Sledeća sala",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=sledecasala,activebackground=BLUE,activeforeground=YELLOW) 
    sledecaSala.pack(side="bottom",pady=10,padx=10)
    tableFrame.pack(anchor="center")
    frame.pack(side="bottom",anchor="center",pady=10,padx=10)
    
def modifikujprofil():
    global frame
    global un
    global pw
    global tableFrame
    global password
    global username
    def forNow():
        global password
        global username
        global currentUser
        global un
        global pw
        pswd=pw.get()
        usnm=un.get()
        if(pswd=="" or usnm==""):
            tkinter.messagebox.showerror("Error","Morate uneti sve podatke")
        elif(len(pswd)<6 or len(usnm)<6):   #mora biti 8 ili vece
            tkinter.messagebox.showerror("Error","Korisničko ime i lozinka moraju imati minimalno 6 karaktera")
        else:
            currentUser.promeniLozinku(pswd)
            currentUser.promeniUsername(usnm)
            password.set(pswd)
            username.set(usnm)
            un.set(usnm)
            pw.set(pswd)
            tkinter.messagebox.showinfo("Uspeh","Uspešno ste izmenili podatke")
        
    if tableFrame is not None:
        tableFrame.destroy()
    if frame is not None:
        frame.destroy()
    un=tk.StringVar()
    pw=tk.StringVar()    
    tableFrame=tk.Frame(bg=PLATINUM)
    tk.Label(tableFrame,text="Lozinka:",justify='center',bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=0,columnspan=1,sticky="w",pady=20)
    pw1=tk.Entry(tableFrame,width=15,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,textvariable=pw,justify="center")
    pw1.grid(row=0,column=1,columnspan=3,pady=20)    #dodaj da moze da se bira show="*" ili ne
    pw1.insert(0,password.get())
    tk.Label(tableFrame,text="Korisničko ime:",justify='center',bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=2,column=0,columnspan=1,sticky="w",pady=20)
    un1=tk.Entry(tableFrame,width=15,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,textvariable=un,justify="center")
    un1.grid(row=2,column=1,columnspan=3,pady=20)
    un1.insert(0,username.get())
    tableFrame.pack(anchor="center")
    tk.Button(tableFrame,text="Potvrdi",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=forNow,activebackground=BLUE,activeforeground=YELLOW).grid(row=4,column=0,columnspan=3,pady=40)

    
def mainmenu():     
    global i
    global currentUser
    i=-1
    global frame
    global tableFrame   
    frame=None
    tableFrame=None
    def infoAndExecute():
        global nazivFilma
        global trajanje
        if(nazivFilma.get()==""):
            tkinter.messagebox.showinfo("Greška","Niste uneli sve podatke")
        else:
            if(False):  #izbrisi
                tkinter.messagebox.showinfo("Greška","Trajanje filma mora biti broj")
            else:
                noviFilm=Film(nazivFilma.get())
                if noviFilm.check==False:
                    tkinter.messagebox.showinfo("Greška","Ovaj film već postoji u bazi")
                else:
                    currentUser.dodajOvajFilm(noviFilm)
                    tkinter.messagebox.showinfo("Uspešno","Uspešno ste dodali film "+nazivFilma.get())
    def dodajfilm():
        global frame
        global tableFrame
        global trajanje
        global nazivFilma
        if tableFrame is not None:
            tableFrame.destroy()
        if frame is not None:
            frame.destroy()
        frame=tk.Frame(bg=PLATINUM)
        nazivFilma=tk.StringVar()
        unetiNaziv=tk.StringVar()
        unetiNaziv.set("Uneti naziv filma")
        imeDir=tk.Label(frame, textvariable=unetiNaziv, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
        imeDir.pack(side="top", fill="x", pady=10)
        nazivField=tk.Entry(frame,width=35,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,textvariable=nazivFilma,justify="center")
        nazivField.pack(anchor="center",pady=0,ipadx=10,ipady=5)
        

        proceed=tk.Button(frame,text="Dodaj",width=10,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,command=infoAndExecute,border=0)
        proceed.pack(anchor="center",pady=30,ipadx=2,ipady=5)
        tmpLabel=tk.Label(frame,text="Obrada zahteva može trajati i do 30 sekundi.",justify='center',bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).pack(anchor="s",pady=20,ipadx=10,ipady=5,side="bottom")
        frame.pack(anchor="center", fill = "x", expand = True)
    
    def dodajtermin():#stavi da se tek naknadno dodaje termin!!!!
        
        def nastavi(id1,id2):
            acceptable_timeframes=["09:00","12:00","15:00","18:00","21:00","00:00","03:00"]
            global currentUser
            global i
            global frame
            global tableFrame
            if tableFrame is not None:
                tableFrame.destroy()
            if frame is not None:
                frame.destroy()
            tableFrame=tk.Frame(bg=PLATINUM)
            
            df=pd.read_csv("data/termini.txt",sep=" ",header=None)
            df.columns=["Sala","Film","Vreme","SlobMesta"]

            inuse_termini=df.loc[df["Sala"]==int(id1),"Vreme"].tolist()
            slob_termini=list(set(acceptable_timeframes)-set(inuse_termini))
            slob_termini.sort()
            value_inside3 = tk.StringVar()
            value_inside3.set(slob_termini[0])
            tk.Label(tableFrame,text="Izabrati vreme prikazivanja",justify='center',bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=2,column=0,columnspan=1,sticky="w",pady=20)
            termin_menu=tk.OptionMenu(tableFrame,value_inside3,*slob_termini)
            termin_menu["menu"].config(bg=PLATINUM,fg=YELLOW,font=("Helvetica",15))
            termin_menu.config(width=6,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,activebackground=BLUE,activeforeground=YELLOW,highlightcolor=YELLOW,highlightbackground=BLUE)
            termin_menu.grid(row=2,column=1,columnspan=3,pady=20)
            chck=tk.Button(tableFrame,text="Potvrdi",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=lambda:nastavi2(id1,id2,value_inside3.get()),activebackground=BLUE,activeforeground=YELLOW)
            chck.grid(row=4,column=1,columnspan=3,pady=40)
            tableFrame.pack(anchor="center")
            
        def nastavi2(id1,id2,id3):
            global currentUser
            tableFrame=tk.Frame(bg=PLATINUM)
            idF=Film.naOsnovuNaziva(id2)

            idS=id1
            idS=int(idS)

            broj_mesta=BioskopskaSala.vratiBrojMesta(idS)
            biosala=BioskopskaSala(broj_mesta,idS)
            termin=Termin(idF,id3)
            biosala.addTermin(termin)
            tkinter.messagebox.showinfo("Uspešno","Uspešno ste dodali termin")
            
        global frame
        global tableFrame
        global trajanje
        global nazivFilma
        if tableFrame is not None:
            tableFrame.destroy()
        if frame is not None:
            frame.destroy()
        tableFrame=tk.Frame(bg=PLATINUM)
        df=pd.read_csv("data/bioskopskasala.txt",sep=" ",header=None)
        options1=df[0].tolist()

        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        options2=df[1].tolist() #ime filma da se bira

        tk.Label(tableFrame,text="Izabrati broj sale",justify='center',bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=0,columnspan=1,sticky="w",pady=20)
        value_inside = tk.StringVar()
        value_inside.set("1")
        sala_menu = tk.OptionMenu(tableFrame, value_inside, *options1)
        sala_menu["menu"].config(bg=PLATINUM,fg=YELLOW,font=("Helvetica",15))
        sala_menu.config(width=2,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,activebackground=BLUE,activeforeground=YELLOW)
        sala_menu.grid(row=0,column=1,columnspan=3,pady=20)
        value_inside2 = tk.StringVar()
        value_inside2.set(options2[0])
        tk.Label(tableFrame,text="Izabrati ime filma",justify='center',bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=0,columnspan=1,sticky="w",pady=20)
        film_menu=tk.OptionMenu(tableFrame,value_inside2,*options2)
        film_menu["menu"].config(bg=PLATINUM,fg=YELLOW,font=("Helvetica",15))
        film_menu.config(width=20,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,activebackground=BLUE,activeforeground=YELLOW)
        film_menu.grid(row=1,column=1,columnspan=3,pady=20)
        
        nastaviKaTerminima=tk.Button(tableFrame,text="Nastavi",width=10,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,command=lambda:nastavi(value_inside.get(),value_inside2.get()),border=0)
        nastaviKaTerminima.grid(row=2,column=1,columnspan=3,pady=20)
        tableFrame.pack(anchor="center")    #staviti da se tek naknadno dodaje termin!!!
    def pregledfilmova():
        global frame
        global tableFrame
        global naz
        global tra
        global ajdi
        global ocene
        if frame is not None:
            frame.destroy()
        global i
        def showMovie():
            global frame
            global naz
            global tra
            global ajdi
            global ocene
            global i
            global tableFrame
            temp=pd.read_csv("data/film.txt",sep=" ",header=None)
            temp.columns=["id","naziv","trajanje","ocena"]  #moze ovako a i ne mora, moze preko objekta
            if(i>=temp.shape[0]-1):
                i=0
            else:
                i+=1
            temp=temp.loc[[i]]
            row=temp.iloc[0]
            trenutniFilm=Film(row["naziv"])
            l1=tk.StringVar()
            l1.set(row["naziv"])
            l2=tk.StringVar()
            l2.set(row["trajanje"])
            l0=tk.StringVar()
            l0.set(row["id"])
            l3=tk.StringVar()
            l3.set(row["ocena"])
            naz.config(textvariable=l1)
            tra.config(textvariable=l2)
            #ajdi.config(textvariable=str(l0)+"/"+str(temp.shape[0]))
            ajdi.config(textvariable=l0)
            ocene.config(textvariable=l3)
            ajdi.grid(row=1,column=0,columnspan=1,padx=10,pady=10,rowspan=2)
            naz.grid(row=1,column=2,columnspan=1,padx=10,pady=10,rowspan=2)
            tra.grid(row=1,column=4,columnspan=1,padx=10,pady=10,rowspan=2)
            ocene.grid(row=1,column=6,columnspan=1,padx=10,pady=10,rowspan=2)
            pustiklip=tk.Button(tableFrame,text="Pusti trejler",width=10,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,activebackground=BLUE,activeforeground=YELLOW,command=lambda:pustiKlip(i))
            delFilm=tk.Button(tableFrame,text="Obriši",width=10,height=2,font=("Helvetica",15),bg=BLUE,fg=YELLOW,activebackground=YELLOW,activeforeground=BLUE,border=0,command=lambda:obrisiFilm(i))
            pustiklip.grid(row=1,column=7,columnspan=1,padx=10,pady=10)           
            delFilm.grid(row=2,column=7,columnspan=1,padx=10,pady=10)
            tableFrame.pack(anchor="center",pady=10,padx=80)
        
        def pustiKlip(id):
            global naz
            url=Film.generisiTrejler(id)
            webbrowser.open(url)
            
        def obrisiFilm(id1):
            global frame
            global tableFrame
            df=pd.read_csv("data/film.txt",sep=" ",header=None)
            df.columns=["id","naziv","trajanje","ocena"]
            tkinter.messagebox.showinfo("Uspešno","Uspešno ste obrisali film "+str(df.loc[df.index==id1,"naziv"].values[0])+" iz baze podataka")
            df= df.loc[df.index != id1]
            
            df.reset_index(drop=True,inplace=True)
            df.to_csv("data/film.txt",sep=" ",header=None,index=False)
            termini=pd.read_csv("data/termini.txt",sep=" ",header=None)
            termini.columns=["idS","idF","vreme","bSMesta"]
            termini=termini.loc[termini["idF"]!=id1]
            termini.reset_index(drop=True,inplace=True)
            termini.to_csv("data/termini.txt",sep=" ",header=None,index=False)
            showMovie()
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]

        if frame is not None:
            frame.destroy()
        if tableFrame is not None:
            tableFrame.destroy()
        tableFrame=tk.Frame(bg=PLATINUM)
        tk.Label(tableFrame,text="ID",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=0,padx=10,pady=10)
        tk.Label(tableFrame,text="Naziv",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=2,padx=10,pady=10)
        tk.Label(tableFrame,text="Trajanje",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=4,padx=10,pady=10)
        tk.Label(tableFrame,text="Ocena",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=6,padx=10,pady=10)
        tk.Label(tableFrame,text="Opcije",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=0,column=7,padx=10,pady=10)
        ajdi=tk.Label(tableFrame,height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
        naz=tk.Label(tableFrame, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
        tra=tk.Label(tableFrame, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
        ocene=tk.Label(tableFrame, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
        showMovie()
        next=tk.Button(tableFrame,text="Sledeći",width=10,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,activebackground=BLUE,activeforeground=YELLOW,border=0,command=lambda:showMovie())
        next.grid(row=5,column=2,columnspan=5,rowspan=3,padx=10,pady=60)
        
        
        
    global username
    ime=existingLogs[existingLogs["username"]==username.get()]["ime"].values[0]
    
    menu=tk.Tk()
    greeter=tk.StringVar()
    greeter.set("Dobrodošli, "+ ime+"!")
    menu.title("Glavni meni")
    menu.config(bg=PLATINUM)
    menu.geometry("1080x720")
    menu.resizable(height = None, width = None)
    frame1=tk.Frame(menu,bg=BLUE)
    frame1.rowconfigure(2)
    frame1.columnconfigure(2)
    e11=tk.Button(frame1,text="Dodaj film",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=dodajfilm,activebackground=BLUE,activeforeground=YELLOW)
    e12=tk.Button(frame1,text="Pregled filmova",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=pregledfilmova,activebackground=BLUE,activeforeground=YELLOW)
    e13=tk.Button(frame1,text="Pregled sala",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=pregledsala,activebackground=BLUE,activeforeground=YELLOW)
    e14=tk.Button(frame1,text="Dodaj termin",width=15,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,command=dodajtermin,activebackground=BLUE,activeforeground=YELLOW)
    e19=tk.Button(frame1,text="Modifikuj profil",width=15,height=2,font=("Helvetica",15),bg=BLUE,fg=YELLOW,border=0,command=modifikujprofil,activebackground=BLUE,activeforeground=PLATINUM)
    frame1.pack(side="left",fill="y")
    separator = ttk.Separator(menu, orient='vertical')
    e11.grid(row = 0, column = 1, pady = 10,padx=10)
    e12.grid(row = 1, column = 1, pady = 10,padx=10)
    e13.grid(row = 2, column = 1, pady = 10,padx=10)
    e14.grid(row = 3, column = 1, pady = 10,padx=10)
    e19.grid(row = 5, column = 1, pady = 20,padx=10)
    separator.pack(side="left", fill="y")
    
    frame2=tk.Frame(menu,bg=PLATINUM)
    e21=tk.Label(frame2,width=15,height=2,font=("Helvetica",20),bg=PLATINUM,fg=BLUE,border=0,textvariable=greeter,justify="center")
    e21.pack(side="top",fill="x",pady=10)
    frame2.pack(side="top",fill="x")
    menu.mainloop()
    
    
    
def main():
    registration()
    
    
if __name__ == "__main__":
    main()

