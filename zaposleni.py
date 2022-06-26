import pandas as pd
from osoba import Osoba
from film import Film
from korisnik import Korisnik   #dodati da se nakon init dodaje u sviKorisnici takodje
class Zaposleni(Korisnik):
    

    def __init__(self, ime, prezime,username,password): #konstruktor
        temp=Osoba(ime,prezime,username,password,isIt="log")
        self.id=temp.id
        self.im=temp.im
        self.prez=temp.prez
        self.username=temp.username
        self.password=temp.password

    def exportZaposleni(self):
        with open("data/zaposleni.txt","a") as f:
            f.write(str(self.id)+" "+self.ime+" "+self.prezime+" "+self.username+" "+self.password+"\n")
            f.close()
        kor=Korisnik(self.username,self.password,self.ime,self.prezime)
        kor.exportKorisnik()    
        
    def dodajOvajFilm(self,film):  #dodavanje novog filma
        film.export()
        with open("data/loggedInfos.txt","a") as f:
            f.write(str(self.id)+" "+str(film.id)+" "+"D"+"\n")
            f.close()
        
    def izbrisiOvajFilm(self,film): #brisanje filma
        film.izbrisiFilm()
        with open("data/loggedInfos.txt","a") as f:
            f.write(str(self.id)+" "+str(film.id)+" "+"I"+"\n")
            f.close()
    
    def promeniLozinku(self,password):
        df=pd.read_csv("data/zaposleni.txt",sep=" ",header=None)
        df.columns=["id","ime","prezime","username","password"]
        df.loc[df['id']==self.id,"password"]=password
        df.to_csv("data/zaposleni.txt",sep=" ",header=None,index=False)  
        
        df=pd.read_csv("data/sviKorisnici.txt",sep=" ",header=None)
        df.columns=["id","ime","prezime","username","password"]
        df.loc[df['id']==self.id,"password"]=password
        df.to_csv("data/sviKorisnici.txt",sep=" ",header=None,index=False)  
        
    def promeniUsername(self,username):
        df=pd.read_csv("data/zaposleni.txt",sep=" ",header=None)
        df.columns=["id","ime","prezime","username","password"]
        df.loc[df['id']==self.id,"username"]=username
        df.to_csv("data/zaposleni.txt",sep=" ",header=None,index=False)
           
        df=pd.read_csv("sviKorisnici.txt",sep=" ",header=None)
        df.columns=["id","ime","prezime","username","password"]
        df.loc[df['id']==self.id,"username"]=username
        df.to_csv("data/sviKorisnici.txt",sep=" ",header=None,index=False) 
        
           
        
def main():
    o1=Zaposleni("djordje","karisic","djordje34","karisic34","log")
    o2=Zaposleni("pera","peric","pera","pera");
    f1=Film("Guardians of The Galaxy II",120)
    o2.dodajOvajFilm(f1)
    x=input()
    o2.izbrisiOvajFilm(f1)
    o1.printer()
    o2.printer()
    
    
    
if __name__ == "__main__":
    main()