#include <WiFi.h>
#include <PubSubClient.h>

// -------- CONFIGURATION RÉSEAU --------
const char* ssid = "LoraChoco";          // Nom du réseau WiFi
const char* wifi_password = "MRB3HBM0R28"; // Mot de passe WiFi

// -------- CONFIGURATION MQTT --------
const char* mqtt_server = "centreia.fr";        // Adresse du serveur broker
const char* clientID = "esp32_mila_yanis";      // Identifiant unique de notre carte
const char* topic_temp = "temperature/mila/yanis"; // Chemin où envoyer les données

// -------- CONFIGURATION DES BROCHES (PINS) --------
#define TEMP_PIN 33   // Pin analogique pour le capteur de température
#define VBATPIN 35    // Pin pour mesurer la tension batterie
#define LED_PIN 13    // Pin de la LED rouge intégrée sur la carte
int compteur = 0;     // Variable pour compter le nombre de messages envoyés

WiFiClient wifiClient;
PubSubClient client(wifiClient);

// Fonction pour gérer la connexion au serveur MQTT
void connectMQTT() {
  while (!client.connected()) {
    Serial.print("Connexion MQTT...");
    if (client.connect(clientID)) {
      Serial.println("OK"); // Connexion réussie
    } else {
      Serial.print("ECHEC, code = "); // Affiche l'erreur si échec
      Serial.println(client.state());
      delay(2000); // Attend 2 sec avant de réessayer
    }
  }
}

void setup() {
  Serial.begin(9600);           // Initialisation du moniteur série
  pinMode(LED_PIN, OUTPUT);     // Configure la pin 13 comme une sortie (LED)
  
  // Règle l'ADC pour lire des tensions jusqu'à 3.3V (pour la précision du capteur)
  analogSetAttenuation(ADC_11db); 

  // Connexion au réseau WiFi
  WiFi.begin(ssid, wifi_password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("."); // Affiche des points pendant la recherche
  }
  Serial.println("\nWiFi connecté");
  
  client.setServer(mqtt_server, 1883); // Configuration de l'adresse du serveur
}

void loop() {
  // Vérifie que l'on est toujours connecté au serveur MQTT
  if (!client.connected()) {
    connectMQTT();
  }
  client.loop(); // Maintient la communication avec le broker

  compteur++; // Incrémente le compteur à chaque nouvelle boucle

  // -------- LECTURE ET LISSAGE DE LA TEMPÉRATURE --------
  long sommeRaw = 0;
  for(int i = 0; i < 20; i++) {       // On fait 20 mesures rapides
    sommeRaw += analogRead(TEMP_PIN); // On les additionne
    delay(5);
  }
  float rawMoyen = sommeRaw / 20.0;    // On calcule la moyenne pour plus de stabilité

  // Conversion de la valeur brute en tension (0 à 3.3V)
  float voltsTemp = (rawMoyen * 3.3) / 4095.0;
  
  // Conversion de la tension en °C (Formule du TMP36 : 10mV / degré avec 0.5V d'offset)
  float temperature = (voltsTemp - 0.5) * 100;

  // Filtre de correction si la valeur est incohérente (cas du 250°C lu par erreur)
  if (temperature > 150) {
    temperature = temperature / 10.0; 
  }

  // -------- MESURE DE LA BATTERIE --------
  float vbat = analogReadMilliVolts(VBATPIN); // Lecture en millivolts
  vbat *= 2;        // Multiplié par 2 à cause du pont diviseur matériel sur la carte
  vbat /= 1000.0;   // Conversion de millivolts en Volts

  // -------- GESTION DE L'ALERTE LED --------
  String etatLED;
  if (temperature > 25.0) {        // Si le seuil de 25°C est dépassé
    digitalWrite(LED_PIN, HIGH);   // Allume la LED rouge
    etatLED = "ALLUMEE (Alerte !)";
  } else {
    digitalWrite(LED_PIN, LOW);    // Éteint la LED
    etatLED = "ETEINTE";
  }

  // -------- AFFICHAGE SUR LE MONITEUR SÉRIE (PC) --------
  Serial.println("================================");
  Serial.print("Message n° : "); Serial.println(compteur);
  Serial.print("Température: "); Serial.print(temperature, 1); Serial.println(" °C");
  Serial.print("Batterie   : "); Serial.print(vbat, 2); Serial.println(" V");
  Serial.print("Etat LED   : "); Serial.println(etatLED);
  Serial.println("================================");

  // -------- FORMATAGE ET ENVOI DES DONNÉES VIA MQTT --------
  // On crée une chaîne de caractères séparée par des ";" pour Node-RED
  String message = String(temperature, 1) + ";" + String(vbat, 2) + ";" + String(compteur);
  client.publish(topic_temp, message.c_str()); // Publication sur le topic dédié
}



