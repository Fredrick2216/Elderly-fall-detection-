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

## 📊 System Architecture

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
