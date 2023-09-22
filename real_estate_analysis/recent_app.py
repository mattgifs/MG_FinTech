 # Initial imports
import pandas as pd
import hvplot.pandas
#from sqlalchemy import create_engine, Column, String
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
import holoviews as hv
from bokeh.models import HoverTool, NumeralTickFormatter
import quandl
import psycopg2
import streamlit as st


# Retrieve data from Quandl API
quandl.ApiConfig.api_key = 'Hxc-vj2V4iBzuusYo__Q'

# Get list of Regions (states only for now)
regions = quandl.get_table('ZILLOW/REGIONS',region_type = 'state')
regions = regions.sort_values('region')
regions = regions.set_index('region_id')

# Get list of indicators
indicators = quandl.get_table('ZILLOW/INDICATORS')
indicators = indicators.set_index('indicator_id')


# User selects region
region_sel = st.selectbox("Select Region", options = regions['region'])
sel_id = regions.loc[regions['region'] == region_sel].index[0]

# User selects indicator
indicator_sel = st.selectbox("Select Indicator", options = indicators)
ind_id = indicators.loc[indicators['indicator'] == indicator_sel].index[0]

## DEBUG - write region and indicator indices to page
#st.write(f'Region ID: {sel_id}')
#st.write(f'Indicator ID: {ind_id}')

###
data = quandl.get_table('ZILLOW/DATA', indicator_id=ind_id,region_id=sel_id)
data = data.set_index('date')
data = data.sort_values('date')
data_values = data['value']

st.sidebar.markdown('## Data Table')
st.sidebar.dataframe(data=data_values,width=1000)

#st.markdown('# Indicator Change Over Time')
st.markdown("---")
total_period_appreciation = (data_values[-1] - data_values[0]) / data_values[0]
num_years = round(len(data_values.resample('M').sum())/12,1)
annualized_appreciation_percentage = (total_period_appreciation**(1 / num_years)) - 1
t12mo_app = (data_values[-1] - data_values[-12]) / data_values[-12]
t24mo_app = (data_values[-1] - data_values[-24]) / data_values[-24]

st.markdown(f" #### Years in Sample: {num_years} ")
st.markdown(f" #### Total Appreciation: {total_period_appreciation:.2%} | Annualized Appreciation: {annualized_appreciation_percentage:.2%}")
st.markdown(f" #### T12Mo: {t12mo_app:.2%} | T24Mo: {t24mo_app:.2%}")

st.markdown("---")
st.bar_chart(data_values, y='value')