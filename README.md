# Rapport projet IoT – Surveillance de température

Ce dépôt contient un projet de surveillance de température basé sur :
- un ESP32 (acquisition et transmission des données)
- un Raspberry Pi (traitement, stockage et interface)

Le projet est structuré en deux parties principales :

- ESP32/ : code embarqué et documentation liée au capteur
- RaspberryPi/ : Node-RED, SQLite, logique serveur

Chaque partie possède son propre README détaillé.

L’objectif de ce projet est de concevoir un système de surveillance de la température à l’aide d’un capteur LM35, d’un ESP32, d’un Raspberry Pi et du protocole MQTT.
Les données mesurées sont transmises vers un serveur MQTT, puis exploitées sur le Raspberry Pi, stockées dans une base de données SQLite et affichées en temps réel à l’aide de Node-RED.
