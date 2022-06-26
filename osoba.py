
from korisnik import Korisnik

class Osoba:
    with open("data/userCounter.txt","r+") as f:
        counter=int(f.readline())
        f.close()
    
    
    def __init__(self,im,prez,un,pw,isIt="register"):   #razlika izmedju korisnika i zaposlenih; count (zaposleni.read(zaposleni.txt)->1)
        if isIt=="register":
            self.username=un                #korisnici count(korisnici.read(zaposleni.txt))->0
            self.password=pw
            self.im=im
            self.prez=prez
            self.id=Osoba.counter
            Osoba.counter+=1
            with open("data/userCounter.txt","a") as f:
                        f.truncate(0)       
                        f.write(str(Osoba.counter))
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
                
                
    def isOsobaAZaposleni(self):
        with open("data/zaposleni.txt","r") as f:
            lines=f.read().splitlines()
            f.close()
        for line in lines:
            if line.split(" ")[3]==self.username and line.split(" ")[4]==self.password:
                return True
        return False