# Aegis Pro: A Physics-Informed AI Platform for Non-Intrusive Elderly Fall Detection 🛡️👵

[![Paper Status: Accepted](https://img.shields.io/badge/Paper-Accepted--ICRAIQ2IT--2026-brightgreen)](#)
[![Publisher: Taylor & Francis](https://img.shields.io/badge/Publisher-Taylor%20%26%20Francis%20%28UK%29-blue)](#)
[![Indexing: Scopus](https://img.shields.io/badge/Indexing-Scopus-orange)](#)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aegis Pro is a zero-wearable, physics-informed computer vision framework designed for real-time elderly safety monitoring, behavioral classification, and instant hazard alerting. By bridging **MediaPipe landmark tracking** with **classical physics kinetics**, Aegis Pro significantly cuts down on false positives common to traditional threshold-based camera systems.

---

## 📖 Table of Contents
1. [Core Philosophy & Technical Innovations](#-core-philosophy--technical-innovations)
2. [Mathematical Formulations](#-mathematical-formulations)
3. [System Architecture](#-system-architecture)
4. [Data & Control Flow](#-data--control-flow)
5. [Software Requirements & Dependency Installation](#-software-requirements--dependency-installation)
6. [Step-by-Step Execution & Deployment Guide](#-step-by-step-execution--deployment-guide)
7. [Audio Alert System (Winsound Deep-Dive)](#-audio-alert-system-winsound-deep-dive)
8. [Publication & Academic Context](#-publication--academic-context)
9. [Defensive Q&A for Presentation Prep](#-defensive-qa-for-presentation-prep)
10. [License & Citation](#-license--citation)

---

## 🚀 Core Philosophy & Technical Innovations

* **Zero-Wearable Bio-Monitoring:** Removes the physical discomfort, charging requirements, and reliability issues of smartwatches or pendants. Monitoring happens completely passively through an ambient camera stream.
* **Physics-Informed DCTP Engine:** Calculates real-time **Velocity ($V$)** and **Jerk Metrics ($J$)** to capture the actual kinetic signature of a mechanical impact ("thud"), differentiating a violent fall from a controlled sitting down action.
* **Floor Persistence Logic:** A custom caching state-machine that "remembers" the patient's critical state if body landmarks are obscured or lost near the floor plane ($S_y > 0.65$).
* **Asynchronous Dual-Threaded Response:** Network (SMTP-SSL email) and hardware audio pipelines run completely decoupled from the main vision stream, ensuring 0% frame-rate drop during emergency dispatches.
* **Automatic Clinical Telemetry:** Aggregates real-time tilt angles, acceleration, and tracking statuses into millisecond-accurate Excel sheets (`Session_ID.xlsx`) and plots Seaborn analytics dashboards automatically at session end.

---

## 🧮 Mathematical Formulations

To make the system computationally lean and predictable, Aegis Pro maps its vision data straight to fundamental kinematic principles.

### 1. The Proximity Boundary
The camera reads the patient on a standardized $(x, y)$ coordinate plane mapped from $0$ (top) to $1$ (bottom). The vertical position of their torso ($S_y$) acts as the floor boundary check:
$$\text{Is Near Floor} = (S_y > 0.65)$$

### 2. Calculating Instantaneous Motion (Velocity)
To distinguish between static leaning and live falling, the system calculates vertical velocity ($V$) as the change in position over time ($t$):
$$V = \frac{\Delta y}{\Delta t}$$

### 3. Measuring Impact Severity (The Jerk Metric)
Jerk ($J$) measures the rate of change of acceleration ($a$). A sudden structural crash against the ground results in a severe kinetic spike distinct from normal human mechanics:
$$J = \frac{\Delta a}{\Delta t} = \frac{\Delta^2 V}{\Delta t^2}$$

### 4. Mathematical Trigger Condition
The **Decision-Tree Control Process (DCTP)** evaluates a structural Boolean tree before dispatching emergency sirens:
$$\text{Trigger Alert} = (\text{Torso Angle} > 75^\circ) \land (S_y > 0.65) \land (J > J_{\text{threshold}})$$

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

🛠️ Software Requirements & Dependency Installation
Optimized to run locally on an edge device (e.g., Laptop, Jetson Nano) with Python 3.9+ on a Windows architecture environment.

Run the following instruction to set up all system dependencies cleanly:
"pip install opencv-python mediapipe face_recognition pandas matplotlib seaborn python-dotenv"

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

Bash
python aegis_pro_main.py

Biometric Initialization: Face the camera stream immediately to establish a biometric session lock and parse target patients.json details.

Live Assessment: The real-time Bio-Telemetry HUD will overlay instantly, visualizing moving vector magnitudes, angles ($\theta$), and signal persistence timers.

Graceful Termination: Press the q key on your keyboard to drop the video capture matrix loops smoothly without destroying transient files.

3. Reviewing Telemetry Logs
Once stopped, check your local directories for auto-generated payloads:

/logs/Session_XYZ.xlsx: Detailed millisecond-level step datasets documenting raw joint spatial coordinates.

/analytics/Analytics_XYZ.png: Generated Seaborn summary visual charts displaying historical velocity curves and event timelines.

🔬 Publication & Academic Context
Conference: The 4th International Conference on Recent Advancements in Artificial Intelligence, Quantum Intelligence, and Inclusive Technologies (ICRAIQ2IT-2026)

Host Institution: NRI Institute of Technology, Vijayawada, India [May 08–09, 2026]

Indexing & Press: Scopus-indexed proceedings curated and distributed by Taylor & Francis, UK.

Societal Domain Alignment: Directly maps to United Nations Sustainable Development Goal 3 (SDG 3: Good Health and Well-being) by actively dropping long-lie immobilization delays for isolated older populations.

Development Metrics: Built using industry-standard Agile-SCRUM methodology, successfully validating functional engineering goals at Technology Readiness Level 4 (TRL 4).

@inproceedings{fredrick2026aegis,
  title={Aegis Pro: A Physics-Informed AI Platform for Non-Intrusive Elderly Fall Detection and Bio-Monitoring},
  author={Leonard Fredrick D. and Maddi Jai Nitin},
  booktitle={Proceedings of ICRAIQ2IT-2026, Taylor \& Francis (UK)},
  year={2026}
}

---

## 📊 System Architecture

The software operates on an organized 4-Tier modular framework to secure lightning-fast local performance:

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
