# Aegis Pro: A Physics-Informed AI Platform for Non-Intrusive Elderly Fall Detection 🛡️👵

<div align="center">
  <img src="https://img.shields.io/badge/Paper-Accepted--ICRAIQ2IT--2026-brightgreen?style=for-the-badge" alt="Paper Status">
  <img src="https://img.shields.io/badge/Publisher-Taylor%20%26%20Francis%20%28UK%29-blue?style=for-the-badge" alt="Publisher">
  <img src="https://img.shields.io/badge/Indexing-Scopus-orange?style=for-the-badge" alt="Indexing">
</div>

<br/>

> **Aegis Pro** is a zero-wearable, physics-informed computer vision framework designed for real-time elderly safety monitoring, behavioral classification, and instant hazard alerting. By bridging **MediaPipe landmark tracking** with **classical physics kinetics**, Aegis Pro eliminates the false positives common to traditional threshold-based camera systems.

---

## 🛠️ System Architecture & Data Topology

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
