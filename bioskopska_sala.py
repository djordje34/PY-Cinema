import pandas as pd
from termin import Termin
from film import Film
class BioskopskaSala:       
    with open("data/salaCounter.txt","r+") as f:
        counter=int(f.readline())
        f.close()    
        
        
    def __init__(self,mesta,id=-1):   #staviti da je razmak izmedju filmova uvek isti ako moze
        self.termini=[]             #ukupno mesta u sali
        self.mesta=mesta
        if id==-1:
            self.id=BioskopskaSala.counter
            BioskopskaSala.counter+=1
            with open("data/salaCounter.txt","a") as f:
                f.truncate(0)       
                f.write(str(BioskopskaSala.counter))
                f.close()
        else:
            self.id=id
        
    def addNewSala(self):
        terminiStr=','.join(str(x) for x in self.termini)
        print(terminiStr)
        with open("data/bioskopskasala.txt","a") as f:
            f.write(str(self.id)+" "+str(self.mesta)+"\n")
            f.close()
    
    def addTermin(self,termin):
        termin.mesta=self.mesta
        self.termini.append(termin)

        with open("data/termini.txt","a") as f:
            f.write(str(self.id) +" "+str(termin.filmid)+" "+str(termin.kad)+" "+str(termin.mesta)+"\n")
            f.close()
            
    def returnAllSale():
        df=pd.read_csv("data/bioskopskasala.txt",sep=" ",header=None)            
        df.columns=["id","mesta"]
        return df    
        
    def loadSala(id):
        df=pd.read_csv("data/bioskopskasala.txt",sep=" ",header=None)
        df.columns=["id","mesta"]
        df=df.loc[df.index==id]
        print(df)
        return BioskopskaSala(df["mesta"].values[0],id)
    
    def vratiTermine(self):
        df=pd.read_csv("data/termini.txt",sep=" ",header=None)
        df.columns=["id","filmid","kad","mesta"]
        df=df.loc[df['id']==self.id]
        print(df)
        return df

    def vratiBrojMesta(id):
        df=pd.read_csv("data/bioskopskasala.txt",sep=" ",header=None)
        df.columns=["id","mesta"]
        df=df.loc[df["id"]==int(id)]
        print(df)
        return df["mesta"].values[0]
            
def vratiFilmPoID(id):
    df=pd.read_csv("data/film.txt",sep=" ",header=None)
    df.columns=["id","naziv","trajanje","ocena"]
    for i in range(len(df)):
        if df.iloc[i,0]==id:
            return Film(df.iloc[i,1])     
        
def main():
    film1=vratiFilmPoID(76)  #izabere se film, i vreme pocetka
    film2=vratiFilmPoID(77)  #napravi se termin
    termin=Termin(film1.id,"15:00")
    termin1=Termin(film2.id,"18:00")
    o1=BioskopskaSala("10")
    o2=BioskopskaSala("20")
    o1.addTermin(termin)
    o1.addTermin(termin1)
    o2.addTermin(termin)
    
if __name__ == "__main__":
    main()