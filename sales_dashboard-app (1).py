import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load the dataset
# Make sure the CSV path is accessible or update the path accordingly
# df = pd.read_csv(r"C:\Users\vishw\OneDrive\Desktop\sales23_cleaned.csv")

# Example placeholder DataFrame until dataset is available
# Remove or replace this when using the real CSV
sample_data = {
    'Region': ['West', 'West', 'East', 'East'],
    'Category': ['Furniture', 'Office Supplies', 'Technology', 'Furniture'],
    'Sub_Category': ['Chairs', 'Paper', 'Phones', 'Tables'],
    'State': ['CA', 'CA', 'NY', 'NY'],
    'Sales': [200, 150, 300, 400],
    'Profit': [50, 20, 80, 110],
    'Order_Date': ['2023-01-01', '2023-02-15', '2023-01-10', '2023-03-05']
}
df = pd.DataFrame(sample_data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("📊 Sales Dashboard", style={'textAlign': 'center'}),

    # Dropdown for selecting Region
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': r, 'value': r} for r in df['Region'].unique()],
            value=df['Region'].iloc[0] if not df.empty else None,
            multi=False
        )
    ], style={'width': '40%', 'margin': 'auto'}),

    # Graphs
    dcc.Graph(id='sales-by-category'),
    dcc.Graph(id='profit-by-state'),
    dcc.Graph(id='sales-trend')
])

# Callbacks for interactivity
@app.callback(
    [dash.dependencies.Output('sales-by-category', 'figure'),
     dash.dependencies.Output('profit-by-state', 'figure'),
     dash.dependencies.Output('sales-trend', 'figure')],
    [dash.dependencies.Input('region-dropdown', 'value')]
)
def update_dashboard(selected_region):
    # Filter data by region
    filtered_df = df[df['Region'] == selected_region]

    # Sales by Category
    fig1 = px.bar(filtered_df, x='Category', y='Sales', color='Sub_Category',
                  title=f"Sales by Category in {selected_region}", barmode='group')

    # Profit by State
    fig2 = px.bar(filtered_df.groupby('State', as_index=False).sum(),
                  x='State', y='Profit', title=f"Profit by State in {selected_region}")

    # Sales Trend over Time
    filtered_df['Order_Date'] = pd.to_datetime(filtered_df['Order_Date'])
    fig3 = px.line(filtered_df.sort_values('Order_Date'),
                   x='Order_Date', y='Sales', color='Category',
                   title=f"Sales Trend in {selected_region}")

    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
