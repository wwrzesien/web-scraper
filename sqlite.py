import sqlite3
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

filename = 'record_database.db'

# ':memory:' -> for testing
try:
    conn = sqlite3.connect(filename)
except sqlite3.Error:
    logger.debug('Connection to database failed.')
c = conn.cursor()

"""Create a new table."""
c.execute("""CREATE TABLE record_players (
            nazwa text,
            typ_napedu text,
            typ_ramiena text,
            regulacja_obr text,
            sterowanie text,
            usb text,
            cena real
)""")
logger.info('Table has been created.')


conn.commit()


def insert_record_player(data):
    """Upload extracted data from website to database."""
    with conn:
        c.execute("""INSERT INTO record_players VALUES (
        :Nazwa, :Typ_napędu, :Typ_ramienia, :Regulacja_obrotów,
        :Sterowanie, :USB, :Cena)""", data)


def download_data():
    """Download data from database."""
    pass
