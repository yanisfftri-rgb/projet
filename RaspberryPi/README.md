Partie RASPBERRY 
Après avoir configuré l'ESP32 pour l'envoi des données, la seconde phase du projet consiste à transformer le Raspberry Pi en un centre de contrôle intelligent. Grâce à l'outil Node-RED, nous centralisons, stockons et visualisons les informations reçues par le protocole MQTT.

1.	Installation de Node-RED 
Pour orchestrer notre flux de données, nous avons installé Node-RED sur le Raspberry Pi. Cet outil de programmation visuelle permet de connecter des périphériques matériels, des API et des services en ligne. L'installation a été réalisée sur la page de code (terminal) du Raspberry, puis l’activation a été effectuée.
•	Code installation : bash <(curl -sL https://github.com/node-red/linux-installers/releases/latest/download/update-nodejs-and-nodered-deb)
•	Code activation : node-red-pi --max-old-space-size=256

2.	Connexion Wi-Fi 
On a ensuite connecté le Raspberry Pi au même Wi-Fi que l’ESP32 ; il a agi comme un client.
•	Connexion au Wi-Fi : LoraChoco : MRB3HBM0R28

3.	Récupération des données (MQTT In) 
Pour récupérer les données, nous avons mis en place un nœud MQTT Input sur Node-RED que l’on a appelé temperature/mila/yanis. Pour cela, on a d’abord installé la librairie node-red-node-sqlite. Nous avons configuré ce nœud avec les paramètres suivants :
•	Serveur : centreia.fr
•	Topic : temperature/mila/yanis (Le sujet spécifique sur lequel l'ESP32 publie ses données. Le Raspberry Pi recherche en permanence ce topic et déclenche le flux dès qu'un nouveau message — contenant la température, la tension batterie et l'index — arrive.)
![Recupération](docs/images/Editmqtt.png)

4.	Transformation des données 
Les données reçues arrivent sous forme d'une chaîne de caractères avec des virgules pour les séparer. On a donc utilisé un nœud fonction pour séparer le message et donc extraire les valeurs individuelles (Température, Batterie, et Compteur). La fonction est appelée « séparation et enregistrement ».
•	Code fonction : msg.payload = msg.payload.split(';')
![Transformation](docs/images/Editfunction.png)
 

5.	Base de données et enregistrement (SQLite)
 Pour conserver un historique des mesures, nous avons mis en place une base de données SQLite directement dans les dossiers du Raspberry Pi. Elle s’appelle mesures2. À chaque réception de message, une requête SQL INSERT est automatiquement générée, ce qui permet aux mesures reçues d'être mises dans la base de données. Sont enregistrés : la date, le temps, la température, la batterie et le compteur. Le code pour cela a été placé dans la fonction « transformation et enregistrement ».
•	Code pour enregistrer les données dans la database : msg.topic = "INSERT INTO mesures2(ts, temps, vbatt, compteur) VALUES (datetime('now'), $temp, $vbatt, $compteur)" return msg;
![sql](docs/images/Editsqlite.png)
![sql data](docs/images/tableausql.png)


6.	Traçage de graphiques (Dashboard) 
Pour visualiser l'évolution de la température sur la durée (courbe de tendance), les mesures de batterie et le compteur, nous avons mis en place des Gauges. Ces graphiques sont accessibles depuis n'importe quel navigateur web connecté au réseau, offrant une surveillance à distance. Pour les mettre en place, nous avons installé la librairie node-red-dashboard. Puis nous avons installé des nœuds de gauges et graphiques que l’on a reliés à la fonction qui transforme nos données. Pour chaque gauge, on a indiqué si la valeur que l’on souhaitait était celle de la température {0}, batterie {1} ou le compteur {2}.
![Température graphe](docs/images/gradiant.jpg)
![Température function](docs/images/gauge.png)
 
7.	Envoi d'alerte Email 
En complément de la LED de sécurité sur l'ESP32, le Raspberry Pi gère les alertes numériques. Nous avons mis en place une alerte qui envoie un mail dès que la température dépasse les 25 degrés. Le message envoie les valeurs mesurées et un mot « alerte ». Pour cela, on a d’abord mis un nœud switch qui permet de rentrer la condition, puis on a mis une fonction qui permet de gérer le message que l’on envoie, puis on a installé la bibliothèque node-red-node-email qui a permis de mettre un nœud qui envoie cet email.
•	Code fonction : msg.payload = 'Alerte température : ' + msg.payload; return msg;
•	Paramétrage nœud email : 
 
![Noeuds Mail](docs/images/yanisfftri.png)
![Function](docs/images/Emailmessage.png)

Toutes nos fonctions ont été réalisées grâce à Node-RED ; on peut ici voir tous les nœuds qui permettent les actions.
![Noeuds](docs/images/complet.png)
 

