import pandas as pd 
import os 

# chemin du dossier contenant les fichiers CSV
chemin_dossier = 'content_Pologne/'

# boucle pour traiter chaque fichier CSV
for fichier in os.listdir(chemin_dossier):
    if fichier.endswith('.csv'):
        # lecture du fichier CSV avec pandas
        df = pd.read_csv(os.path.join(chemin_dossier, fichier))
        print(df)
