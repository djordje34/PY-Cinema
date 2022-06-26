import tkinter as tk
from tkinter import messagebox
from tkinter.font import BOLD
from numpy import isin
import pandas as pd
from tkinter import ttk
from film import Film
from movieInfoMenu import movieInfo
from rezervacijaMenu import Rezervacija
YELLOW="#E7BB41"
GREY="#393E41"
LIGHT_GREY="#D3D0CB"
PLATINUM="#E7E5DF"
BLUE="#44BBA4"

def findLongestTitle():
    df=pd.read_csv("data/film.txt",sep=" ",header=None)
    df.columns=["id","naziv","trajanje","ocena"]
    longestTitle=""
    for element in df["naziv"].values:
        if len(element)>len(longestTitle):
            longestTitle=element
    return len(longestTitle)

class KorisnickiInterfejs:

    def __init__(self, user):
        self.keyword=""
        self.pageCounter=1
        self.rezCounter=1
        self.user=user
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        self.noOfMovies=len(df[1].tolist())
        self.root = tk.Tk()
        greeter=tk.StringVar()
        greeter.set("Dobrodošli, "+user.im+"!")
        self.root.title("Korisnički interfejs")
        self.mainframe=tk.Frame(self.root, bg=PLATINUM)
        self.menuframe=tk.Frame(self.root, bg=BLUE)
        self.root.config(bg=PLATINUM)
        self.root.geometry("1080x720")
        self.root.resizable(height = None, width = None)
        w1=tk.Label(self.mainframe,width=15,height=2,font=("Helvetica",20,"bold"),bg=PLATINUM,fg=BLUE,border=0,textvariable=greeter,justify="center")
        w1.pack(side="top",fill="x")
        
        element1=tk.Button(self.menuframe,text="Pregled filmova",height=2,command=self.pregledFilmova,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        element1.grid(row=0,column=0,padx=10,pady=10)
        element3=tk.Button(self.menuframe,text="Moje rezervacije",command=self.mojeRezervacije,height=2,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        element3.grid(row=1,column=0,padx=10,pady=10)
        self.menuframe.pack(side="left",fill="y")        
        self.mainframe.pack(side="top",fill="x")
        self.root.mainloop()
    
    def resetMainFrame(self):
        if self.mainframe!=None:
            self.mainframe.destroy()
            self.mainframe=tk.Frame(self.root, bg=PLATINUM)
        
    def pregledFilm(self):   #izabrati film->prikazati dostupne termine->izabrati termin->izabrati broj mesta->mejl->rezervacija
        
        self.resetMainFrame()
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        sviF=df[1].tolist()
        value_inside = tk.StringVar()
        value_inside.set(sviF[0])
        tk.Label(self.mainframe,text="Izaberite film:",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=0,padx=10,pady=10)
        filmovi = tk.OptionMenu(self.mainframe, value_inside, *sviF)
        filmovi["menu"].config(bg=PLATINUM,fg=YELLOW,font=("Helvetica",15))
        filmovi.config(width=findLongestTitle(),height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,activebackground=BLUE,activeforeground=YELLOW,highlightcolor=YELLOW,highlightbackground=BLUE)
        filmovi.grid(row=0,column=1,padx=10,pady=10,columnspan=3)
        self.mainframe.pack(side="top",anchor="n",pady=10) 
        
    def pregledFilmova(self):
        def showNextPage():
            self.resetMainFrame()
            if self.pageCounter*6<=self.noOfMovies:
                self.pageCounter+=1
            else:
                self.pageCounter=1
            self.pregledFilmova()
            
        def searchRoutine():
            if self.pageCounter!=1:
                self.pageCounter=1
            self.keyword=keyw.get()
            self.pregledFilmova()    
        def pregledJednogFullInfo(i):
            newWind=movieInfo(i)
        self.resetMainFrame()
        keyw=tk.StringVar()
        keyw.set(self.keyword)
        if self.keyword=="":
            df=pd.read_csv("data/film.txt",sep=" ",header=None)
            self.noOfMovies=len(df[1].tolist())
            df.columns=["id","naziv","trajanje","ocena"]
        else:
            df=pd.read_csv("data/film.txt",sep=" ",header=None)
            df.columns=["id","naziv","trajanje","ocena"]
            df=df[df.apply(lambda row: row.astype(str).str.contains(self.keyword, case=False).any(), axis=1)]
            if len(df)==0:
                messagebox.showinfo("Info","Nema rezultata pretrage!")
                self.keyword=""
                self.pregledFilmova()
                return
        def pustiTrejlerZaFilm(i):
             Film.pustiTrejler(i)
        self.noOfMovies=len(df)
        pretraga=tk.Entry(self.mainframe,width=20,font=("Helvetica",20),bg=PLATINUM,fg=BLUE,highlightcolor=YELLOW,highlightbackground=BLUE,textvariable=keyw,border=0.5)
        pretraga.grid(row=0,column=0,padx=10,pady=10)
        pretrazi=tk.Button(self.mainframe,text="Pretraži",command=lambda:searchRoutine(),height=2,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        pretrazi.grid(row=0,column=1,padx=10,pady=10)
        tk.Label(self.mainframe,text="Naziv filma",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=0,padx=10,pady=10)
        tk.Label(self.mainframe,text="Trajanje",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=1,padx=10,pady=10)
        tk.Label(self.mainframe,text="Ocena",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=2,padx=10,pady=10)
        tk.Label(self.mainframe,text="Opcije",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=3,padx=10,pady=10,columnspan=3)
        for i in range((self.pageCounter-1)*6,self.pageCounter*6):
            if i<self.noOfMovies:
                tk.Label(self.mainframe,text=df["naziv"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=0,padx=10,pady=10)
                tk.Label(self.mainframe,text=df["trajanje"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=1,padx=10,pady=10)
                tk.Label(self.mainframe,text=df["ocena"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=2,padx=10,pady=10)
                trejler=tk.Button(self.mainframe,text="Trejler",height=2,command=lambda i=i: pustiTrejlerZaFilm(df.index[i]),bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
                trejler.grid(row=i+2,column=3,padx=10,pady=10)
                viseInfo=tk.Button(self.mainframe,text="Više informacija",height=2,command=lambda i=i: pregledJednogFullInfo(df.index[i]),bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
                viseInfo.grid(row=i+2,column=4,padx=10,pady=10)
                rezervisiMesto=tk.Button(self.mainframe,text="Rezerviši",height=2,command=lambda i=i: self.rezervisiMesto(df.index[i]),bg=BLUE,fg=YELLOW,font=("Helvetica",15),border=0,activebackground=YELLOW,activeforeground=BLUE)
                rezervisiMesto.grid(row=i+2,column=5,padx=10,pady=10)
            tk.Label(self.mainframe,text="Strana "+str(self.pageCounter),bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=self.pageCounter*6+2,column=4,padx=10,pady=10,columnspan=1)
        slStrana=tk.Button(self.mainframe,text="Sledeca strana",height=2,command=showNextPage,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        slStrana.grid(row=self.pageCounter*6+2,column=0,padx=10,pady=10,columnspan=4)
        self.mainframe.pack(side="top",anchor="n",pady=10)
        
    def rezervisiMesto(self,id):    
        ef=Rezervacija(id,self.user)
    
    def obrisiRezervaciju(self,i):
       
        rez=pd.read_csv("data/reservationInfos.txt",sep=" ",header=None)
        rez.columns=["idU","idS","idF","vreme","bMesta"]
        finalEl=rez        
        rez=rez.loc[rez["idU"]==self.user.id]        
        rez.reset_index(drop=True,inplace=True)
       
        el=rez.loc[rez.index==i]
       
        termin=pd.read_csv("data/termini.txt",sep=" ",header=None)
        termin.columns=["idS","idF","vreme","bSMesta"]
       
        idS1,idF1,vreme1=el["idS"].values[0],el["idF"].values[0],el["vreme"].values[0]

        termin.loc[((termin["idS"]==idS1)&(termin["idF"]==idF1)&(termin["vreme"]==vreme1)&(termin["bSMesta"]>-1)),"bSMesta"]+=int(el["bMesta"].values[0])
        termin.to_csv("data/termini.txt",sep=" ",header=None,index=False)

        finalEl.drop(finalEl.loc[(finalEl["idU"]==self.user.id) & (finalEl["idS"]==idS1) & (finalEl["idF"]==idF1) & (finalEl["vreme"]==vreme1)&(finalEl["bMesta"]>-1)].index,inplace=True)

        finalEl.to_csv("data/reservationInfos.txt",sep=" ",header=None,index=False)
        messagebox.showinfo("Obaveštenje","Uspešno ste obrisali rezervaciju!")
        self.mojeRezervacije()    
        
        
    def mojeRezervacije(self):
        self.resetMainFrame()
        
        allRes=pd.read_csv("data/reservationInfos.txt",sep=" ",header=None)
        allRes.columns=["idU","idS","idF","vreme","bMesta"]
        allRes=allRes.loc[allRes["idU"]==self.user.id]
        
        imeF=pd.read_csv("data/film.txt",sep=" ",header=None)
        imeF.columns=["id","naziv","trajanje","ocena"]
        imeF=imeF.loc[imeF["id"].isin(allRes["idF"])]

        self.noOfMovies=len(allRes)
        fin=allRes.merge(imeF,left_on="idF",right_on="id")
        fin=fin.drop_duplicates()
        fin.reset_index(inplace=True,drop=True)

        tk.Label(self.mainframe,text="Naziv filma",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=0,padx=10,pady=10)
        tk.Label(self.mainframe,text="Sala",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=1,padx=10,pady=10)
        tk.Label(self.mainframe,text="Vreme početka",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=2,padx=10,pady=10)
        tk.Label(self.mainframe,text="Broj rezervisanih mesta",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=3,padx=10,pady=10)
        tk.Label(self.mainframe,text="Opcije",bg=PLATINUM,fg=BLUE,font=("Helvetica",15,"bold")).grid(row=1,column=4,padx=10,pady=10)
        for i in range(self.noOfMovies):
            tk.Label(self.mainframe,text=fin["naziv"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=0,padx=10,pady=10)
            tk.Label(self.mainframe,text=fin["idS"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=1,padx=10,pady=10)
            tk.Label(self.mainframe,text=fin["vreme"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=2,padx=10,pady=10)
            tk.Label(self.mainframe,text=fin["bMesta"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=3,padx=10,pady=10)
            izb=tk.Button(self.mainframe,text="Obriši",height=2,command=lambda i=i: self.obrisiRezervaciju(fin.index[i]),bg=BLUE,fg=YELLOW,font=("Helvetica",15),border=0,activebackground=YELLOW,activeforeground=BLUE)
            izb.grid(row=i+2,column=4,padx=15,pady=10)
           
        
        
        
        self.mainframe.pack(side="top",anchor="n",pady=10)
        
def main():
    pass
        
if __name__ == '__main__':
    main()
    