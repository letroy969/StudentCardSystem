-- PostgreSQL Database Schema for Student Card System
-- Compatible with Render's PostgreSQL database

-- Create student_cards table
CREATE TABLE IF NOT EXISTS student_cards (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(10),
    name VARCHAR(100),
    surname VARCHAR(100),
    qualification VARCHAR(100),
    student_number VARCHAR(50),
    campus VARCHAR(50) DEFAULT 'Mbombela Campus',
    photo_path VARCHAR(255),
    proof_of_registration_path VARCHAR(255),
    verification_status VARCHAR(20) DEFAULT 'pending' CHECK (verification_status IN ('pending', 'verified', 'rejected')),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    account_type VARCHAR(10) DEFAULT 'student' CHECK (account_type IN ('student', 'staff')),
    security_id_number_hash VARCHAR(255),
    security_mother_name_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create lecture_cards table
CREATE TABLE IF NOT EXISTS lecture_cards (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(10),
    name VARCHAR(100),
    surname VARCHAR(100),
    qualification VARCHAR(100),
    employee_number VARCHAR(50),
    campus VARCHAR(50) DEFAULT 'Mbombela Campus',
    photo_path VARCHAR(255),
    proof_of_employment_path VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create support_tickets table
CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for support_tickets updated_at
CREATE TRIGGER update_support_tickets_updated_at BEFORE UPDATE
    ON support_tickets FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_student_cards_email ON student_cards(email);
CREATE INDEX IF NOT EXISTS idx_lecture_cards_email ON lecture_cards(email);
CREATE INDEX IF NOT EXISTS idx_support_tickets_email ON support_tickets(email);

