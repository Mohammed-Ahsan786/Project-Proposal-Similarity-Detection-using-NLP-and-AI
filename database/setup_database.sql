-- Create Schema
CREATE SCHEMA project_db;

-- Create Tables ----------------------------

CREATE TABLE project_db.students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) NOT NULL,
    branch VARCHAR(50) NOT NULL
);

-- This table will contain all the users of our website
CREATE TABLE project_db.users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50),
    CHECK (role IN ('student', 'teacher', 'admin')),
    CHECK (email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$')
);

-- Create an index on email for faster query
CREATE INDEX email_index ON project_db.users(email);

CREATE TABLE project_db.groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) UNIQUE NOT NULL,
    leader_id INT NOT NULL,
    FOREIGN KEY (leader_id) REFERENCES project_db.students(student_id) ON DELETE CASCADE,
    CHECK (LENGTH(group_name) >= 3)
);

CREATE TABLE project_db.group_members (
    group_id INT NOT NULL,
    student_id INT NOT NULL,
    PRIMARY KEY (group_id, student_id),
    FOREIGN KEY (student_id) REFERENCES project_db.students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES project_db.groups(group_id) ON DELETE CASCADE
);

CREATE TABLE project_db.projects (
    project_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    abstract TEXT NOT NULL,
    category VARCHAR(300) NOT NULL,
    group_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    FOREIGN KEY (group_id) REFERENCES project_db.groups(group_id) ON DELETE CASCADE,
    CHECK (LENGTH(title) >= 10),
    CHECK (LENGTH(abstract) >= 10),
    CHECK (status IN ('accepted', 'rejected', 'pending'))
);

-- This table will contain all settings for our project that can be configured by admin
CREATE TABLE project_db.settings (
    setting_id SERIAL PRIMARY KEY,
    setting_name VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT
);

-- Testing configuarations and adding dummy data --------------------------------------------------------------

-- Inserting 4 students into the students table
INSERT INTO project_db.students (name, roll_no, branch)
VALUES
    ('Aditya Mishra', '12345', 'Computer Science'),
    ('Didar Abbas', '12346', 'Computer Science'),
    ('Rohit Pandey', '12347', 'Computer Science'),
    ('Ahsan Ansari', '12348', 'Computer Science');

-- Inserting a single group into the groups table
INSERT INTO project_db.groups (group_name, leader_id)
VALUES
    ('VBSS', 1); 
    
INSERT INTO project_db.group_members(group_id, student_id) 
VALUES
    (1,1),
    (1,2),
    (1,3),
    (1,4);

INSERT INTO project_db.projects (title, abstract, category, group_id)
VALUES
    ('Project Proposal Similarity Detection using NLP and AI', 
    'In this project student has to find the similarity in the submitted projects by students on the Title and Abstract.
    The students submit their project ideas to the system. The system then check the title and abstract with
    previously submitted projects in the system. The main aim of the project is to avoid repetition of the projects.
    Based on the set threshold the system should automatically reject the proposal if there is high similarity with
    any of the previous projects. As a future scope this project maybe extented to the patent application process
    to make the patent application process efficient.',
 'AI & NLP',
  1);
