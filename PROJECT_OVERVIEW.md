# Digital Core - Professional Agency Management System

## Project Overview
**Digital Core** is a sophisticated full-stack application designed for digital agencies to streamline their operations, automate client onboarding, and maintain a professional online presence. The system integrates a high-performance React frontend with a robust Django backend, featuring automated document generation and secure administrative controls.

---

## Core Features
### 1. Automated Client Onboarding & Consent
- **Public Consent Portal**: A clean, professional form for clients to provide project details and legal consent.
- **Automated Communication**: Instant email confirmations upon submission and final signed PDF agreements sent upon admin approval.
- **Maintenance Tracking**: Automatic calculation of maintenance periods based on deployment dates.

### 2. Powerful Administration Panel
- **Consent Management**: Review, accept, or reject client consents with mandatory deployment date tracking.
- **Content Management**: Effortlessly update the agency's projects, services, and client testimonials.
- **Site Configuration**: Control global branding (Agency Name, Contact Info, About Story) from a centralized dashboard.

### 3. Modern User Experience
- **Interactive Branding**: Dynamic components like the animated Cookie Banner and responsive layouts.
- **Real-time Feedback**: Integrated loading states (spinners) for all critical actions like submitting forms or downloading documents.

### 4. Search Engine Optimization (SEO)
- **Built-in SEO Tools**: Automated meta-tag management for every page.
- **Structured Data**: JSON-LD Schema.org generation for "Professional Service", "FAQ", and "Article" types to boost search visibility.

---

## Technology Stack
### Frontend (`Webora-Frontend`)
- **React (Vite)**: Core framework for a fast, component-based UI.
- **Framer Motion**: Premium micro-animations and page transitions.
- **Vanilla CSS / Utility Classes**: Precise styling control for a modern aesthetic.
- **React Icons**: Extensive library for visual indicators.

### Backend (`WeboraBackend`)
- **Django**: Reliable Python-based web framework.
- **Django REST Framework (DRF)**: Scalable API architecture.
- **ReportLab**: High-fidelity PDF generation engine.
- **SMTP Integration**: Secure email delivery via Gmail API.

---

## Folder Structure

### 📂 `Webora-Frontend`
- `src/components/`: Reusable UI elements (Buttons, Cards, Modals) and Layout (Navbar, Footer).
- `src/pages/public/`: Main website pages (Home, About, Services, Projects, Contact).
- `src/pages/admin/`: Protected administrative views (Dashboard, Manage Consents).
- `src/context/`: Global application state management (AppContext).
- `src/services/`: API client and endpoint configurations.
- `src/utils/`: SEO keyword logic and Schema.org generators.

### 📂 `WeboraBackend`
- `apps/consents/`: Core business logic for client agreements, PDF generation, and email triggers.
- `apps/site_settings/`: Models for agency-wide configuration and branding.
- `config/`: Central project settings, URL routing, and security policies.
- `media/`: Storage for generated PDFs and uploaded media assets.

---
*Status: Active Development - Version 1.5 (Digital Core Rebranding)*
