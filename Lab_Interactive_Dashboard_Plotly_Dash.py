# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
	children = [
		html.H1(
			'SpaceX Launch Records Dashboard',
			style = {
				'textAlign': 'center', 
				'color': '#503D36',
				'font-size': 40
			}
		),
		# TASK 1: Add a dropdown list to enable Launch Site selection
		# The default select value is for ALL sites
		dcc.Dropdown(
			id = 'site-dropdown',
			options =
			[
				{'label': 'All Sites', 'value': 'ALL'},
				{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
				{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
				{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
				{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
			],
			value = 'ALL',
			placeholder = 'Select a Launch Site here',
			searchable = True
		),
		html.Br(),

		# TASK 2: Add a pie chart to show the total successful launches count for all sites
		# If a specific launch site was selected, show the Success vs. Failed counts for the site
		html.Div(dcc.Graph(id = 'success-pie-chart')),
		html.Br(),

		html.P("Payload range (Kg):"),
		# TASK 3: Add a slider to select payload range
		dcc.RangeSlider(
			id = 'payload-slider',
			min = 0, 
			max = 10000, 
			step = 1000,
			marks = {
				0: '0',
				2500: '2,500',
				5000: '5,000',
				7500: '7,500',
				10000: '10,000'
			},
			value = [min_payload, max_payload]
		),

		html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
	]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
	Output(component_id = 'success-pie-chart', component_property = 'figure'),
	Input(component_id = 'site-dropdown', component_property = 'value')
)
def get_pie_chart(entered_site):
	filtered_df = spacex_df
	if entered_site == 'ALL':
		fig = px.pie(
			filtered_df, 
			values = 'class', 
			names = 'Percent of successful launches per site', 
			title = 'Launch Site '
		)
		return fig
	# return the outcomes piechart for a selected site
	else:
		site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
		fig = px.pie(
			site_df, 
			names = 'class', 
			title = f'Success vs Failure for {entered_site}',
			labels = {0 : 'Failed', 1 : 'Succeeded'}
		)
		return fig
		
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
	Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
	Input(component_id = 'site-dropdown', component_property = 'value'), 
	Input(component_id = "payload-slider", component_property = "value")
)
def get_scatter_chart(entered_site, entered_payload):
	low_payload, high_payload = entered_payload
	payload_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low_payload) &
        (spacex_df['Payload Mass (kg)'] <= high_payload)
    ]
	if entered_site == 'ALL':
		fig = px.scatter(
			payload_df, 
			x = 'Payload Mass (kg)',
			y = 'class',
			color="Booster Version Category",
			title = 'Correlation between Payload and Success for all Sites'
		)
		return fig
	else:
		site_df = payload_df[payload_df['Launch Site'] == entered_site]
		fig = px.scatter(
			site_df, 
			x = 'Payload Mass (kg)',
			y = 'class',
			color="Booster Version Category",
			title = f'Correlation between Payload and Success for {entered_site}'
		)
		return fig

# Run the app
if __name__ == '__main__':
	app.run()
