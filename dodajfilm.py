import tkinter as tk
import tkinter.messagebox
from numpy import integer
import pandas as pd
from film import Film
global nazivFilma
global trajanje

YELLOW="#E7BB41"
GREY="#393E41"
LIGHT_GREY="#D3D0CB"
PLATINUM="#E7E5DF"
BLUE="#44BBA4"
class DodajFilm:
    
    def __init__(self):
        global nazivFilma
        global trajanje
        self.meni=tk.Tk()
        self.meni.title("Dodaj film")
        self.meni.config(bg=PLATINUM)
        self.meni.geometry("1080x720")
        self.meni.resizable(height = None, width = None)
        frame=tk.Frame(bg=PLATINUM)
        nazivFilma=tk.StringVar()
        trajanje=tk.StringVar()
        unetiNaziv=tk.StringVar()
        unetiNaziv.set("Uneti naziv filma")
        imeDir=tk.Label(frame, textvariable=unetiNaziv, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
        imeDir.pack(side="top", fill="x", pady=10)
        nazivField=tk.Entry(frame,width=35,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,textvariable=nazivFilma,justify="center")
        nazivField.pack(anchor="center",pady=0,ipadx=10,ipady=5)
        
        unetiT=tk.StringVar()
        unetiT.set("Uneti trajanje filma")
        usernameDir=tk.Label(frame, textvariable=unetiT, height=1,bg=PLATINUM,fg=BLUE,font=("Helvetica",15))
        usernameDir.pack(side="top", fill="x", pady=10)
        trajanjeField=tk.Entry(frame,width=5,font=("Helvetica",18),bg="#FFFFFF",fg=BLUE,border=0,textvariable=trajanje,justify="center")
        trajanjeField.pack(anchor="center",pady=0,ipadx=10,ipady=5)
        proceed=tk.Button(frame,text="Dodaj",width=10,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,command=self.infoAndExecute,border=0)
        proceed.pack(anchor="center",pady=30,ipadx=2,ipady=5)
        
        ret=tk.Button(frame,text="Nazad",width=10,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,command=self.returnToAnotherWindow,border=0)
        ret.pack(anchor="center",pady=30,ipadx=2,ipady=5)
        frame.pack(anchor="center", fill = "x", expand = True)
        self.meni.mainloop()
        
        
    def infoAndExecute(self):
        global nazivFilma
        global trajanje
        if(trajanje.get()=="" or nazivFilma.get()==""):
            tkinter.messagebox.showinfo("Greška","Niste uneli sve podatke")
        else:
            if(trajanje.get().isdigit()==False):
                tkinter.messagebox.showinfo("Greška","Trajanje filma mora biti broj")
            else:
                temp=Film(nazivFilma.get(),trajanje.get())
                tkinter.messagebox.showinfo("Uspešno","Uspešno ste dodali film "+nazivFilma.get())
        print(nazivFilma.get(),trajanje.get())
            
    def returnToAnotherWindow(self):
        self.meni.destroy()             #dodati dugme za nazad!
        mainmenu()
def main():
    DodajFilm()
    
           
if __name__ == '__main__':
    main()
    
    
