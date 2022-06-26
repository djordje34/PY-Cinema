import pandas as pd
from film import Film

class Termin:
    
    
    def __init__(self,film,kad):
        self.filmid=film
        self.kad=kad
        self.mesta=0
        df=pd.read_csv("data/film.txt",sep=" ",header=None)
        df.columns=["id","naziv","trajanje","ocena"]
        print(df["id"],self.filmid)
        dfF=df.loc[df["id"]==self.filmid]
        self.film=Film(dfF["naziv"].values[0])
        
    def setMesta(self,mesta):
        self.mesta=mesta
    def oduzmiMesto(self,num):
        self.mesta-=num
        
    
    
    def returnIDTermini(id):
        df=pd.read_csv("data/termini.txt",sep=" ",header=None)
        df.columns=["filmid","kad","mesta"]
        df=df.loc[df['filmid']==id]
        return df
        
    def returnAssociatedElements(id):
        df=pd.read_csv("data/termini.txt",sep=" ",header=None)
        df.columns=["salaid","filmid","kad","mesta"]
        df.loc[df["salaid"]==id]
        return{
            "idSale":df["id"].values[0],
            "idFilma":df["filmid"].values[0],
            "vreme":df["kad"].values[0],
            "slobodnaMesta":df["mesta"].values[0]
        }
        
    def readTermini(df):
        termini=[]
        for i in range(len(df)):
            termini.append(Termin(df.iloc[i,0],df.iloc[i,1]))
        return termini
    
    
    def iterateThroughDataframeUsingFor():
        df=pd.read_csv("data/termini.txt",sep=" ",header=None)
        df.columns=["filmid","kad","mesta"]
        for i in range(len(df)):
            print(df.iloc[i,0])