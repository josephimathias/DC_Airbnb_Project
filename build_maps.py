def build_map_df(df, column_for_map, summary_type):
    '''This function creates a dataframe that contains summary statistics for
    neighborhoods based on the column selected.
    df = dataframe containing information
    column_for_map = the column that you'd like to view. Name should be in quotation marks.
    summary_type = mean, median, count, or sum. Should be in quotation marks'''
    if summary_type == 'mean':
        map_df = df.groupby('neighbourhood_cleansed')[column_for_map].mean().reset_index()
        return map_df
    if summary_type == 'median':
        map_df = df.groupby('neighbourhood_cleansed')[column_for_map].median().reset_index()
        return map_df
    if summary_type == 'count':
        map_df = df.groupby('neighbourhood_cleansed')[column_for_map].count().reset_index()
        return map_df
    if summary_type == 'sum':
        map_df = df.groupby('neighbourhood_cleansed')[column_for_map].sum().reset_index()
        return map_df
    
    
def build_map(map_df, legendname):
    import folium
    import os
    import json
    '''This function builds a map of DC by neighborhood based on the
    dataframe that you made with the build_map_df function.
    map_df = dataframe that includes neighborhoods in one column and a summary statistic
    in the second column. Create using build_map_df function.
    legendname = variable being examined and units'''
    state_path = os.path.join(os.getcwd(),'data', 'neighbourhoods.geojson') 
    state_geojson = json.load(open(state_path))

    nm = folium.Map(location=[38.9072, -77.0369],
        zoom_start=11)

    folium.Choropleth(
        geo_data=state_geojson,
        name='choropleth',
        data=map_df,
        columns=[map_df.columns[0], map_df.columns[1]],
        key_on='feature.properties.neighbourhood',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legendname
    ).add_to(nm)

    folium.LayerControl().add_to(nm)

    return nm