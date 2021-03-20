# Projet : scraping hôtels

## Description du projet
Le but de ce projet de formation est de proposer le meilleur hôtel possible à une famille de 4 personnes (2 adultes, 2 enfants) aux dates et à la destination de leur choix. Cette famille souhaite réserver une seule chambre familiale et veut prendre en compte les critères suivants : note de l'hôtel par leurs autres voyageurs, prix de la chambre, proximité du centre-ville et présence des services de climatisation, wi-fi et minibar.

Ce programme propose donc de choisir une destination et des dates de voyage. Un scraping du site Tripadvisor est ensuite réalisé pour lister tous les hôtels et extraire les critères de choix de la famille. Chaque hôtel se voir attribuer un score de pertinence. La liste de tous les hôtels, leurs services et leur score est enfin présenté à l'utilisateur.

Le projet a été entièrement réalisé en Test Driven Development. Seules quelques fonctions implémentant le scraping ne rentrent pas dans la couverture de tests.

La présentation finale du projet est disponible sur ce lien : [Présentation.pdf](https://github.com/maellerenaud/scraping-for-hotel-recommendation/files/6175488/Presentation.pdf)


## Installation et prérequis

- Copier le projet git dans votre ordinateur avec la commande `git clone`
- Ouvrez le projet avec un IDE (Visual Studio Code, Pycharm...)
- Installez les paquets suivants en tapant les commandes suivantes dans un terminal
    - `sudo apt install python3-tk`
    - `sudo apt install sqlite3`
    - `python3 -m pip3 install selenium`

## Lancement de l'interface graphique

### Change path

- Ouvrez le fichier main.py, et commentez la ligne 10 avec le commentaire suivant `Path chromedriver for Alexandre` avec un `#` devant
- Décommentez la ligne 11 en enlevant le `#`
- Effectuez la même opération dans le fichier utils.py sur les lignes 44 et 45

### In case of problem

- Dans le cas où l'interface ne se lance pas, faites un terminal à la racine du projet lancer la commande `pwd`, puis copier coller le chemin  dans le fichier main.py à la ligne 11 juste avant `/chromedriver` .
- Effectuez la même opération dans le fichier utils.py à la ligne 45.

### Choix de l'hôtel

- Ensuite, lancer le fichier main.py
- Remplissez la ville, la date de début, la date de fin.
- Les résultats s'affichent par la suite
- Vous pouvez avoir plus d'informaitons en cliquant sur un hôtel
