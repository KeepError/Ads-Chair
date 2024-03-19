# Ads Chair

A service that analyzes the video/audio which a user listens to and collects data on their activity to find the best moments to display ads

## Deploying

### Server

Requirement: Docker, Docker-Compose

Execute command `docker compose up`

### ESP

Requirement: [MPU6050 by Electronic Cats - Library for Arduino](https://www.arduino.cc/reference/en/libraries/mpu6050/)

Upload `esp/activity.ino` to ESP32

### Grafana

Import Dashboard from `grafana/dashboard`

## Accessing

### Frontend

Available at http://127.0.0.1:8080

### Grafana

Available at http://127.0.0.1:3000

### (Optional) Backend

Available at http://127.0.0.1:8000
