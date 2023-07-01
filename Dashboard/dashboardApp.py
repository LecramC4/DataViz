import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input

import dataset
from dataset import line, area, hist, bar, pie

#---------------- ELEMENTOS AUXILIARES (Layout) ----------------------#


# Marcas para el RangeSlider
marks = {
	0: '0',
	50: '50',
	100: '100',
	300: '300',
	500: '500',
	1000: '1000',
	1500: '1500',
}

# Marcas para el Slider
monthsNames = {
	1 : 'Enero',
	2 : 'Febrero',
	3 : 'Marzo',
	4 : 'Abril',
	5 : 'Mayo',
	6 : 'Junio',
	7 : 'Julio',
	8 : 'Agosto',
	9 : 'Septiembre',
	10 : 'Octubre',
	11 : 'Noviembre',
	12 : 'Diciembre'
}

# Funcion para crear un Dropdown
def newDropdown(opt, dropID):

	match opt:
		case 'global':
			options = [
				"Horas Vistas", "Promedio de Espectadores", "Peak de Espectadores",
				"Transmisiones", "Promedio de Canales Activos", "Juegos Transmitidos", 
				"Promedio de Espectadores por Canal"
			]
			value = "Horas Vistas"

		case 'ranks':
			options = [
				"Horas Vistas", "Peak de Espectadores", "Peak de Canales",
				"Cantidad de Streamers", "Promedio de Espectadores"
			]
			value = "Horas Vistas"

		case 'years':
			options = list( range(2016, 2023) )
			value = 2016


	# Creacion Dropdown.
	dropdown = html.Div([
		dcc.Dropdown( 
			options=options,
			value=value,
			id=dropID,
			clearable=False,
		)
	])
	return dropdown


#------------------- DASHBOARD LAYOUT  ----------------------------#


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
	dbc.NavbarSimple(
		brand="DASHBOARD: Twitch Top 200 Juegos (2016 - 2022)",
		color='#7FDBFF',
		dark=False,
		sticky='top',
	),
	html.Br(),

	html.H1(children='Twitch: Top 200 Juegos (2016 - 2022)', style={'textAlign':'center'}),
	html.Br(),

	# LinePlot + AreaPlot
	# Cuenta con un Dropdown que permite cambiar la categoria a graficar.
	dbc.Container([
		html.Br(),
		dbc.Row(children=[
			dbc.Col( html.H3(children="LinePlot", style={'textAlign':'left'}) ), 
			dbc.Col(
				html.Div([ newDropdown('global', 'LA_idx') ]),
				width=3,
			),
			dbc.Col( html.H3(children="AreaPlot"), style={'textAlign':'right'} ),
		]),
		dbc.Row(children=[
			dbc.Col( html.Div([dcc.Graph(id='lineplot')]) ), 
			dbc.Col( html.Div([dcc.Graph(id='areaplot')]) ),
		]),
		html.Br(),
	]),
	html.Br(),

	# Bar Chart
	# Cuenta con dos Dropdown, uno para la categoria y otro para seleccionar el año.
	# Cuenta con un Slider que permite moverse a lo largo de los 12 meses.
	dbc.Container([
		html.Br(),
		dbc.Row(children=[
			dbc.Col( html.H3(children="Bar Chart", style={'textAlign':'left'}) ), 
			dbc.Col(
				html.Div([ newDropdown('ranks', 'bar_idx') ]),
				width=3,
			),
		]),
    	dbc.Col( html.Div([dcc.Graph(id='bar chart')]) ),
    	html.Br(),
   		dbc.Row(children=[
			dbc.Col( html.Div([ newDropdown('years', 'bar_yr') ]), width=1 ), 
			dbc.Col( html.Div([dcc.Slider(
				min=1, max=12, value=1,
				step=None, marks = { i : {
					"label" : f"{monthsNames[i]}",
					"style" : {"color":"black"}
				} for i in range(1,13)}, id='bar_mth')
			])),
		]),
		html.Br(),
	]),
	html.Br(),

	# Pie Chart
	# Cuenta con dos Dropdown, uno para la categoria y otro para seleccionar el año.
	# Cuenta con un Slider que permite moverse a lo largo de los 12 meses.
	dbc.Container([
		html.Br(),
		dbc.Row(children=[
			dbc.Col( html.H3(children="Pie Chart", style={'textAlign':'left'}) ), 
			dbc.Col(
				html.Div([ newDropdown('ranks', 'pie_idx') ]),
				width=3,
			),
		]),
    	dbc.Col( html.Div([dcc.Graph(id='pie chart')]) ),
   		html.Br(),
   		dbc.Row(children=[
			dbc.Col( html.Div([ newDropdown('years', 'pie_yr') ]), width=1 ), 
			dbc.Col( html.Div([dcc.Slider(
				min=1, max=12, value=1,
				step=None, marks = { i : {
					"label" : f"{monthsNames[i]}",
					"style" : {"color":"black"}
				} for i in range(1,13)}, id='pie_mth')
			])),
		]),
		html.Br(),
	]),
	html.Br(),

	# Histogram
	# Cuenta con un Dropdown para seleccionar el año a enfocar.
	# Cuenta con un Slider que permite seleccionar el mes.
	# Cuenta con un RangeSlider, para poder enfocar el rango que se desea observar.
	dbc.Container([
    	html.Br(),
    	dbc.Row(children=[
    		dbc.Col( html.H3(children="Histogram", style={'textAlign':'left'}) ),
			dbc.Col( html.Div([ newDropdown('years', 'hist_yr') ]), width=1 ),
		]),
    	dbc.Col( html.Div([dcc.Graph(id='histogram')]) ),
		html.Br(),
		dbc.Col( html.Div([
			dcc.Slider(
				min=1, max=12, value=1,
				step=None, marks = { i : {
					"label" : f"{monthsNames[i]}",
					"style" : {"color":"black"}
				} for i in range(1,13)}, id='hist_mth')
		])),
		html.Br(),
		dbc.Col( html.H6(children="Rango", style={'textAlign':'center'}) ), 
		dbc.Col( html.Div([
			dcc.RangeSlider(
				0, 1500, value=[0, 1500],
				step=None, marks ={ i : {
					"label" : f"{i}",
					"style" : {"color":"black"}
				} for i in marks},
				allowCross=False, id='hist_range')
		])),
		html.Br(),
	]),
	html.Br(),
], style={'background-color': 'gray'})


#-------------------------- CALLBACKS -----------------------------#

@callback(
	Output('lineplot', 'figure'),
	Input('LA_idx', 'value'),		# Dropdown: Categoria
)
def update_line(value):
	return line(value)


@callback(
	Output('areaplot', 'figure'),
	Input('LA_idx', 'value'),		# Dropdown: Categoria
)
def update_areaplot(value):
	return area(value)


@callback(
	Output('histogram', 'figure'),
	Input('hist_yr', 'value'),		# Dropdown: Año
	Input('hist_mth', 'value'),		# Slider: Mes
	Input('hist_range', 'value')	# RangeSlider: Rango
)
def update_histogram(hist_yr, hist_mth, hist_range):
	return hist(hist_yr, hist_mth, hist_range)


@callback(
	Output('bar chart', 'figure'),
	Input('bar_idx', 'value'),		# Dropdown: Categoria
	Input('bar_yr', 'value'),		# Dropdown: Año
	Input('bar_mth', 'value'),		# Slider: Mes
)
def update_barchart(bar_idx, bar_yr, bar_mth):
	return bar(bar_idx, bar_yr, bar_mth)


@callback(
	Output('pie chart', 'figure'),
	Input('pie_idx', 'value'),		# Dropdown: Categoria
	Input('pie_yr', 'value'),		# Dropdown: Año
	Input('pie_mth', 'value'),		# Slider: Mes
)
def update_piechart(pie_idx, pie_yr, pie_mth):
	return pie(pie_idx, pie_yr, pie_mth)

# END: Callback Section

if __name__ == '__main__':
    app.run_server(debug=True)