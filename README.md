# Digital Booth Intelligence Platform

### Hyperlocal Governance Intelligence & Analytics Engine

---

## Overview

The Digital Booth Intelligence Platform is a hyperlocal governance analytics system that transforms static booth-level data into a structured, intelligent decision-support engine.

It creates a Digital Twin of a Booth by mapping:

* Booths
* Streets
* Citizens
* Government Schemes
* Beneficiaries
* Grievances
* Notifications

The system enables micro-level governance insights such as scheme coverage analysis, eligibility gap detection, street-wise intelligence, and targeted communication simulation.

---

## Core Features

### Digital Booth Twin

* Hierarchical data structure: Booth → Streets → Citizens
* Structured relational database design
* Synthetic population simulation for realistic analytics

---

### Intelligent Segmentation Engine

Automatic citizen classification based on rule-based logic:

* Youth
* Senior Citizen
* Farmer
* MSME Owner
* General

Segmentation is computed dynamically at data insertion time and stored for analytics.

---

### Scheme Mapping and Beneficiary Tracking

* Many-to-many mapping between citizens and schemes
* Scheme penetration analytics
* Beneficiary coverage percentage calculation

---

### Gap Detection Engine

Identifies:

* Eligible population
* Covered beneficiaries
* Uncovered eligible citizens
* Gap percentage

This enables actionable governance insights and implementation monitoring.

---

### Booth-Level Analytics

Provides:

* Total citizens
* Total streets
* Total beneficiaries
* Segment distribution
* Booth-level scheme coverage

Acts as the Digital Booth Summary endpoint for dashboards.

---

### Street-Level Intelligence

* Street-wise scheme penetration
* Hyperlocal citizen filtering
* Street-level grievance tracking
* Heatmap-ready coverage data

---

### Issue and Grievance Tracking

* Street-level issue reporting
* Status tracking (Open / Closed)
* Accountability mapping at micro level

---

### Hyperlocal Notification Simulation

Simulates targeted governance communication:

* Sends notification to specific streets
* Targets only consented citizens
* Returns number of affected households
* Enforces role-based access control

---

### Role-Based Access Control (Basic)

Implements a simple role check mechanism:

* Admin
* Volunteer
* Analyst

Critical endpoints (e.g., notification dispatch) are restricted to authorized roles.

---

## System Architecture

Frontend (Future Integration)
↓
FastAPI Backend
↓
SQLAlchemy ORM
↓
PostgreSQL Database

---

## Data Model

### Core Tables

* booths
* streets
* citizens
* schemes
* beneficiaries
* issues
* notifications
* users

### Relationships

Booth
→ Streets
→ Citizens
↔ Schemes (Many-to-Many via Beneficiaries)
→ Issues
→ Notifications

---

## Analytics Capabilities

The system supports:

* Scheme coverage percentage
* Booth-level penetration analysis
* Street-level penetration analysis
* Segment distribution reporting
* Eligibility gap detection
* Targeted household counts
* Governance summary metrics

---

## Sample API Endpoints

Booth Summary
GET /booths/{booth_id}/summary

Scheme Coverage
GET /schemes/{scheme_id}/coverage

Gap Analysis
GET /schemes/{scheme_id}/gap-analysis

Street-Level Citizens
GET /streets/{street_id}/citizens

Send Hyperlocal Notification
POST /notifications/

---

## Synthetic Data Generation

The project includes a data generation script using:

* Faker
* Pandas

It generates 200–300 synthetic citizens with realistic age and occupation distributions across multiple streets. This enables full analytics demonstration without using real voter data.

---

## Privacy and Ethical Considerations

* No real personal data is used
* Consent-based targeting logic implemented
* Role-based access control enforced
* Designed for governance analytics and public administration support

---

## Technology Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Faker
* Pandas

---

## Vision

The Digital Booth Intelligence Platform enables:

* Data-driven governance
* Micro-level accountability
* Scheme penetration monitoring
* Gap identification
* Hyperlocal decision support

It transforms static booth-level records into a living governance intelligence system.

---
