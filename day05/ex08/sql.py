
""" 
◦ id: serial, primary key
◦ name: unique, variable character chain, 64 byte maximum size, non null.
◦ climate: variable character chain.
◦ diameter: whole.
◦ orbital_period: whole.
◦ population: large whole.
◦ rotation_period: whole.
◦ surface_water: real.
◦ terrain: variable character chain, 128 bytes maximum size


ex08_people
◦ id: serial, primary key.
◦ name: unique, variable character chain, 64 byte maximum size, non null.
◦ birth_year: variable character chain, 32 byte maximum size.
◦ gender: variable character chain, 32 byte maximum size.
◦ eye_color: variable character chain, 32 byte maximum size.
◦ hair_color: variable character chain, 32 byte maximum size.
◦ height: whole.
◦ mass: real.
◦ homeworld: variable character chain, 64 byte maximum size, foreign key, referencing the name column of the 08_planets table.

 """


ex08_planets = """
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR(64),
                diameter INT,
                orbital_period INT,
                population BIGINT ,
                rotation_period INT,
                surface_water REAL,
                terrain VARCHAR(128)
            );
        """

ex08_people = """
            CREATE TABLE IF NOT EXISTS ex08_people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INT,
                mass REAL,
                homeworld VARCHAR(64),
                FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
            );
        """