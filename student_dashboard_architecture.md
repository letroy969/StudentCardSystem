# Student Dashboard — System Architecture & Database Schema

This document contains a blueprint for the **AI-powered Student Dashboard**: a high-level system architecture (components + data flow), deployment notes on Oracle Cloud Infrastructure (OCI), and a detailed relational database schema (ER diagram + SQL `CREATE TABLE` statements) you can use as a starting point.

---

## 1. High-level Architecture

**Goals:** secure user auth, upload & store documents, integrate OCI Generative AI for summarization & quiz generation, admin management, and simple web deployment.

### Components

* **Frontend (React / Next.js)**

  * Pages: Login / Register, Dashboard, Upload Notes, AI Assistant (Summarize, Quiz), Admin Panel.
  * Interacts with backend via REST or GraphQL.

* **Backend API (Node.js + Express or FastAPI)**

  * Endpoints for auth, file upload, AI job requests, admin actions.
  * Responsible for input validation, rate limiting, and orchestrating calls to OCI.

* **Database (MySQL or Oracle Autonomous DB)**

  * Stores users, user profiles, uploads metadata, AI results, and admin logs.

* **File Storage**

  * OCI Object Storage (for uploaded PDFs, profile photos, exported summaries).

* **OCI Generative AI Service**

  * Handles summarization, Q&A, quiz generation, prompt templates, and optionally fine-tuning or embedding store.

* **Authentication & Authorization**

  * JWT tokens issued by backend; role-based access (student, admin).

* **Worker / Job Queue (optional)**

  * For long-running AI tasks (e.g., large PDF processing). Use OCI Functions or a lightweight worker using Bull / Redis or OCI Streaming + Functions.

* **Deployment**

  * Frontend deployed to OCI Web Apps or static hosting (CDN).
  * Backend on OCI Compute instances, Container Instances, or OCI Functions (serverless).

### Data Flow (simplified)

1. Student logs in or registers → JWT received.
2. Student uploads PDF or image → File stored in OCI Object Storage; metadata saved in DB.
3. Student requests "Summarize" → Backend enqueues job and calls OCI Generative AI with a prompt template + file content (or file text extracted by OCR).
4. OCI returns summary/quiz → Backend saves results in DB and stores derived artifacts (PDF summary) in Object Storage.
5. Student views results in Dashboard.
6. Admin can manage users and view system activity from Admin Panel.

---

## 2. Security & Compliance Notes

* Use HTTPS for all endpoints.
* Store sensitive configs in OCI Vault (API keys, DB credentials).
* Limit file upload types and size; scan for malware if possible.
* Enforce RBAC: only admins can manage users or view all system activity.
* Log actions for audit (admin changes, uploads, AI calls).

---

## 3. Database Schema (ER overview)

**Entities**: `users`, `profiles`, `uploads`, `ai_jobs`, `ai_results`, `admin_logs`, `roles`.

Relationships (short):

* `users` 1---1 `profiles` (each user has one profile)
* `users` 1---* `uploads` (user uploads many files)
* `uploads` 1---* `ai_jobs` (a single upload can spawn multiple AI jobs)
* `ai_jobs` 1---1 `ai_results`
* `users` *---* `roles` via `user_roles` (for RBAC)

---

## 4. SQL Schema (MySQL-compatible)

```sql
-- roles
CREATE TABLE roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  description VARCHAR(255)
);

-- users
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP NULL,
  is_active BOOLEAN DEFAULT TRUE
);

-- user_roles (many-to-many)
CREATE TABLE user_roles (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- profiles (user-specific data)
CREATE TABLE profiles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL UNIQUE,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  date_of_birth DATE,
  phone VARCHAR(30),
  photo_url VARCHAR(1000),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- uploads (notes, PDFs)
CREATE TABLE uploads (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  filename VARCHAR(500),
  object_storage_url VARCHAR(1000),
  mime_type VARCHAR(100),
  size_bytes BIGINT,
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ai_jobs (track request to AI)
CREATE TABLE ai_jobs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  upload_id INT NULL,
  user_id INT NOT NULL,
  job_type VARCHAR(50) NOT NULL, -- e.g., 'summarize','quiz','qa'
  prompt_template TEXT,
  status ENUM('queued','running','completed','failed') DEFAULT 'queued',
  requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP NULL,
  FOREIGN KEY (upload_id) REFERENCES uploads(id) ON DELETE SET NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ai_results (store AI output)
CREATE TABLE ai_results (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ai_job_id INT NOT NULL UNIQUE,
  summary TEXT,
  quiz_json JSON, -- list of Q&A pairs
  extra_notes TEXT,
  result_url VARCHAR(1000), -- e.g., exported PDF summary
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ai_job_id) REFERENCES ai_jobs(id) ON DELETE CASCADE
);

-- admin_logs
CREATE TABLE admin_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  admin_user_id INT NOT NULL,
  action VARCHAR(255) NOT NULL,
  target_type VARCHAR(50),
  target_id INT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (admin_user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- optional: embeds for semantic search
CREATE TABLE embeddings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  upload_id INT,
  vector BLOB,
  metadata JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (upload_id) REFERENCES uploads(id) ON DELETE CASCADE
);
```

> Note: If you use Oracle Autonomous DB, adapt types accordingly (CLOB for large text, BLOB for vectors, etc.).

---

## 5. Prompt Templates (examples)

* **Summarize (concise)**

  * `"You are an expert study assistant. Summarize the following text in 6 bullet points focusing on key definitions and formulas: {document_text}"`

* **Generate Quiz**

  * `"Create 8 multiple-choice questions from the following notes. Each question should have one correct answer and three distractors. Mark the correct option."`

* **Explain like I'm 15**

  * `"Explain the following concept in simple terms suitable for a 15-year-old, using a short example."`

---

## 6. Deployment Checklist (OCI-focused)

1. Create an OCI tenancy and set up compartments for Dev / Prod.
2. Provision Object Storage buckets for uploads & artifacts.
3. Set up Oracle Autonomous DB or MySQL instance.
4. Store API keys & secrets in OCI Vault.
5. Configure IAM policies and network security groups.
6. Deploy backend to OCI Functions or Container Instances; use a managed load balancer if needed.
7. Deploy frontend to OCI Web App or static hosting with CDN.
8. Set up monitoring & alarms (OCI Monitoring) and centralized logs (OCI Logging).

---

## 7. Next Steps / Recommendations

* Start by creating the database schema and scaffolding the backend endpoints for auth and file upload.
* Implement a small proof-of-concept: upload a PDF, extract text, send to OCI Generative AI, and display the summary.
* Keep commits small and document milestones on GitHub and LinkedIn.

---
