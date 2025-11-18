-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS student_card_db;
USE student_card_db;

-- Create student_cards table
CREATE TABLE IF NOT EXISTS student_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    title VARCHAR(10),
    name VARCHAR(100),
    surname VARCHAR(100),
    qualification VARCHAR(100),
    student_number VARCHAR(50),
    campus VARCHAR(50) DEFAULT 'Mbombela Campus',
    photo_path VARCHAR(255),
    proof_of_registration_path VARCHAR(255),
    verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(email)
);

-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    account_type ENUM('student', 'staff') DEFAULT 'student',
    security_id_number_hash VARCHAR(255),
    security_mother_name_hash VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create lecture_cards table
CREATE TABLE IF NOT EXISTS lecture_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    title VARCHAR(10),
    name VARCHAR(100),
    surname VARCHAR(100),
    qualification VARCHAR(100),
    employee_number VARCHAR(50),
    campus VARCHAR(50) DEFAULT 'Mbombela Campus',
    photo_path VARCHAR(255),
    proof_of_employment_path VARCHAR(255),
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(email)
);

-- Create support_tickets table
CREATE TABLE IF NOT EXISTS support_tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status ENUM('open', 'in_progress', 'resolved', 'closed') DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
); 