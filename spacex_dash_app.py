# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
	# TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] +
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),
	
	TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
	
	# TASK 3: Add a slider to select payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload, max=max_payload,
                    step=1000,  # Adjust step as needed
                    marks={i: '{}'.format(i) for i in range(int(min_payload), int(max_payload)+1, 5000)},
                    value=[min_payload, max_payload]
                    ),
    
	# TASK 4: Add a scatter chart to show the correlation between payload and launch success
	html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Pie Chart Callback
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Total Success Launches for site {selected_site}')
    return fig

# TASK 4: Scatter Chart Callback
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                     color="Booster Version Category",
                     title='Correlation between Payload and Success for all Sites' if selected_site == 'ALL' 
                           else f'Correlation between Payload and Success for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()