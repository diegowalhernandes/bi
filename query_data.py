import sqlite3

def query_data():
    conn = sqlite3.connect('transacoes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    rows = query_data()
    print("Transações no banco de dados:")
    for row in rows:
        print(row)
