# MyPro Backend

This is the backend for the MyPro application, built with FastAPI. It includes:

- User registration and login
- Role-based access control
- Email verification for new users

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mypro-backend.git

2. Install dependencies:
    pip install -r requirements.txt

3. Set up the database and environment variables.

4. Run the application:
uvicorn app.main:app --reload

# Mysql Query Create Database : 

CREATE DATABASE mypro_db;
USE mypro_db;


# To Create Tables 

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

# Insert Roles

INSERT INTO roles (name) VALUES ('admin'), ('customer');

# Create the users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),  -- For email verification
    token_expires_at TIMESTAMP,       -- For email verification
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

# Create the audit_logs Table

CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


# Insert New user 

INSERT INTO users (
    full_name,
    email,
    phone_no,
    password,
    role_id,
    is_active,
    verification_token,
    token_expires_at
) VALUES (
    'John Doe',                      -- Full Name
    'john.doe@example.com',          -- Email
    '1234567890',                    -- Phone Number
    'hashed_password_here',          -- Hashed Password # Refer hashwd.py
    (SELECT id FROM roles WHERE name = 'customer'),  -- Role ID
    FALSE,                           -- is_active (inactive until email verification)
    'verification_token_here',       -- Verification Token
    NOW() + INTERVAL 24 HOUR         -- Token Expiry (24 hours from now)
);

# Verify a User’s Email

UPDATE users
SET is_active = TRUE,
    verification_token = NULL,
    token_expires_at = NULL
WHERE verification_token = 'verification_token_here';

# FETCH ALL USER 

SELECT 
    users.id,
    users.full_name,
    users.email,
    users.phone_no,
    users.is_active,
    roles.name AS role
FROM users
JOIN roles ON users.role_id = roles.id;

# Fetch Audit Logs for a User

SELECT 
    audit_logs.id,
    audit_logs.action,
    audit_logs.ip_address,
    audit_logs.timestamp
FROM audit_logs
WHERE audit_logs.user_id = 1;  -- Replace 1 with the user's ID

# DELETE USER 

DELETE FROM users WHERE id = 1;  -- Replace 1 with the user's ID
