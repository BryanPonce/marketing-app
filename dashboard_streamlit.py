
# coding=ISO-8859-1

# importo las librerias necesarias para poder trabajar mi dataframe

import pandas as pd
import numpy as np 
import plotly.express as px #---- pip install plotly-express
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st #---- pip install streamlit

# **para mostrar el streamlit en el navegador: streamlit run dashboard_streamlit.py **

# importo los datos que usare en mi aplicacion de visualizacion

url= 'https://raw.githubusercontent.com/BryanPonce/marketing-app/main/dataset_mkt_29_08.csv'
df =  pd.read_csv(url, encoding='ISO-8859-1')

# quito los espacios en los nombres de las columnas porque entra en conflicto con los
# filtros de Streamlit

df.columns = df.columns.str.replace(' ', '_')

# modifico mis datos para poder unificar los resultados por semana, de manera
# que pueda crear nuevas columnas que nos den metricas no incluidas en el dataset

df1= pd.pivot_table(data=df,index=['inicio_del_informe','batch','paid','plataforma_ad','escuela'],
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

# hago operaciones con columnas que me permitan obtener nuevas metricas
# importantes para el negocio.

# me deshago de los inf y los nan ya que sabemos que esas operaciones
# son un error, ya que vienen de medios sin inversion

df1['cac']= df1['importe_gastado'] / df1['inscrito']
df1['cvr']= (df1['inscrito'] / df1['leads_hubspot'])*100
df1['roas']= df1['ventas'] / df1['importe_gastado']
df1['cvr_paid']= (df1['inscrito'] / df1['leads'])*100
df1.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# cambio el orden de las columnas, solo por estetica en las tablas

df1 = df1.reindex(columns=[
    'inicio_del_informe','batch','escuela','paid','plataforma_ad','importe_gastado',
    'clics','leads','leads_hubspot','registro_eb','asistio','ensayo','inscrito',
    'ventas','cac','cvr','roas','cvr_paid'
    ]
)

# redondeo valores para evitar muchos flotantes en las tablas y hacerlas mas 
# faciles de leer

df1['importe_gastado']= df1['importe_gastado'].round(decimals=2)
df1['leads']= df1['leads'].apply(int)
df1['ventas']= df1['ventas'].round(decimals=2)
df1['cac']= df1['cac'].round(decimals=2)
df1['cvr']= df1['cvr'].round(decimals=1)
df1['roas']= df1['roas'].round(decimals=1)
df1['cvr_paid']= df1['cvr_paid'].round(decimals=1)

# ------ configuracion de streamlit--------

st.set_page_config(page_title= 'Dashboard All In One',
                   page_icon= ':bar_chart:',
                   layout= 'wide'   
)

# indico la data que sera utilizada en streamlit

#st.dataframe(df1)

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
paid_s = st.sidebar.multiselect(
    'Plataformas pagadas?',
    options= df1['paid'].unique(),
    default= df1['paid'].unique()
)
plataforma_s = st.sidebar.multiselect(
    'Selecciona la plataforma',
    options= df1['plataforma_ad'].unique(),
    default= df1['plataforma_ad'].unique()
)


# ------- conectar sidebar al dataframe mostrado ------

df_select = df1.query('batch == @batch_s & escuela == @escuela_s & paid == @paid_s & plataforma_ad == @plataforma_s')

# seleccionamos para stream el dataframe con los filtros

st.dataframe(df_select)

# -------- pagina principal de streamlit --------

st.title('Dashboard All In One :bar_chart:')
st.markdown('##')

# creo variables para usar mis top kpi's en las visualizaciones de streamlit

ventas_totales= round(df_select['ventas'].sum(), 2)
cac_total= round(df_select['importe_gastado'].sum() / df_select['inscrito'].sum(), 2)
cvr_total= round((df_select['inscrito'].sum() / df_select['leads_hubspot'].sum())*100, 1)
inv_total= round(df_select['importe_gastado'].sum(), 2)
roas_total= round(df_select['ventas'].sum() / df_select['importe_gastado'].sum(), 1)
ins_total= df_select['inscrito'].sum()

# especifico en cuantas columnas quiero dividir mi pagina de streamlit

left_column, right_column= st.columns(2)

# como se mostrara la informacion en streamlit

with left_column:
    st.subheader(f'Ventas Totales: $ {ventas_totales:,} MXN')
    st.subheader(f'Inversion: $ {inv_total:,} MXN')   
    st.subheader(f'ROAS: {roas_total}')
with right_column:
    st.subheader(f'Alumnos: {ins_total:,}')
    st.subheader(f'CAC: $ {cac_total:,} MXN')
    st.subheader(f'CVR: {cvr_total} %')
    
# separo la seccion de los kpi's con un markdown

st.markdown('---')

# creo el grafico de ventas por batch

ventas_x_batch= (
    df_select.groupby(by=['batch']).sum()[['ventas']].sort_values(by='ventas')     
)

fig_ventas_batch= px.bar(
    ventas_x_batch,
    y= 'ventas',
    x= ventas_x_batch.index,
    orientation='v',
    title= '<b>Ventas por Batch</b>',
    color_discrete_sequence= ['#0083B8']*len(ventas_x_batch),
    template= 'plotly_white'
)

fig_ventas_batch.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False))
)

# creo una nueva grafica de alumnos inscritos vs cac por batch

ins_b_cac= pd.pivot_table(data=df_select,index=['batch'],
                values=['importe_gastado','inscrito',
                ],
                aggfunc={'importe_gastado': np.sum,
                'inscrito':np.sum
                },
                fill_value=0
)
ins_b_cac['cac']= round(ins_b_cac['importe_gastado'] / ins_b_cac['inscrito'],2)

fig_ins_cac = make_subplots(specs=[[{'secondary_y':True}]])

fig_ins_cac.add_trace(
    go.Scatter(
        x=ins_b_cac.index,
        y=ins_b_cac['cac'],
        name= 'CAC x Batch'),
        secondary_y=True
)
fig_ins_cac.add_trace(
    go.Bar(
        x=ins_b_cac.index,
        y=ins_b_cac['inscrito'],
        name= 'Inscritos x Batch'),
        secondary_y= False
)
fig_ins_cac.update_layout(
    title='<b>Inscritos vs CAC</b>',
    xaxis_title='Batch',
    yaxis_title='Inscritos / CAC',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
)
fig_ins_cac.update_yaxes(
    title_text='CAC x Batch',
    secondary_y=True
)    
fig_ins_cac.update_yaxes(
    title_text='Inscritos x Batch',
    secondary_y=False
)

# creo dos nuevas columnas en el streamlit para mostrar estos graficos juntos

left_column, right_column= st.columns(2)

# muestro cada grafico en una columna

left_column.plotly_chart(fig_ventas_batch, use_container_width=True)
right_column.plotly_chart(fig_ins_cac, use_container_width=True)

st.markdown('---')

# grafico inv vs roas-------------------------------------------------------

inv_v_roas= pd.pivot_table(data=df_select,index=['batch'],
                values=['importe_gastado','ventas',
                ],
                aggfunc={'importe_gastado': np.sum,
                'ventas':np.sum
                },
                fill_value=0
)
inv_v_roas['roas']= round(inv_v_roas['ventas'] / ins_b_cac['importe_gastado'],1)
inv_v_roas['importe_gastado']= round(inv_v_roas['importe_gastado'],0)
inv_v_roas['ventas']= round(inv_v_roas['ventas'],0)

fig_inv_roas = make_subplots(specs=[[{'secondary_y':True}]]
)
fig_inv_roas.add_trace(
    go.Scatter(
        x=inv_v_roas.index,
        y=inv_v_roas['roas'],
        name= 'ROAS x Batch'
        ),
        secondary_y= True,
)
fig_inv_roas.add_trace(
    go.Bar(
        x=inv_v_roas.index,
        y=inv_v_roas['importe_gastado'],
        name= 'Inversion x Batch'
        ),
        secondary_y= False,
)

fig_inv_roas.update_layout(
    title='<b>Inversion vs ROAS</b>',
    xaxis_title='Batch',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
)
fig_inv_roas.update_yaxes(
    title_text='ROAS x batch',
    secondary_y=True,
)
fig_inv_roas.update_yaxes(
    title_text='Inversion x batch',
    secondary_y=False,
)

# creo el grafico de nuestro funnel de conversion--------------------------------------------------

data_funnel= df_select[['leads','leads_hubspot','registro_eb','asistio','ensayo','inscrito']]
data_funnel= data_funnel.transpose()
x= data_funnel.sum(axis=1)
y= data_funnel.index

fig_funnel = go.Figure(go.Funnel(
    y = y,
    x = x,
    textposition = 'inside',
    textinfo = 'value+percent initial',
    opacity = 0.65, 
    marker = {'color': ['deepskyblue', 'lightsalmon', 'tan', 'teal', 'silver'],
    'line': {'width': [4, 2, 2, 3, 1, 1], 
    'color': ['wheat', 'wheat', 'wheat', 'wheat', 'wheat']
    }
    },
    connector = {'line': {'color': 'royalblue', 'dash': 'dot', 'width': 3
    }
    }
    )
)

# dos columnas para mostrar mis dos graficos---------------------------------

left_column, right_column= st.columns(2)

left_column.plotly_chart(fig_inv_roas, use_container_width=True)
right_column.plotly_chart(fig_funnel, use_container_width=True)

# separo nuevamente la seccion------------------------------------------------

st.markdown('---')
