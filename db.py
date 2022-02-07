import sqlite3


def get_db():
        db = sqlite3.connect("pythonchallenge", detect_types=sqlite3.PARSE_DECLTYPES)
        db.row_factory = sqlite3.Row
        print("Successful connection to db", db)

        try:
            create = db.execute("""create table pythonchallengetable (
                                      id integer primary key autoincrement,
                                      city text,
                                      language text,
                                      total_time text,
                                      mean_time text,
                                      min_time text,
                                      max_time text

                                )""")
            print(f"Table pythonchallengetable is created in {db}", create)
        except sqlite3.OperationalError:
            print(f"Table already exists in {db} ")

        return db


def insert_db(db, countries: str, regions: str, time_data):

    insert = db.execute(
        'INSERT INTO pythonchallengetable (city, language, total_time, mean_time, min_time, max_time) VALUES (?, ?, ?, ?, ?, ?)',
        (str(countries), str(regions), time_data['total'], time_data['mean'], time_data['min'], time_data['max'])
    )

    print(f"Saved data {insert} ")

    return insert
