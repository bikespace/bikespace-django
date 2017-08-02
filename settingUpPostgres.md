#instructions:

LOG INTO POSTGRES (` su - postgres`) and run:

`createdb bicycle_parking;`

Next create a new user by running:

`createuser staff --pwprompt`
(in the config file for postgers I made the password `pw`, so if the password you add isn't `pw`, remember to change the config file)

Switch into the database (`psql`):

`\connect bicycle_parking`

Create a new table with:

`CREATE TABLE bicycle_parking_pins_tb (
  id BIGSERIAL NOT NULL PRIMARY KEY,
  ip varchar NOT NULL,
  latitude NUMERIC(8, 8) NOT NULL,
  longitude NUMERIC(8, 8) NOT NULL,
  point_timestamp integer NOT NULL,
  survey_answers json NOT NULL,
  comments varchar[] NOT NULL);`

Lastly, we have to grant PRIVILEGES to the new user
`GRANT ALL PRIVILEGES ON TABLE bicycle_parking_pins_tb TO staff;`
