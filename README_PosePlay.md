# PosePlay

## AI-Powered Fitness Platform Built on AWS Cloud

Serverless. Scalable. Intelligent.

PosePlay is a real-time AI fitness system that uses Computer Vision and
AWS Serverless Architecture to track exercises, calculate posture
angles, count repetitions, and store workout analytics in the cloud.

Developed for the AWS AI for Bharat Hackathon 2026.

------------------------------------------------------------------------

## Problem Statement

Many people:

-   Perform exercises incorrectly
-   Lack real-time feedback
-   Have no structured workout tracking
-   Cannot afford personal trainers
-   Lose motivation due to lack of gamification

PosePlay solves this using AI-powered pose tracking and AWS cloud
infrastructure.

------------------------------------------------------------------------

## Solution Overview

PosePlay transforms a normal webcam into an intelligent AI fitness coach
that:

-   Detects body posture using MediaPipe
-   Calculates joint angles in real time
-   Counts repetitions automatically
-   Assigns workout score
-   Stores workout data securely in AWS
-   Enables leaderboard-ready cloud backend

------------------------------------------------------------------------

## AWS Cloud Architecture

User (Webcam) ↓ OpenCV + MediaPipe (AI Engine) ↓ Reps & Score Generated
↓ Amazon API Gateway (HTTP API) ↓ AWS Lambda (Python 3.12) ↓ Amazon
DynamoDB (Workout Storage)

### AWS Services Used

-   Amazon API Gateway -- Secure REST API endpoint
-   AWS Lambda -- Serverless compute for workout processing
-   Amazon DynamoDB -- NoSQL database for user workout storage
-   IAM Roles & Policies -- Secure service access

------------------------------------------------------------------------

## Core Features

### AI Engine

-   Real-time pose tracking
-   Joint angle calculation
-   Multi-exercise detection:
    -   Squat
    -   Push-up
    -   Bicep Curl
-   Automatic repetition counter
-   Game-based scoring
-   FPS monitoring
-   Video recording toggle

### Cloud Integration

-   Workout data saved to DynamoDB
-   Serverless backend via Lambda
-   REST API via API Gateway
-   Leaderboard-ready design
-   Scalable architecture

------------------------------------------------------------------------

## Installation & Setup

Install Dependencies:

pip install opencv-python mediapipe numpy requests

Run Application:

python main.py

------------------------------------------------------------------------

## Controls

R -- Start/Stop Recording\
M -- Change Exercise Mode\
Q -- Quit Application

------------------------------------------------------------------------

## API Example

POST /save

https://`<your-api-id>`{=html}.execute-api.ap-south-1.amazonaws.com/save

Request Body:

{ "username": "karan1", "exercise": "Squat", "reps": 20, "score": 200,
"timestamp": 1771051231 }

Response:

Workout saved successfully!

------------------------------------------------------------------------

## Why This Project Aligns with AWS Hackathon

-   Uses AWS Serverless Architecture
-   Fully scalable cloud backend
-   AI + Cloud integration
-   Real-world health-tech use case
-   Production-ready API structure
-   Free-tier deployable

------------------------------------------------------------------------

## Scalability & Cost Efficiency

-   No server maintenance required
-   Auto scaling via Lambda
-   On-demand billing (DynamoDB)
-   Minimal cost in Free Tier
-   Ready for millions of users

------------------------------------------------------------------------

## Future Enhancements

-   AI feedback using Amazon Bedrock
-   Voice coaching via Amazon Polly
-   User authentication via Amazon Cognito
-   Workout analytics via Amazon QuickSight
-   Video storage in Amazon S3
-   Step-based workflow using AWS Step Functions

------------------------------------------------------------------------
