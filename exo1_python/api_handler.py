# Récupération des données de l'API JCDecaux

import requests  # Nécessaire pour faire des requêtes HTTP
# Importation des variables de config
from config import API_BASE_URL, API_KEY, API_VERSION
# Nécessaire pour afficher les informations sous forme de tableau
from tabulate import tabulate

# Récupérer les stations


def get_stations():
    url = f"{API_BASE_URL}/{API_VERSION}/stations?apiKey={API_KEY}"
    response = requests.get(url)
    print(url)
    return response.json()

# Initialiser les informations


def get_cities():
    stations = get_stations()
    cities = list(set([station["contract_name"] for station in stations]))
    cities.sort()
    return cities


def get_info():
    stations = get_stations()
    nb_stations = len(stations)
    nb_bikes = sum([station["bike_stands"] for station in stations])

    # Ajout des informations demandées
    nb_open_stations = sum(
        [1 for station in stations if station["status"] == "OPEN"])
    nb_closed_stations = nb_stations - nb_open_stations
    nb_available_bikes = sum([station["available_bikes"]
                             for station in stations])
    nb_unavailable_bikes = nb_bikes - nb_available_bikes

    info = {
        "Nombre de stations": nb_stations,
        "Stations ouvertes": nb_open_stations,
        "Stations fermées": nb_closed_stations,
        "Nombre de vélos": nb_bikes,
        "Vélos disponibles": nb_available_bikes,
        "Vélos indisponibles": nb_unavailable_bikes,
    }

    table = [[key, value] for key, value in info.items()]
    return tabulate(table, headers=["Information",
                                    "Valeur"], tablefmt="grid")


def get_info_by_city(city):
    stations = get_stations()
    cities = get_cities()

    if (city == "" or city == " "):

        return f"Villes disponibles : {', '.join(cities)}"

    city = city.lower()

    stations_by_city = [
        station for station in stations if station["contract_name"] == city]
    nb_stations = len(stations_by_city)
    nb_bikes = sum([station["bike_stands"] for station in stations_by_city])

    if (nb_stations == 0):
        return f"Aucune station n'a été trouvée pour la ville de {city}"

    # Ajout des informations demandées
    nb_open_stations = sum(
        [1 for station in stations_by_city if station["status"] == "OPEN"])
    nb_closed_stations = nb_stations - nb_open_stations
    nb_available_bikes = sum([station["available_bikes"]
                             for station in stations_by_city])
    nb_unavailable_bikes = nb_bikes - nb_available_bikes

    info = {
        "Nombre de stations": nb_stations,
        "Stations ouvertes": nb_open_stations,
        "Stations fermées": nb_closed_stations,
        "Nombre de vélos": nb_bikes,
        "Vélos disponibles": nb_available_bikes,
        "Vélos indisponibles": nb_unavailable_bikes,
    }

    table = [[key, value] for key, value in info.items()]
    return tabulate(table, headers=["Information",
                                    "Valeur"], tablefmt="grid")
