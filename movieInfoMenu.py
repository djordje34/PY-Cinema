import base64
from sys import maxsize
from tkinter import ttk
import turtle
from urllib.request import urlopen
import pandas as pd
import tkinter as tk
from film import Film
from PIL import Image,ImageTk
from io import BytesIO
YELLOW="#E7BB41"
GREY="#393E41"
LIGHT_GREY="#D3D0CB"
PLATINUM="#E7E5DF"
BLUE="#44BBA4"
class movieInfo:
    def __init__(self, id):
        def on_closing():
            self.root.destroy()
        self.root=tk.Toplevel()
        self.root.title("Dodatne informacije o filmu")
        self.root.geometry("1080x720")
        self.root.resizable(height = None, width = None)
        self.root.config(bg=PLATINUM)        
        self.root.columnconfigure(4, minsize=4)
        df=Film.naOsnovuIndeksa(id)
        allItems=Film.getAllIMDBStuff(df[1])
        self.plot=allItems[3]
        self.ocena=allItems[0]
        self.trajanje=allItems[1]
        self.zanr=allItems[2]
        self.reziser=allItems[4]
        self.glumac=allItems[5]
        #tk.Label(self.root,text="Naziv filma",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=1,padx=10,pady=10)
        tk.Label(self.root,text="Ocena",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=1,padx=10,pady=10)
        tk.Label(self.root,text="Trajanje (min)",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=2,padx=10,pady=10)
        tk.Label(self.root,text="Žanr(ovi)",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=3,padx=10,pady=10)  
        tk.Label(self.root,text="Plot",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=3,column=2,padx=10,pady=10,columnspan=2)
        tk.Label(self.root,text="Režiser",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=4,padx=10,pady=10)
        tk.Label(self.root,text="Glavna uloga",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=5,padx=10,pady=10)
        tk.Label(self.root,text=Film.getImefromInd(id),bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=3,column=0,padx=10)
        tk.Label(self.root,text=allItems[0],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=1,padx=10)  
        tk.Label(self.root,text=allItems[1],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=2,padx=10)
        tk.Label(self.root,text=allItems[2],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=3,padx=10)
        tk.Label(self.root,text=allItems[6],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=4,padx=10)
        tk.Label(self.root,text=allItems[5],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=5,padx=10)
        text=tk.Text(self.root,bg=PLATINUM,fg=BLUE,font=("Helvetica",15),width=36,height=6,wrap=tk.WORD,border=0)
        text.insert(tk.END,self.plot)
        text.grid(row=4,column=2,padx=10,pady=10,columnspan=2)
        text.config(state=tk.DISABLED)
        URL = allItems[4]


        u = urlopen(URL)
        raw_data = u.read()
        u.close()

        im = Image.open(BytesIO(raw_data))
        im = im.resize((192,256), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        label = tk.Label(self.root,image=photo)
        #label.image = photo
        label.grid(row=0,column=0,rowspan=3,padx=10)
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()
        

def main():
    a=movieInfo(7)
    print(a.plot)
    
    
if __name__=="__main__":
    main()