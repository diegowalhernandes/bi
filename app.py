import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
import plotly.express as px
import pandas as pd
import sqlite3

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def fetch_data():
    conn = sqlite3.connect('transacoes.db')
    df = pd.read_sql_query("SELECT * FROM transacoes", conn)
    conn.close()

    # Adiciona uma coluna 'tipo' baseada nas colunas 'data_entrada' e 'data_saida'
    df['tipo'] = df.apply(lambda row: 'entrada' if pd.notnull(row['data_entrada']) else 'saida', axis=1)

    print("Dados carregados do banco de dados:")
    print(df.head())  # Adiciona um print para verificar os dados carregados
    return df

app.layout = dbc.Container([
    dbc.Row([
        # Coluna da Esquerda - Filtros
        dbc.Col([
            html.H5("Filtros"),
            dcc.Dropdown(id='year-dropdown', placeholder='Ano', clearable=True),
            dcc.Dropdown(id='month-dropdown', placeholder='Mês', clearable=True),
            dcc.Dropdown(id='category-dropdown', placeholder='Categoria', clearable=True),
            dcc.Dropdown(id='type-dropdown', placeholder='Tipo', clearable=True)
        ], width=2),
        # Coluna do Centro - Cards e Gráficos
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Total de Entrada"),
                            html.H2(id="total-entrada", className="card-value")
                        ]), className="mb-4"
                    ),
                ], width=4),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Total de Saída"),
                            html.H2(id="total-saida", className="card-value")
                        ]), className="mb-4"
                    ),
                ], width=4),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Saldo"),
                            html.H2(id="saldo", className="card-value")
                        ]), className="mb-4"
                    ),
                ], width=4)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="expense-income-chart")
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="category-expense-chart")
                ], width=12)
            ])
        ], width=7),
        # Coluna da Direita - Tabela e Gráfico de Pizza
        dbc.Col([
            dash_table.DataTable(
                id='data-table',
                page_size=15,
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left'}
            ),
            dcc.Graph(id="income-expense-pie-chart")
        ], width=3)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Atualizar Dados", id="update-button", color="primary", className="mt-3"),
        ], width=2)
    ])
], fluid=True)

@app.callback(
    [Output("total-entrada", "children"),
     Output("total-saida", "children"),
     Output("saldo", "children"),
     Output("data-table", "data"),
     Output("data-table", "columns"),
     Output("expense-income-chart", "figure"),
     Output("category-expense-chart", "figure"),
     Output("income-expense-pie-chart", "figure"),
     Output("year-dropdown", "options"),
     Output("month-dropdown", "options"),
     Output("category-dropdown", "options"),
     Output("type-dropdown", "options")],
    [Input("update-button", "n_clicks"),
     Input("year-dropdown", "value"),
     Input("month-dropdown", "value"),
     Input("category-dropdown", "value"),
     Input("type-dropdown", "value")]
)
def update_dashboard(n_clicks, selected_year, selected_month, selected_category, selected_type):
    df = fetch_data()
    
    print("Verificando DataFrame:")
    print(df.head())

    if df.empty or 'tipo' not in df.columns or 'valor' not in df.columns or 'categoria' not in df.columns:
        print("DataFrame vazio ou colunas esperadas não encontradas.")
        total_entrada = "R$ 0,00"
        total_saida = "R$ 0,00"
        saldo = "R$ 0,00"
        data_table_data = []
        data_table_columns = []
        expense_income_fig = px.bar(title="Nenhuma transação encontrada.")
        category_expense_fig = px.bar(title="Nenhuma transação encontrada.")
        income_expense_pie_fig = px.pie(title="Nenhuma transação encontrada.")
        year_options = []
        month_options = []
        category_options = []
        type_options = []
    else:
        print("DataFrame contém os dados esperados.")
        
        # Aplicar filtros
        if selected_year:
            df = df[df['data_entrada'].str.startswith(selected_year) | df['data_saida'].str.startswith(selected_year)]
        if selected_month:
            df = df[df['data_entrada'].str[5:7] == selected_month | df['data_saida'].str[5:7] == selected_month]
        if selected_category:
            df = df[df['categoria'] == selected_category]
        if selected_type:
            df = df[df['tipo'] == selected_type]
        
        # Calcula os totais de entrada, saída e saldo
        total_entrada = df[df['tipo'] == 'entrada']['valor'].sum() if 'entrada' in df['tipo'].unique() else 0
        total_saida = df[df['tipo'] == 'saida']['valor'].sum() if 'saida' in df['tipo'].unique() else 0
        saldo = total_entrada - total_saida
        
        # Calcula o maior e menor valor
        maior_valor = df['valor'].max() if not df['valor'].empty else 0
        menor_valor = df['valor'].min() if not df['valor'].empty else 0
        
        print("Totais calculados:")
        print(f"Total de Entrada: {total_entrada}")
        print(f"Total de Saída: {total_saida}")
        print(f"Saldo: {saldo}")

        total_entrada = f"R$ {total_entrada:,.2f}"
        total_saida = f"R$ {total_saida:,.2f}"
        saldo = f"R$ {saldo:,.2f}"
        
        # Configura a tabela de dados
        data_table_data = df.to_dict('records')
        data_table_columns = [{'name': col, 'id': col} for col in df.columns]
        
        # Gráfico de Despesas x Receita
        expense_income_fig = px.bar(df, x='categoria', y='valor', color='tipo', barmode='group', title='Despesas x Receita', labels={'valor': 'Valor', 'categoria': 'Categoria', 'tipo': 'Tipo'})
        
        # Gráfico de Despesas por Categoria
        category_expense_fig = px.bar(df[df['tipo'] == 'saida'], x='categoria', y='valor', title='Despesas por Categoria', labels={'valor': 'Valor', 'categoria': 'Categoria'})
        
        # Gráfico de Pizza (Receita vs Despesas)
        income_expense_pie_fig = px.pie(values=[total_entrada, total_saida], names=['Entrada', 'Saída'], title='Distribuição entre Receita e Despesas')
        
        # Opções para dropdowns
        year_options = [{'label': year, 'value': year} for year in sorted(df['data_entrada'].dropna().apply(lambda x: x[:4]).unique())]
        month_options = [{'label': month, 'value': month} for month in sorted(df['data_entrada'].dropna().apply(lambda x: x[5:7]).unique())]
        category_options = [{'label': category, 'value': category} for category in sorted(df['categoria'].unique())]
        type_options = [{'label': tipo, 'value': tipo} for tipo in sorted(df['tipo'].unique())]

    return total_entrada, total_saida, saldo, data_table_data, data_table_columns, expense_income_fig, category_expense_fig, income_expense_pie_fig, year_options, month_options, category_options, type_options

if __name__ == '__main__':
    app.run_server(debug=True, port=5001)
