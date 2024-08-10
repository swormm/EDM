import base64
from requests import request as req
from requests import post, get, options, Session
import requests
import json
from datetime import date
import os
import sys
from rich import print
from rich.console import Console
from rich.table import Table
import inquirer
import locale
import ctypes
from datetime import datetime
import pandas as pd
from tabulate import tabulate

# START
os.system("cls")
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
console = Console()
ctypes.windll.kernel32.SetConsoleTitleW("ED Moyenne by sym (this men is so crazy <3 !!!)")

banner = fr"""


            __________     __  ___                                
           / ____/ __ \   /  |/  /___  __  _____  ____  ____  ___
          / __/ / / / /  / /|_/ / __ \/ / / / _ \/ __ \/ __ \/ _ \
         / /___/ /_/ /  / /  / / /_/ / /_/ /  __/ / / / / / /  __/
        /_____/_____/  /_/  /_/\____/\__, /\___/_/ /_/_/ /_/\___/
                                    /____/                        


                        discord // s.worm


"""



class Client:
    def __init__(self, ident, password, keepSession=True):
        self.__idents = [ident,password]
        self.BASE = "https://api.ecoledirecte.com/v3/"
        self.__BASEHEADER= {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            }
        self.LOGINPAYLOAD = 'data={"uuid": "","identifiant": "' + ident + '","motdepasse":"' + password + '","isReLogin": false}'
        self.__PARAMS = {"verbe": "post", "v":"4.26.3"}


        if keepSession:
            self.session = Session()
            self.raw_data = self.session.post(self.BASE + "/login.awp?verbe=get&v=4.57.1", data=self.LOGINPAYLOAD, headers=self.__BASEHEADER).json()
        else:
            self.session = None
            self.raw_data = self.session.post(self.BASE + "/login.awp?v=4.26.3", data=self.LOGINPAYLOAD,headers=self.__BASEHEADER).json()

        if self.raw_data['message']:
            #print(f"[+] LOGS : {self.raw_data}")
            tokenconn = self.raw_data["token"]
            self.__BASEHEADER= {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            'X-Token': f'{self.raw_data["token"]}'
            }
            if self.raw_data['code'] == 250:
                self.raw_data_dualauth = self.session.post(self.BASE + "/connexion/doubleauth.awp?verbe=get&v=4.57.1", data=self.LOGINPAYLOAD,headers=self.__BASEHEADER).json()
                #print(f"[+] LOGS : {self.raw_data_dualauth}")

                def decode_base64(encoded_str):
                    decoded_bytes = base64.b64decode(encoded_str)
                    return decoded_bytes.decode('utf-8')

                def encode_base64(str_to_encode):
                    encoded_bytes = str_to_encode.encode('utf-8')
                    encoded_str = base64.b64encode(encoded_bytes)
                    return encoded_str.decode('utf-8')

                # Assurez-vous que les données contiennent la question et les propositions
                if 'data' in self.raw_data_dualauth and 'question' in self.raw_data_dualauth['data'] and 'propositions' in self.raw_data_dualauth['data']:
                    # Décoder la question
                    question_encoded = self.raw_data_dualauth['data']['question']
                    question_decoded = decode_base64(question_encoded)

                    # Afficher la question
                    print("\n==========================Question===============================")
                    print("\nQuestion:", question_decoded)

                    # Décoder les propositions
                    propositions_encoded = self.raw_data_dualauth['data']['propositions']
                    propositions_decoded = [decode_base64(prop) for prop in propositions_encoded]

                    # Afficher les propositions
                    print("\n=========================Propositions=========================")
                    for i, proposition in enumerate(propositions_decoded, 1):
                        print(f"{i}. {proposition}")

                    choice = input("\n -> ")
                    encode_choice = encode_base64(choice)

                    self.CHOICEPAYLOADS = 'data={"choix":"'+ encode_choice + '"}'

                #print(f"[+] LOGS : {self.CHOICEPAYLOADS}")
                try:
                    self.raw_data_rep = post(self.BASE + "/connexion/doubleauth.awp?verbe=post&v=4.57.1", data=self.CHOICEPAYLOADS,headers=self.__BASEHEADER).json()
                #print(self.raw_data_rep)
                except:
                    print("[-] ERROR : Veuillez réessayer")


                #print(self.raw_data_rep['data']['cv'])
                #print(self.raw_data_rep['data']['cn'])
                #decode_cn = base64.b64decode(self.raw_data_rep['data']['cn'])
                #decode_cv = base64.b64decode(self.raw_data_rep['data']['cv'])

                #print(tokenconn)

                self.LOGINPAYLOADWITHDUAL = 'data={"uuid": "","identifiant": "' + ident + '","motdepasse":"' + password + '","isReLogin": false, "cn": "' + self.raw_data_rep['data']['cn'] +'", "cv": "' + self.raw_data_rep['data']['cv'] +'"}'
                try:
                    self.raw_data_log_with_dual = self.session.post(self.BASE + "/login.awp?v=4.26.3", data=self.LOGINPAYLOADWITHDUAL,headers=self.__BASEHEADER).json()
                except:
                    print("[-] ERROR : Veuillez réessayer")
                #print(self.raw_data_log_with_dual)
                loginRes = self.raw_data_log_with_dual
                #account = loginRes['data']['accounts']



                def fetch_notes(token: str):
                    payload = 'data={"anneeScolaire": ""}'
                    response = req("POST", "https://api.ecoledirecte.com/v3/eleves/" + str(loginRes['data']['accounts'][0]['id']) + "/notes.awp?verbe=get&v=4.57.1", data=payload, headers=self.__BASEHEADER).json()
                    #print(payload)
                    #print(self.__BASEHEADER)
                    return response

                ctypes.windll.kernel32.SetConsoleTitleW(f"ED Moyenne Im behind you {loginRes['data']['accounts'][0]['prenom']}")
                print(f"\n=========================Bonjour, {loginRes['data']['accounts'][0]['prenom']}=========================")
                #print("Collecte des notes...")
                #print(loginRes['data']['accounts'][0]['id'])
                #print("[reverse green]Terminé.[/] Pressez [reverse]ENTER[/] pour quitter.")
                self.__BASEHEADER= {
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                'X-Token': f'{loginRes["token"]}'
                }
                print(" - Connexion réussie.")
                #qchoice = input("\n1 - emplois du temps\n2 - Moyenne des Notes\n3 - Cahier de texte\n\n--> ")
                tokenconn = loginRes["token"]
                notesRes = fetch_notes(tokenconn)
                #print(notesRes)


                def handle_notes(data):
                    periodes = data['periodes']
                    notes = data['notes']

                    for periode in periodes:
                        matieres = periode['ensembleMatieres']['disciplines']
                        notes_list = []  # Liste des notes (=> calcul de la médiane)
                        notes_periode = 0  # Somme des notes de la période
                        diviseur_periode = 0  # Somme des coefficients
                        infos_matieres = {}
                        missing_subject_weight = False

                        for matiere in matieres:
                            notes_list_matiere = []
                            notes_matiere = 0
                            diviseur_matiere = 0
                            coef_matiere = float(matiere['coef']) or 1
                            if not float(matiere['coef']):
                                missing_subject_weight = True
                            notesM = list(filter(lambda note: (note['codePeriode'] == periode['idPeriode']) and
                                                              (note['codeMatiere'] == matiere['codeMatiere']), notes))
                            for note in notesM:
                                try:
                                    if not note["nonSignificatif"]:
                                        notes_matiere += (locale.atof(note['valeur']) / locale.atof(note['noteSur'])) * \
                                            locale.atof(note['coef'])
                                        diviseur_matiere += locale.atof(note['coef'])
                                        notes_list.append(locale.atof(
                                            note['valeur']) / locale.atof(note['noteSur']))
                                        notes_list_matiere.append(locale.atof(
                                            note['valeur']) / locale.atof(note['noteSur']))
                                except:
                                    pass

                            moyenne_matiere = None
                            notes_list_matiere.sort()

                            if diviseur_matiere:
                                moyenne_matiere = (notes_matiere / diviseur_matiere)
                                notes_periode += moyenne_matiere * coef_matiere
                                diviseur_periode += coef_matiere
                            infos_matieres[matiere['codeMatiere']] = {
                                'moyenne': moyenne_matiere if diviseur_matiere else None,
                                'mediane': notes_list_matiere[round((len(notes_list_matiere) - 1) / 2)] if notes_list_matiere else None,
                                'rang': matiere['rang'],
                                'coef': coef_matiere
                            }

                        notes_list.sort()

                        if diviseur_periode:
                            # Création du tableau
                            table = Table(title=periode['periode'])
                            table.add_column("Matière", style='cyan', justify='left')
                            table.add_column("Coef", style='white', justify='center')
                            table.add_column("Moyenne", style='magenta', justify='center')
                            table.add_column("Médiane", style='hot_pink', justify='center')
                            table.add_column("Rang", style='green', justify='right')

                            for codeMatiere in infos_matieres:
                                matiere = infos_matieres[codeMatiere]
                                if codeMatiere:
                                    table.add_row(codeMatiere, str(matiere['coef']),
                                                  str(round(
                                                      matiere['moyenne'] * 20, 1) if matiere['moyenne'] else None).zfill(4),
                                                  str(round(
                                                      matiere['mediane'] * 20, 1) if matiere['mediane'] else None).zfill(4),
                                                  f"#{str(matiere['rang']).zfill(2)}")
                            moyenne_periode = notes_periode / diviseur_periode
                            table.add_row("GENERAL", "0", str(round(moyenne_periode * 20, 1)),
                                          str(round((notes_list[round((len(notes_list) - 1) / 2)]) * 20, 1)), "#00", style='red')
                            console.print(table)
                            print("Moyenne exacte:", moyenne_periode * 20)
                            if missing_subject_weight:
                                print("Certaines matières de cette période n'avaient pas de coefficient. La moyenne générale générée est donc probablement erronée.")
                            print()


                date_actuelle = datetime.now()
                date_formatee = date_actuelle.strftime("%Y-%m-%d")
                time_slots = [
                    "08:15 - 09:10",
                    "09:15 - 10:10",
                    "10:30 - 11:25",
                    "11:25 - 12:20",
                    "12:20 - 13:15",
                    "13:55 - 14:50",
                    "14:55 - 15:50",
                    "15:55 - 16:45"
                ]
                def emploisdutemps():
                    payload = 'data={"dateDebut": "'+ date_formatee + '","dateFin": "'+ date_formatee + '","avecTrous": false}'
                    response = req("POST", "https://api.ecoledirecte.com/v3/E/" + str(loginRes['data']['accounts'][0]['id']) + "/emploidutemps.awp?verbe=get&v=4.57.1", data=payload, headers=self.__BASEHEADER).json()
                    #print(payload)
                    #print(self.__BASEHEADER)
                    return response

                def cahierdetexte():
                    payload = 'data={}'
                    response = req("POST", "https://api.ecoledirecte.com/v3/Eleves/" + str(loginRes['data']['accounts'][0]['id']) + "/cahierdetexte.awp?verbe=get&v=4.57.1", data=payload, headers=self.__BASEHEADER).json()
                    #print(payload)
                    #print(self.__BASEHEADER)
                    #print(response)
                    return response


                while True:
                    print("________________________________________")
                    qchoice = input("\n1 - emplois du temps\n2 - Moyenne des Notes\n3 - Cahier de texte\n4 - exit\n________________________________________\n\n--> ")
                    if qchoice == "1" or "2" or "3" or "4":
                        if qchoice == "4":
                            break
                        if qchoice == "2":
                            print("\n")
                            handle_notes(notesRes['data'])
                            #break
                        if qchoice == "1":
                            print("\n")
                            empl = emploisdutemps()
                            # Check if the list is empty or if 'matiere' key is missing in all dictionaries
                            if not empl['data'] or all('matiere' not in entry for entry in data):
                                print("Pas de cours aujourd'hui")
                                #break
                            else:
   
                                df = pd.DataFrame(empl['data'])
   
                                if len(df) > len(time_slots):
                                    raise ValueError("Il n'y a pas assez de créneaux horaires pour le nombre de cours.")
   
                                df['heures'] = time_slots[:len(df)]
                                df = df[['matiere', 'heures']]
                                #break
                            #print(emploisdutemps)
   
                        if qchoice == "3":
                            print("\n")
                            cahi = cahierdetexte()
                            data = cahi['data']
   
                            def afficher_tableau_devoirs(data):
                                # Création d'une liste pour stocker les données du tableau
                                table = []
                                for date, devoirs in data.items():
                                    for devoir in devoirs:
                                        table.append([
                                            date,
                                            devoir['matiere'],
                                            "Oui" if devoir['aFaire'] else "Non",
                                            "Oui" if devoir['documentsAFaire'] else "Non",
                                            devoir['donneLe'],
                                            "Oui" if devoir['effectue'] else "Non",
                                            "Oui" if devoir['interrogation'] else "Non",
                                            "Oui" if devoir['rendreEnLigne'] else "Non"
                                        ])
   
                                headers = ["Date", "Matière", "À Faire", "Documents à Faire", "Donné le", "Effectué", "Interrogation", "Rendre en Ligne"]
                                print(tabulate(table, headers=headers))
   
                            afficher_tableau_devoirs(data)
                    else:
                        print("Choix invalide. Veuillez réessayer.")
                        #break
                #input("\nPress ENTER TO SEE THE LOGIN Result")
                #print(loginRes)


        else:
            print(" - Connexion réussie.")

class Eleve(Client):
    def __init__(self, ident, password, keepSession = True):
        super(Eleve, self).__init__(ident=ident,password=password, keepSession=keepSession)

print(banner)
print("\n=========================CONNEXION=========================\n")
user = input("// Username > ")
passwd = input("// password > ")



Eleve(user, passwd)
