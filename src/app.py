import pandas as pd
import json
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Load the dataset
df_path = "rahvad_filtered.csv"
df = pd.read_csv(df_path)

# Load the GeoJSON data
with open('gadm41_EST_1.json') as f:
    geojson_data = json.load(f)

# Extract state names from GeoJSON
state_names = [feature['properties']['NAME_1'] for feature in geojson_data['features']]

# Generate random colors for each state
np.random.seed(0)  # For reproducibility
colors = [f'rgb({np.random.randint(255)}, {np.random.randint(255)}, {np.random.randint(255)})' for _ in state_names]

# Create DataFrame with state names and colors
color_df = pd.DataFrame({
    'state': state_names,
    'color': colors
})

# Streamlit setup
st.title("Eesti rahvuslik koosseis")
st.header("Ülevaade rahvaste paiknemisest Eestis.")

# Filter by year using slider
years = df['Aasta'].unique()
selected_year = st.slider("Vali aasta", min_value=min(years), max_value=max(years), value=min(years))

# Filter by gender using radio buttons
genders = df['Sugu'].unique()
selected_gender = st.radio("Vali sugu", genders)

# Create checkboxes for nationalities
nationalities = df.columns[4:]  # Assuming columns 4 and onwards are ethnicities
selected_nationalities = []

st.write("Vali rahvused:")
for nationality in nationalities:
    if st.checkbox(nationality, key=nationality):
        selected_nationalities.append(nationality)

# Add space between selection and the chart
st.write("")

# Apply filters
filtered_df = df[(df['Aasta'] == selected_year) & (df['Sugu'] == selected_gender)]

if selected_nationalities:
    # Bar chart display (default view)
    bar_fig = go.Figure()

    for nationality in selected_nationalities:
        bar_fig.add_trace(go.Bar(
            x=filtered_df['Maakond'],
            y=filtered_df[nationality],
            name=nationality,
        ))

    bar_fig.update_layout(
        barmode='group',
        title=f"{', '.join(selected_nationalities)} distribution in {selected_year} ({selected_gender})",
        xaxis_title='Maakond',
        yaxis_title="Population",
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    st.plotly_chart(bar_fig)


# Display filtered data
if selected_nationalities:
    st.write(f"Filtered data for {selected_year}, {selected_gender}:")
    st.dataframe(filtered_df[['Maakond'] + selected_nationalities])
else:
    st.write("Vali vähemalt üks rahvus, et kuvada andmeid.")


# # Load the dataset
# df_path = "../data/processed/rahvad_filtered.csv"
# df = pd.read_csv(df_path)

# # Load the GeoJSON data
# with open('../data/raw/gadm41_EST_1.json') as f:
#     geojson_data = json.load(f)

# # Extract state names from GeoJSON
# state_names = [feature['properties']['NAME_1'] for feature in geojson_data['features']]

# # Streamlit setup
# st.title("Eesti rahvuslik koosseis")
# st.header("Ülevaade rahvaste paiknemisest Eestis.")

# # Filter by year using slider
# years = df['Aasta'].unique()
# selected_year = st.slider("Vali aasta", min_value=min(years), max_value=max(years), value=min(years))

# # Filter by gender using radio buttons
# genders = df['Sugu'].unique()
# selected_gender = st.radio("Vali sugu", genders)

# # Filter by nationality using dropdown
# nationalities = df.columns[4:]  # Assuming columns 4 and onwards are ethnicities
# selected_nationality = st.selectbox("Vali rahvus", nationalities)

# # Apply filters
# filtered_df = df[(df['Aasta'] == selected_year) & (df['Sugu'] == selected_gender)]
# st.markdown("<br>", unsafe_allow_html=True)


# # Option to switch between map and bar chart
# # view_option = st.selectbox("Vali vaade", ["Kaart", "Tulpdiagramm"])
# # if view_option == "Tulpdiagramm":
# #     # Create a bar chart
# bar_fig = go.Figure(go.Bar(
#     x=filtered_df['Maakond'],
#     y=filtered_df[selected_nationality],
#     marker=dict(color='rgba(50, 150, 200, 0.7)')
# ))

# bar_fig.update_layout(
#     title=f"{selected_nationality} distribution in {selected_year} ({selected_gender})",
#     xaxis_title='Maakond',
#     yaxis_title=selected_nationality,
#     margin={"r":0, "t":0, "l":0, "b":0}
# )

# st.plotly_chart(bar_fig)
# # elif view_option == "Kaart":
# #     # Map colors based on filtered data
# #     color_map = {row['state']: row['color'] for idx, row in color_df.iterrows()}

# #     # Create the GeoJSON Lines map (borders of states)
# #     fig = go.Figure(go.Choroplethmapbox(
# #         geojson=geojson_data,
# #         locations=filtered_df['Maakond'],
# #         featureidkey="properties.NAME_1",
# #         z=filtered_df[selected_nationality],
# #         colorscale='Viridis',
# #         zmin=0,
# #         zmax=filtered_df[selected_nationality].max(),
# #         marker_opacity=0.7,
# #         marker_line_width=0,
# #         colorbar_title=selected_nationality
# #     ))

# bar_fig.update_layout(
#     mapbox_style="carto-positron",
#     mapbox_zoom=6,
#     mapbox_center={"lat": 58.5975, "lon": 24.9873},
#     margin={"r":0, "t":0, "l":0, "b":0},
#     title=f"{selected_nationality} distribution in {selected_year} ({selected_gender})"
# )

# # st.plotly_chart(bar_fig)


# # Display filtered data
# st.write(f"Filtered data for {selected_year}, {selected_gender}, {selected_nationality}:")
# st.dataframe(filtered_df[['Maakond', selected_nationality]])




# Generate random colors for each state
# np.random.seed(0)  # For reproducibility
# colors = [f'rgb({np.random.randint(255)}, {np.random.randint(255)}, {np.random.randint(255)})' for _ in state_names]

# # Create DataFrame with state names and colors
# color_df = pd.DataFrame({
#     'state': state_names,
#     'color': colors
# })


# df_path = "../data/processed/rahvad.csv"

# def load_data(path):
#     df = pd.read_csv(path)
#     return df

# # Load GeoJSON data
# with open('../data/raw/gadm41_EST_1.json') as f:
#     geojson_data = json.load(f)

# df_raw = load_data(df_path)
# df_rahvad = df_raw.copy()

# st.title("Eesti rahvuslik koosseis")
# st.header("Ülevaade rahvaste paiknemisest Eestis.")

# st.slider("sup", 2018, 2024)


# # Extract state names and their corresponding values
# state_names = [feature['properties']['NAME_1'] for feature in geojson_data['features']]
# state_values = df_rahvad.groupby('Maakond').max().reset_index()

# st.text(state_names)

# df_rahvad

# # Map colors to states based on highest values
# state_colors = {}
# for state in state_names:
#     max_value = state_values[state_values['Maakond'] == state].drop('Maakond', axis=1).max(axis=1).values[0]
#     color = flag_colors.get(state, 'rgb(200, 200, 200)')  # Default to gray if not found
#     state_colors[state] = color

# # Create DataFrame for plotting
# color_df = pd.DataFrame(list(state_colors.items()), columns=['state', 'color'])

# # Create the Choroplethmapbox
# fig = go.Figure(go.Choroplethmapbox(
#     geojson=geojson_data,
#     locations=color_df['state'],
#     featureidkey="properties.NAME_1",
#     colorscale=[[0, 'rgba(255,255,255,0)'], [1, 'rgba(255,255,255,0)']],
#     color=color_df['color'],
#     marker=dict(
#         opacity=0.5,
#         line=dict(
#             color='black',
#             width=0.5
#         )
#     ),
# ))

# fig.update_layout(
#     mapbox_style="carto-positron",
#     mapbox_zoom=6,
#     mapbox_center={"lat": 58.5975, "lon": 24.9873},
#     margin={"r":0, "t":0, "l":0, "b":0}
# )

# st.plotly_chart(fig)










# # # Load GeoJSON data
# # with open('../data/raw/gadm41_EST_1.json', 'r') as file:
# #     counties = json.load(file)

# # Load the GeoJSON data
# with open('../data/raw/gadm41_EST_1.json') as f:
#     geojson_data = json.load(f)

# # Extract state names
# state_names = [feature['properties']['NAME_1'] for feature in geojson_data['features']]

# # Debug: Check if ADM1_NAME exists in GeoJSON features
# print(counties['features'][0]['properties'])  # Look for 'ADM1_NAME' or similar field

# # Ensure that ADM1_NAME matches df_rahvad['Maakond']
# fig = go.Figure(go.Choroplethmapbox(
#     geojson=counties, 
#     locations=df_rahvad['Maakond'],  # This should match ADM1_NAME in the GeoJSON
#     featureidkey="properties.ADM1_NAME",  # Match the ADM1_NAME in GeoJSON properties
#     z=df_rahvad['Eestlased'],  # Numeric data to color the map
#     colorscale="Viridis", 
#     zmin=0, 
#     zmax=8,
#     marker_opacity=0.5, 
#     marker_line_width=0
# ))

# fig.update_layout(
#     mapbox_style="carto-positron",
#     mapbox_zoom=6,
#     mapbox_center={"lat": 58.5975, "lon": 24.9873},
#     margin={"r":0, "t":0, "l":0, "b":0}
# )

# st.plotly_chart(fig)





# st.cache_data()


# st.dataframe(data=mpg_df)

# st.title( 'My 1st version')
# st.header ('MPG data exploration')
# if st.sidebar.checkbox("Show dataframe:"):
#     st.dataframe(data=mpg_df)

# left_column, middle_column, right_column = st.columns(3)

# show_means = middle_column.radio(label='Show Class Means', ["Yes", "No"])

# years = ["All"]+sorted(pd.unique(mpg_df["Year"]

# year = left_column.selectbox("choose a year: ", years)


# means = reduced_df.groupy("class").mean(numeric_only=True)

# plot_types = ["Matplotlib", "Plotly"]
# plot_type = right_column.radio("Choose a plot type: ", plot_types)

# get reload
# deepcopy
# sidebar in vsc

# col1, col2 = st.columns(2)
# col1.write('Column 1')
# .co12 write( 'Column 2')

# create a copy, we don't want to work with our row data.

# clean and integritize the data (check and fix discrepancies)