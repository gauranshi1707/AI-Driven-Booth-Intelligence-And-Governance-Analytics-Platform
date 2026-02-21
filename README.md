# FortifyMe

# FortifyMe

### Security That Learns You

FortifyMe is an on-device behavioral authentication system designed to protect high-risk mobile actions such as payments and sensitive confirmations. Instead of relying solely on credentials like PINs, biometrics, or OTPs, FortifyMe analyzes how a user interacts with the device and detects behavioral anomalies in real time.

FortifyMe strengthens existing security layers by verifying behavior before allowing sensitive actions to proceed.

---

## Problem Statement

Modern mobile security systems authenticate credentials, not users.

If an attacker:

* Gains access to an unlocked phone
* Forces the user to unlock the device
* Obtains OTP access

They can complete high-risk transactions without detection.

There is currently no behavioral validation layer inside sensitive mobile flows.

FortifyMe addresses this gap.

---

## Solution Overview

FortifyMe operates inside protected transaction flows and:

* Learns the user’s behavioral interaction patterns
* Builds a baseline profile over multiple sessions
* Detects anomalous behavior in real time
* Assigns a risk score before transaction confirmation
* Applies proportional friction based on risk level

All processing is performed on-device.

---

## Behavioral Signals Collected

FortifyMe collects interaction-level signals during protected sessions.

### 1. Keystroke Timing

Time between key press and release (hold duration).

### 2. Inter-Key Latency

Time gap between consecutive key presses.

### 3. Typing Speed per Field

Characters typed divided by time spent in input field.

### 4. Swipe Velocity

Distance moved per unit time during gesture interaction.

### 5. Scroll Acceleration

Rate of change in scrolling speed.

### 6. Device Orientation

Tilt and stability via accelerometer and gyroscope.

### 7. Form Completion Time

Total time from screen load to transaction confirmation.

Each session generates a structured feature vector used for anomaly detection.

No raw biometric data leaves the device.

---

## Behavioral Intelligence Model

FortifyMe uses multi-signal anomaly detection.

Single deviations are not treated as threats.

Example:

* Slow typing alone → not suspicious
* Unusual swipe pattern alone → not suspicious
* Orientation shift alone → not suspicious

However:

Multiple simultaneous deviations
→ Elevated anomaly score

The model supports gradual drift tolerance:

* Confirmed sessions update baseline slowly
* Long-term behavioral changes are accommodated
* Sudden large deviations are flagged

The system detects deviation, not emotional state.

---

## Modes of Operation

### Trusted Users

* Multiple trusted profiles supported
* Each builds an independent behavioral baseline
* System differentiates owner, trusted user, and unknown user

---

### Handoff Mode

Designed for temporary device sharing.

* Activated manually
* Default 5-minute duration (customizable)
* Relaxed anomaly threshold
* Automatically expires

Prevents false positives during legitimate sharing.

---

### Panic Trigger

Explicit user-activated protection.

Activation:

* User-defined keyword displayed
* Double tap confirms panic mode

Upon activation:

* Panic mode enabled
* SMS sent to trusted devices
* Last known location shared
* Timestamp recorded
* Remote lock option available
* SOS alert capability enabled

Panic trigger is voluntary and explicit.

---

## Risk Response Flow

During protected actions:

1. Behavioral signals collected
2. Feature vector generated
3. Anomaly score computed
4. Risk tier assigned

### Low Risk

Transaction proceeds normally.

### Medium Risk

Additional authentication required.

### High Risk

Transaction temporarily blocked.
Re-authentication required.
Optional trusted-device alert triggered.

FortifyMe protects high-risk actions without locking the entire device.

---

## Cross-Device Sync

FortifyMe supports secure behavioral model synchronization across devices to:

* Prevent cold-start issues
* Maintain behavioral continuity
* Preserve trusted user profiles

Only processed behavioral models are synced, not raw logs.

---

## Technology Stack

Frontend:

* Android (Kotlin)

Behavior Capture:

* Touch event listeners
* TextWatcher
* GestureDetector
* SensorManager (Accelerometer & Gyroscope)

Model:

* On-device anomaly detection
* Isolation Forest or statistical Z-score model
* Sub-100 ms inference time

Storage:

* Encrypted local database

---

## Privacy & Security Principles

* No cross-app monitoring
* No system-wide keylogging
* No raw data transmission
* On-device scoring only
* User-controlled panic activation
* Explicit consent for location sharing

Privacy-first by design.

---

## Implementation Plan

Phase 1
Develop protected transaction flow and interaction capture engine.

Phase 2
Implement feature extraction and baseline modeling.

Phase 3
Integrate anomaly scoring and risk classification.

Phase 4
Add Trusted Users, Handoff Mode, and Panic Trigger.

Phase 5
Testing, threshold tuning, demo preparation.

---
* A more technical developer-focused README
* Or a research-oriented version for academic submission
