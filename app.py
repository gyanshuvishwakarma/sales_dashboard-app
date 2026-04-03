import os
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# ==============================
# FILE PATH (AUTO - NO ERROR)
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sales23_advanced.csv")

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"File not found: {CSV_PATH}")

print("Using file:", CSV_PATH)

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv(CSV_PATH)

# Clean columns
df.columns = df.columns.str.strip()

# Convert date
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')

# ==============================
# DASH APP
# ==============================
app = dash.Dash(__name__)
server = app.server  # for deployment

regions = sorted(df['Region'].dropna().unique())
quarters = sorted(df['Quarter'].dropna().unique())

# ==============================
# STYLES
# ==============================
BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#e2e8f0"

def card_style():
    return {
        'backgroundColor': CARD,
        'padding': '15px',
        'borderRadius': '10px',
        'minWidth': '180px',
        'textAlign': 'center',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.3)'
    }

# ==============================
# LAYOUT
# ==============================
app.layout = html.Div(style={
    'backgroundColor': BG,
    'color': TEXT,
    'padding': '20px',
    'fontFamily': 'Arial'
}, children=[

    html.H1("🚀 Advanced Sales Dashboard", style={'textAlign': 'center'}),

    # FILTERS
    html.Div([
        dcc.Dropdown(
            id='region',
            options=[{'label': r, 'value': r} for r in regions],
            value=regions[0] if regions else None,
            placeholder="Select Region",
            style={'width': '45%', 'color': 'black'}
        ),

        dcc.Dropdown(
            id='quarter',
            options=[{'label': q, 'value': q} for q in quarters],
            value=quarters[0] if quarters else None,
            placeholder="Select Quarter",
            style={'width': '45%', 'color': 'black'}
        ),
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),

    # KPI CARDS
    html.Div(id='kpis', style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'marginTop': '20px'
    }),

    # ROW 1
    html.Div([
        dcc.Graph(id='sales-category'),
        dcc.Graph(id='sales-pie'),
    ], style={'display': 'flex'}),

    # ROW 2
    html.Div([
        dcc.Graph(id='sales-trend'),
        dcc.Graph(id='discount-impact'),
    ], style={'display': 'flex'}),
])

# ==============================
# CALLBACK
# ==============================
@app.callback(
    [Output('kpis', 'children'),
     Output('sales-category', 'figure'),
     Output('sales-pie', 'figure'),
     Output('sales-trend', 'figure'),
     Output('discount-impact', 'figure')],
    [Input('region', 'value'),
     Input('quarter', 'value')]
)
def update_dashboard(region, quarter):

    data = df.copy()

    if region:
        data = data[data['Region'] == region]

    if quarter:
        data = data[data['Quarter'] == quarter]

    if data.empty:
        empty = px.scatter(title="No Data Available")
        return [html.Div("No Data")], empty, empty, empty, empty

    # KPIs
    total_sales = data['Sales'].sum()
    total_profit = data['Profit'].sum()
    avg_margin = data['Profit_Margin_%'].mean()
    orders = len(data)

    kpis = [
        html.Div([html.H3("Total Sales"), html.P(f"${total_sales:,.0f}")], style=card_style()),
        html.Div([html.H3("Total Profit"), html.P(f"${total_profit:,.0f}")], style=card_style()),
        html.Div([html.H3("Profit Margin"), html.P(f"{avg_margin:.2f}%")], style=card_style()),
        html.Div([html.H3("Orders"), html.P(f"{orders}")], style=card_style()),
    ]

    # CHART 1
    fig1 = px.bar(
        data.groupby('Category')['Sales'].sum().reset_index(),
        x='Category', y='Sales',
        title="Sales by Category",
        template='plotly_dark'
    )

    # CHART 2
    fig2 = px.pie(
        data,
        names='Sales_Category',
        values='Sales',
        title="Sales Distribution",
        template='plotly_dark'
    )

    # CHART 3
    fig3 = px.line(
        data.groupby('Order_Date')['Sales'].sum().reset_index(),
        x='Order_Date', y='Sales',
        title="Sales Trend",
        template='plotly_dark'
    )

    # CHART 4
    fig4 = px.bar(
        data.groupby('High_Discount')['Profit'].sum().reset_index(),
        x='High_Discount', y='Profit',
        title="Discount Impact on Profit",
        template='plotly_dark'
    )

    return kpis, fig1, fig2, fig3, fig4


# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8050)
    