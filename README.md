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
