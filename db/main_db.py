import sqlite3

from config import path_db
from db import queries


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.purchases_table)
    conn.commit()
    conn.close()


def add_purchase(purchase):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.insert_purchase, (purchase,))
    conn.commit()
    purchase_id = cursor.lastrowid
    conn.close()
    return purchase_id


def update_purchase(purchase_id, new_purchase=None, bought=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if new_purchase is not None:
        cursor.execute(queries.update_purchase, (new_purchase, purchase_id))

    elif bought is not None:
        cursor.execute(
            "UPDATE purchases SET bought = ? WHERE id = ?",
            (bought, purchase_id)
        )

    conn.commit()
    conn.close()


def get_purchase(filter_type):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == 'all':
        cursor.execute(queries.select_purchases)
    elif filter_type == 'bought':
        cursor.execute(queries.select_purchases_bought)
    elif filter_type == 'unbought':
        cursor.execute(queries.select_purchases_unbought)

    purchases = cursor.fetchall()
    conn.close()
    return purchases


def delete_bought_purchases():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM purchases WHERE bought = 1")
    conn.commit()
    conn.close()

def delete_purchase(purchase_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM purchases WHERE id = ?", (purchase_id,))
    conn.commit()
    conn.close()
