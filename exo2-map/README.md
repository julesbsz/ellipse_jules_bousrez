Pour ce projet, j’ai choisi d’utiliser React et [Next.js](https://nextjs.org/), des technologies que j’apprécie particulièrement. Pour la carte géographique, je me suis servie de [Mapbox](https://www.mapbox.com/) qui met à disposition une API gratuite avec une documentation très complète.

Lien de l’application (hébergé avec [Vercel](https://vercel.com/)) : [https://ellipse-jules-bousrez.vercel.app/](https://ellipse-jules-bousrez.vercel.app/)

## Informations

Le code source est constitué de 5 fichiers principaux :

-   [data.ts](https://github.com/julesbsz/ellipse_jules_bousrez/blob/master/exo2-map/api/data.ts) : Ce fichier contient une fonction qui récupère et trie les données auprès de l’API JCDecaux.

-   [page.tsx](https://github.com/julesbsz/ellipse_jules_bousrez/blob/master/exo2-map/app/page.tsx) : Ce fichier permet d’injecter sur la page web l’unique composant parent, la carte géographique.

-   [Map.tsx](https://github.com/julesbsz/ellipse_jules_bousrez/blob/master/exo2-map/components/Map.tsx) : Ce fichier contient le composant principal; la carte. On y instancie une carte avec les données de l’API.

-   [Position.tsx](https://github.com/julesbsz/ellipse_jules_bousrez/blob/master/exo2-map/components/Position.tsx) : Ce composant permet d’afficher notre position sur la map et notre zoom en temps réel.

-   [Informations.tsx](https://github.com/julesbsz/ellipse_jules_bousrez/blob/master/exo2-map/components/Informations.tsx) : Ce composant permet d’afficher les informations d’une station en particulier lorsqu’on clique sur son marqueur.

La données présentes sur la map sont mise à jour toutes les minutes. Plus d’informations sont détaillées dans les commentaires présents dans le code.
