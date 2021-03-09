DROP DATABASE IF EXISTS medical_center;

CREATE DATABASE medical_center;

\c medical_center

CREATE TABLE doctors
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE patients
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE diseases
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE doctors_patients
(
  id SERIAL PRIMARY KEY,
  doctor_id INTEGER REFERENCES doctors ON DELETE CASCADE,
  patient_id INTEGER REFERENCES patients ON DELETE CASCADE
);

CREATE TABLE patients_diseases
(
  id SERIAL PRIMARY KEY,
  patient_id INTEGER REFERENCES patients ON DELETE CASCADE,
  disease_id INTEGER REFERENCES diseases ON DELETE CASCADE
);