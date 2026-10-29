-- Create restart table
CREATE TABLE restart(
	student_id INT PRIMARY KEY,
	student_name VARCHAR(255) NOT NULL,
	restart_city VARCHAR(255) NOT NULL,
	graduation_date TIMESTAMP NOT NULL
);

-- Create cloud_practitioner table
CREATE TABLE cloud_practitioner(
	student_id INT PRIMARY KEY,
	certification_date TIMESTAMP NOT NULL,
);