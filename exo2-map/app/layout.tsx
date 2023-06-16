import "./globals.css"; // Importation des styles globaux

export const metadata = {
	title: "Ellipse Bikes",
	description: "Ellipse Bikes - JCDecaux API - Mapbox - Next.js - React",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
	return (
		<html lang="en">
			<body>{children}</body>
		</html>
	);
}
