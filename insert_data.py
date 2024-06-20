import sqlite3

# Lista de transações a ser inserida
transacoes = [
    {"data_entrada": "2024-01-10", "valor": 150.75, "categoria": "Alimentação", "empresa": "Supermercado XYZ"},
    {"data_saida": "2024-02-10", "valor": 80.00, "categoria": "Transporte", "empresa": "Empresa de Táxi ABC"},
    {"data_entrada": "2024-03-12", "valor": 200.00, "categoria": "Entretenimento", "empresa": "Cinema 123"},
    {"data_saida": "2024-04-25", "valor": 300.50, "categoria": "Educação", "empresa": "Curso de Inglês DEF"},
    {"data_entrada": "2024-05-08", "data_saida": "2024-05-12", "valor": 450.00, "categoria": "Saúde", "empresa": "Clínica Médica GHI"},
    {"data_entrada": "2024-06-01", "valor": 120.00, "categoria": "Lazer", "empresa": "Parque de Diversões"},
    {"data_saida": "2024-07-15", "valor": 95.50, "categoria": "Alimentação", "empresa": "Restaurante ABC"},
    {"data_entrada": "2024-08-20", "valor": 300.00, "categoria": "Transporte", "empresa": "Aluguel de Carros XYZ"},
    {"data_saida": "2024-09-05", "valor": 180.00, "categoria": "Educação", "empresa": "Libraria 123"},
    {"data_entrada": "2024-10-12", "data_saida": "2024-10-15", "valor": 250.75, "categoria": "Saúde", "empresa": "Farmácia ABC"},
    {"data_entrada": "2024-11-22", "valor": 170.00, "categoria": "Entretenimento", "empresa": "Teatro XYZ"},
    {"data_saida": "2024-12-31", "valor": 200.00, "categoria": "Alimentação", "empresa": "Padaria DEF"},
    {"data_entrada": "2025-01-10", "valor": 320.00, "categoria": "Lazer", "empresa": "Cinema 456"},
    {"data_saida": "2025-02-20", "valor": 150.00, "categoria": "Transporte", "empresa": "Táxi 789"},
    {"data_entrada": "2025-03-05", "data_saida": "2025-03-10", "valor": 450.00, "categoria": "Educação", "empresa": "Curso de Idiomas"},
    {"data_entrada": "2025-04-15", "valor": 90.00, "categoria": "Saúde", "empresa": "Clínica XYZ"},
    {"data_saida": "2025-05-25", "valor": 130.00, "categoria": "Entretenimento", "empresa": "Show de Música"},
    {"data_entrada": "2025-06-18", "data_saida": "2025-06-20", "valor": 200.00, "categoria": "Alimentação", "empresa": "Restaurante 123"},
    {"data_entrada": "2025-07-08", "valor": 140.00, "categoria": "Lazer", "empresa": "Clube ABC"},
    {"data_saida": "2025-08-12", "valor": 190.00, "categoria": "Transporte", "empresa": "Locadora de Carros"},
    {"data_entrada": "2025-09-22", "data_saida": "2025-09-25", "valor": 270.50, "categoria": "Educação", "empresa": "Escola de Dança"},
    {"data_entrada": "2025-10-14", "valor": 160.00, "categoria": "Saúde", "empresa": "Hospital 123"},
    {"data_saida": "2025-11-30", "valor": 220.00, "categoria": "Entretenimento", "empresa": "Cinema ABC"},
    {"data_entrada": "2025-12-05", "data_saida": "2025-12-10", "valor": 310.75, "categoria": "Alimentação", "empresa": "Mercado XYZ"},
    {"data_entrada": "2026-01-15", "valor": 100.00, "categoria": "Lazer", "empresa": "Parque Aquático"},
    {"data_saida": "2026-02-25", "valor": 140.00, "categoria": "Transporte", "empresa": "Serviço de Táxi"},
    {"data_entrada": "2026-03-08", "data_saida": "2026-03-12", "valor": 290.50, "categoria": "Educação", "empresa": "Faculdade ABC"},
    {"data_entrada": "2026-04-20", "valor": 180.00, "categoria": "Saúde", "empresa": "Consultório Médico"},
    {"data_saida": "2026-05-10", "valor": 150.00, "categoria": "Entretenimento", "empresa": "Evento Cultural"},
    {"data_entrada": "2026-06-18", "data_saida": "2026-06-22", "valor": 240.00, "categoria": "Alimentação", "empresa": "Restaurante DEF"},
    {"data_entrada": "2026-07-08", "valor": 170.00, "categoria": "Lazer", "empresa": "Parque de Diversões XYZ"},
    {"data_saida": "2026-08-15", "valor": 200.00, "categoria": "Transporte", "empresa": "Aluguel de Carros ABC"},
    {"data_entrada": "2026-09-22", "data_saida": "2026-09-28", "valor": 275.50, "categoria": "Educação", "empresa": "Curso de Informática"},
    {"data_entrada": "2026-10-14", "valor": 120.00, "categoria": "Saúde", "empresa": "Laboratório de Análises"},
    {"data_saida": "2026-11-30", "valor": 250.00, "categoria": "Entretenimento", "empresa": "Cinema XYZ"},
    {"data_entrada": "2026-12-05", "data_saida": "2026-12-12", "valor": 310.00, "categoria": "Alimentação", "empresa": "Supermercado ABC"}
]

# Função para inserir os dados
def insert_data(transacoes):
    conn = sqlite3.connect('transacoes.db')
    cursor = conn.cursor()
    
    for transacao in transacoes:
        cursor.execute('''
            INSERT INTO transacoes (data_entrada, data_saida, valor, categoria, empresa)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            transacao.get("data_entrada"),
            transacao.get("data_saida"),
            transacao["valor"],
            transacao["categoria"],
            transacao["empresa"]
        ))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_data(transacoes)
    print("Dados inseridos com sucesso!")
