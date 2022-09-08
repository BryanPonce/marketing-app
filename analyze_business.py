
# coding=ISO-8859-1

# import required libraries for this page

import pandas as pd
import numpy as np 
import plotly.express as px #---- pip install plotly-express
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st #---- pip install streamlit


# import visualization data

url= 'https://raw.githubusercontent.com/BryanPonce/marketing-app/main/dataset_mkt_29_08.csv'
df =  pd.read_csv(url, encoding='ISO-8859-1')

# replace characters to avoid problems with the streamlit filter

df.columns = df.columns.str.replace(' ', '_')

# create a pivot table to find new metrics in dataset

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

# getting new metrics from existing data

# replace inf and nan because we have mediums with no investment

df1['cac']= df1['importe_gastado'] / df1['inscrito']
df1['cvr']= (df1['inscrito'] / df1['leads_hubspot'])*100
df1['roas']= df1['ventas'] / df1['importe_gastado']
df1['cvr_paid']= (df1['inscrito'] / df1['leads'])*100
df1.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# reorder columns for easier dataset reading

df1 = df1.reindex(columns=[
    'inicio_del_informe','batch','escuela','paid','plataforma_ad','importe_gastado',
    'clics','leads','leads_hubspot','registro_eb','asistio','ensayo','inscrito',
    'ventas','cac','cvr','roas','cvr_paid'
    ]
)

# round values for easier reading

df1['importe_gastado']= df1['importe_gastado'].round(decimals=2)
df1['leads']= df1['leads'].apply(int)
df1['ventas']= df1['ventas'].round(decimals=2)
df1['cac']= df1['cac'].round(decimals=2)
df1['cvr']= df1['cvr'].round(decimals=1)
df1['roas']= df1['roas'].round(decimals=1)
df1['cvr_paid']= df1['cvr_paid'].round(decimals=1)

# create a function to show data on specific page in streamlit 

def show_analyze_business():

    # ------- sidebar --------

    st.sidebar.header('Filter')
    batch_s = st.sidebar.multiselect(
        'Select Batch',
        options= df1['batch'].unique(),
        default= df1['batch'].unique()
    )
    escuela_s = st.sidebar.multiselect(
        'Select School',
        options= df1['escuela'].unique(),
        default= df1['escuela'].unique()
    )
    paid_s = st.sidebar.multiselect(
        'Paid Media?',
        options= df1['paid'].unique(),
        default= df1['paid'].unique()
    )
    plataforma_s = st.sidebar.multiselect(
        'Select Platform',
        options= df1['plataforma_ad'].unique(),
        default= df1['plataforma_ad'].unique()
    )

    # ------- connect sidebar to dataframe ------

    df_select = df1.query('batch == @batch_s & escuela == @escuela_s & paid == @paid_s & plataforma_ad == @plataforma_s')

    # select for streamlit the filtered dataset

    # st.dataframe(df_select)

    # -------- streamlit page name --------

    st.title('Dashboard All In One: Business :bar_chart:')
    st.markdown('##')

    # create variables for streamlit kpi section

    ventas_totales= round(df_select['ventas'].sum(), 2)
    cac_total= round(df_select['importe_gastado'].sum() / df_select['inscrito'].sum(), 2)
    cvr_total= round((df_select['inscrito'].sum() / df_select['leads_hubspot'].sum())*100, 1)
    inv_total= round(df_select['importe_gastado'].sum(), 2)
    roas_total= round(df_select['ventas'].sum() / df_select['importe_gastado'].sum(), 1)
    ins_total= df_select['inscrito'].sum()

    # divide streamlit section in two columns

    left_column, right_column= st.columns(2)

    # order data for streamlit kpi section display

    with left_column:
        st.subheader(f'Total Sales: $ {ventas_totales:,} MXN')
        st.subheader(f'Investment: $ {inv_total:,} MXN')   
        st.subheader(f'ROAS: {roas_total}')
    with right_column:
        st.subheader(f'Alumns: {ins_total:,}')
        st.subheader(f'CAC: $ {cac_total:,} MXN')
        st.subheader(f'CVR: {cvr_total} %')
    
    # separate kpi section from visualization area with markdown

    st.markdown('---')

    # alumns vs cac by batch graph

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
            name= 'CAC by Batch'),
            secondary_y=True
    )
    fig_ins_cac.add_trace(
        go.Bar(
            x=ins_b_cac.index,
            y=ins_b_cac['inscrito'],
            name= 'Alumns per Batch'),
            secondary_y= False
    )
    fig_ins_cac.update_layout(
        title='<b>Alumns vs CAC</b>',
        xaxis_title='Batch',
        yaxis_title='Alumns / CAC',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    fig_ins_cac.update_yaxes(
        title_text='CAC by Batch',
        secondary_y=True
    )    
    fig_ins_cac.update_yaxes(
        title_text='Alumns per Batch',
        secondary_y=False
    )
    # sales per batch graph

    ventas_x_batch= (
        df_select.groupby(by=['batch']).sum()[['ventas']].sort_values(by='ventas')     
    )

    fig_ventas_batch= px.bar(
        ventas_x_batch,
        y= 'ventas',
        x= ventas_x_batch.index,
        orientation='v',
        title= '<b>Sales per Batch</b>',
        color_discrete_sequence= ['#0083B8']*len(ventas_x_batch),
        template= 'plotly_white'
    )

    fig_ventas_batch.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
    )

    # two new columns to display these graphs:
    # sales per batch & cac vs alumns

    left_column, right_column= st.columns(2)

    # choosing where my plots will be displayed

    left_column.plotly_chart(fig_ventas_batch, use_container_width=True)
    right_column.plotly_chart(fig_ins_cac, use_container_width=True)

    st.markdown('---')

    # graph: inv vs roas-------------------------------------------------------

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
            name= 'ROAS by Batch'
            ),
            secondary_y= True,
    )
    fig_inv_roas.add_trace(
        go.Bar(
            x=inv_v_roas.index,
            y=inv_v_roas['importe_gastado'],
            name= 'Investment by Batch'
            ),
            secondary_y= False,
    )

    fig_inv_roas.update_layout(
        title='<b>Investment vs ROAS</b>',
        xaxis_title='Batch',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    fig_inv_roas.update_yaxes(
        title_text='ROAS by batch',
        secondary_y=True,
    )
    fig_inv_roas.update_yaxes(
        title_text='Investment by batch',
        secondary_y=False,
    )

    # conversion funnel graph --------------------------------------------------

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

    # two new columns to display my graphs: inv vs roas & conversion funnel---------------------------------

    left_column, right_column= st.columns(2)

    left_column.plotly_chart(fig_inv_roas, use_container_width=True)
    right_column.plotly_chart(fig_funnel, use_container_width=True)

    # new markdown------------------------------------------------

    st.markdown('---')
