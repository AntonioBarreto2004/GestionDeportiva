create database sport_management;

use sport_management;

CREATE TABLE Allergies (
  id INT NULL AUTO_INCREMENT PRIMARY KEY,
  allergie_name VARCHAR(45) NOT NULL,
  description TEXT NOT NULL
  );

CREATE TABLE disabilities (
  id INT NULL AUTO_INCREMENT,
  disability_name VARCHAR(45) NOT NULL,
  description TEXT NOT NULL
  );

CREATE TABLE rol (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name_rol VARCHAR(20) NOT NULL
  );

CREATE TABLE people (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  last_name VARCHAR(230) NOT NULL,
  photo_user VARCHAR(255) NOT NULL,
  birthdate DATE NOT NULL,
  gender ENUM('Masculino', 'Femenino') NOT NULL,
  telephone_number VARCHAR(10) NOT NULL,
  date_create DATE NOT NULL,
  type_document_id ENUM('Cedula de Ciudadania', 'Tarjeta de Identidad', 'Registro Civil') NOT NULL,
  num_document INT(11) NOT NULL,
  Allergies_id INT NOT NULL,
  disabilities_id INT NOT NULL,
  file VARCHAR(255) NOT NULL,
  file_v VARCHAR(255) NOT NULL,
  file_f VARCHAR(255) NOT NULL,
  modified_at DATETIME NOT NULL,
  is_instructors TINYINT(4) NULL DEFAULT NULL,
  FOREIGN KEY (Allergies_id) REFERENCES Allergies (id),
  FOREIGN KEY (disabilities_id) REFERENCES disabilities (id)
 );
 
 CREATE TABLE user (
  id INT(11) NOT NULL AUTO_INCREMENT,
  people_id INT(11) NOT NULL,
  rol_id INT(11) NOT NULL,
  is_staff TINYINT(4) NULL DEFAULT 0,
  is_active TINYINT(1) NULL DEFAULT 1,
  password VARCHAR(128) NOT NULL,
  FOREIGN KEY (rol_id) REFERENCES rol (id),
  FOREIGN KEY (people_id) REFERENCES people (id)
  );
 
 CREATE TABLE instructors (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  people_id INT(11) NOT NULL,
  specialization VARCHAR(100) NOT NULL,
  experience_years INT(11) NOT NULL,
  FOREIGN KEY (people_id) REFERENCES people(id)
);

CREATE TABLE sports (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  sport_name VARCHAR(30) NOT NULL,
  description VARCHAR(256) NULL DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
  );
  
CREATE TABLE athlete (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  instructor_id INT(11) NULL,
  people_id INT(11) NOT NULL,
  at_technicalv VARCHAR(50) NOT NULL,
  at_tacticalv VARCHAR(50) NOT NULL,
  at_physicalv VARCHAR(50) NOT NULL,
  sports_id INT(11) NOT NULL,
  FOREIGN KEY (instructor_id) REFERENCES instructors (id),
  FOREIGN KEY (people_id)REFERENCES people (id),
  FOREIGN KEY (sports_id)REFERENCES sports (id)
);

CREATE TABLE team (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  team_name VARCHAR(40) NOT NULL,
  sport_id INT(11) NOT NULL,
  team_image VARCHAR(255) NOT NULL,
  date_create_Team TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  description VARCHAR(256) NULL DEFAULT NULL,
  instructors_id INT(11) NOT NULL,
  FOREIGN KEY (sport_id) REFERENCES sports (id),
  FOREIGN KEY (instructors_id) REFERENCES instructors (id)
);

CREATE TABLE athlete_team (
  athlete_id INT(11) NOT NULL,
  team_id INT(11) NOT NULL,
  dorsal INT(11) NOT NULL,
  positions_initial VARCHAR(45) NOT NULL,
  position_alternative VARCHAR(45) NOT NULL,
  FOREIGN KEY (athlete_id) REFERENCES athlete (id),
  FOREIGN KEY (team_id) REFERENCES team (id)
);

CREATE TABLE category (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  sport_id INT(11) NOT NULL,
  category_type ENUM('Individual', 'Por Equipos') NULL DEFAULT NULL,
  c_name VARCHAR(30) NOT NULL,
  date_create_Category TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  FOREIGN KEY (sport_id) REFERENCES sports (id)
  );

CREATE TABLE tournaments (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name_tournament VARCHAR(100) NOT NULL,
  athlete_id INT(11) NULL,
  team_id INT(11) NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  description TEXT NULL DEFAULT NULL,
  tournament_type ENUM('Individual', 'Team', 'Knockout') NOT NULL,
  max_teams INT(11) NULL DEFAULT NULL,
  max_participants_per_ethlete INT(11) NULL DEFAULT NULL,
  location VARCHAR(100) NULL DEFAULT NULL,
  prize VARCHAR(100) NULL DEFAULT NULL,
  registration_fee DECIMAL(10,0) NULL,
  enrollment_status TINYINT NOT NULL,
  FOREIGN KEY (athlete_id) REFERENCES athlete (id),
  FOREIGN KEY (team_id) REFERENCES team (id)
);

CREATE TABLE programming_tournaments (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  tournament_id INT(11) NOT NULL,
  score INT NULL,
  position INT NULL,
  matches_played INT NULL,
  win INT NULL,
  lose INT NULL,
  draw INT NULL,
  penalty_score INT NULL,
  registration_date DATE NOT NULL,
  status VARCHAR(255) NOT NULL,
  FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
);

CREATE TABLE services (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  service_name VARCHAR(40) NOT NULL,
  service_status TINYINT(1) NULL DEFAULT NULL,
  description TEXT NULL DEFAULT NULL,
  service_value DECIMAL(10,0) NULL DEFAULT NULL,
  start_date DATE NULL DEFAULT NULL,
  end_date DATE NULL DEFAULT NULL
  );

CREATE TABLE receipt_payment (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  r_athlete INT(11) NOT NULL,
  r_service INT(11) NOT NULL,
  pay_day DATE NULL DEFAULT NULL,
  full_value DECIMAL(10,2) NULL DEFAULT NULL,
  FOREIGN KEY (r_athlete) REFERENCES athlete (id),
  FOREIGN KEY (r_service)REFERENCES services (id)
  );
  
CREATE TABLE anthropometric (
  id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  athlete_id INT(11) NOT NULL,
  atpt_controlDate DATE NOT NULL,
  atpt_arm INT(11) NOT NULL,
  atpt_chest VARCHAR(45) NOT NULL,
  atpt_hip INT(11) NOT NULL,
  atpt_calf INT(11) NOT NULL,
  atpt_humerus INT(11) NOT NULL,
  atpt_femur INT(11) NOT NULL,
  atpt_wrist INT(11) NOT NULL,
  atpt_triceps INT(11) NOT NULL,
  atpt_suprailiac INT(11) NOT NULL,
  atpt_pectoral INT(11) NOT NULL,
  atpt_height INT(11) NOT NULL,
  atpt_weight INT(11) NOT NULL,
  atpt_bmi INT(11) NOT NULL,
  atpt_updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  FOREIGN KEY (athlete_id) REFERENCES athlete(id)
);

  

