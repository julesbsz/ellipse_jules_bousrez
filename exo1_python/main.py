# Affichage des données

from rich import print  # Librairie pour améliorer l'affichage dans le terminal
from api_handler import get_global_info, get_info_by_city

mainMenu = '''

[bold blue]Bienvenue sur l'application de gestion des vélos en libre-service[/bold blue]

[bold]Menu principal[/bold]
1. Informations générales
2. Informations par ville

3. Quitter

'''

# Lancer le programme


def run(mainMenu):
    print("\n" * 100 + mainMenu)

    action = input('Entrer un nombre pour commencer : ')

    # Tant que l'action n'est pas 3 (quitter) -> on continue
    while action != '3':
        print("\n")

        # Si l'action est 1, on affiche les informations globales
        if action == '1':
            print(get_global_info(), end='\n\n')

        # Si l'action est 2, on demande une ville à l'utilisateur -> on affiche les informations de cette ville
        elif action == '2':
            city = input(
                'Entrer le nom de la ville (laisser vide pour afficher la liste des villes disponibles): ')
            response = get_info_by_city(city)

            # Tant que le statut de la réponse est une erreur, on affiche le message d'erreur et on redemande une ville à l'utilisateur
            while response[0]["status"] == "error":
                print("[bold red]" + response[1]
                      ["message"] + "[/bold red]", end='\n\n')
                city = input(
                    'Entrer le nom de la ville (laisser vide pour afficher la liste des villes disponibles): ')
                response = get_info_by_city(city)

            # Si la ville entrée existe, on affiche les informations de cette ville
            print('\n', response[1]["message"], end='\n\n')

        # Si l'action est vide, on affiche le menu principal
        elif action == '':
            print('\n' * 100)
            print(mainMenu)

        # Si l'action n'existe pas, on affiche un message d'erreur
        else:
            print(
                '[bold red]Action inconnue, veuillez réessayer.[/bold red]', end='\n\n')

        action = input(
            'Entrer un nombre pour continuer (laisser vide pour afficher au menu principal): ')

    print('À bientôt !', end='\n\n')


run(mainMenu)
