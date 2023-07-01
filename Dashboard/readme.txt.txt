Alumnos:
	Victor Avila RM.
	Marcel Gutiérrez G.

Dataset: 
	Twitch - Top 200 Juegos (2016 - 2022)
	Dos CSV, twitch_global_data.csv y twitch_game_data.csv
	https://www.kaggle.com/datasets/rankirsh/evolution-of-top-games-on-twitch?select=Twitch_game_data.csv

Archivos Dashboard:
	dashboardApp.py: Layout del Dashboard y Callbacks.
	dataset.py: Carga del Dataset, más generación de los graficos (a través de funciones).

Ejecución Dashboard: python3 dashboardApp.py

Graficos + Componentes:
	
	LinePlot / AreaPlot
		Dropdown: Categoria/Indice a graficar.

	BarChart & PieChart
		Dropdown: Categoria/Indice a graficar.
		Dropdown: Año a enfocar.
		Slider: Mes a enfocar.

	Histogram:
		Dropdown: Año a enfocar.
		Slider: Mes a enfocar.
		RangeSlider: Delimitar rango de valores, para poder enfocar secciones del grafico.

Categorias Usadas (para los Gráficos):
	
	Horas Vistas: Cantidad de horas vistas por los usuarios.
	Peak Espectadores: Cant. maxima de espectadores obtenida.
	Peak Canales: Cant. maxima de canales simultaneamente transmitiendo un juego.
	Promedio Canales Activos: Promedio de Canales que estan activos.
	Transmisiones: Cant. de transmisiones emitidas.
	Promedio de Espectadores: Promedio de espectadores por stream.
	Promedio de Espectadores por Canal: Promedio de espectadores por canal que transmite determinado juego.
	Cantidad de Streamers: Maxima cant. de streamers que transmitieron determinado juego.
