# Backend Development Report - Digital Core Rebranding & Consent Flow

## Project Overview
Refactored the agency branding from "Webora" to **"Digital Core"** and implemented a fully automated, professional client consent and document management system.

## Major Changes

### 1. Agency Rebranding
- **Site Settings**: Updated `SiteSetting` model default `companyName` to "Digital Core".
- **Email Templates**: Refactored all automated email bodies (Client Confirmation, Admin Notification, Final Agreement) to reflect the new agency name.
- **Freelancer Identity**: Updated the default freelancer name in PDF generation context to "Digital Core".

### 2. Consent Management System (`apps/consents`)
- **Model Enhancements**:
    - Added `deployment_date` field to `Consent` model to track when a project officially starts.
    - Added `version_number` for document tracking.
- **View Logic (`views.py`)**:
    - **Refined Email Workflow**: Split the process into two stages:
        1. **Submission**: Immediate confirmation email sent to the client.
        2. **Acceptance**: Final PDF agreement generated and sent ONLY after admin approval.
    - **Robust Date Parsing**: Implemented `get_deployment_datetime` helper to handle various date formats and ensure timezone-aware `datetime` objects, resolving previous `AttributeError` and `RuntimeWarning` issues.
    - **Maintenance Calculation**: Automatically calculates the 1-year maintenance end date starting from the `deployment_date`.

### 3. Configuration & Infrastructure
- **SMTP Configuration**: Configured `config/settings.py` with secure environment variables for Gmail SMTP integration.
- **Error Handling**: Improved error logging for email delivery failures to prevent silent crashes.

## Implemented API Endpoints
- `POST /api/v1/consents/`: Submit new client consent (triggers confirmation email).
- `POST /api/v1/consents/{id}/accept/`: Admin accepts consent with `deployment_date` (triggers PDF generation and final email).
- `GET /api/v1/consents/{id}/download_pdf/`: Download the generated agreement.

---
*Date of Report: March 18, 2026*
