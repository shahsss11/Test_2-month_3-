# C - R - U - D

purchases_table = """
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purchase TEXT NOT NULL,
        bought INTEGER DEFAULT 0,
        quantity INTEGER DEFAULT 1
    )
"""

# Create - создание записи
insert_purchase = 'INSERT INTO purchases (purchase, quantity) VALUES (?, ?)'

# Read - Просмотр записи
select_purchases = 'SELECT * FROM purchases'

select_purchases_bought = 'SELECT * FROM purchases WHERE bought = 1'

select_purchases_unbought = 'SELECT * FROM purchases WHERE bought = 0'


# Update - Обновить запись
update_purchase = 'UPDATE purchases SET purchase = ? WHERE id = ?'


# Delete - Удаление записи
delete_purchase = 'DELETE FROM purchases WHERE id = ?'

delete_bought_purchases = 'DELETE FROM purchases WHERE bought = 1'