
from korisnickiInterfejs import KorisnickiInterfejs
class Korisnik:
    with open("data/userCounter.txt","r+") as f:
        counter=int(f.readline())
        f.close()
            
            
    def __init__(self,im,prez,un,pw,isIt="register"):   #razlika izmedju korisnika i zaposlenih; count (zaposleni.read(zaposleni.txt)->1)
        if isIt=="register":
            self.username=un                #korisnici count(korisnici.read(zaposleni.txt))->0
            self.password=pw
            self.im=im
            self.prez=prez
            self.id=Korisnik.counter
            Korisnik.counter+=1
            with open("data/userCounter.txt","a") as f:
                        f.truncate(0)       
                        f.write(str(Korisnik.counter))
                        f.close()
        else:
            with open("data/sviKorisnici.txt","r") as f:
                lines=f.read().splitlines()
                f.close()
            for line in lines:
                if line.split(" ")[3]==un and line.split(" ")[4]==pw:
                    self.id=int(line.split(" ")[0])
                    self.im=line.split(" ")[1]
                    self.prez=line.split(" ")[2]
                    self.username=line.split(" ")[3]
                    self.password=line.split(" ")[4]
                    break
        
    def exportKorisnik(self):
        with open("data/sviKorisnici.txt","a") as f:
            f.write(str(self.id)+" "+self.im+" "+self.prez+" "+self.username+" "+self.password+"\n")
            f.close()
            
            
    def isKorisnikAZaposleni(self):
        with open("data/zaposleni.txt","r") as f:
            lines=f.read().splitlines()
            f.close()
        for line in lines:
            if line.split(" ")[3]==self.username and line.split(" ")[4]==self.password:
                return True
        return False
    
    def pristup(self):
        kinterfejs=KorisnickiInterfejs(self)