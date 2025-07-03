#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#include <Adafruit_MLX90614.h>

// === Wi-Fi credentials ===
const char* ssid     = "ROG_Phone3";
const char* password = "123456789";

// === Firebase configuration ===
#define FIREBASE_URL "***************************"

// === Timing intervals ===
#define REPORTING_PERIOD_MS 500    // Sensor print interval
const unsigned long timerDelay = 5000;  // Firebase upload interval (ms)

// === Shared sensor data (volatile for cross-task safety) ===
volatile float BPM         = 0.0;
volatile float SpO2        = 0.0;
volatile float temperature = 0.0;

// === Sensor objects ===
PulseOximeter pox;
Adafruit_MLX90614 mlx;
TwoWire I2C_MLX = TwoWire(1);  // Custom I2C for MLX90614
uint32_t tsLastReport = 0;      // timestamp for serial printing

// Callback: called on heartbeat detection
void onBeatDetected() {
    Serial.println("Beat Detected!");
}

// -----------------------------------------------------------------------------
// HTTP Upload Task (runs on core 1, FreeRTOS)
// -----------------------------------------------------------------------------
void httpUploadTask(void* parameter) {
    const TickType_t delayTicks = timerDelay / portTICK_PERIOD_MS;
    for (;;) {
        if (WiFi.status() == WL_CONNECTED) {
            HTTPClient http;
            http.begin(FIREBASE_URL);
            http.addHeader("Content-Type", "application/json");

            // Copy shared values into locals
            float bpm  = BPM;
            float spo2 = SpO2;
            float temp = temperature;

            // Build JSON payload with one decimal place for each value
            String payload = String("{") +
                             "\"BPM\":"        + String(bpm, 1)  +
                             ",\"SpO2\":"       + String(spo2, 1) +
                             ",\"Temperature\":" + String(temp, 1) +
                             "}";

            int httpCode = http.PUT(payload);
            if (httpCode > 0) {
                Serial.printf("Firebase upload response: %d\n", httpCode);
            } else {
                Serial.printf("Firebase upload failed, code: %d\n", httpCode);
            }
            http.end();
        } else {
            Serial.println("WiFi disconnected, cannot upload");
        }
        vTaskDelay(delayTicks);
    }
}

// -----------------------------------------------------------------------------
// Arduino setup()
// -----------------------------------------------------------------------------
void setup() {
    Serial.begin(115200);
    delay(100);

    // Connect to Wi-Fi
    Serial.print("Connecting to WiFi: ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("WiFi connected, IP: ");
    Serial.println(WiFi.localIP());

    // Initialize Pulse Oximeter (MAX30100)
    Serial.print("Initializing Pulse Oximeter... ");
    if (!pox.begin()) {
        Serial.println("FAILED");
        for (;;) { /* Halt */ }
    }
    Serial.println("SUCCESS");
    pox.setIRLedCurrent(MAX30100_LED_CURR_14_2MA);
    pox.setOnBeatDetectedCallback(onBeatDetected);

    // Initialize MLX90614 temperature sensor on I2C port 1 (pins 16=SDA, 17=SCL)
    I2C_MLX.begin(16, 17);
    if (!mlx.begin(0x5A, &I2C_MLX)) {
        Serial.println("MLX90614 init failed!");
        for (;;) { /* Halt */ }
    }
    Serial.println("Sensors initialized successfully");

    // Create HTTP upload task on core 1
    xTaskCreatePinnedToCore(
        httpUploadTask,  // Task function
        "HTTP Task",    // Name
        8192,            // Stack size (bytes)
        NULL,            // Parameter
        1,               // Priority
        NULL,            // Task handle
        1                // Core 1
    );
}

// -----------------------------------------------------------------------------
// Arduino loop(): only sensor logic, no blocking HTTP
// -----------------------------------------------------------------------------
void loop() {
    // Fast update for MAX30100
    pox.update();

    // Read sensor values
    BPM         = pox.getHeartRate();
    SpO2        = pox.getSpO2();
    temperature = mlx.readObjectTempC();

    // Print every REPORTING_PERIOD_MS with one decimal place
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        Serial.printf("💓 %.1f  🩸 %.1f%%  🌡 %.1f°C\n", BPM, SpO2, temperature);
        tsLastReport = millis();
    }
}
