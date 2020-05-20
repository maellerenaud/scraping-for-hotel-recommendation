# Projet : scraping hôtels

## Installation et prérequis

- Copier le projet git dans votre ordinateur avec la commande `git clone`
- Ouvrez le projet avec un IDE (Visual Studio Code, Pycharm...)
- Installez les paquets suivants en tapant les commandes suivantes dans un terminal
    - `sudo apt install python3-tk`
    - `sudo apt install sqlite3`
    - `python3 -m pip3 install selenium`

## Lancement de l'interface graphique

### Change path

- Ouvrez le fichier main.py, et commentez la ligne 10 avec le commentaire suivant `Path chromedriver for Alexandre` avec un `#` devant
- Décommentez la ligne 11 en enlevant le `#`
- Effectuez la même opération dans le fichier utils.py sur les lignes 44 et 45

### In case of problem

- Dans le cas où l'interface ne se lance pas, faites un terminal à la racine du projet lancer la commande `pwd`, puis copier coller le chemin  dans le fichier main.py à la ligne 11 juste avant `/chromedriver` .
- Effectuez la même opération dans le fichier utils.py à la ligne 45.

### Choix de l'hôtel

- Ensuite, lancer le fichier main.py
- Remplissez la ville, la date de début, la date de fin.
- Les résultats s'affichent par la suite
- Vous pouvez avoir plus d'informaitons en cliquant sur un hôtel