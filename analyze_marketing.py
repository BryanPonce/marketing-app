
# coding=ISO-8859-1

import pandas as pd
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st 

# import visualization data

url= 'https://raw.githubusercontent.com/BryanPonce/marketing-app/main/dataset_mkt_19_09.csv'
df =  pd.read_csv(url, encoding='ISO-8859-1')

# replace characters to avoid problems with the streamlit filter

df.columns = df.columns.str.replace(' ', '_')

# for this page we will only use marketing information, so i select only paid media

df1=df[df['paid']==1]

# create a pivot table to find new metrics in dataset

df1= pd.pivot_table(data=df1,index=['paid','fuente_original','inicio_del_informe','batch','plataforma_ad','escuela',
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
df1['cpl_hubspot']= df1['importe_gastado'] / df1['leads_hubspot']
df1['cpl_campaigns']= df1['importe_gastado'] / df1['leads']
df1['costo_registro']= df1['importe_gastado'] / df1['registro_eb']
df1['costo_asistente']= df1['importe_gastado'] / df1['asistio']
df1['costo_ensayo']= df1['importe_gastado'] / df1['ensayo']
df1.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# reorder columns for easier dataset reading

df1 = df1.reindex(columns=[
    'paid','inicio_del_informe','batch','escuela','fuente_original','plataforma_ad',
    'desglose_de_fuente_original_2','importe_gastado','clics',
    'leads','cpl_campaigns','leads_hubspot','cpl_hubspot',
    'registro_eb','costo_registro','asistio','costo_asistente',
    'ensayo','costo_ensayo','inscrito','cac','cvr','cvr_paid',
    'ventas','roas'
    ]
)

def show_analyze_marketing():

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
    plataforma_s = st.sidebar.multiselect(
        'Advertising Platform',
        options= df1['plataforma_ad'].unique(),
        default= df1['plataforma_ad'].unique()
    )

    # ------- connect sidebar to dataframe ------

    df_select = df1.query('batch == @batch_s & escuela == @escuela_s & plataforma_ad == @plataforma_s')

    # select for streamlit the filtered dataset

    #st.dataframe(df_select)

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

    # alumns per platform -----------------------------------------------------------

    alumns_x_platform= (
        df_select.groupby(by=['plataforma_ad']).sum()[['inscrito']].sort_values(by='inscrito')     
    )

    fig_alumns_platform= px.bar(
        alumns_x_platform,
        y= 'inscrito',
        x= alumns_x_platform.index,
        orientation='v',
        title= '<b>Alumns per Platform</b>',
        color_discrete_sequence= ['#0083B8']*len(alumns_x_platform),
        template= 'plotly_white'
    )

    fig_alumns_platform.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False))
    )

    # results vs cost ----------------------------------------------------------------

    # create a pivot table for the paid steps on the funnel

    df_paid= pd.pivot_table(data=df_select, index='paid',
                    values=[
                        'leads','importe_gastado','leads_hubspot',
                        'registro_eb','asistio','ensayo','inscrito'
                    ],
                    aggfunc={
                        'leads': np.sum ,'importe_gastado': np.sum,
                        'leads_hubspot':np.sum,'registro_eb':np.sum,
                        'asistio':np.sum,'ensayo':np.sum,'inscrito':np.sum,
                    },
                    fill_value=0
    )
    
    # new variables for measured metrics

    df_paid['cpl_hubspot']= round(df_paid['importe_gastado'].sum() / df_paid['leads_hubspot'].sum(),2)
    df_paid['cpl_campaigns']= round(df_paid['importe_gastado'].sum() / df_paid['leads'].sum(),2)
    df_paid['costo_registro']= round(df_paid['importe_gastado'].sum() / df_paid['registro_eb'].sum(),2)
    df_paid['costo_asistente']= round(df_paid['importe_gastado'].sum() / df_paid['asistio'].sum(),2)
    df_paid['costo_ensayo']= round(df_paid['importe_gastado'].sum() / df_paid['ensayo'].sum(),2)
    df_paid['cac']= round(df_paid['importe_gastado'].sum() / df_paid['inscrito'].sum(),2)

    # i create a new dataset only with costs variables  

    df_costs= df_paid.filter(['cpl_hubspot','cpl_campaigns','costo_registro',
                             'costo_asistente','costo_ensayo','cac'
                             ],
                             axis=1
    )
    df_costs= df_costs.reindex(columns=['cpl_campaigns','cpl_hubspot','costo_registro',
                                       'costo_asistente','costo_ensayo','cac'
                                       ]
    )
    df_costs= df_costs.transpose()

    # drop the cost variables in df_paid 

    df_paid = df_paid.drop(['cpl_hubspot','cpl_campaigns','costo_registro','costo_asistente',
                           'costo_ensayo','cac','importe_gastado'
                           ], 
                           axis=1
    )

    # format both df to fit the visualization
    
    df_paid= df_paid.reindex(columns=['leads','leads_hubspot','registro_eb',
                                     'asistio','ensayo','inscrito'
                                     ]
    )
    df_paid= df_paid.transpose()

    # now create the visualization ------------------------------ 

    funnel_vs_cost = make_subplots(specs=[[{'secondary_y':True}]])

    funnel_vs_cost.add_trace(
        go.Scatter(
            x= df_paid.index,
            y= df_costs[1],
            name= 'Cost per Result'),
            secondary_y=True
    )
    funnel_vs_cost.add_trace(
        go.Bar(
            x= df_paid.index,
            y= df_paid[1],
            name= 'Results per Stage'),
            secondary_y= False
    )
    funnel_vs_cost.update_layout(
        title='<b>Results per Stage</b>',
        xaxis_title='Stage',
        yaxis_title='Alumns / Stage',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    funnel_vs_cost.update_yaxes(
        title_text='Cost per Result',
        secondary_y=True
    )    
    funnel_vs_cost.update_yaxes(
        title_text='Results per Stage',
        secondary_y=False
    )
    funnel_vs_cost.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y2', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=True
    )
    funnel_vs_cost.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=False
    )

    # two new columns to display these graphs:
    # alumns per platform & results vs cost per stage

    left_column, right_column= st.columns(2)

    # choosing where my plots will be displayed

    left_column.plotly_chart(fig_alumns_platform, use_container_width=True)
    right_column.plotly_chart(funnel_vs_cost, use_container_width=True)

    st.markdown('---')

    # get data leads vs cpl per batch

    batch_cpl= pd.pivot_table(data=df_select, index=['batch'],     
                    values=['leads','importe_gastado'],
                    aggfunc={'leads':np.sum,'importe_gastado':np.sum},
                    fill_value=0
    )
    batch_cpl['cpl']= round(batch_cpl['importe_gastado'] / batch_cpl['leads'],2)

    # now create the visualization ------------------------------ 

    leads_vs_cpl = make_subplots(specs=[[{'secondary_y':True}]])

    leads_vs_cpl.add_trace(
        go.Scatter(
            x= batch_cpl.index,
            y= batch_cpl['cpl'],
            name= 'Cost per Lead'),
            secondary_y=True
    )
    leads_vs_cpl.add_trace(
        go.Bar(
            x= batch_cpl.index,
            y= batch_cpl['leads'],
            name= 'Leads per Batch'),
            secondary_y= False
    )
    leads_vs_cpl.update_layout(
        title='<b>Leads vs CPL per Batch</b>',
        xaxis_title='Batch',
        yaxis_title='Leads vs CPL',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    leads_vs_cpl.update_yaxes(
        title_text='Cost per Lead',
        secondary_y=True
    )    
    leads_vs_cpl.update_yaxes(
        title_text='Leads per Batch',
        secondary_y=False
    )
    leads_vs_cpl.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y2', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=True
    )
    leads_vs_cpl.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=False
    )    

    # get data alumns vs cac per batch

    batch_cac= pd.pivot_table(data=df_select, index=['batch'],     
                    values=['inscrito','importe_gastado'],
                    aggfunc={'inscrito':np.sum,'importe_gastado':np.sum},
                    fill_value=0
    )
    batch_cac['cac']= round(batch_cac['importe_gastado'] / batch_cac['inscrito'],2)

    # now create the visualization ------------------------------ 

    alumns_vs_cac = make_subplots(specs=[[{'secondary_y':True}]])

    alumns_vs_cac.add_trace(
        go.Scatter(
            x= batch_cac.index,
            y= batch_cac['cac'],
            name= 'CAC'),
            secondary_y=True
    )
    alumns_vs_cac.add_trace(
        go.Bar(
            x= batch_cac.index,
            y= batch_cac['inscrito'],
            name= 'Alumns per Batch'),
            secondary_y= False
    )
    alumns_vs_cac.update_layout(
        title='<b>Alumns vs CAC per Batch</b>',
        xaxis_title='Batch',
        yaxis_title='Alumns vs CAC',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    alumns_vs_cac.update_yaxes(
        title_text='CAC',
        secondary_y=True
    )    
    alumns_vs_cac.update_yaxes(
        title_text='Alumns per Batch',
        secondary_y=False
    )
    alumns_vs_cac.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y2', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=True
    )
    alumns_vs_cac.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=False
    )  

    # two new columns to display these graphs:
    # leads vs cpl & alumns vs cac

    left_column, right_column= st.columns(2)

    # choosing where my plots will be displayed

    left_column.plotly_chart(leads_vs_cpl, use_container_width=True)
    right_column.plotly_chart(alumns_vs_cac, use_container_width=True)

    # new markdown------------------------------------------------

    st.markdown('---')
