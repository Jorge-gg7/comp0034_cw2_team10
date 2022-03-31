from dash import Output, Input
import json

import plotly_express as px
import pandas as pd

df1 = pd.read_csv(
    '../datasets/business-demographics-updated.csv')
df2 = pd.read_csv(
    '../datasets/business-survival-rates-updated.csv')

# This json file is sourced from the London Data Store
# https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london?resource=9ba8c833-6370-4b11-abdc-314aa020d5e0

f = open(
    '../datasets/london_boroughs.json')

geoj = json.load(f)


def register_callbacks(dash_app):
    @dash_app.callback([Output('map', 'figure')],
                       [Input('slct_yr', 'value')]
                       )
    def update_map(option_slctd):
        dff1 = df1.copy()
        geojj = geoj.copy()
        dff1 = dff1[dff1["year"] == option_slctd]

        fig = px.choropleth_mapbox(
            data_frame=dff1,
            featureidkey='properties.code',
            locations='code',
            geojson=geojj,
            mapbox_style="carto-positron",
            color='birth-death_rate',
            hover_name='area',
            hover_data=['active_enterprises', 'birth_rate', 'death_rate', 'birth-death_rate'],
            color_continuous_scale='Viridis',
            custom_data=['area'],
            opacity=0.5,
            center={'lat': 51.509865, 'lon': -0.118092},
            title=('Birth Rate-Death Rate (%) of businesses in {}'.format(option_slctd)),
            labels={'birth-death_rate': '%'}
        )
        return [fig]

    @dash_app.callback(
        [Output('surv-graph', 'figure'),
         Input('map', 'clickData'),
         Input('slct_yr', 'value')]
    )
    def update_bar(clk_data, year):
        dff2 = df2.copy()

        if clk_data is None:
            dff2 = dff2[dff2["year"] == 2004]
            dff2 = dff2[dff2['area'] == 'City of London']

            survival_rates = ['1_year_survival_rate', '2_year_survival_rate', '3_year_survival_rate',
                              '4_year_survival_rate', '5_year_survival_rate']
            new_names = {'5_year_survival_rate': '5 Years', '4_year_survival_rate': '4 Years',
                         '3_year_survival_rate': '3 Years',
                         '2_year_survival_rate': '2 Years', '1_year_survival_rate': '1 Year'}

            fig1 = px.bar(dff2, x='area', y=survival_rates, barmode='group', orientation='v',
                          title='Business Survival Rates in City '
                                'of London after '
                                '2004',
                          labels={'area': '', 'variable': 'Years after 2004'})

            fig1.for_each_trace(lambda t: t.update(name=new_names[t.name],
                                                   legendgroup=new_names[t.name],
                                                   hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name])
                                                   ))
            return [fig1]
        else:
            dff2 = dff2[dff2["year"] == year]
            click_area = clk_data['points'][0]['customdata'][0]
            dff2 = dff2[dff2["area"] == click_area]

            survival_rates = ['1_year_survival_rate', '2_year_survival_rate', '3_year_survival_rate',
                              '4_year_survival_rate', '5_year_survival_rate']
            new_names = {'5_year_survival_rate': '5 Years', '4_year_survival_rate': '4 Years',
                         '3_year_survival_rate': '3 Years',
                         '2_year_survival_rate': '2 Years', '1_year_survival_rate': '1 Year'}

            fig1 = px.bar(dff2, x='area', y=survival_rates, barmode='group', orientation='v',
                          title='Business Survival Rates in {} '
                                'after {}'.format(click_area, year),
                          labels={'area': '', 'variable': 'Years after {}'.format(year)})

            fig1.for_each_trace(lambda t: t.update(name=new_names[t.name],
                                                   legendgroup=new_names[t.name],
                                                   hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name])
                                                   ))
            return [fig1]
