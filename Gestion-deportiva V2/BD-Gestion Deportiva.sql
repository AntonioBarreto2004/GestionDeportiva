
CREATE TABLE Allergies (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  description TEXT NOT NULL,
  status BOOLEAN
);

CREATE TABLE disabilities (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  description TEXT NOT NULL,
  status BOOLEAN
);

CREATE TABLE specialConditions (
  id SERIAL PRIMARY KEY,
  name VARCHAR(45) NOT NULL,
  description TEXT NOT NULL,
  status BOOLEAN
);

CREATE TABLE rol (
  id SERIAL PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  description TEXT,
  status BOOLEAN
);

CREATE TABLE people (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  last_name VARCHAR(230) NOT NULL,
  photo_user BYTEA,
  birthdate DATE NOT NULL,
  gender VARCHAR(10) NOT NULL,
  telephone_number VARCHAR(10) NOT NULL,
  date_create DATE NOT NULL,
  type_document VARCHAR(20) NOT NULL,
  num_document INT NOT NULL,
  file_documentIdentity BYTEA,
  file_EPS_certificate BYTEA,
  file_informed_consent BYTEA,
  modified_at TIMESTAMP NOT NULL
);

CREATE TABLE peopleAllergies (
  id SERIAL PRIMARY KEY,
  people_id INT,
  allergies_id INT,
  FOREIGN KEY (people_id) REFERENCES people(id),
  FOREIGN KEY (allergies_id) REFERENCES Allergies(id)
);

CREATE TABLE peopleDisabilities (
  id SERIAL PRIMARY KEY,
  people_id INT,
  disabilities_id INT,
  FOREIGN KEY (people_id) REFERENCES people(id),
  FOREIGN KEY (disabilities_id) REFERENCES disabilities(id)
);

CREATE TABLE peopleSpecialConditions (
  id SERIAL PRIMARY KEY,
  people_id INT,
  specialConditions_id INT,
  FOREIGN KEY (people_id) REFERENCES people(id),
  FOREIGN KEY (specialConditions_id) REFERENCES specialConditions(id)
);

CREATE TABLE "user" (
  id SERIAL PRIMARY KEY,
  people_id INT,
  rol_id INT,
  is_active BOOLEAN,
  password VARCHAR(128) NOT NULL,
  last_login TIMESTAMP,
  FOREIGN KEY (rol_id) REFERENCES rol(id),
  FOREIGN KEY (people_id) REFERENCES people(id)
);

CREATE TABLE instructors (
  id SERIAL PRIMARY KEY,
  people_id INT,
  specialization INT,
  experience_years INT NOT NULL,
  FOREIGN KEY (people_id) REFERENCES people(id)
);

create table specialization(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description text(250),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create table instructor_specialization(
  id SERIAL PRIMARY KEY,
  instructor_id int,
  specialization_id int,
  FOREIGN KEY (instructor_id) REFERENCES instructors(id),
  FOREIGN KEY (specialization_id) REFERENCES specialization(id)
);

CREATE TABLE sports (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30) NOT NULL,
  description VARCHAR(256),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status BOOLEAN
);

CREATE TABLE athlete (
  id SERIAL PRIMARY KEY,
  people_id INT NOT NULL,
  technical VARCHAR(50) NOT NULL,
  tactical VARCHAR(50) NOT NULL,
  physical VARCHAR(50) NOT NULL,
  sports_id INT,
  status BOOLEAN,
  FOREIGN KEY (people_id) REFERENCES people(id),
  FOREIGN KEY (sports_id) REFERENCES sports(id)
);

CREATE TABLE athlete_instructor (
  id SERIAL PRIMARY KEY,
  athlete_id INT,
  instructor_id INT,
  FOREIGN KEY (athlete_id) REFERENCES athlete(id),
  FOREIGN KEY (instructor_id) REFERENCES instructors(id)
);

CREATE TABLE team (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  sport_id INT NOT NULL,
  image VARCHAR(255) NOT NULL,
  date_create_Team TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  description VARCHAR(256),
  instructors_id INT NOT NULL,
  FOREIGN KEY (sport_id) REFERENCES sports (id),
  FOREIGN KEY (instructors_id) REFERENCES instructors (id)
);

CREATE TABLE athlete_team (
  id SERIAL PRIMARY KEY,
  athlete_id INT NOT NULL,
  team_id INT NOT NULL,
  dorsal INT NOT NULL,
  positions_initial VARCHAR(45) NOT NULL,
  position_alternative VARCHAR(45) NOT NULL,
  FOREIGN KEY (athlete_id) REFERENCES athlete (id),
  FOREIGN KEY (team_id) REFERENCES team (id)
);

CREATE TABLE category (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30) NOT NULL,
  description TEXT,
  date_create TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE category_sports (
  id SERIAL PRIMARY KEY,
  category_id INT NOT NULL,
  sport_id INT NOT NULL,
  FOREIGN KEY (category_id) REFERENCES category(id),
  FOREIGN KEY (sport_id) REFERENCES sports(id)
);

CREATE TABLE tournaments (
  id SERIAL PRIMARY KEY,
  name_tournament VARCHAR(100) NOT NULL,
  athlete_id INT,
  team_id INT,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  description TEXT,
  max_teams INT,
  max_participants_ethlete INT,
  location VARCHAR(100),
  prize VARCHAR(100),
  registration_fee DECIMAL(10,0),
  enrollment_status BOOLEAN NOT NULL,
  FOREIGN KEY (athlete_id) REFERENCES athlete (id),
  FOREIGN KEY (team_id) REFERENCES team (id)
);

CREATE TABLE programming_tournaments (
  id SERIAL PRIMARY KEY,
  tournament_id INT NOT NULL,
  score INT,
  position INT,
  matches_played INT,
  win INT,
  lose INT,
  tie INT,
  penalty_score INT,
  registration_date DATE NOT NULL,
  status VARCHAR(255) NOT NULL,
  FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
);

CREATE TABLE services (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  status BOOLEAN,
  description TEXT,
  service_value DECIMAL(10,0),
  start_date DATE,
  end_date DATE
);

CREATE TABLE receipt_payment (
  id SERIAL PRIMARY KEY,
  athlete INT NOT NULL,
  service INT NOT NULL,
  pay_day DATE,
  full_value DECIMAL(10,2),
  FOREIGN KEY (athlete) REFERENCES athlete (id),
  FOREIGN KEY (service) REFERENCES services (id)
);

CREATE TABLE anthropometric (
  id SERIAL PRIMARY KEY,
  athlete_id INT NOT NULL,
  controlDate DATE NOT NULL,
  arm INT,
  chest VARCHAR(45),
  hip INT,
  twin INT,
  humerus INT,
  femur INT,
  wrist INT,
  triceps INT,
  supraspinal INT,
  pectoral INT,
  zise INT,
  weight INT,
  bmi INT,
  updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (athlete_id) REFERENCES athlete(id)
);


