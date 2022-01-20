#!/usr/bin/env python
# coding: utf-8

# # <center>Interactive Data Visualization in Python With Bokeh</center>

# ## Adding Interaction

# In[1]:


import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral11
from bokeh.layouts import column, row, gridplot
from bokeh.models import Slider, Select
from bokeh.models import Div, Spinner


# In[2]:

# Membaca data dari dataset
data = pd.read_csv("./data/top10sedit.csv")
data.rename(columns={'nrgy': 'energy', 'dnce': 'dance',
            'dur': 'duration'}, inplace=True)
data.set_index('year', inplace=True)


# In[3]:

# Membuat variable list untuk top genre musik dengan kolom top_genre
top_genre_list = data.top_genre.unique().tolist()

# Membuat color mapper untuk warna pada circle nanti
color_mapper = CategoricalColorMapper(
    factors=top_genre_list, palette=Spectral11)


# In[4]:

# Membuat kolom untuk source yang nanti akan digunakan sebagai ColumnDataSource
source = ColumnDataSource(data={
    'x': data.loc[2010].bpm,
    'y': data.loc[2010].energy,
    'artist': data.loc[2010].artist,
    'top_genre': data.loc[2010].top_genre,
})


# In[ ]:


# Membuat figur plot
plot = figure(title='2010', x_axis_label='bpm', y_axis_label='energy',
              plot_height=700, plot_width=1300, toolbar_location="below", tools=[HoverTool(tooltips='@artist'), "pan, wheel_zoom, box_zoom, reset"])
plot.title.text = 'Top Spotify Listened Artist for 2010'
# Menambahkan circle kedalam figur plot
points = plot.circle(x='x', y='y', source=source, fill_alpha=1, size=12, line_color="black", color=dict(
    field='top_genre', transform=color_mapper), legend_field='top_genre')

# Set posisi anotasi legend pada figur plot
plot.legend.location = 'bottom_left'
plot.legend.label_text_font_size = '13pt'
plot.legend.glyph_width = 25
plot.legend.glyph_height = 25

# Membuat text area dengan div
div = Div(
    text="""
          <p></p>
          """,
    width=200,
    height=30,
)

# Membuat text area dengan div
divDesc = Div(
    text="""
          <p><b>BPM (Beats Per Minute):</b> Adalah kecepatan ketukan/tempo musik, semakin tinggi semakin cepat ketukan/tempo musik tersebut.</p>
          <p><b>Energy:</b> Energi dari sebuah musik, semakin tinggi maka semakin energetik musik tersebut.</p>
          <p><b>Dance:</b> Jika semakin tinggi maka akan semakin mudah untuk berjoget dengan musik tersebut.</p>
          <p><b>Duration (Per Second/Detik):</b> Durasi musik, jika semakin tinggi, maka semakin lama durasi musik tersebut.</p>
          """,
    height=30,
)

# Membuat spinner untuk fitur pembesaran circle
spinner = Spinner(
    title="Circle size",
    low=0,
    high=60,
    step=5,
    value=points.glyph.size,
    width=200,
)
spinner.js_link("value", points.glyph, "size")


# Menambahkan fungsi callback pada update_plot
def update_plot(attr, old, new):
    # buat variable 'yr' dengan slide.value dan source.data tadi menjadi new_data
    # variable yr akan digunakan pada slider tahun nanti
    yr = slider.value
    x = x_select.value
    y = y_select.value

    # Pelabelan axis plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y

    # new data
    new_data = {
        'x': data.loc[yr][x],
        'y': data.loc[yr][y],
        'artist': data.loc[yr].artist,
        'top_genre': data.loc[yr].top_genre,
    }
    source.data = new_data

    # Title dinamik yang menampilkan judul plot dengan tahun sesuai slider
    plot.title.text = 'Top Spotify Listened Artist for %d' % yr


# Membuat objek slider
slider = Slider(start=2010, end=2019, step=1, value=2010, title='Year')
slider.on_change('value', update_plot)


# Buat menu dropdown untuk axis x dan y
# Membuat item dropdown untuk axis x
x_select = Select(
    options=['bpm', 'energy', 'dance', 'duration'],
    value='bpm',
    title='Parameter untuk x-axis'
)
# Tambahkan fungsi callback update_plot kedalam properti value pada saat memilih item dropdown pada x axis
x_select.on_change('value', update_plot)

# Membuat item dropdown untuk axis y
y_select = Select(
    options=['bpm', 'energy', 'dance', 'duration'],
    value='energy',
    title='Parameter untuk y-axis'
)
# Tambahkan fungsi callback update_plot kedalam properti value pada saat memilih item dropdown pada y axis
y_select.on_change('value', update_plot)

# Membuat layout untuk tampilan urutan setiap objek
layout = row(plot, column(y_select, x_select, slider, div, spinner, divDesc))
curdoc().add_root(layout)


# In[5]:


# bokeh serve --show myapp.py


# For more on all things interaction in Bokeh, [**Adding Interactions**](https://docs.bokeh.org/en/latest/docs/user_guide/interaction.html) in the Bokeh User Guide is a great place to start.

# In[ ]:
