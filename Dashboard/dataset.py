import plotly.express as px
import pandas as pd

#------------------------ CARGA DEL DATASET --------------------------#

# Cargamos los DataFrames.
tw_ranks = pd.read_csv("Twitch_game_data.csv", encoding="ISO-8859-1")
tw_global = pd.read_csv("Twitch_global_data.csv", encoding="ISO-8859-1")

# Ajustamos los DataFrames.
# Convertimos las columnas a strings
tw_ranks.columns = list(map(str, tw_ranks.columns))
tw_global.columns = list(map(str, tw_global.columns))

# Quitamos los elementos que correspondan al año 2023.
tw_ranks = tw_ranks[tw_ranks.Year != 2023]
tw_global = tw_global[tw_global.year != 2023]

# Establecemos nuevo indice y eliminamos la columna repetida.
tw_global.index = tw_global.year
tw_global.index.name = 'Year'
tw_global.drop('year', axis=1, inplace=True)

#---------------- ELEMENTOS AUXILIARES (GRAFICOS) ----------------------#

# Lista de Años y Meses en formato String 
years = list(map(str, range(2016, 2023)))
months = list(map(str, range(1, 13)))

# Diccionario de Meses
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

# Diccionario de Indices/Categorias
idxNames = {
	"Horas Vistas" : "Hours_watched",
	"Peak de Espectadores" : "Peak_viewers",
	"Peak de Canales" : "Peak_channels",
	"Cantidad de Streamers" : 'Streamers',
	"Promedio de Espectadores" : "Avg_viewers",
	"Transmisiones" : "Streams",
	"Promedio de Canales Activos" : "Avg_channels",
	"Juegos Transmitidos" : "Games_streamed",
	"Promedio de Espectadores por Canal" : "Viewer_ratio"
}

# Estilo de Colores
colors = {
	'background': '#111111',
	'text': '#7FDBFF',
	'background2': '#222222'
}

#-------------------- CONSTRUCCION GRAFICOS ------------------------------#

# LinePlot
def line(value): 
	yrs = list(map(str, range(2016, 2023)))
	tw_stats = pd.DataFrame(index=yrs)

	for x in range(1,13):
		aux = tw_global[ tw_global.Month == x ]
		aux = aux.loc[ :, idxNames[value] ]
		tw_stats.insert( x-1, months[x-1], aux.values )

	tw_stats = tw_stats.transpose()

	fig = px.line(tw_stats, x=months, y=yrs)
	fig.update_layout(title = "<b>Twitch: {} (2016 - 2022)</b>".format( value ), title_x = 0.5)
	fig.update_xaxes(title_text = "<b>Mes</b>", gridcolor = 'dimgray')
	fig.update_yaxes(
		title_text = "<b>{}</b>".format(value),
		gridcolor = 'dimgray'
	)
	fig.update_layout(
		plot_bgcolor = colors['background'],
		paper_bgcolor = colors['background2'],
		font_color = colors['text']
	)

	return fig


# AreaPlot
def area(value): 
	yrs = list(map(str, range(2016, 2023)))
	tw_stats = pd.DataFrame(index=yrs)

	for x in range(1,13):
		aux = tw_global[ tw_global.Month == x ]
		aux = aux.loc[ :, idxNames[value] ]
		tw_stats.insert( x-1, months[x-1], aux.values )

	tw_stats = tw_stats.transpose()

	fig = px.area(tw_stats, x=months, y=yrs, line_group=months)
	fig.update_layout(title = "<b>Twitch: {} (2016 - 2022)</b>".format( value ), title_x = 0.5)
	fig.update_xaxes(title_text = "<b>Mes</b>", gridcolor = 'dimgray')
	fig.update_yaxes(
		title_text = "<b>{}</b>".format(value),
		gridcolor = 'dimgray'
	)
	fig.update_layout(
		plot_bgcolor = colors['background'],
		paper_bgcolor = colors['background2'],
		font_color = colors['text']
	)

	return fig


# Histogram
def hist(hist_yr, hist_mth, hist_range):
	idx = "Avg_viewer_ratio"
	hgram = tw_ranks.loc[ (tw_ranks["Month"] == hist_mth) & (tw_ranks["Year"] == hist_yr) ]
	hgram = hgram.loc[ (hgram[ idx ] >= hist_range[0]) & (hgram[ idx ] <= hist_range[1]) ]
	
	fig = px.histogram(hgram, x=idx)
	fig.update_layout(
		title = "<b>Top 200 Juegos: Promedio de Espectadores por Canal ({}, {})</b>".format(monthsNames[hist_mth], hist_yr),
		title_x = 0.5
	)
	fig.update_xaxes(
		title_text = "<b>Promedio de Espectadores por Canal</b>",
		gridcolor = 'dimgray'
	)
	fig.update_yaxes(
		title_text = "<b>Cantidad de Juegos</b>",
		gridcolor = 'dimgray'
	)
	fig.update_layout(
		plot_bgcolor = colors['background'],
		paper_bgcolor = colors['background2'],
		font_color = colors['text']
	)

	return fig


# Bar Chart
def bar(bar_idx, bar_yr, bar_mth):
	bar = tw_ranks.loc[ (tw_ranks.Rank <= 10) & (tw_ranks.Year == bar_yr) & (tw_ranks.Month == bar_mth) ]

	fig = px.bar(bar, x=idxNames[bar_idx], y="Game", orientation='h')
	fig.update_layout(
		title = "<b>Top 10 Juegos: {} ({}, {})</b>".format(bar_idx, monthsNames[bar_mth], bar_yr), 
		title_x = 0.5
	)
	fig.update_xaxes(
		title_text = "<b>{}</b>".format(bar_idx),
		gridcolor = 'dimgray'
	)
	fig.update_yaxes(
		title_text = "<b>Juego</b>", 
		gridcolor = 'dimgray'
	)
	fig.update_layout(
		plot_bgcolor = colors['background'],
		paper_bgcolor = colors['background2'],
		font_color = colors['text']
	)
	
	return fig


# Pie Chart
def pie(pie_idx, pie_yr, pie_mth):
	pie = tw_ranks.loc[ (tw_ranks.Rank <= 5) & (tw_ranks.Year == pie_yr) & (tw_ranks.Month == pie_mth) ]

	fig = px.pie(pie, values=idxNames[pie_idx], names='Game')
	fig.update_layout(
		title = "<b>Top 5 Juegos: {} ({}, {})</b>".format(pie_idx, monthsNames[pie_mth], pie_yr), 
		title_x = 0.5
	)
	fig.update_layout(
		plot_bgcolor = colors['background'],
		paper_bgcolor = colors['background2'],
		font_color = colors['text']
	)

	return fig
