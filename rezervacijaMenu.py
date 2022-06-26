from datetime import datetime
import os
import re
import smtplib
import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
import pandas as pd
from sqlalchemy import true
from film import Film
from tkinter import ttk
from tkinter.simpledialog import askstring
YELLOW="#E7BB41"
GREY="#393E41"
LIGHT_GREY="#D3D0CB"
PLATINUM="#E7E5DF"
BLUE="#44BBA4"

os.environ['TWILIO_ACCOUNT_SID']="AC097502c04788730f9662ac4cfbb1e429"
os.environ['TWILIO_AUTH_TOKEN']="18e9396b47e6c97819586cd29522a656"
class Rezervacija:
    def resetMainFrame(self):
        if self.mainframe!=None:
            self.mainframe.destroy()
            self.mainframe=tk.Frame(self.root, bg=PLATINUM)
            
    def __init__(self,id,currentUser):  #MORA I KORISNIK DA SE STAVI
        def on_closing():
            self.root.destroy()
        self.user=currentUser    
        self.id=id    
        self.root=tk.Toplevel()
        self.mainframe=tk.Frame(self.root, bg=PLATINUM)
        self.root.title("Rezervacija")
        self.root.geometry("1080x720")
        self.root.resizable(height = None, width = None)
        self.root.config(bg=PLATINUM)        
        self.root.columnconfigure(4, minsize=4)
        self.termini=pd.read_csv("data/termini.txt",sep=" ",header=None)
        movie=Film.naOsnovuIndeksa(self.id)
        self.nazivFilma=movie[1]
        self.termini.columns=["idS","idF","vreme","brojSMesta"]
        self.termini=self.termini.loc[self.termini["idF"]==movie[0]]
        self.termini=self.termini.loc[self.termini["brojSMesta"]>0]
        self.noOf=len(self.termini.index)
        if self.noOf==0:
            messagebox.showinfo("Greška","Nema slobodnih termina za ovaj film.")
            self.root.destroy()
        self.updatePage()
        self.mainframe.pack(side="top",anchor="n",pady=10)
        self.root.mainloop()  
    def faultyCheckItems(self):    
        self.termini=pd.read_csv("data/termini.txt",sep=" ",header=None)
        movie=Film.naOsnovuIndeksa(self.id)
        self.nazivFilma=movie[1]
        self.termini.columns=["idS","idF","vreme","brojSMesta"]
        self.termini=self.termini.loc[self.termini["idF"]==movie[0]]
        self.termini=self.termini.loc[self.termini["brojSMesta"]>0]
        self.noOf=len(self.termini.index)
        
    def rezervisi(self,idS,idF,vreme,brojSMesta):
        print(idS,idF,vreme,brojSMesta)
        def confirm(idS,idF,vreme,brojSMesta,bMesta):
            print(bMesta)
            
            df=pd.DataFrame(columns=["idU","tel"])
            df=pd.read_csv("data/telefon.txt",sep=" ",header=None)
            
            if df.empty or df.loc[df[0]==self.user.id].empty:
                regex =r"\+?\d+"
                prompt = askstring("Unos broja telefona", "Unesite Vaš broj telefona")
                if(re.fullmatch(regex, prompt)):
                    df.loc[len(df)]=[self.user.id,prompt]
                    df.to_csv("data/telefon.txt",sep=" ",header=None,index=False)
                else:
                    messagebox.showinfo("Greška","Broj nije validan.")
                    self.root.destroy() 
            elif not df.loc[df[0]==self.user.id].empty:

                prompt=str(df.loc[df[0]==self.user.id][1].values[0])
            mov=pd.read_csv("data/film.txt",sep=" ",header=None)
            imeF=mov.loc[mov[0]==idF][1].values[0]
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            splitTime=vreme.split(":")
            fullTime=''.join([str(x) for x in splitTime])
            client = Client(account_sid, auth_token)
            genCode=str(self.user.id)+str(idS)+str(idF)+str(vreme).split(":")[0]+str(vreme).split(":")[1]+str(brojSMesta)+str(bMesta)+str(fullTime)
            mess="\nPozdrav, "+str(bMesta) +" mesta za film "+str(imeF)+" u terminu "+str(vreme)+" su uspešno rezervisana.\nVaš jedinstveni kod rezervacije: "+genCode
            
            message = client.messages \
                            .create(
                                body=mess,
                                from_='+18782167408',
                                to='+'+prompt
                            )

            print(message.sid)

                
                
                
            tempT=pd.read_csv("data/termini.txt",sep=" ",header=None)
            tempT.columns=["idS","idF","vreme","brojSMesta"]
            print(tempT.loc[(tempT["idS"]==idS) & (tempT["idF"]==idF) & (tempT["vreme"]==vreme),"brojSMesta"].values[0])
            tempT.loc[(tempT["idS"]==idS) & (tempT["idF"]==idF) & (tempT["vreme"]==vreme),"brojSMesta"]-=int(bMesta)
            tempT.to_csv("data/termini.txt",sep=" ",header=None,index=False)
            self.saveReservation(idS,idF,vreme,bMesta)
            messagebox.showinfo("Uspešno","Uspešno ste rezervisali {bMesta} mesta.".format(bMesta=bMesta))
            self.updatePage()
            temp.destroy()
        valSetter= lambda brojSMesta:10 if brojSMesta>=10 else brojSMesta
        x=valSetter(brojSMesta)
        
        df=pd.read_csv("data/reservationInfos.txt",sep=" ",header=None)
        df.columns=["idU","idS","idF","vreme","bMesta"]
        isInThere=df.loc[(df["idU"]==self.user.id)&(df["idS"]==idS)&(df["idF"]==idF)&(df["vreme"]==vreme)]
        if not isInThere.empty:
            already=isInThere["bMesta"].sum()
            x=10-isInThere["bMesta"].values[0]
            if x==0:
                messagebox.showinfo("Greška","Već ste rezervisali maksimalno mesta")
                self.root.destroy()
        temp=tk.Toplevel()
        temp.title("Rezervacija")
        temp.config(bg=PLATINUM,padx=10,pady=10)
        nums=[x for x in range(1,x+1)]
        val=tk.StringVar()
        val.set(nums[0])
        tk.Label(temp,text="Izaberite broj mesta",bg=PLATINUM,font="Helvetica 15",fg=YELLOW).pack(side="top",anchor="n",pady=10,padx=10)
        howmany=tk.OptionMenu(temp,val,*nums)
        howmany["menu"].config(bg=PLATINUM,fg=YELLOW,font=("Helvetica",15))
        howmany.config(width=20,height=2,font=("Helvetica",15),bg=YELLOW,fg=BLUE,border=0,activebackground=BLUE,activeforeground=YELLOW)
        howmany.pack(side="top", anchor="n", pady=10)
        confirmB=tk.Button(temp,text="Potvrdi",command=lambda:confirm(idS,idF,vreme,brojSMesta,val.get()),bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        confirmB.pack(side="bottom", anchor="s", pady=20)
        temp.mainloop()
    def updatePage(self):
        
        def showNextPage():
            self.resetMainFrame()
            if self.pageCounter*6<=self.noOf:
                self.pageCounter+=1
            else:
                self.pageCounter=1
            self.updatePage()
        
        self.resetMainFrame()
        self.faultyCheckItems()
        sala=pd.read_csv("data/bioskopskasala.txt",sep=" ",header=None)
        sala.columns=["idS","brojMesta"]

        self.pageCounter=1
        tk.Label(self.mainframe,text=self.nazivFilma,bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=0,column=0,padx=10,pady=10,columnspan=5)
        tk.Label(self.mainframe,text="Broj sale",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=0,padx=10,pady=10,columnspan=1)
        tk.Label(self.mainframe,text="Vreme početka",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=1,padx=10,pady=10,columnspan=1)
        tk.Label(self.mainframe,text="Ukupan kapacitet sale",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=2,padx=10,pady=10,columnspan=1)
        tk.Label(self.mainframe,text="Broj slobodnih mesta",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=3,padx=10,pady=10,columnspan=1)
        tk.Label(self.mainframe,text="Opcije",bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=1,column=4,padx=10,pady=10,columnspan=1)
        for i in range((self.pageCounter-1)*6,self.pageCounter*6):
            if i<self.noOf:
                tk.Label(self.mainframe,text=self.termini["idS"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=0,padx=10,pady=10)
                tk.Label(self.mainframe,text=self.termini["vreme"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=1,padx=10,pady=10)
                tk.Label(self.mainframe,text=sala.loc[sala["idS"]==self.termini["idS"].values[i],"brojMesta"].values[0],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=2,padx=10,pady=10)
                tk.Label(self.mainframe,text=self.termini["brojSMesta"].values[i],bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=i+2,column=3,padx=10,pady=10)
                rez=tk.Button(self.mainframe,text="Rezerviši",command=lambda i=i: self.rezervisi(self.termini["idS"].values[i],self.termini["idF"].values[i],self.termini["vreme"].values[i],self.termini["brojSMesta"].values[i],),height=2,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
                rez.grid(row=i+2,column=4,padx=10,pady=10)
            tk.Label(self.mainframe,text="Strana "+str(self.pageCounter),bg=PLATINUM,fg=BLUE,font=("Helvetica",15)).grid(row=self.pageCounter*6+2,column=4,padx=10,pady=10,columnspan=1)
        slStrana=tk.Button(self.mainframe,text="Sledeca strana",height=2,command=showNextPage,bg=YELLOW,fg=BLUE,font=("Helvetica",15),border=0,activebackground=BLUE,activeforeground=YELLOW)
        slStrana.grid(row=self.pageCounter*6+2,column=0,padx=10,pady=10,columnspan=4)
        if self.pageCounter!=self.noOf//6+1:
            self.pageCounter+=1
        self.mainframe.pack(side="top",anchor="n",pady=10)
        
    def saveReservation(self,idS,idF,vreme,bMesta):
        
        df=pd.read_csv("data/reservationInfos.txt",sep=" ",header=None)
        df.columns=["idU","idS","idF","vreme","bMesta"]
        isInThere=df.loc[(df["idU"]==self.user.id)&(df["idS"]==idS)&(df["idF"]==idF)&(df["vreme"]==vreme)]

        if not isInThere.empty:

            df.loc[(df["idS"]==idS)&(df["idF"]==idF)&(df["vreme"]==vreme),"bMesta"]+=int(bMesta)

            df.to_csv("data/reservationInfos.txt",sep=" ",header=None,index=False)
        else:    
            with open("data/reservationInfos.txt","a") as f:
                f.write(str(self.user.id)+" "+str(idS)+" "+str(idF)+" "+str(vreme)+" "+str(bMesta)+"\n")
                f.close()  
        
        
def main():
    rezervacija=Rezervacija(1)
    
    
    
if __name__ == "__main__":
    main()