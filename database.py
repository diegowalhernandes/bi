import sqlite3

def init_db():
    conn = sqlite3.connect('transacoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY,
            data_entrada TEXT,
            data_saida TEXT,
            valor REAL,
            categoria TEXT,
            empresa TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
