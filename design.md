# Design: PosePlay Fitness Tracker

## 1. Architecture Overview

PosePlay follows a modular monolithic architecture with clear separation between pose detection, exercise logic, UI rendering, and video recording components.

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Application Loop                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Camera     │  │    Pose      │  │   Exercise   │      │
│  │   Capture    │─▶│  Detection   │─▶│   Tracker    │      │
│  │              │  │  (MediaPipe) │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                              │               │
│                                              ▼               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Video     │  │      UI      │  │    Score     │      │
│  │   Recorder   │  │   Renderer   │◀─│   Manager    │      │
│  │              │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 2. Component Design

### 2.1 Camera Capture Module

**Responsibility**: Manage webcam input and frame processing

**Key Functions**:
- Initialize video capture device
- Read frames continuously
- Mirror frames horizontally for natural UX
- Handle camera disconnection gracefully

**Implementation**:
```python
cap = cv2.VideoCapture(0)
success, frame = cap.read()
frame = cv2.flip(frame, 1)  # Horizontal flip
```

### 2.2 Pose Detection Module

**Responsibility**: Detect and track human body landmarks using MediaPipe

**Configuration**:
- Detection confidence: 0.7 (70%)
- Tracking confidence: 0.7 (70%)

**Key Functions**:
- Process RGB frames through MediaPipe Pose
- Extract 33 body landmarks with x, y, z coordinates
- Draw pose skeleton on frame

**Landmarks Used**:
- Squat: LEFT_HIP, LEFT_KNEE, LEFT_ANKLE
- Pushup: LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST
- Bicep: LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST

### 2.3 Angle Calculation Module

**Responsibility**: Calculate joint angles from three landmark points

**Algorithm**:
```
Given three points: a (proximal), b (joint), c (distal)
1. Calculate angle using arctangent:
   radians = arctan2(c.y - b.y, c.x - b.x) - arctan2(a.y - b.y, a.x - b.x)
2. Convert to degrees: angle = |radians × 180 / π|
3. Normalize: if angle > 180, angle = 360 - angle
4. Return angle in range [0, 180]
```

**Function Signature**:
```python
def calculate_angle(a: list, b: list, c: list) -> float
```

### 2.4 Exercise Tracker Module

**Responsibility**: Implement exercise-specific logic for rep counting

**State Machine Design**:
Each exercise uses a two-stage state machine:
- Stage transitions trigger rep counting
- Prevents double-counting within same movement

#### 2.4.1 Squat Tracker

**States**:
- UP: knee angle > 160° (standing position)
- DOWN: knee angle < 90° (squat position)

**Transition Logic**:
```
UP → DOWN: counter++, score += 10
DOWN → UP: no action (preparing for next rep)
```

#### 2.4.2 Pushup Tracker

**States**:
- UP: elbow angle > 160° (arms extended)
- DOWN: elbow angle < 70° (chest near ground)

**Transition Logic**:
```
UP → DOWN: counter++, score += 10
DOWN → UP: no action (preparing for next rep)
```

#### 2.4.3 Bicep Curl Tracker

**States**:
- DOWN: elbow angle > 160° (arm extended)
- UP: elbow angle < 40° (arm fully curled)

**Transition Logic**:
```
DOWN → UP: counter++, score += 10
UP → DOWN: no action (preparing for next rep)
```

### 2.5 Score Manager

**Responsibility**: Track and manage workout scoring

**Rules**:
- Award 10 points per completed repetition
- Maintain cumulative score during session
- Reset score on mode switch

**Data Structure**:
```python
counter: int = 0  # Total reps
score: int = 0    # Total points
```

### 2.6 UI Renderer Module

**Responsibility**: Display workout information and visual feedback

**Components**:

1. **Semi-transparent Overlay Panel** (350×200px)
   - Background: Black with 60% opacity
   - Position: Top-left corner
   - Contents:
     - Title: "POSEPLAY PRO" (green)
     - Mode: Current exercise (yellow)
     - Reps: Repetition count (white)
     - Score: Current score (cyan)
     - Stage: Current movement stage (red)

2. **Performance Metrics** (Top-right)
   - FPS counter (yellow)
   - Recording status (red when active, gray when inactive)

3. **Pose Visualization**
   - Landmark points (circles)
   - Skeletal connections (lines)
   - Overlaid on video feed

**Color Scheme**:
- Title: RGB(0, 255, 0) - Green
- Mode: RGB(255, 255, 0) - Yellow
- Reps: RGB(255, 255, 255) - White
- Score: RGB(0, 255, 255) - Cyan
- Stage: RGB(0, 0, 255) - Red
- Recording ON: RGB(0, 0, 255) - Red
- Recording OFF: RGB(200, 200, 200) - Gray

### 2.7 Video Recorder Module

**Responsibility**: Record workout sessions to video files

**Configuration**:
- Codec: XVID (cross-platform compatibility)
- Frame rate: 20 FPS
- Filename format: `poseplay_{timestamp}.avi`

**State Management**:
```python
recording: bool = False
out: cv2.VideoWriter | None = None
```

**Operations**:
- Start: Initialize VideoWriter with current frame dimensions
- Record: Write frames when recording=True
- Stop: Release VideoWriter resources

### 2.8 Input Handler Module

**Responsibility**: Process keyboard input for application control

**Key Bindings**:
- `R`: Toggle video recording
- `M`: Cycle through exercise modes
- `Q`: Quit application

**Mode Cycling Logic**:
```python
mode_list = ["Squat", "Pushup", "Bicep"]
mode_index = (mode_index + 1) % len(mode_list)
```

## 3. Data Flow

### 3.1 Main Processing Pipeline

```
1. Capture frame from webcam
2. Flip frame horizontally
3. Convert BGR → RGB
4. Process through MediaPipe Pose
5. Convert RGB → BGR
6. If landmarks detected:
   a. Extract relevant joint coordinates
   b. Calculate joint angle
   c. Update exercise state machine
   d. Increment counter/score if transition occurs
   e. Draw pose landmarks
7. Calculate FPS
8. Render UI overlay
9. Write frame to video (if recording)
10. Display frame
11. Process keyboard input
12. Repeat
```

### 3.2 State Transitions

```
Exercise State Machine:
┌─────────┐
│  INIT   │
│stage=None│
└────┬────┘
     │
     ▼
┌─────────────────────────────────┐
│   Angle Threshold Detection     │
└────┬────────────────────────┬───┘
     │                        │
     ▼                        ▼
┌─────────┐              ┌─────────┐
│ STAGE_1 │◀────────────▶│ STAGE_2 │
│         │              │         │
└─────────┘              └─────────┘
     │                        │
     └────────────┬───────────┘
                  │
                  ▼
         counter++, score+=10
```

## 4. Error Handling

### 4.1 Camera Failures
- Check `cap.isOpened()` before processing
- Break loop if frame read fails
- Release resources in finally block

### 4.2 Pose Detection Failures
- Check `results.pose_landmarks` before accessing
- Skip exercise logic if no landmarks detected
- Continue rendering UI even without pose data

### 4.3 Resource Cleanup
```python
# Cleanup sequence:
1. Release video writer (if active)
2. Release camera capture
3. Destroy all OpenCV windows
```

## 5. Performance Optimization

### 5.1 Frame Processing
- Process frames at native camera resolution
- No unnecessary resizing or transformations
- Efficient color space conversions (BGR ↔ RGB)

### 5.2 UI Rendering
- Pre-calculate overlay dimensions
- Use addWeighted for efficient alpha blending
- Minimize text rendering calls

### 5.3 FPS Calculation
```python
cTime = time.time()
fps = 1 / (cTime - pTime)
pTime = cTime
```

## 6. Configuration Parameters

### 6.1 MediaPipe Configuration
```python
min_detection_confidence = 0.7
min_tracking_confidence = 0.7
```

### 6.2 Exercise Thresholds

| Exercise | Upper Threshold | Lower Threshold | Transition |
|----------|----------------|-----------------|------------|
| Squat    | 160°           | 90°             | UP → DOWN  |
| Pushup   | 160°           | 70°             | UP → DOWN  |
| Bicep    | 160°           | 40°             | DOWN → UP  |

### 6.3 Scoring Configuration
```python
POINTS_PER_REP = 10
```

### 6.4 UI Configuration
```python
OVERLAY_WIDTH = 350
OVERLAY_HEIGHT = 200
OVERLAY_ALPHA = 0.6
FONT = cv2.FONT_HERSHEY_SIMPLEX
```

### 6.5 Video Recording Configuration
```python
CODEC = 'XVID'
RECORDING_FPS = 20.0
FILENAME_FORMAT = 'poseplay_{timestamp}.avi'
```

## 7. Testing Strategy

### 7.1 Unit Tests
- `test_calculate_angle()`: Verify angle calculations for known coordinates
- `test_stage_transitions()`: Verify state machine logic
- `test_score_calculation()`: Verify scoring rules

### 7.2 Integration Tests
- Test camera initialization and frame capture
- Test MediaPipe pose detection with sample images
- Test video recording start/stop cycles

### 7.3 Property-Based Tests

**Testing Framework**: Hypothesis (Python)

#### Property 7.3.1: Angle Calculation Range
**Validates: Requirements 3.8**

For any three points a, b, c, the calculated angle must be in range [0, 180].

```python
@given(
    a=st.tuples(st.floats(-1000, 1000), st.floats(-1000, 1000)),
    b=st.tuples(st.floats(-1000, 1000), st.floats(-1000, 1000)),
    c=st.tuples(st.floats(-1000, 1000), st.floats(-1000, 1000))
)
def test_angle_range(a, b, c):
    angle = calculate_angle(a, b, c)
    assert 0 <= angle <= 180
```

#### Property 7.3.2: Rep Counter Monotonicity
**Validates: Requirements 3.2.1, 3.2.2, 3.2.3**

The rep counter must never decrease during a workout session.

```python
@given(st.lists(st.floats(0, 180), min_size=10, max_size=100))
def test_counter_monotonic(angles):
    counter = 0
    stage = None
    prev_counter = 0
    
    for angle in angles:
        counter, stage = process_squat(angle, counter, stage)
        assert counter >= prev_counter
        prev_counter = counter
```

#### Property 7.3.3: Score Consistency
**Validates: Requirements 3.3**

Score must always equal counter × 10.

```python
@given(st.integers(0, 1000))
def test_score_consistency(reps):
    score = reps * 10
    assert score == reps * POINTS_PER_REP
```

#### Property 7.3.4: Stage Transition Validity
**Validates: Requirements 3.2**

Stage transitions must only occur at defined angle thresholds.

```python
@given(
    st.lists(st.floats(0, 180), min_size=2, max_size=50),
    st.sampled_from(['Squat', 'Pushup', 'Bicep'])
)
def test_valid_transitions(angles, exercise):
    stage = None
    for angle in angles:
        new_stage = get_stage(angle, exercise)
        if stage != new_stage:
            assert is_valid_transition(stage, new_stage, angle, exercise)
        stage = new_stage
```

#### Property 7.3.5: FPS Calculation Positive
**Validates: Requirements 3.1**

FPS must always be positive when time delta is positive.

```python
@given(
    st.floats(0.001, 1.0)  # Time deltas between 1ms and 1s
)
def test_fps_positive(time_delta):
    fps = 1 / time_delta
    assert fps > 0
```

## 8. Future Enhancements

### 8.1 Modularization
- Extract exercise logic into separate classes
- Create ExerciseBase abstract class
- Implement factory pattern for exercise selection

### 8.2 Configuration File
- Move thresholds to JSON/YAML config
- Allow user customization of scoring
- Configurable UI colors and layout

### 8.3 Cloud Integration
- Add API client module for AWS integration
- Implement workout data serialization
- Add authentication module

### 8.4 Multi-User Support
- User profile management
- Workout history tracking
- Progress analytics

## 9. Dependencies

### 9.1 Core Libraries
- `opencv-python` (cv2): Video capture and processing
- `mediapipe`: Pose detection and landmark tracking
- `numpy`: Mathematical operations and array handling
- `time`: Timestamp and FPS calculation
- `requests`: Future API integration

### 9.2 Version Requirements
- Python: 3.8+
- OpenCV: 4.5+
- MediaPipe: 0.8+
- NumPy: 1.19+

## 10. Deployment Considerations

### 10.1 Platform Support
- Windows: Full support
- macOS: Full support
- Linux: Full support (requires camera permissions)

### 10.2 Hardware Requirements
- Webcam: 640×480 minimum, 1280×720 recommended
- CPU: Multi-core processor for real-time processing
- RAM: 4GB minimum, 8GB recommended
- Storage: 100MB for application, additional for recordings

### 10.3 Installation
```bash
pip install opencv-python mediapipe numpy requests
python main.py
```

## 11. Security Considerations

### 11.1 Privacy
- All processing done locally (no cloud transmission in current version)
- Video recordings stored locally
- No personal data collection

### 11.2 Resource Management
- Proper cleanup of camera resources
- Bounded memory usage
- No file system vulnerabilities

## 12. Correctness Properties

The following properties must hold for the system to be considered correct:

1. **Angle Bounds**: All calculated angles ∈ [0°, 180°]
2. **Counter Monotonicity**: counter(t+1) ≥ counter(t) for all time t
3. **Score Invariant**: score = counter × 10 at all times
4. **Stage Consistency**: Stage transitions only at defined thresholds
5. **FPS Positivity**: FPS > 0 when processing frames
6. **Resource Safety**: All resources released on exit
7. **State Determinism**: Same angle sequence produces same counter value
