# Affichage des données

from rich import print  # Librairie pour améliorer l'affichage dans le terminal
from api_handler import get_info, get_info_by_city, get_cities

welcomeMessage = '''

[bold blue]Bienvenue sur l'application de gestion des vélos en libre-service[/bold blue]

[bold]Menu principal[/bold]
1. Informations générales
2. Information par ville

3. Afficher le menu
4. Quitter

'''

print(welcomeMessage)

action = input('Entrer un nombre pour commencer : ')

while action != '4':
    print("\n")

    if action == '1':
        print(get_info(), end='\n\n')
    elif action == '2':
        city = input(
            'Entrer le nom de la ville (laisser vide pour afficher la liste des villes disponibles): ')
        print(get_info_by_city(city), end='\n\n')
    elif action == '3':
        print('\n' * 100)
        print(welcomeMessage)
    else:
        print('Action inconnue')

    action = input('Entrer un nombre pour continuer : ')

print('À bientôt !', end='\n\n')
