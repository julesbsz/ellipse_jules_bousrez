import React from "react";

interface PositionComponentProps {
	lng: number;
	lat: number;
	zoom: number;
}

function PositionComponent({ lng, lat, zoom }: PositionComponentProps) {
	return (
		// Affichage des coordonnées et du zoom en temps réel
		<div className="positionbar">
			<p>
				Position: {lng} | Latitude: {lat} | Zoom: {zoom}
			</p>
		</div>
	);
}

export default PositionComponent;
