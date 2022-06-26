from cProfile import label
from email import message
import tkinter as tk
from matplotlib.pyplot import text
import pandas as pd
from tkinter import messagebox
import tkinter
YELLOW="#E7BB41"
GREY="#393E41"
LIGHT_GREY="#D3D0CB"
PLATINUM="#E7E5DF"
BLUE="#44BBA4"

def character_limit(text,x):
    if len(text.get()) > 0:
        text.set(text.get()[:x])

class adminMenu:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("Korisnički interfejs")
        self.mainframe=tk.Frame(self.root, bg=PLATINUM)
        self.menuframe=tk.Frame(self.root, bg=BLUE)
        self.root.config(bg=PLATINUM)
        self.root.geometry("1080x720")
        self.root.resizable(height = None, width = None)
        element1=tk.Button(self.menuframe,text="Pregledaj naloge",command=self.pregledajNaloge,height=2,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        element1.grid(row=0,column=0,padx=10,pady=10,ipadx=7)
        element3=tk.Button(self.menuframe,text="Dodaj novi nalog",command=self.dodajNalog,height=2,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        element3.grid(row=1,column=0,padx=10,pady=10,ipadx=7)
        element7=tk.Button(self.menuframe,text="Dodaj novu salu",height=2,command=self.dodajSalu,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        element7.grid(row=3,column=0,padx=10,pady=10,ipadx=12)
        self.menuframe.pack(side="left",fill="y")        
        self.mainframe.pack(side="top",fill="x")
        self.pageCounter=1
        nalozi=pd.read_csv("data/zaposleni.txt",sep=" ",header=None)
        self.noOfUsers=len(nalozi)
        self.root.mainloop()
        
    def resetMainFrame(self):
        self.mainframe.destroy()
        self.mainframe=tk.Frame(self.root, bg=PLATINUM) 
        
    def obrisiNalog(self,i):
        df=pd.read_csv("data/zaposleni.txt",sep=" ",header=None)
        svi=pd.read_csv("data/sviKorisnici.txt",sep=" ",header=None)
        df.columns=["ID","ime","prezime","username","password"]
        svi.columns=["ID","ime","prezime","username","password"]
        koji=df.loc[df.index==i,"ID"].values[0]
        df=df.loc[df.index!=i]
        svi=svi.loc[svi["ID"]!=koji]
        df.to_csv("data/zaposleni.txt",sep=" ",header=None,index=False)
        svi.to_csv("data/sviKorisnici.txt",sep=" ",header=None,index=False)
        
        self.noOfUsers-=1
        
        messagebox.showinfo("Uspešno","Nalog je uspešno obrisan")
        self.pregledajNaloge()
    def pregledajNaloge(self):
        
        def nextPage():

            self.resetMainFrame()
            if self.pageCounter*6<self.noOfUsers:
                self.pageCounter+=1
            else:
                self.pageCounter=1
            self.pregledajNaloge()
            
        self.resetMainFrame()
        
        nalozi=pd.read_csv("data/zaposleni.txt",sep=" ",header=None)
        nalozi.columns=["ID","ime","prezime","username","password"]
        tk.Label(self.mainframe,text="ID",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=0,padx=10,pady=10,ipadx=7)
        tk.Label(self.mainframe,text="Ime",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=1,padx=10,pady=10,ipadx=7)
        tk.Label(self.mainframe,text="Prezime",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=2,padx=10,pady=10,ipadx=7)
        tk.Label(self.mainframe,text="Username",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=3,padx=10,pady=10,ipadx=7)
        tk.Label(self.mainframe,text="Password",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=4,padx=10,pady=10,ipadx=7)
        tk.Label(self.mainframe,text="Opcije",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=5,padx=10,pady=10,ipadx=7)
        for i in range((self.pageCounter-1)*6,self.pageCounter*6):
            if i < self.noOfUsers:
                tk.Label(self.mainframe,text=nalozi.iloc[i][0],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+1,column=0,padx=10,pady=10,ipadx=7)
                tk.Label(self.mainframe,text=nalozi.iloc[i][1],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+1,column=1,padx=10,pady=10,ipadx=7)
                tk.Label(self.mainframe,text=nalozi.iloc[i][2],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+1,column=2,padx=10,pady=10,ipadx=7)
                tk.Label(self.mainframe,text=nalozi.iloc[i][3],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+1,column=3,padx=10,pady=10,ipadx=7)
                tk.Label(self.mainframe,text=nalozi.iloc[i][4],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+1,column=4,padx=10,pady=10,ipadx=7)
                obr=tk.Button(self.mainframe,text="Obriši",command=lambda i=i:self.obrisiNalog(i),height=2,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
                obr.grid(row=i+1,column=5,padx=10,pady=10,ipadx=7)
        slStrana=tk.Button(self.mainframe,text="Sledeca strana",height=2,command=nextPage,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        slStrana.grid(row=self.pageCounter*6+2,column=0,padx=10,pady=10,columnspan=4)
        self.mainframe.pack(side="top",fill="x")
        #prikazati korisnike po 6,7,8 po stranici
    
    def dodajNalog(self):
        def potvrdiNalog(ime,prezime,username,password):
            df=pd.read_csv("data/zaposleni.txt",sep=" ",header=None)
            svi=pd.read_csv("data/sviKorisnici.txt",sep=" ",header=None)
            df.columns=["ID","ime","prezime","username","password"]
            svi.columns=["ID","ime","prezime","username","password"]
            if username in svi["username"].values:
                messagebox.showinfo("Greška","Korisničko ime je zauzeto")
                return
            else:
                newID=svi["ID"].max()+1
                newElement=pd.DataFrame([[newID,ime,prezime,username,password]],columns=["ID","ime","prezime","username","password"])
                df=df.append(newElement)
                svi=svi.append(newElement)
                
                df.to_csv("data/zaposleni.txt",sep=" ",header=None,index=False)
                svi.to_csv("data/sviKorisnici.txt",sep=" ",header=None,index=False)
                messagebox.showinfo("Uspešno","Nalog je uspešno dodat")
                self.noOfUsers+=1
                self.dodajNalog()

            
        username=tk.StringVar()
        password=tk.StringVar()
        ime=tk.StringVar()
        prezime=tk.StringVar()
        username.trace("w", lambda *args: character_limit(username,15))
        password.trace("w", lambda *args: character_limit(password,15))
        ime.trace("w", lambda *args: character_limit(ime,13))  
        prezime.trace("w", lambda *args: character_limit(prezime,22))      
        self.resetMainFrame()
        tk.Label(self.mainframe,text="Ime",bg=PLATINUM,fg=BLUE,font=("Helvetica",15),).grid(row=0,column=0,padx=10,pady=10,ipadx=7)
        tk.Label(self.mainframe,text="Prezime",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=0,padx=10,pady=10,ipadx=7)
        tk.Label(self.mainframe,text="Username",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=2,column=0,padx=10,pady=10,ipadx=7)
        tk.Label(self.mainframe,text="Password",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=3,column=0,padx=10,pady=10,ipadx=7)
        
        imeU=tk.Entry(self.mainframe,bg="white",fg=BLUE,font=("Helvetica",15),border=0,textvariable=ime).grid(row=0,column=1,padx=10,pady=10,ipadx=7)
        prezimeU=tk.Entry(self.mainframe,bg="white",fg=BLUE,font=("Helvetica",15),border=0,textvariable=prezime).grid(row=1,column=1,padx=10,pady=10,ipadx=7)
        usernameU=tk.Entry(self.mainframe,bg="white",fg=BLUE,font=("Helvetica",15),border=0,textvariable=username).grid(row=2,column=1,padx=10,pady=10,ipadx=7)
        passwordU=tk.Entry(self.mainframe,bg="white",fg=BLUE,font=("Helvetica",15),border=0,textvariable=password).grid(row=3,column=1,padx=10,pady=10,ipadx=7)
        potvrda=tk.Button(self.mainframe,text="Potvrdi",command=lambda:potvrdiNalog(ime.get(),prezime.get(),username.get(),password.get()),height=2,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        potvrda.grid(row=4,column=1,padx=10,pady=10,ipadx=7,columnspan=2)
        self.mainframe.pack(fill="both",anchor="center")
        
        
    def dodajSalu(self):
        def dodajSaluConf(id,val):
            df=pd.read_csv("data/bioskopskasala.txt",sep=" ",header=None)
            df.columns=["ID","bMesta"]
            temp=pd.DataFrame([[id,val]],columns=["ID","bMesta"])
            df=df.append(temp)
            df.to_csv("data/bioskopskasala.txt",sep=" ",header=None,index=False)
            messagebox.showinfo("Uspešno","Sala broj "+str(id)+" je uspešno dodata")
            
        self.resetMainFrame()
        df=pd.read_csv("data/bioskopskasala.txt",sep=" ",header=None)
        df.columns=["ID","bMesta"]
        newID=df["ID"].max()+1    
        nm=tk.StringVar()
        tk.Label(self.mainframe,text="Dodavanje sale broj "+str(newID),bg=PLATINUM,fg=BLUE,font=("Helvetica",15),).grid(row=0,column=0,padx=10,pady=10,ipadx=7,columnspan=3,rowspan=2)
        tk.Label(self.mainframe,text="Broj mesta sale:",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=2,column=0,padx=10,pady=10,ipadx=7)
        unos=tk.Entry(self.mainframe,textvariable=nm,bg="white",fg=BLUE,font=("Helvetica",20),border=0,width=2)
        unos.grid(row=2,column=1,padx=10,pady=10,ipadx=7)
        conf=tk.Button(self.mainframe,text="Potvrdi",command=lambda:dodajSaluConf(newID,nm.get()),height=2,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        conf.grid(row=2,column=2,padx=10,pady=10,ipadx=7,columnspan=3)
        self.mainframe.pack()
        
def main():
    a=adminMenu()
    
    
if __name__=="__main__":
    main()