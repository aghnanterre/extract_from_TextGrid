#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: extractionMots.py
#iso-8859-1

#Auteur : Amal Guha, Modyco (CNRS UMR 7114 - Université Paris Nanterre)
# écrit pour fonctionner avec Python 3.6.4

#####################################################################
#####################################################################
#
#	Le programme extrait les mots d'une transcription qui contiennent "<n'importe quelle série de lettres>" dedans
#
#####################################################################
#####################################################################

#
# Fonction qui renvoie la liste des mots de la chaîne texte qui contiennent critère
#
def motsQuiContiennent (texte,critere):
	#bornes indiquant la portée d'un @s
	borneDeb="["
	borneFin="]"
	#spliter les mots séparés par des espaces
	listeMotsProvisoire=texte.split()
	#spliter les mots séparés par des apostrophes
	listeMots=list()
#	for m in listeMotsProvisoire:
#			listeMots.extend(m.split('\''))
	listeMots=listeMotsProvisoire
	resu=list()
	courant=0
	#print("\tLISTE MOTS : ",listeMots)
	idx=0 # initialisation de l'index de m dans la listeMots
	for m in listeMots:
		#print("m = ",m)
		motAAjouter=m
		if critere in m:
			indicem=texte.index(m)
			courant=indicem
			courant2=courant
			# si critere==@s, alors il faut inclure dans m les mots précédents jusqu'à trouver le crochet ouvrant
			if (critere=="@s") and borneFin in m:
				#print("idx = ",idx) #debug
				idxr=idx # idxr peut régresser sans toucher à la valeur de idx
				#print("idxr=",idxr) #debug
				#print("borneDeb = ",borneDeb) #debug
				print("motAAjouter = ",motAAjouter)
				cestLePremier=(borneDeb in motAAjouter)
				#print("cestLePremier = ",cestLePremier) #debug
				while (cestLePremier) != True: # boucle pour reculer
					if idxr>0:
						idxr=idxr-1
						cestLePremier=borneDeb in listeMots[idxr]
					else: # si on est au début de listeMots, on sort de la boucle qui recule
						cestLePremier=True
					motAAjouter=listeMots[idxr]+" "+motAAjouter # on agrège le mot précédent
					courant2=texte.index(motAAjouter)
					print("mot à ajouter : ",motAAjouter)
			resu.append([motAAjouter.lower(),courant2])
		idx=idx+1 # incrémentation de l'index de m
	return resu


##########################################################################################################################################
# FONCTION PRINCIPALE : extraction
#################################################################################
#fonction extraction(repertoireFichierTraite : string,nomEnquete:sting,nomRepertoireFichiersSortie : nom du répertoire où mettre les fichiers résultats
#
#################################################################################

def extraction(repertoireFichierTraite,nomEnquete,requete):
	# extraction du fichier sur lequel effectuer la requête
	# fichier Texte exporté depuis Praat au format txt, codage utf-8

	try :
		fo = open(repertoireFichierTraite+"/"+nomEnquete, "r")
	except IOError:
		print(e)

	# Initialisation des variables
	nomTrouve=0
	texteTrouve=0
	nbOcc=0
	resu=""
	#---------------------------------------------------
	#BOUCLE PRINCIPALE (de traitement du fichier Textgrid entree.txt)
	#il faut remettre le pointeur au début du fichier
	print("***********************************************************************************************")
	print ("extraction dans l'enquête ",nomEnquete)
	resu=resu+"******************************\n"
	resu=resu+"Enumération des tours de parole dans le fichier "+nomEnquete+"\n"
	resu=resu+"******************************\n"

	fo.seek(0)
	indiceNomCourant=-1
	cptLignes=0
#	resuCSV="mot;sec. TDP;index;Tire;texte TDP;Enquete;\n"
	resuCSV=""
	nbMotsEnquete=0


	for line in fo:
		cptLignes=cptLignes+1
#		print("for line = ",cptLignes) #debug

# Identification du locuteur (nomTire)
		trouveNomEnPosition = line.find("name =")
		if trouveNomEnPosition>0:
			print ("tire trouvée pour ",nomEnquete," : \n",line)
			nbMotsTourDeParole=0
			nomTrouve=1
			indiceNomCourant +=1
			line= line[trouveNomEnPosition+8:]
			nomTire=line[0:len(line)-3]
			print ("Tire : ", nomTire)

	# positionIntervalle (coordonnée x du début de l'intervalle)
		trouveXEnPosition= line.find("xmin")
		if trouveXEnPosition>0:
			line= line[trouveNomEnPosition+12:]
			xDebBrut=line[8:]
			xDeb=xDebBrut.split(".")[0]

	# positionIntervalle (coordonnée x de la fin d'intervalle)
		trouveXEnPosition= line.find("xmax")
		if trouveXEnPosition>0:
			line= line[trouveNomEnPosition+12:]
			xFinBrut=line[8:]
			xFin=xFinBrut.split(".")[0]

	# lorsque la ligne contient "text"
		trouveTexteEnPosition = line.find("text")
		if trouveTexteEnPosition>0:
	# Si cette ligne du Textgrid correspond à un intervalle (éventuellement texte =="")
			line2= line[trouveTexteEnPosition+8:]
			texte=line2[0:len(line2)-3] # ici on récupère ce qui est entre les guillemets.

			# C'est ici qu'on compte les occurrences de requete
			if (texte!=""):
			# suppression des marques de chevauchement
				texte=texte.replace('<','')
				texte=texte.replace('>','')
			# suppression des parenthèses
				texte=re.sub('\(.*?\)','', texte.rstrip())
			# suppression de l'éventuel point final
				texte2=texte
				if len(texte)>1:
					if texte[len(texte)-1]==".":
						texte2=texte[0:len(texte)-1]

#extraction proprement dite
				listeMotsQuiContiennent= motsQuiContiennent(texte2,requete)
				if listeMotsQuiContiennent:
					for m in listeMotsQuiContiennent:
						resuCSV=resuCSV+str(m[0])+";"+xDeb+";"+str(m[1])+";"+nomTire+";"+texte+";"+nomEnquete+";\n"

	print (cptLignes," lignes traitées")

	fichierResuEnquete=open(nomRepertoireFichiersSortie+"/"+row+"_"+requete+".csv",'w')
	fichierResuEnquete.write(resuCSV)
	fichierResuEnquete.close()
	fo.close()

	return(resuCSV)


#####################################################################################################################################################################################################################################################################################

#PROGRAMME PRINCIPAL

##############################################################################################################################################################################################################################################################################
import os
import os.path
import sys
import string
import re
import time
import datetime


###
###  PARAMETRES
###
print("*********************\n DEBUT EXECUTION \n*********************\n")

# la requete est passée en argument, et affectée à la variable req
req=sys.argv[1]

# dite quel travail fait le programme
print ("ce programme recherche les occurrences de ",req, " et ce sera dans le répertoire resultats.")

# DATE
date=datetime.datetime.now().strftime("%y_%m_%d")
print("date (pour les résultats) = ",date,"\n")

#Repertoire où sont tous les fichiers à traiter
repertoireFichierTraite="./corpus"

#Repertoire des resultats
nomRepertoireFichiersSortie="resultats"
try:
	os.mkdir(nomRepertoireFichiersSortie)
except OSError:
	pass


nomRepertoireFichiersSortie = "resultats/"+date+"/"
try:
	os.mkdir(nomRepertoireFichiersSortie)
except OSError:
	pass

print("nomRepertoireFichiersSortie = ",nomRepertoireFichiersSortie,"\n")


#################################################################
# RE-CREATION DU FICHIER CSV QUI CONTIENT LA LISTE DES Textgrids
#
#### récupération de la liste des fichiers dans le répertoire des transcriptions à traiter ;
print("Récupération de la liste des fichiers du répertoire où il y a les transcriptions à compter ",repertoireFichierTraite,"\n")
listefic = os.listdir(repertoireFichierTraite)


####écriture de la liste des fichiers récupérée plus haut dans un fichier listeEnquetesACompter.csv
print("Ecriture du fichier qui contient la liste des enquêtes traitées\n")
listeEnquetesTraitees = nomRepertoireFichiersSortie+"/""0_enquetesExtractionCSV.csv"
listeFichiers = open(listeEnquetesTraitees, 'a')
listefic.sort()
for f in listefic:
	listeFichiers.write(f+"\n")
print("La liste des enquêtes à traiter est dans le fichier log : ",listeEnquetesTraitees,"\n")

listeTranscriptionsATraiter = listefic # si on n'a pas listefic, on peut remplir listeTranscriptionsAtraiter avec le contenu du fichier listeEnquetesTraitees

#################################################################
#  FICHIER ResuGlobal.csv

fichierResuGlobal=open(nomRepertoireFichiersSortie+"/0_global"+"_"+req+".csv",'w')
fichierResuGlobal.write("mot;seconde;index mot à extraire;Tire; TDP;Enquête\n")
for row in listeTranscriptionsATraiter:
	if not row.find(".DS_Store")>-1: # si dans la liste des fichiers du répertoire, il y a ".DS_Store", on ignore.
		resEnquete=extraction(repertoireFichierTraite,row,req)
		zz=resEnquete.find("texte TDP")
		fichierResuGlobal.write(resEnquete)
fichierResuGlobal.close()


# pour préparer le découpage en plusieurs morceaux
#for i in range(ord('A'),ord('z')+1):
#    print(str(i)+" : "+chr(i))
