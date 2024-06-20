import sqlite3
import pandas as pd

def fetch_data():
    conn = sqlite3.connect('transacoes.db')
    df = pd.read_sql_query("SELECT * FROM transacoes", conn)
    conn.close()
    return df

def export_to_excel(df, file_name):
    df.to_excel(file_name, index=False)

if __name__ == '__main__':
    df = fetch_data()
    file_name = 'transacoes.xlsx'
    export_to_excel(df, file_name)
    print(f'Dados exportados com sucesso para {file_name}')
