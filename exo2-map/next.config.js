/** @type {import('next').NextConfig} */
const nextConfig = {
	env: {
		NEXT_PUBLIC_MAPBOX_GL_ACCESS_TOKEN: process.env.NEXT_PUBLIC_MAPBOX_GL_ACCESS_TOKEN,
		NEXT_PUBLIC_JCDECAUX_API_KEY: process.env.NEXT_PUBLIC_JCDECAUX_API_KEY,
	},
	compiler: {
		styledComponents: true,
	},
	experimental: {
		appDir: true,
	},
};

module.exports = nextConfig;
