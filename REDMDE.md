# Entrainement d'un réseau de neuronnes visant à jouer au jeu Snake à l'aide d'un algorithme génétique 


- Cette archive contient deux fichiers .py et un fichier README.txt

- Le fichier "snake_game.py" est un fichier contenant les fonctions permettant de jouer au 
  jeu Snake.
- Le fichier "snake_game.py" a été implémenté par Slava Korolev et repris du dépôt Github:
  https://github.com/slavadev/snake_nn/blob/master/snake_game.py (des modifications y ont 
  été faites notamment la suppression des lignes de code utilisant le module curses et 
  l'ajout des 2 fonction process_input et play qui serviront à l'implémentation de 
  l'algorithme génétique).

- Le fichier "GeneticAI.py" implémenté par moi-même contient deux classes: une pour le joueur
  (réseau de neurones implémenté avec Pytorch) et une pour le processus de l'algorithme
  génétique.

- Pour lancer le projet il suffit d'executer le script "GeneticAI.py". Il est possible de
  changer les paramètres (taille de la population, nombre de générations, dimension des
  couches cachées du réseaux de neurones ...) dans le code de la fonction main de ce
  script)

- Il faut noter que l'optimisation des poids du réseau n'est pas stable et que dans le cas
  où la profondeur de vue du joueur est assez élevée, la vitesses d'execution est assez 
  lente. 