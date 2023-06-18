# Récupération des données de l'API JCDecaux

from config import API_BASE_URL, API_KEY, API_VERSION

import requests  # Librairie pour envoyer des requêtes HTTP
# Librairie pour afficher des tableaux dans le terminal
from tabulate import tabulate


def get_stations():  # Récupérer les stations
    url = f"{API_BASE_URL}/vls/{API_VERSION}/stations?apiKey={API_KEY}"
    response = requests.get(url)
    return response.json()


# Récupérer une station (ne fonctionne pas)
def get_single_station(station_number, contract_name):
    url = f"{API_BASE_URL}/vls/{API_VERSION}/stations/{station_number}?contract={contract_name}?apiKey={API_KEY}"
    print(url)
    response = requests.get(url)
    return response.json()  # Response: {error: 'unauthorized'}


def get_contracts():  # Récupérer les contrats (ne fonctionne pas)
    url = f"{API_BASE_URL}/vls/{API_VERSION}/contracts?apiKey={API_KEY}"
    print(url)
    response = requests.get(url)
    return response.json()  # Response: {error: 'unauthorized'}


# Récupérer les parcs d'un contrat (ne fonctionne pas)
def get_park_list_of_contract(contract_name):
    url = f"{API_BASE_URL}/parking/{API_VERSION}/contracts/{contract_name}/parks?apiKey={API_KEY}"
    print(url)
    response = requests.get(url)
    return response.json()  # Response: {error: 'unauthorized'}


def get_cities():  # Récupérer les villes
    stations = get_stations()
    cities = list(set([station["contract_name"] for station in stations]))
    cities.sort()
    return cities


def get_global_info():  # Récupérer les informations globales (action 1 du menu principal)
    stations = get_stations()

    nb_stations = len(stations)
    nb_stations_open = sum(
        [1 for station in stations if station["status"] == "OPEN"])
    nb_stations_closed = nb_stations - nb_stations_open

    nb_available_bikes = sum([station["available_bikes"]
                             for station in stations])
    nb_available_bike_stands = sum(
        [station["available_bike_stands"] for station in stations])

    info = {
        "Nombre de stations": nb_stations,
        "Stations ouvertes": nb_stations_open,
        "Stations fermées": nb_stations_closed,
        "Nombre de vélos": nb_available_bikes,
        "Nombre de places": nb_available_bike_stands,
    }

    table = [[key, value] for key, value in info.items()]
    return tabulate(table, headers=["Information",
                                    "Valeur"], tablefmt="grid")


# Récupérer les informations par ville (action 2 du menu principal)
def get_info_by_city(city):
    stations = get_stations()
    cities = get_cities()

    # Si la ville n'est pas renseignée, on retourne un statut d'erreur avec la liste des villes disponibles
    if (city == "" or city == " "):
        available_cities = ", ".join(cities)
        response = [{"status": "error"}, {
            "message": f"Villes disponibles : {available_cities}"}]
        return response

    # On met la ville entrée en minuscule
    city = city.lower()

    # Si la ville n'existe pas, on retourne un statut d'erreur avec un message d'erreur
    if city not in cities:
        response = [{"status": "error"},
                    {"message": f"La ville {city} n'existe pas. Veuillez réessayer."}]
        return response

    # On récupère les stations de la ville
    stations = [
        station for station in stations if station["contract_name"].lower() == city]

    nb_stations = len(stations)
    nb_stations_open = sum(
        [1 for station in stations if station["status"] == "OPEN"])
    nb_stations_closed = nb_stations - nb_stations_open

    nb_available_bikes = sum([station["available_bikes"]
                              for station in stations])
    nb_available_bike_stands = sum(
        [station["available_bike_stands"] for station in stations])

    info = {
        "Nombre de stations": nb_stations,
        "Stations ouvertes": nb_stations_open,
        "Stations fermées": nb_stations_closed,
        "Nombre de vélos": nb_available_bikes,
        "Nombre de places": nb_available_bike_stands,
    }

    # On retourne un statut de succès avec les informations sous forme de tableau
    table = [[key, value] for key, value in info.items()]
    message = tabulate(table, headers=["Information",
                                       "Valeur"], tablefmt="grid")
    response = [{"status": "success"}, {"message": message}]
    return response
