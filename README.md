# Aegis Pro: A Physics-Informed AI Platform for Non-Intrusive Elderly Fall Detection 🛡️👵

[![Paper Status: Accepted](https://img.shields.io/badge/Paper-Accepted--ICRAIQ2IT--2026-brightgreen)](https://github.com/your-username/aegis-pro)
[![Publisher: Taylor & Francis](https://img.shields.io/badge/Publisher-Taylor%20%26%20Francis%20%28UK%29-blue)](https://github.com/your-username/aegis-pro)
[![Indexing: Scopus](https://img.shields.io/badge/Indexing-Scopus-orange)](https://github.com/your-username/aegis-pro)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aegis Pro is a zero-wearable, physics-informed computer vision framework designed for real-time elderly safety monitoring, behavioral classification, and instant hazard alerting. By bridging **MediaPipe landmark tracking** with **classical physics kinetics**, Aegis Pro significantly cuts down on false positives common to traditional threshold-based camera systems.

---

## 🚀 Key Innovations & Features

* **Zero-Wearable Bio-Monitoring:** Removes the physical discomfort and reliability issues of smartwatches or pendants. Monitors purely through an ambient camera stream.
* **Physics-Informed DCTP Engine:** Calculates real-time **Velocity ($V$)** and **Jerk Metrics ($J = \Delta a / \Delta t$)** to capture the actual kinetic signature of a mechanical impact ("thud"), differentiating a violent fall from a controlled sitting down action.
* **Floor Persistence Logic:** A custom caching state-machine that "remembers" the patient's critical state if body landmarks are obscured or lost near the floor plane ($S_y > 0.65$).
* **Multi-Tier Local Audio Alerts:** Driven by low-latency native Windows `winsound` architecture:
    * *Level 1:* Soft rhythmic warning beeps for hazardous states (e.g., severe bending).
    * *Level 2:* High-intensity emergency siren for verified critical falls.
* **Asynchronous Dual-Threaded Response:** Network (SMTP-SSL email) and hardware audio pipelines run completely decoupled from the main vision stream, ensuring 0% frame-rate drop during emergency dispatches.
* **Automatic Clinical Telemetry:** Aggregates real-time tilt angles, acceleration, and tracking statuses into millisecond-accurate Excel sheets (`Session_ID.xlsx`) and plots Seaborn analytics dashboards automatically at session end.

---

🛠️ Software & Dependency Requirements
The platform is optimized to run locally on an edge device or standard system with Python 3.9+:

command:
pip install opencv-python mediapipe face_recognition pandas matplotlib seaborn python-dotenv

Data Flow Diagram (DFD)
Traces the physical data lifecycle from initial environmental exposure to log filing:
graph LR
    Video[Webcam Video Input] --> Perception[Perception Layer: MediaPipe & dlib]
    Perception --> Motion[Motion Analysis: Velocity & Jerk]
    Motion --> Classify[State Classification]
    Classify --> Output[Alert Output Generation]
    Output --> Log[Display HUD & Log Excel]

Control Flow Diagram (CFD)
Illustrates how the operational state cycle remains responsive through iterative loops:

graph TD
    Monitor[1. Monitor Movement] --> Analyze[2. Analyze Kinetic Parameters]
    Analyze --> Decide[3. Decide Threat Urgency]
    Decide --> Execute[4. Execute Alarms / SMTP Threads]
    Execute --> Update[5. Update Cache States]
    Update --> Monitor

🏎️ Step-by-Step Execution & Deployment Guide
1. Registry & Directory Configuration
Set up a folder named /encodings in your root file tree and insert clear baseline reference images of target patients.

Update your local user database file named patients.json with appropriate recipient parameters:
{
  "patient_01": {
    "name": "John Doe",
    "emergency_contact": "caregiver@domain.com"
  }
}

2. Launching the App
Kickstart the execution script right from your command line:
python aegis_pro_main.py

Biometric Initialization: Face the camera stream immediately to establish a biometric session lock and parse target patients.json details.Live Assessment: The real-time Bio-Telemetry HUD will overlay instantly, visualizing moving vector magnitudes, angles ($\theta$), and signal persistence timers.Graceful Termination: Press the q key on your keyboard to drop the video capture matrix loops smoothly without destroying transient files.

3. Reviewing Telemetry Logs
Once stopped, check your local directories for auto-generated payloads:

/logs/Session_XYZ.xlsx: Detailed millisecond-level step datasets documenting raw joint spatial coordinates.

/analytics/Analytics_XYZ.png: Generated Seaborn summary visual charts displaying historical velocity curves and event timelines.

🔊 Audio Alert System (Winsound Deep-Dive)
Aegis Pro integrates a zero-dependency, ultra-low latency internal audio dispatch machine powered natively via the Windows winsound API.

Multi-Tier Warning StructureTo bypass screen dependencies for immediate notification, the system routes tasks asynchronously on secondary worker threads using the following operational thresholds:Level 0: Safe StateSymptom: Normal daily activities.Action: Complete operational silence; regular system telemetry monitoring.Level 1: Hazardous Warning (Severe Bending)Symptom: System observes Torso angle passing $75^\circ$ but height metrics stay elevated above the floor threshold ($S_y < 0.65$).Action: Triggers slow, repetitive soft warnings (winsound.Beep(800, 300)) to signal room caretakers.Level 2: Critical Emergency Alert (Verified Fall)Symptom: Impact parameters validate alongside floor boundary breaches, or tracking fails inside the danger zone for more than 15 consecutive seconds.Action: Dispatches a high-frequency continuous distress emergency siren (winsound.Beep(2500, 1200)) while generating the primary thread SMTP transmission request concurrently.🔬 Publication & Academic ContextConference: The 4th International Conference on Recent Advancements in Artificial Intelligence, Quantum Intelligence, and Inclusive Technologies (ICRAIQ2IT-2026)Host Institution: NRI Institute of Technology, Vijayawada, India [May 08–09, 2026]Indexing & Press: Scopus-indexed proceedings curated and distributed by Taylor & Francis, UK.Societal Domain Alignment: Directly maps to United Nations Sustainable Development Goal 3 (SDG 3: Good Health and Well-being) by actively dropping long-lie immobilization delays for isolated older populations.Development Metrics: Built using industry-standard Agile-SCRUM methodology, successfully validating functional engineering goals at Technology Readiness Level 4 (TRL 4).

```mermaid
graph TD
    A[Webcam Video Input] -->|720p/30fps| B[Pre-processing Unit]
    
    subgraph Perception_Layer [Perception & Identification]
        B --> C{Facial Recognition}
        C -->|Match ID| D[(Patient Registry JSON)]
        B --> E[MediaPipe Pose Engine]
        E -->|33 Landmarks| F[Coordinate Mapping]
    end

    subgraph Logic_Engine [DCTP Logic Engine]
        F --> G[Physics Analysis: Velocity & Jerk]
        F --> H[Torso Tilt & Height Analysis]
        G & H --> I{State Classification}
        I -->|If Signal Lost| J[Floor Persistence Logic]
    end

    subgraph Response_Layer [Multi-Tier Response]
        I --> K[Real-time HUD Telemetry]
        I --> L{Decision Trigger}
        L -->|Critical Fall| M[High-Intensity Siren]
        L -->|Critical Fall| N[High-Priority SMTP Email]
        L -->|Bending/Warning| O[Rhythmic Audio Beeps]
    end

    K & L --> Q[Data Archiver: Pandas/Excel]

