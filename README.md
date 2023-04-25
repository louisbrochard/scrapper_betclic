# scrapper_betclic
Python scrapper for Betclic football odds. 

Run scraper.py with a working internet connexion for a scrapping of all current odds on Betclic.com. 
The championship scrapped are the ones in the excel files and can be modify there while keeping the structure. 

The scrapper catch 1/N/2 odds. 
The labels of the output dataframe are the following : 
  Home : team playing home
  Away : team playing away
  Date : Match play
  Heure : Match time
  1 : Home win odd
  N : Draw odd
  2 : Away win odd
  Difference de temps : Minuts left before kickoff
