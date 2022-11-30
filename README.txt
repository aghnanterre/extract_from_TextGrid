
Le programme extractionMots.py extrait les tours de parole des textgrids d'un corpus de transcriptions Praat (.Textgrid) qui contiennent les occurrences d'un "mot" (truc entre deux espaces) donné en argument dans la commande d'exécution de extractionMots.py

1. PREREQUIS
2. FONCTIONNEMENT
3. REMARQUES
4. EXECUTION

1. PREREQUIS
- Python 3.9.12
- un dossier "MonDossierExctraction" (ou le nom que vous voulez), dans lequel il y a un sous-dossier "corpus", lequel contient des Textgrids
(ATTENTION : les textgrids doivent être codés en UTF-8, sans CRLF line terminators).
- le dossier MonDossierExctraction doit contenir les trois fichiers suivants :
	extractionMots.py - c'est le programme python
	scriptExtract.sh - c'est le script unix qui lance l'exécution du programme Python
	README.txt (le présent fichier)
- le sous-répertoire corpus doit contenir tous les fichiers TextGrid dont on veut extraire les tours de parole

2. FONCTIONNEMENT
À l'execution, le programme crée un sous-répertoire resultats, et dedans, un dossier à la date du jour, où sera déposée l'extraction sous forme de fichier csv

- le programme crée dans le répertoire resultats/<date>/ des fichiers csv (pour chaque tirede chaque enquête où a requête a produit des résultats) avec les colonnes suivantes :
	·mot : le mot à extraire, sont la valeur est spécifiée dans l'appel au programme extraction.py
	·sec. TDP : seconde du tour de parole
	·index mot à extraire : indice de l'occurrence du mot extrait dans le TDP (tour de parole)
	·Enquete : nom de l'enquête
	·Tire : nom de la tire
	·xFin : seconde de fin du TDP
	·texte TDP : le texte du TDP

- le programme crée dans le même répertoire un fichier Global csv qui liste tous les textgrids contenus dans /corpus au moment de l'exécution


3. REMARQUES :

* Je ne me souviens plus si les lettres capitales sont traitées, autrement dit il faut peut être prévoir plusieurs lignes dans scriptExtract.sh, par exemple :
 	Python extractionMots.py "oui"
	Python extractionMots.py "Oui"

*	Je ne me souviens pas non plus si ça marche pour plusieurs mots :
	Python extractionMots.py "ben oui"


* cas spécial : si le paramètre est @s alors le "mot" extrait est soit le mot qui contient @s, soit tout ce qui est entre les crochets droits dans la chaîne de car
actères [...]@s



4	EXECUTION
	Pour exécuter la requête  :

- ajouter dans le fichier scriptExtract.sh des lignes de la forme :

	Python extractionMots.py "oui"
	
	 ...où ce qui est entre guillemets est un mot à extraire.

- Ouvrir une fenêtre Terminal
- aller dans le répertoire .../MonDossierExtraction en faisant pwd .../MonDossierExctraction
- la commande ./scriptExtract.sh lance l'exécution.
