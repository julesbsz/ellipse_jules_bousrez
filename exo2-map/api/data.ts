// Appel à l'API JCDecaux pour récupérer les données
async function getStations() {
	const response = await fetch(`https://api.jcdecaux.com/vls/v1/stations?apiKey=${process.env.NEXT_PUBLIC_JCDECAUX_API_KEY}`);
	const data = await response.json();

	// Si la requête n'a pas abouti, on lève une erreur
	if (!response.ok) {
		throw new Error("Erreur lors du chargement des données ->", data.message);
	}

	// On formate les données pour ne garder que celles qui nous intéressent
	const stations = data.map((station: any) => {
		return {
			id: station.number,
			name: station.name,
			position: {
				lat: station.position.lat,
				lng: station.position.lng,
			},
			bikes: station.available_bikes,
			stands: station.available_bike_stands,
			empty_stands: station.available_bike_stands,
			address: station.address,
			city: station.contract_name,
			last_update: station.last_update,
		};
	});

	return stations;
}

export default getStations;
