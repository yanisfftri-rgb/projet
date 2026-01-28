# ESP32 – Acquisition et transmission

Partie Arduino / ESP32

Cette partie du rapport se concentre uniquement sur le développement du code Arduino exécuté sur l’ESP32. Pour réaliser notre projet, nous avons commencé par développer le code Arduino afin de permettre l’acquisition des mesures et leur transmission vers le serveur MQTT.
Le programme est structuré autour de plusieurs fonctionnalités principales décrites ci-dessous.

1. Connexion au réseau Wi-Fi
Afin de transmettre les données de température, nous avons choisi d’utiliser une connexion Wi-Fi, car l’ESP32 dispose d’un module Wi-Fi intégré.
La connexion est établie au démarrage du programme à l’aide des identifiants du réseau. Tant que la carte n’est pas connectée, le programme reste en attente, ce qui garantit que les données ne sont envoyées que lorsque la connexion est active.

2. Connexion au serveur central (MQTT)
Pour stocker et centraliser les données, nous utilisons un serveur MQTT hébergé à l’adresse centreia.fr.
La bibliothèque PubSubClient permet de gérer la connexion au broker MQTT ainsi que l’envoi des messages.
Un identifiant unique est attribué à l’ESP32 afin d’assurer une communication fiable avec le serveur.
![ESP32](docs/images/photoesp.jpeg)

3. Acquisition de la température (base du projet)
L’objectif principal du projet est d’obtenir des valeurs de température afin de les transmettre au serveur.
Pour cela, nous utilisons un capteur de température LM35, connecté à l’ESP32 sur la broche analogique PIN 33, avec une alimentation en 3,3 V et une masse commune.
La température est mesurée à partir de la tension délivrée par le capteur. Afin d’améliorer la stabilité des mesures, plusieurs lectures successives sont effectuées, puis une moyenne est calculée avant la conversion en degrés Celsius.
  
4. Mise en place d’un compteur de messages
Lors de l’envoi de données sans fil, il peut arriver que certains messages soient perdus.
Pour s’assurer du bon suivi des transmissions, nous avons mis en place un compteur qui s’incrémente à chaque envoi de données.
Ce compteur est transmis avec les autres informations, ce qui permet de vérifier la continuité des messages côté serveur.

5. Surveillance de la consommation et de la batterie
Un objet IoT doit pouvoir fonctionner de manière autonome sur batterie.
Nous avons donc connecté une batterie LiPo à l’ESP32 et mis en place une surveillance de sa tension via la PIN 35.
La tension mesurée permet de suivre l’état de la batterie et d’anticiper une éventuelle décharge. Cette information est également transmise au serveur avec les autres données.
 
![ESP32 batterie](docs/images/photoespbat.jpeg)

Nous avons par ailleurs voulu observer la consommation d'énergie de la carte. Pour ce faire, nous avons suivi l’évolution de la tension de la batterie sur une durée de deux heures : nous sommes passés d’une tension de 3,82 V à 3,79 V.
En nous basant sur la courbe de décharge de la batterie, nous avons constaté que la capacité est passée de 50 % à 40 %. Cette perte de 10 % en 2 heures nous permet de supposer que l'autonomie totale de la batterie est de 20 heures lorsque les mesures sont envoyées toutes les 10 secondes. Pour optimiser cette autonomie, nous pourrions augmenter l'intervalle entre chaque envoi afin de réduire la fréquence des mesures.
![Tableau](docs/images/phototableauvaleurs.jpeg)
 
6. Indicateur visuel d’alerte (LED de sécurité)
Il n’est pas toujours possible de surveiller en permanence l’interface Node-RED.
C’est pourquoi nous avons intégré une LED rouge connectée à la PIN 13 de l’ESP32.
Lorsque la température dépasse un seuil critique, la LED s’allume automatiquement afin de fournir une alerte visuelle immédiate.
Si la température repasse en dessous du seuil, la LED s’éteint.
![ESP32 alerte](docs/images/alertevisu.jpeg)

7. Transmission des données via Wi-Fi et MQTT
Les données collectées par l’ESP32 sont envoyées périodiquement au serveur MQTT via le réseau Wi-Fi.
Chaque message contient :
•	la température mesurée,
•	la tension de la batterie,
•	le numéro du message (compteur).
Les données sont formatées sous forme d’une chaîne de caractères, ce qui facilite leur traitement et leur affichage sur Node-RED.
