import pandas as pd
import imdb
import omdb
import urllib
import re
import webbrowser
class Film:
    
    with open("data/filmCounter.txt","r+") as f:
        counter=int(f.readline())
        f.close()
    
    
    def __init__(self,naziv):  #konstruktor
        
        self.check=True #da li je film vec u fajlu 
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        for i in range(len(df)):
            s = ''.join(ch for ch in naziv.lower() if ch.isalnum())
            p= ''.join(ch for ch in df.iloc[i,1].lower() if ch.isalnum())
            if  p==s:
                self.id=df.iloc[i,0]
                self.naziv=df.iloc[i,1]
                self.trajanje=df.iloc[i,2]
                self.ocena=df.iloc[i,3]
                self.check=False    #film vec postoji u fajlu
                break
        if self.check==True:    #film ne postoji u fajlu, dodaj
                self.naziv=naziv
                self.id=Film.counter
                Film.counter+=1
                self.ocena,self.trajanje=self.getOceneTrajanjeFilma()
                with open("data/filmCounter.txt","a") as f:
                    f.truncate(0)       
                    f.write(str(Film.counter))
                    f.close()
                
        
    def export(self):   #exportuj film u fajl
        with open("data/film.txt","a") as f:
            f.write(str(self.id)+" \""+self.naziv+"\" "+str(self.trajanje)+" "+str(self.ocena)+"\n")
            f.close()
    
    def izbrisiFilm(self):  #izbrisi film iz fajla
        with open("data/film.txt","r") as f:
            lines=f.readlines()
            f.close()
        with open("data/film.txt","w") as f:
            for line in lines:
                if line.split(" ")[0]!=str(self.id):
                    f.write(line)
            f.close()
        with open("data/termini.txt","w") as f:
            for line in lines:
                if line.split(" ")[1]!=str(self.id):
                    f.write(line)
            f.close()
            
        with open("data/reservationInfos.txt","w") as f:
            for line in lines:
                if line.split(" ")[3]!=str(self.id):
                    f.write(line)
            f.close()
    
    def promeniNazivFilma(self,naziv):
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]
        df.loc[df['id']==self.id,"naziv"]=naziv
        df.to_csv("data/film.txt",sep=" ",header=None,index=False)
        
    def getOceneTrajanjeFilma(self):        
        
        i = imdb.IMDb()
        s = i.search_movie(self.naziv)
        m = i.get_movie(s[0].movieID)
        return m.get('rating'),m.data['runtimes'][0]
    
    def getAllIMDBStuff(naziv,crit="all"):
        i = imdb.IMDb()
        s = i.search_movie(naziv)
        m = i.get_movie(s[0].movieID)
        if crit=="all":
            return m.get('rating'),m.data['runtimes'][0],m.get('genres'),m.get('plot')[0],m.get('cover url'),m.get('cast')[0],m.get('director')[0]
        elif crit=="image":
            return m.get('cover url')
        
    def generisiTrejler(id):
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]
        nazivF=df.loc[df.index==id,"naziv"].values[0]
        nazivF=nazivF.replace(" ","+")

        html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+ nazivF+"+trailer")
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url="https://www.youtube.com/watch?v=" + video_ids[0]
        return url
    
    def pustiTrejler(id):
        url=Film.generisiTrejler(id)
        webbrowser.open(url)
    def returnAllMovies():
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]
        return df       
    def naOsnovuID(id):
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]
        return (df.loc[df['id']==id])
    
    def naOsnovuNaziva(naziv):
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]
        return (df.loc[df['naziv']==naziv,"id"].values[0])
    def naOsnovuIndeksa(i):
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]
        return (df.loc[df.index==i].values[0])
    
    def getImefromInd(i):
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]
        return (df.loc[df.index==i].values[0][1])
    
    
def main():

    o3=Film("House of Gucci");
    o3.export()
    print(o3.ocena)

    
    
    
if __name__ == "__main__":
    main()        