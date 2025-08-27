DROP DATABASE IF EXISTS ShelterDB;
CREATE DATABASE ShelterDB;

USE ShelterDB;

CREATE TABLE Shelter (
    ShelterID INT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL
);

CREATE TABLE Dog (
    AnimalID INT PRIMARY KEY,
    Breed VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Age INT NOT NULL,
    Vaccinated BOOLEAN NOT NULL,
    ReadyForAdoption BOOLEAN NOT NULL,
    ShelterID INT,
    FoodType VARCHAR(50) NOT NULL,
    DailyFoodAmount INT NOT NULL,
    FOREIGN KEY (ShelterID) REFERENCES Shelter(ShelterID)
);

CREATE TABLE Cat (
    AnimalID INT PRIMARY KEY,
    Breed VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Age INT NOT NULL,
    Vaccinated BOOLEAN NOT NULL,
    Neutered BOOLEAN NOT NULL,
    ShelterID INT,
    LitterType VARCHAR(50) NOT NULL,
    DailyLitterAmount INT NOT NULL,
    FOREIGN KEY (ShelterID) REFERENCES Shelter(ShelterID)
);

CREATE TABLE Bird (
    AnimalID INT PRIMARY KEY,
    Species VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Age INT NOT NULL,
    Vaccinated BOOLEAN NOT NULL,
    CanFly BOOLEAN NOT NULL,
    ShelterID INT,
    CageSize VARCHAR(50) NOT NULL,
    FOREIGN KEY (ShelterID) REFERENCES Shelter(ShelterID)
);