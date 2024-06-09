import sqlite3

def list_tables():
    conn = sqlite3.connect('transacoes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return tables

if __name__ == '__main__':
    tables = list_tables()
    print("Tabelas no banco de dados:")
    for table in tables:
        print(table[0])
