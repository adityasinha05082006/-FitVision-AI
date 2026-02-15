# Requirements: PosePlay Fitness Tracker

## 1. Overview

PosePlay is an AI-powered fitness tracking application that uses computer vision to monitor exercises in real-time, count repetitions, calculate scores, and provide visual feedback through a webcam interface.

## 2. User Stories

### 2.1 Exercise Tracking
As a fitness enthusiast, I want to perform exercises in front of my webcam so that the system can automatically track my movements and count repetitions.

### 2.2 Multi-Exercise Support
As a user, I want to switch between different exercise modes (Squat, Pushup, Bicep Curl) so that I can track various workout types in a single session.

### 2.3 Real-Time Feedback
As a user, I want to see real-time visual feedback including my pose skeleton, current stage, rep count, and score so that I can monitor my workout progress.

### 2.4 Performance Monitoring
As a user, I want to see FPS and system performance metrics so that I can ensure the application is running smoothly.

### 2.5 Workout Recording
As a user, I want to record my workout sessions to video files so that I can review my form later or share my progress.

### 2.6 Gamification
As a user, I want to earn points for each completed repetition so that I stay motivated during workouts.

## 3. Acceptance Criteria

### 3.1 Pose Detection
- The system shall detect human pose landmarks using MediaPipe with minimum 70% detection confidence
- The system shall track pose landmarks with minimum 70% tracking confidence
- The system shall process webcam feed at a minimum of 15 FPS on standard hardware

### 3.2 Exercise Recognition

#### 3.2.1 Squat Detection
- The system shall calculate the angle between hip, knee, and ankle joints
- The system shall recognize "UP" stage when knee angle > 160 degrees
- The system shall recognize "DOWN" stage when knee angle < 90 degrees
- The system shall increment counter only when transitioning from UP to DOWN stage

#### 3.2.2 Pushup Detection
- The system shall calculate the angle between shoulder, elbow, and wrist joints
- The system shall recognize "UP" stage when elbow angle > 160 degrees
- The system shall recognize "DOWN" stage when elbow angle < 70 degrees
- The system shall increment counter only when transitioning from UP to DOWN stage

#### 3.2.3 Bicep Curl Detection
- The system shall calculate the angle between shoulder, elbow, and wrist joints
- The system shall recognize "DOWN" stage when elbow angle > 160 degrees
- The system shall recognize "UP" stage when elbow angle < 40 degrees
- The system shall increment counter only when transitioning from DOWN to UP stage

### 3.3 Scoring System
- The system shall award 10 points for each completed repetition
- The system shall maintain cumulative score throughout the session
- The system shall reset score when switching exercise modes

### 3.4 User Interface
- The system shall display a semi-transparent overlay panel showing:
  - Application title
  - Current exercise mode
  - Repetition count
  - Current score
  - Current stage (UP/DOWN)
  - FPS counter
  - Recording status
- The system shall draw pose landmarks and connections on the video feed
- The system shall mirror the webcam feed horizontally for natural user experience

### 3.5 Video Recording
- The system shall support toggling video recording on/off via 'R' key
- The system shall save recordings in AVI format with XVID codec
- The system shall include timestamp in recording filename
- The system shall display recording status on screen
- The system shall properly release video writer resources when stopping

### 3.6 Mode Switching
- The system shall support cycling through exercise modes via 'M' key
- The system shall reset counter and score when switching modes
- The system shall support at least 3 exercise types: Squat, Pushup, Bicep Curl

### 3.7 Application Control
- The system shall exit gracefully when 'Q' key is pressed
- The system shall release all camera and video resources on exit
- The system shall handle camera disconnection without crashing

### 3.8 Angle Calculation
- The system shall calculate joint angles using arctangent of coordinate differences
- The system shall normalize angles to 0-180 degree range
- The system shall handle edge cases where angle > 180 degrees

## 4. Technical Requirements

### 4.1 Dependencies
- Python 3.x
- OpenCV (cv2) for video capture and processing
- MediaPipe for pose detection
- NumPy for mathematical calculations
- Requests library for future API integration

### 4.2 Performance
- Minimum 15 FPS processing rate
- Maximum 100ms latency for pose detection
- Support for standard webcam resolutions (640x480 to 1920x1080)

### 4.3 Hardware Requirements
- Webcam (built-in or external)
- CPU capable of real-time video processing
- Minimum 4GB RAM recommended

## 5. Future Enhancements (Out of Scope for Current Version)

### 5.1 Cloud Integration
- Save workout data to AWS DynamoDB via API Gateway and Lambda
- User authentication via AWS Cognito
- Workout history and analytics

### 5.2 Advanced Features
- Form correction feedback using AI
- Voice coaching
- Multi-user support
- Leaderboard system
- Custom exercise creation
- Workout plans and routines

### 5.3 Additional Exercise Types
- Lunges
- Planks
- Jumping jacks
- Sit-ups

## 6. Constraints and Assumptions

### 6.1 Constraints
- Single user per session
- Requires adequate lighting for pose detection
- User must be fully visible in camera frame
- Left-side body landmarks used for tracking

### 6.2 Assumptions
- User has working webcam
- User performs exercises in front of camera
- User is familiar with proper exercise form
- Sufficient space for exercises in camera view

## 7. Non-Functional Requirements

### 7.1 Usability
- Simple keyboard controls (R, M, Q)
- Clear visual feedback
- Intuitive UI layout

### 7.2 Reliability
- Graceful handling of camera failures
- Proper resource cleanup on exit
- No memory leaks during extended sessions

### 7.3 Maintainability
- Modular code structure
- Clear function separation
- Documented angle calculation logic

### 7.4 Portability
- Cross-platform support (Windows, macOS, Linux)
- Standard Python libraries
- No platform-specific dependencies
