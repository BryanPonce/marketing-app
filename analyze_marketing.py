# coding=ISO-8859-1

import pandas as pd
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st 

# import visualization data

url= 'https://raw.githubusercontent.com/BryanPonce/marketing-app/main/dataset_mkt_29_08.csv'
df =  pd.read_csv(url, encoding='ISO-8859-1')

# replace characters to avoid problems with the streamlit filter

df.columns = df.columns.str.replace(' ', '_')

# for this page we will only use marketing information, so i select only paid media

df1=df[df['paid']==1]

# create a pivot table to find new metrics in dataset

df1= pd.pivot_table(data=df1,index=['inicio_del_informe','batch','plataforma_ad','escuela',
                'desglose_de_fuente_original_2'
                ],
                values=['importe_gastado','leads','clics','leads_hubspot','registro_eb',
                'asistio','ensayo','inscrito','ventas'
                ],
                aggfunc={'importe_gastado': np.sum,'leads': np.sum ,'clics': np.sum,
                'leads_hubspot':np.sum,'registro_eb':np.sum,'asistio':np.sum,'ensayo':np.sum,
                'inscrito':np.sum,'ventas':np.sum
                },
                fill_value=0
)

df1=df1.reset_index()

# getting new metrics from existing data

df1['cac']= df1['importe_gastado'] / df1['inscrito']
df1['cvr']= (df1['inscrito'] / df1['leads_hubspot'])*100
df1['roas']= df1['ventas'] / df1['importe_gastado']
df1['cvr_paid']= (df1['inscrito'] / df1['leads'])*100
df1.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# reorder columns for easier dataset reading

df1 = df1.reindex(columns=[
    'inicio_del_informe','batch','escuela','plataforma_ad','desglose_de_fuente_original_2',
    'importe_gastado','clics','leads','leads_hubspot','registro_eb','asistio','ensayo',
    'inscrito','ventas','cac','cvr','roas','cvr_paid'
    ]
)

def show_analyze_marketing():

    # ------- sidebar --------

    st.sidebar.header('Filtros')
    batch_s = st.sidebar.multiselect(
        'Selecciona el Batch',
        options= df1['batch'].unique(),
        default= df1['batch'].unique()
    )
    escuela_s = st.sidebar.multiselect(
        'Selecciona la Escuela',
        options= df1['escuela'].unique(),
        default= df1['escuela'].unique()
    )
    plataforma_s = st.sidebar.multiselect(
        'Plataforma de anuncios',
        options= df1['plataforma_ad'].unique(),
        default= df1['plataforma_ad'].unique()
    )
    fuente_s = st.sidebar.multiselect(
        'Selecciona la campaña o keyword (Search)',
        options= df1['desglose_de_fuente_original_2'].unique(),
        default= df1['desglose_de_fuente_original_2'].unique()
    )

    # ------- connect sidebar to dataframe ------

    df_select = df1.query('batch == @batch_s & escuela == @escuela_s & plataforma_ad == @plataforma_s & desglose_de_fuente_original_2 == @fuente_s')

    # select for streamlit the filtered dataset

    st.dataframe(df_select)

    # -------- streamlit page name --------

    st.title('Dashboard All In One: Marketing :bar_chart:')
    st.markdown('##')

    # create variables for streamlit kpi section

    ventas_totales= round(df_select['ventas'].sum(), 2)
    cac_total= round(df_select['importe_gastado'].sum() / df_select['inscrito'].sum(), 2)
    paid_cvr_total= round((df_select['inscrito'].sum() / df_select['leads'].sum())*100, 1)
    hs_cvr_total= round((df_select['inscrito'].sum() / df_select['leads_hubspot'].sum())*100, 1)
    inv_total= round(df_select['importe_gastado'].sum(), 2)
    roas_total= round(df_select['ventas'].sum() / df_select['importe_gastado'].sum(), 1)
    ins_total= df_select['inscrito'].sum()
    leads_total=int(df_select['leads'].sum())
    paid_cpl_total= round(df_select['importe_gastado'].sum() / df_select['leads'].sum(), 2)
    hs_cpl_total= round(df_select['importe_gastado'].sum() / df_select['leads_hubspot'].sum(), 2)

    # divide streamlit section in two columns

    left_column, right_column= st.columns(2)

    # order data for streamlit kpi section display

    with left_column:
        st.subheader(f'Investment: $ {inv_total:,} MXN')   
        st.subheader(f'ROAS: {roas_total}')
        st.subheader(f'Total Leads: {leads_total:,}')
        st.subheader(f'Campaigns CPL: $ {paid_cpl_total} MXN')
        st.subheader(f'Hubspot CPL: $ {hs_cpl_total} MXN')
    with right_column:
        st.subheader(f'Total Sales: $ {ventas_totales:,} MXN')
        st.subheader(f'Alumns: {ins_total:,}')
        st.subheader(f'CAC: $ {cac_total:,} MXN')
        st.subheader(f'Hubspot CVR: {hs_cvr_total} %')
        st.subheader(f'Campaigns CVR: {paid_cvr_total} %')
    
    # separate kpi section from visualization area with markdown

    st.markdown('---')