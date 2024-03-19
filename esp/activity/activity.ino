#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <MPU6050.h>

// Replace these with your WiFi credentials
const char* ssid = "<SSID>";
const char* password = "<PASSWORD>";

// Replace this with your server address
const char* serverAddress = "http://<IP>:8000/set-user-active";

// Initialize the MPU6050
MPU6050 mpu;

// Array to store last rotation values
const int rotationValuesNum = 20;
float rotationValues[rotationValuesNum] = {0};
int rotationIndex = 0;

void setup() {
  Serial.begin(115200);

  wifi_setup();

  mpu_setup();
}

void wifi_setup() {
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");

  // Display the IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void mpu_setup() {
  Wire.begin();
  // initialize device
  Serial.println("Initializing I2C devices...");
  mpu.initialize();

  // verify connection
  Serial.println("Testing device connections...");
  Serial.println(mpu.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

  mpu.CalibrateGyro(10);
  mpu.CalibrateAccel(10);
}

void loop() {
  bool active = getActivity();
  sendActivity(active);

  delay(500);
}

bool getActivity() {
  // Read accelerometer data
  int16_t ax, ay, az;
  int16_t gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Calculate total acceleration magnitude
  float gtotal = sqrt(sq(gx) + sq(gy) + sq(gz));

  // Update rotation values array
  rotationValues[rotationIndex] = gtotal;
  rotationIndex = (rotationIndex + 1) % rotationValuesNum;

  // Calculate average rotation value
  float gtotalavg = 0;
  for (int i = 0; i < rotationValuesNum; i++) {
    gtotalavg += rotationValues[i];
  }
  gtotalavg /= rotationValuesNum;

  Serial.print("Rotation X: ");
  Serial.print(gx);
  Serial.print(", Y: ");
  Serial.print(gy);
  Serial.print(", Z: ");
  Serial.print(gz);
  Serial.print(", Total: ");
  Serial.print(gtotal);
  Serial.print(", Average: ");
  Serial.print(gtotalavg);
  Serial.println(" rad/s");

  // Check if motion exceeds threshold
  bool active = (gtotal < 500) || (gtotal > 2000);

  return active;
}

void sendActivity(bool active) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected. Cannot send request.");
    return;
  }

  HTTPClient http;

  // Construct the request body
  String requestBody = "{\"active\": " + String(active ? "true" : "false") + "}";

  // Start HTTP connection
  http.begin(serverAddress);

  // Set headers
  http.addHeader("Content-Type", "application/json");

  // Send POST request
  int httpResponseCode = http.POST(requestBody);

  // Check for response
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error sending POST request: ");
    Serial.println(httpResponseCode);
  }

  // End HTTP connection
  http.end();
}
