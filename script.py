import os
import requests
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd

data_index = pd.read_excel('index.xlsx')

j = 0

while j != 41 : 

    try :
        url = data_index.iloc[j,1]

        # Récupération du contenu de la page
        response = requests.get(url)
        html = response.content

        # Initialisation de Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Recherche de toutes les balises div avec la classe "scoreboard_contestantLabel"
        equipes = []
        for div in soup.find_all('div', {'class': 'scoreboard_contestantLabel'}):
            # Récupération du nom de l'équipe
            equipe = div.text.strip()
            equipes.append(equipe)

        # Récupération des dates et heures des matchs
        dates_heures = []
        for div in soup.find_all('div', {'class': 'event_infoTime'}):
            # Récupération de la date et l'heure du match
            date_str = div.text.strip()
            if date_str.startswith("Aujourd'hui"):
                date = datetime.date.today()
                heure_str = date_str.replace("Aujourd'hui", "").strip()
            elif date_str.startswith("Demain"):
                date = datetime.date.today() + datetime.timedelta(days=1)
                heure_str = date_str.replace("Demain", "").strip()
            else:
                date_heure = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M')
                date = date_heure.date()
                heure_str = date_heure.time().strftime("%H:%M")
            dates_heures.append((date, heure_str))

        # Regroupement des équipes par deux pour reconstituer les matchs
        matchs = []
        for i in range(0, len(equipes), 2):
            matchs.append((equipes[i], equipes[i+1]))

        # Recherche de toutes les balises contenants les journées
        #journee = []
        #for tag in soup.find_all('span', {'class': 'breadcrumb_itemLabel'}):
            # Récupération de la journée
        #   jour = tag.text.strip()
        #   journee.append(jour)

        # Recherche de toutes les balises contenant les cotes
        cotes = []
        for tag in soup.find_all('span', {'class': re.compile('oddValue.*')}):
            # Récupération de la cote
            cote = tag.text.strip()
            cotes.append(cote)

        # Récupération des cotes pour chaque match
        cotes_matchs = []
        for i in range(len(matchs)):
            cotes_matchs.append((matchs[i], dates_heures[i], cotes[i*3:i*3+3]))

        # Création d'un DataFrame Pandas avec les colonnes 'Equipe 1', 'Equipe 2', 'Date', 'Heure', 'Cotes 1', 'Cotes N' et 'Cotes 2'
        df = pd.DataFrame(columns=['Home', 'Away', 'Date', 'Heure', 'Cotes 1', 'Cotes N', 'Cotes 2'])

        # Remplissage du DataFrame avec les données récupérées
        for match, (date, heure), cotes in cotes_matchs:
            equipe1, equipe2 = match
            cotes_1, cotes_N, cotes_2 = cotes
            new_row = pd.DataFrame({'Home': [equipe1], 'Away': [equipe2], 'Date': [date], 'Heure': [heure], 'Cotes 1': [cotes_1], 'Cotes N': [cotes_N], 'Cotes 2': [cotes_2]})
            df = pd.concat([df, new_row], ignore_index=True)


        # Calcul de la différence entre la date du match et la date actuelle
        maintenant = datetime.datetime.now()
        diff_temps = []
        for date_match, heure_match in dates_heures:
            datetime_match = datetime.datetime.combine(date_match, datetime.datetime.strptime(heure_match, "%H:%M").time())
            diff = (datetime_match - maintenant).total_seconds() / 60
            diff_temps.append(str(diff) + " minutes")

        # Ajout de la colonne "Différence de temps" au DataFrame
        df['Différence de temps'] = diff_temps


        #=========================================================================================================================================================================================================
        #=========================================================================================================================================================================================================
        #=========================================================================================================================================================================================================
        #=========================================================================================================================================================================================================

        n_rows = len(df)

        i = 0
        while i < n_rows :
            table_name = df['Home'][i] + '_' + df['Away'][i]
            new_df = df.loc[i]
            new_df.to_frame().T.to_csv(data_index.iloc[j,2] + table_name + '.csv', index=False, mode='a', header=not os.path.exists(data_index.iloc[j,2] + table_name + '.csv'))
            i = i + 1

        print(j)    
        j = j + 1

    except :
        j = j + 1
        continue