import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import sqlite3

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Inserir Transações"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data de Entrada"),
                    dbc.Input(id="data-entrada", type="date"),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data de Saída"),
                    dbc.Input(id="data-saida", type="date"),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Valor"),
                    dbc.Input(id="valor", type="number", step=0.01),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Categoria"),
                    dbc.Input(id="categoria", type="text"),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Empresa"),
                    dbc.Input(id="empresa", type="text"),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Adicionar", id="submit-button", color="primary", className="mt-3"),
                ]),
            ]),
            html.Div(id="output-message", className="mt-3")
        ], width=6)
    ])
])

@app.callback(
    Output("output-message", "children"),
    Input("submit-button", "n_clicks"),
    State("data-entrada", "value"),
    State("data-saida", "value"),
    State("valor", "value"),
    State("categoria", "value"),
    State("empresa", "value")
)
def update_output(n_clicks, data_entrada, data_saida, valor, categoria, empresa):
    if n_clicks is not None and all([data_entrada, valor, categoria, empresa]):
        conn = sqlite3.connect('transacoes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transacoes (data_entrada, data_saida, valor, categoria, empresa)
            VALUES (?, ?, ?, ?, ?)
        ''', (data_entrada, data_saida, valor, categoria, empresa))
        conn.commit()
        conn.close()
        return "Transação adicionada com sucesso!"
    return "Por favor, preencha todos os campos obrigatórios."

if __name__ == '__main__':
    app.run_server(debug=True, port=5001)
