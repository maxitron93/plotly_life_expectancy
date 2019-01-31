import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Read the data from the csv file
df = pd.read_csv('gapminderDataFiveYear.csv')

# Initialize the app
app = dash.Dash()
server = app.server

# Create the list of years for the year drop-down
year_options = []
for year in df['year'].unique():
  year_options.append({'label':str(year), 'value':year})

# Create the app layout
app.layout = html.Div([
  dcc.Dropdown(id='year-picker', options=year_options, value=df['year'].min()),
  dcc.Graph(id='graph')
])

# Connect the year picker drop down to the graph
@app.callback(Output('graph', 'figure'), [Input('year-picker', 'value')])


def update_figure(selected_year):
  # Data only for selected year from the dropdown
  filtered_df = df[df['year'] == selected_year]

  # Create a trace for each continent
  traces = []
  for continent_name in filtered_df['continent'].unique():
    df_by_continent = filtered_df[filtered_df['continent'] == continent_name]
    traces.append(go.Scatter(
      x = df_by_continent['gdpPercap'],
      y = df_by_continent['lifeExp'],
      mode = 'markers',
      opacity = 0.7,
      name = continent_name
    ))
  
  # Return the dictionary that will go inside the graph call
  return {'data': traces,
          'layout': go.Layout(title = 'Life Expectancy vs GDP per Capita',
                              xaxis = {'title':'GDP per Capita', 'type':'log'},
                              yaxis = {'title':'Live Expectancy'}
                              )}

if __name__ == '__main__':
  app.run_server()
