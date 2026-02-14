# 🏋️ PosePlay -- AI Powered Multi-Exercise Fitness Game

PosePlay is an AI-based real-time exercise tracking and gamified fitness
application built using **Computer Vision + AWS Cloud Backend**.

This project was developed for an AWS Hackathon to demonstrate: -
Real-time pose detection - Exercise recognition - Cloud-connected
workout tracking - Scalable serverless backend architecture

------------------------------------------------------------------------

## 🚀 Features

### 🎯 Core Features

-   Real-time pose tracking using MediaPipe
-   Angle calculation for accurate exercise detection
-   Multi-Exercise Mode (Squat, Push-up, Bicep Curl)
-   Automatic repetition counter
-   Game-based scoring system
-   FPS performance tracking
-   Video recording support

### ☁️ Cloud Features (AWS Powered)

-   Workout data stored in AWS DynamoDB
-   Serverless backend using AWS Lambda
-   REST API via API Gateway
-   Cloud-based leaderboard ready
-   Scalable architecture

------------------------------------------------------------------------

## 🏗️ AWS Architecture

User → OpenCV App → API Gateway → AWS Lambda → DynamoDB

-   **API Gateway** handles HTTP requests
-   **Lambda Function (Python)** processes workout data
-   **DynamoDB** stores user exercise performance
-   Fully serverless & scalable

------------------------------------------------------------------------

## 🛠️ Tech Stack

### 💻 Frontend / App

-   Python
-   OpenCV
-   MediaPipe
-   NumPy

### ☁️ Backend

-   AWS Lambda (Python 3.12)
-   Amazon API Gateway (HTTP API)
-   Amazon DynamoDB

------------------------------------------------------------------------

## 📦 Installation (Local)

``` bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install requests
```

Run the application:

``` bash
python main.py
```

------------------------------------------------------------------------

## 📡 API Example

### Save Workout Data

POST Request:

    https://<your-api-id>.execute-api.ap-south-1.amazonaws.com/save

JSON Body:

``` json
{
  "username": "karan1",
  "exercise": "Squat",
  "reps": 20,
  "score": 200,
  "timestamp": 1771051231
}
```

Response:

    Workout saved successfully!

------------------------------------------------------------------------

## 🧠 Future Improvements

-   AI form correction feedback
-   Real-time leaderboard
-   Mobile app version
-   AWS Cognito authentication
-   Cloud analytics dashboard

------------------------------------------------------------------------

## 🏆 Why This Project Stands Out

-   Combines AI + Computer Vision + Cloud
-   Fully Serverless Architecture
-   Real-time + Cloud-connected fitness tracking
-   Scalable to millions of users

------------------------------------------------------------------------

## 👨‍💻 Developed By

Karan Soni\
AWS Hackathon 2026
