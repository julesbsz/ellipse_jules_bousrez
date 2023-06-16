import React, { useEffect, useState } from "react";

function InformationsComponent(data: any) {
	const [station, setStation] = useState<any>({});

	useEffect(() => {
		// On met à jour les informations de la station sélectionnée quand on clique sur une station
		setStation(data.data);
	}, [data]);

	if (station) {
		return (
			<div className="informations">
				<p>
					Station: {station.name} | Bikes: {station.bikes} | Stands: {station.stands} | Empty stands: {station.empty_stands} | Address: {station.address} | City: {station.city}
				</p>
			</div>
		);
	} else {
		return (
			<div className="informations">
				<p>No station selected</p>
			</div>
		);
	}
}

export default InformationsComponent;
