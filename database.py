import sqlite3


DB = "ixxy.db"


def connect():
    return sqlite3.connect(DB)


def create():

    db = connect()
    cur = db.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY,
        username TEXT,
        created TEXT DEFAULT CURRENT_TIMESTAMP

    )
    """)


    db.commit()
    db.close()



def add_user(
    user_id,
    username
):

    db = connect()
    cur = db.cursor()


    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (id, username)
        VALUES (?,?)
        """,
        (
            user_id,
            username
        )
    )


    db.commit()
    db.close()



def users_count():

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM users"
    )

    result = cur.fetchone()[0]

    db.close()

    return result