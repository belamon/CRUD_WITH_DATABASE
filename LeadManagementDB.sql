#1. Create a new database 
CREATE DATABASE LeadManagementDB;
Use LeadManagementDB;


#2. CREATE TABLES
#2.A Create table data_lead
CREATE TABLE data_lead (
	lead_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL, 
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    company_sector VARCHAR(50) NOT NULL,
    lead_source VARCHAR(50) NOT NULL,
    date_created DATE NOT NULL,
    sales_rep VARCHAR(50) NOT NULL,
    transaction INT NOT NULL,
    status VARCHAR(50) NOT NULL
);

#2.B valid_user
CREATE TABLE valid_user (
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL  
);

#2.C sales_reps
CREATE TABLE sales_reps(
	rep_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);

#2.D company_sector 
CREATE TABLE company_sector (
	sector_id INT PRIMARY KEY AUTO_INCREMENT,
    sector_name VARCHAR(50) UNIQUE NOT NULL
);

#2.E lead_source
CREATE TABLE lead_source(
	source_id INT PRIMARY KEY AUTO_INCREMENT,
    source_name VARCHAR(50) UNIQUE NOT NULL
);

#3. INSERT VALUES
#3.A Insert values into data_lead
INSERT INTO data_lead (first_name, last_name, email, phone_number, company_sector, lead_source, date_created, sales_rep, transaction, status)
VALUES 
    ('John', 'Doe', 'john.doe@example.com', '1234567890', 'Finance', 'LinkedIn', '2024-09-01', 'Sabrina', 1000000, 'hot'),
    ('Jane', 'Smith', 'jane.smith@example.com', '0987654321', 'Technology', 'Facebook', '2024-09-15', 'Mutiara', 2000000, 'cold'),
	('Bela', 'Moneta', 'bela.mo@example.com', '0787554221', 'Finance', 'LinkedIn', '2024-09-11', 'Sabrina', 500000, 'hot'),
	('Alexa', 'Alcer', 'alexa.mo@example.com', '0482557221', 'Real Estate', 'LinkedIn', '2024-09-10', 'Sabrina', 170000, 'hot'),
    ('Alice', 'Brown', 'alice.brown@example.com', '1122334455', 'Real Estate', 'Instagram', '2024-09-20', 'Samantha', 3000000, 'closed');
    
#3.B Insert values into valid_user
INSERT INTO valid_user (username, password)
VALUES 
    ('admin', 'adminpassword'),
    ('user1', 'user1password');

#3.C Insert values into sales_reps
INSERT INTO sales_reps (name) 
VALUES 
    ('Sabrina'), 
    ('Mutiara'), 
    ('Samantha');

#3.D Insert values into company_sector
INSERT INTO company_sector (sector_name) 
VALUES 
    ('Finance'), 
    ('Technology'), 
    ('Real Estate');

#3.E Insert values into lead_source
INSERT INTO lead_source (source_name) 
VALUES 
    ('LinkedIn'), 
    ('Facebook'),   
    ('Instagram');
