DROP DATABASE IF EXISTS employees;
CREATE DATABASE IF NOT EXISTS employees;
USE employees;
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    EmployeeID      INT             NOT NULL,
    ManagerID      INT             NOT NULL,
    FirstName  VARCHAR(25)     NOT NULL,
    MiddleName  VARCHAR(25)     NOT NULL,
    LastName   VARCHAR(25)     NOT NULL,
	JobTitle  VARCHAR(50),
    NationalIDNumber INT NOT NULL,
    BirthDate  VARCHAR(25),
    MaritalStatus VARCHAR(2),
    Gender      ENUM ('M','F')  NOT NULL,    
    HireDate   VARCHAR(25),
    PhoneNumber VARCHAR(20),
    EmailAddress VARCHAR(50),
    PRIMARY KEY (EmployeeID)
);

SHOW VARIABLES LIKE "secure_file_priv";
LOAD DATA INFILE "D:\\Desktop\\invento\\data\\Employees.csv"
INTO TABLE employees
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

select * from employees;
