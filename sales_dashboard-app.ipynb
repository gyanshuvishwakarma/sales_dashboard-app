{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4be17f40-5b0b-4ebf-be47-cf7c046e1020",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8050/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x1f97bd91fd0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\vishw\\AppData\\Local\\Temp\\ipykernel_10888\\2368794471.py:53: SettingWithCopyWarning:\n",
      "\n",
      "\n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import dash\n",
    "from dash import dcc, html\n",
    "import plotly.express as px\n",
    "\n",
    "# Load the dataset\n",
    "df = pd.read_csv(r\"C:\\Users\\vishw\\OneDrive\\Desktop\\sales23_cleaned.csv\")\n",
    "\n",
    "# Initialize the Dash app\n",
    "app = dash.Dash(__name__)\n",
    "\n",
    "# Layout of the dashboard\n",
    "app.layout = html.Div([\n",
    "    html.H1(\"📊 Sales Dashboard\", style={'textAlign': 'center'}),\n",
    "\n",
    "    # Dropdown for selecting Region\n",
    "    html.Div([\n",
    "        html.Label(\"Select Region:\"),\n",
    "        dcc.Dropdown(\n",
    "            id='region-dropdown',\n",
    "            options=[{'label': r, 'value': r} for r in df['Region'].unique()],\n",
    "            value='West',\n",
    "            multi=False\n",
    "        )\n",
    "    ], style={'width': '40%', 'margin': 'auto'}),\n",
    "\n",
    "    # Graphs\n",
    "    dcc.Graph(id='sales-by-category'),\n",
    "    dcc.Graph(id='profit-by-state'),\n",
    "    dcc.Graph(id='sales-trend')\n",
    "])\n",
    "\n",
    "# Callbacks for interactivity\n",
    "@app.callback(\n",
    "    [dash.dependencies.Output('sales-by-category', 'figure'),\n",
    "     dash.dependencies.Output('profit-by-state', 'figure'),\n",
    "     dash.dependencies.Output('sales-trend', 'figure')],\n",
    "    [dash.dependencies.Input('region-dropdown', 'value')]\n",
    ")\n",
    "def update_dashboard(selected_region):\n",
    "    # Filter data by region\n",
    "    filtered_df = df[df['Region'] == selected_region]\n",
    "\n",
    "    # Sales by Category\n",
    "    fig1 = px.bar(filtered_df, x='Category', y='Sales', color='Sub_Category',\n",
    "                  title=f\"Sales by Category in {selected_region}\", barmode='group')\n",
    "\n",
    "    # Profit by State\n",
    "    fig2 = px.bar(filtered_df.groupby('State', as_index=False).sum(),\n",
    "                  x='State', y='Profit', title=f\"Profit by State in {selected_region}\")\n",
    "\n",
    "    # Sales Trend over Time\n",
    "    filtered_df['Order_Date'] = pd.to_datetime(filtered_df['Order_Date'])\n",
    "    fig3 = px.line(filtered_df.sort_values('Order_Date'),\n",
    "                   x='Order_Date', y='Sales', color='Category',\n",
    "                   title=f\"Sales Trend in {selected_region}\")\n",
    "\n",
    "    return fig1, fig2, fig3\n",
    "\n",
    "# Run the app\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e264e8e8-803a-4448-b32e-07ec445de85f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
