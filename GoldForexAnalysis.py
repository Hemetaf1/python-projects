import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, dcc, html, dash_table
import plotly.express as px


file_path = '/home/hemetaf/Downloads/Telegram Desktop/gold (2).xlsx'
data = pd.read_excel(file_path)


#print(data.isnull().sum())
#data = data.fillna(0)  # or use data.dropna()

data['Profit'] = data['Profit'].astype(str).str.replace(',', '.').astype(float)

data['Open Time'] = pd.to_datetime(data['Open Time'])
data['Close Time'] = pd.to_datetime(data['Close Time'])


data = data.fillna(0).drop_duplicates()

data = data[data['Symbol'] == 'XAUUSD']

profit_losses = data['Profit']


total_net_profit = profit_losses.sum()

gross_profit = profit_losses[profit_losses > 0].sum()
gross_loss = profit_losses[profit_losses < 0].sum()

num_profitable_trades = (profit_losses > 0).sum()
num_losing_trades = (profit_losses < 0).sum()

# cumulative profit
data = data.sort_values('Close Time')
data['Cumulative Profit'] = data['Profit'].cumsum()
print(data['Close Time'])

# Drawdown 
data['Cumulative Max'] = data['Cumulative Profit'].cummax()

# renumber the rows
data = data.reset_index(drop=True)

print(data.head())


data['Drawdown'] = data['Cumulative Max'] - data['Cumulative Profit']
max_drawdown = data['Drawdown'].max()

#Due to the unavailibility of the initial balance, I am not sure about max_drawdown_percentage
max_drawdown_percentage = (max_drawdown / data['Cumulative Max'].max()) * 100


# Volatility (Standard Deviation of Profit)
volatility = profit_losses.std()

average_profit = data[data['Profit'] > 0]['Profit'].mean()
average_loss = data[data['Profit'] < 0]['Profit'].mean()
risk_reward_ratio = average_profit / abs(average_loss)
print()

average_return = profit_losses.mean()
sharpe_ratio = average_return / volatility


gross_profit = data[data['Profit'] > 0]['Profit'].sum()
gross_loss = data[data['Profit'] < 0]['Profit'].sum()

num_profitable_trades = len(data[data['Profit'] > 0])
num_loss_trades = len(data[data['Profit'] < 0])

num_total_trades = len(data)
percentage_profit_trades = (num_profitable_trades / num_total_trades) * 100
percentage_loss_trades = (num_loss_trades / num_total_trades) * 100

expectancy = total_net_profit / num_total_trades

# Metrics results
results = {
    "Metric": [
        "Gross Profit",
        "Gross Loss",
        "Total Net Profit",
        "Profit Trades (% Of Total)",
        "Loss Trades (% Of Total)",
        "Total Number of Trades",
        "Maximum Drawdown",
        "Maximal Drawdown Percentage",
        "Volatility (Standard Deviation of Profit)",
        "Risk-Reward Ratio",
        "Sharpe Ratio",
        "Expectancy"
    ],
    "Value": [
        f"{gross_profit:.2f}",
        f"{gross_loss:.2f}",
        f"{total_net_profit:.2f}",
        f"{percentage_profit_trades:.2f}%",
        f"{percentage_loss_trades:.2f}%",
        num_total_trades,
        f"{max_drawdown:.2f}",
        f"{max_drawdown_percentage:.2f}%",
        f"{volatility:.2f}",
        f"{risk_reward_ratio:.2f}",
        f"{sharpe_ratio:.2f}",
        f"{expectancy:.2f}"
    ]
}

print(results)

# Check for any anomalies in the 'Profit' column
print("Describe CumProf Column:")
cumulative_profit_description = data['Cumulative Profit'].describe()



# Plot Cumulative Profit
plt.figure(figsize=(10, 6))
plt.plot(data['Close Time'], data['Cumulative Profit'], label='Cumulative Profit')
plt.title('Cumulative Profit Over Time')
plt.xlabel('Time')
plt.ylabel('Cumulative Profit')
plt.legend()
plt.grid(True)
plt.show()

# Plot Drawdown
plt.figure(figsize=(10, 6))
plt.plot(data['Close Time'], data['Drawdown'], label='Drawdown', color='red')
plt.title('Drawdown Over Time')
plt.xlabel('Time')
plt.ylabel('Drawdown')
plt.legend()
plt.grid(True)
plt.show()

# Plot Profit Distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['Profit'], bins=50, kde=True)
plt.title('Profit Distribution')
plt.xlabel('Profit')
plt.ylabel('Frequency')
plt.grid(True)    
plt.show()

plt.figure(figsize=(10, 6))  # Adjust the width as needed
plt.plot(data.index, data['Profit'], linestyle='-', color='b')
plt.title('Profits in Order of the Index')
plt.xlabel('Index')
plt.ylabel('Profit')
plt.grid(True)

'''
ax = plt.gca()
ax.xaxis.set_major_locator(MaxNLocator(nbins=100))  # Adjust nbins to control tick frequency
'''
plt.show()


###Dashboard
app = Dash(__name__)

cumulative_profit_fig = px.line(data, x='Close Time', y='Cumulative Profit', title='Cumulative Profit Over Time')
drawdown_fig = px.line(data, x='Close Time', y='Drawdown', title='Drawdown Over Time')
profit_dist_fig = px.histogram(data, x='Profit', nbins=50, title='Profit Distribution')
profit_index = px.line(data, x=data.index, y='Profit', title='Profit Over Index')

app.layout = html.Div(children=[
    html.H1(children='Trading Strategy Analysis Dashboard'),

    dcc.Graph(
        id='cumulative-profit',
        figure=cumulative_profit_fig
    ),
    
    dcc.Graph(
        id='drawdown',
        figure=drawdown_fig
    ),

    dcc.Graph(
        id='profit-dist',
        figure=profit_dist_fig
    ),
    dcc.Graph(
        id='profit-time',
        figure=profit_index
    ),

    html.H2(children='Metrics Report'),

    dash_table.DataTable(
        id='metrics-table',
        columns=[{"name": i, "id": i} for i in results.keys()],
        data=pd.DataFrame(results).to_dict('records'),
        style_table={'width': '50%', 'margin': 'auto'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '5px'
        },
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
