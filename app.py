from shiny import reactive, render  
from shiny.express import input, ui  
from shinywidgets import render_plotly  
import pandas as pd  
import plotly.express as px  
import seaborn as sns  
import palmerpenguins 

# Load penguins data into DataFrame
penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Pranali's Penguin Data", fillable=True)

# Create sidebar UI elements
with ui.sidebar(open="open"):
    # Heading
    ui.h2("Sidebar")

    # Dropdown to choose Plotly attribute
    ui.input_selectize(
        "selected_attribute",
        "Choose Plotly attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Input for Plotly histogram bins count
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 40)

    # Slider for Seaborn bins count
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 40, 20)

    # Checkbox group for selecting species
    ui.input_checkbox_group(
        "selected_species_list",
        "species",
        ["Gentoo", "Chinstrap", "Adelie"],
        selected=["Gentoo", "Chinstrap"],
        inline=True,
    )

     # Creates a checkbox group input for islands
    ui.input_checkbox_group(
        "selected_island_list",
        "Islands",
        penguins_df["island"].unique().tolist(),
        selected=penguins_df["island"].unique().tolist(),
        inline=True,
    )

    # Horizontal rule
    ui.hr()

    # Link to GitHub repo
    ui.a(
        "Pranali's GitHub Repo",
        href="https://github.com/TechPranali/cintel-02-data",
        target="_blank",
    )

# Create layout with two cards
with ui.layout_columns():
    with ui.card(full_screen=True):  
        # Heading for Penguin Data Table
        ui.h2("Penguin Data Table")

        # Render penguins DataFrame as DataTable
        @render.data_frame
        def penguins_datatable():
            return render.DataTable(penguins_df)

    with ui.card(full_screen=True): 
        # Heading for Penguin Data Grid
        ui.h2("Penguin Data Grid")

        # Render penguins DataFrame as DataGrid
        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(penguins_df)

# Horizontal rule
ui.hr()

# Create layout with three cards for different plots
with ui.layout_columns():
    with ui.card(full_screen=True):
        # Heading for Species Plotly Histogram
        ui.h2("Species Plotly Histogram")

        # Render Plotly histogram
        @render_plotly
        def plotly_histogram():
            return px.histogram(
                filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            )

    with ui.card(full_screen=True):
        # Heading for Seaborn Histogram
        ui.h2("Seaborn Histogram")

        # Render Seaborn histogram
        @render.plot(alt="Species Seaborn Histogram")
        def seaborn_histogram():
            seaborn_plot = sns.histplot(
                data=filtered_data(),
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
                multiple="dodge",
                hue="species",
            )
            seaborn_plot.set_title("Species Seaborn Histogram")
            seaborn_plot.set_ylabel("Measurement")

    with ui.card(full_screen=True):
        # Heading for Species Plotly Scatterplot
        ui.h2("Species Plotly Scatterplot")

        # Render Plotly scatterplot
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                title="Plotly Scatterplot",
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                symbol="species",
            )

# Reactive calculation to filter data based on selected species
@reactive.calc
def filtered_data():
    return penguins_df[
        penguins_df["species"].isin(input.selected_species_list())
    ]
