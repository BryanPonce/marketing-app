
# coding=ISO-8859-1

# import required libraries for this page

import pandas as pd
import numpy as np 
import plotly.express as px #---- pip install plotly-express
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st #---- pip install streamlit

def load_df():

    url= 'https://raw.githubusercontent.com/BryanPonce/marketing-app/main/dataset_mkt_21_09.csv'
    df =  pd.read_csv(url, encoding='ISO-8859-1')

    df.columns = df.columns.str.replace(' ', '_')
    
    df['batch']= df['batch'].astype(int)
    df['inicio_del_informe']= df['inicio_del_informe'].astype('datetime64[ns]')
    df['nombre_del_conjunto_de_anuncios']= df['nombre_del_conjunto_de_anuncios'].astype(str)
    df['campaign_name']= df['campaign_name'].astype(str)
    df['leads']= df['leads'].astype(int)
    df['clics']= df['clics'].astype(int)
    df['impresiones']= df['impresiones'].astype(int)
    df['importe_gastado']= df['importe_gastado'].astype(float)
    df['paid']= df['paid'].astype(int)
    df['leads_hubspot']= df['leads_hubspot'].astype(int)
    df['escuela']= df['escuela'].astype(str)
    df['fuente_original']= df['fuente_original'].astype(str)
    df['desglose_de_fuente_original_1']= df['desglose_de_fuente_original_1'].astype(str)
    df['plataforma_ad']= df['plataforma_ad'].astype(str)
    df['desglose_de_fuente_original_2']= df['desglose_de_fuente_original_2'].astype(str)
    df['kw_paid_search']= df['kw_paid_search'].astype(str)
    df['sesion']= df['sesion'].astype(str)
    df['registro_eb']= df['registro_eb'].astype(int)
    df['asistio']= df['asistio'].astype(int)
    df['ensayo']= df['ensayo'].astype(int)
    df['ventas']= df['ventas'].astype(float)
    df['inscrito']= df['inscrito'].astype(int)
    df['fecha_de_creacion']= df['fecha_de_creacion'].astype('datetime64[ns]')
    df['dia']= df['dia'].astype(str)
    df['hora']= df['hora'].astype(str)

    return df

df= load_df()

# create a pivot table to find new metrics in dataset

df1= pd.pivot_table(data=df,index=['batch','inicio_del_informe','paid','plataforma_ad',
                'fuente_original','desglose_de_fuente_original_1',
                'desglose_de_fuente_original_2','escuela','sesion','dia','hora'
                ],
                values=['importe_gastado','leads','leads_hubspot','registro_eb',
                'asistio','ensayo','inscrito','ventas'
                ],
                aggfunc={'importe_gastado': np.sum,'leads': np.sum ,'leads_hubspot':np.sum,
                'registro_eb':np.sum,'asistio':np.sum,'ensayo':np.sum,'inscrito':np.sum,
                'ventas':np.sum
                },
                fill_value=0
)

df1=df1.reset_index()

df1['eb_rate']= (df1['registro_eb'] / df1['leads_hubspot'])*100
df1['ass_rate']= (df1['asistio'] / df1['leads_hubspot'])*100
df1['cvr']= (df1['inscrito'] / df1['leads_hubspot'])*100
df1['roas']= df1['ventas'] / df1['importe_gastado']
df1.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# create a function to show data on specific page in streamlit 

def show_analyze_call_center():

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
    semana_s = st.sidebar.multiselect(
        'Need to see a specific week?',
        options= df1['inicio_del_informe'].unique(),
        default= df1['inicio_del_informe'].unique()
    )

    # ------- connect sidebar to dataframe ------

    df_select = df1.query('batch == @batch_s & escuela == @escuela_s & paid == @paid_s & plataforma_ad == @plataforma_s & inicio_del_informe == @semana_s')

    # select for streamlit the filtered dataset

    #st.dataframe(df_select)

    # -------- streamlit page name --------

    st.title('Dashboard All In One: Call Center :bar_chart:')
    st.markdown('##')

    # create variables for streamlit kpi section --------------------------------------------------------------------------------------------

    leads_total= df_select['leads_hubspot'].sum()
    eb_total= df_select['registro_eb'].sum()
    eb_rate= round(((df_select['registro_eb'].sum() / df_select['leads_hubspot'].sum())*100), 1)
    asist_total= df_select['asistio'].sum()
    asist_rate= round(((df_select['asistio'].sum() / df_select['registro_eb'].sum())*100), 1)
    asist_rate_total= round(((df_select['asistio'].sum() / df_select['leads_hubspot'].sum())*100), 1)
    ensayo_total= df_select['ensayo'].sum()
    ensayo_rate= round(((df_select['ensayo'].sum() / df_select['asistio'].sum())*100), 1)
    ensayo_rate_total= round(((df_select['ensayo'].sum() / df_select['leads_hubspot'].sum())*100), 1)
    ins_total= df_select['inscrito'].sum()
    ins_rate= round(((df_select['inscrito'].sum() / df_select['ensayo'].sum())*100), 1)
    cvr_total= round(((df_select['inscrito'].sum() / df_select['leads_hubspot'].sum())*100), 1)
    

    # divide streamlit section in two columns

    left_column, right_column= st.columns(2)

    # order data for streamlit kpi section display

    with left_column:
        st.subheader('Rates based on total leads')
        st.write(f'Leads on Hubspot: {leads_total:,}')   
        st.write(f'Total EB Registrations: {eb_total:,}')
        st.write(f'Total EB Rate: {eb_rate:,} %')
        st.write(f'Total Assistants: {asist_total:,}')
        st.write(f'Total Assistance Rate: {asist_rate_total} %')
        st.write(f'Total Essays: {ensayo_total:,}')
        st.write(f'Total Essay Rate: {ensayo_rate_total} %')
        st.write(f'Total Alumns: {ins_total:,}')
        st.write(f'Conversion Rate: {cvr_total} %')
        
    with right_column:
        st.subheader('Stage rates based on previous step')
        st.write(f'Leads on Hubspot: {leads_total:,}')   
        st.write(f'EB Registrations: {eb_total:,}')
        st.write(f'EB Rate: {eb_rate:,} %')
        st.write(f'Total Assistants: {asist_total:,}')
        st.write(f'Assistance Rate: {asist_rate} %')
        st.write(f'Total Essays: {ensayo_total:,}')
        st.write(f'Essay Rate: {ensayo_rate} %')
        st.write(f'Total Alumns: {ins_total:,}')
        st.write(f'Alumn Rate: {ins_rate} %')
        
    st.markdown('---')

    # eb registration vs day of the week--------------------------------------------------------------------------------
    
    st.subheader('This plot shows how assistance rate behaves depending on the day users submit their contact information')
    
    eb_x_day= pd.pivot_table(data=df_select, index=['dia'],     
                    values=['registro_eb','leads_hubspot'],
                    aggfunc={'registro_eb':np.sum,'leads_hubspot':np.sum},
                    fill_value=0
    )
    eb_x_day= eb_x_day.reset_index()
    eb_x_day['eb_rate']= round((eb_x_day['registro_eb'] / eb_x_day['leads_hubspot']*100),1)

    eb_vs_day = make_subplots(specs=[[{'secondary_y':True}]])

    eb_vs_day.add_trace(
        go.Scatter(
            x= eb_x_day['dia'],
            y= eb_x_day['eb_rate'],
            name= 'EB Registration Rate %'),
            secondary_y=True
    )
    eb_vs_day.add_trace(
        go.Bar(
            x= eb_x_day['dia'],
            y= eb_x_day['registro_eb'],
            name= 'EB Registrations'),
            secondary_y= False
    )
    eb_vs_day.update_layout(
        title='<b>EB Registration Rate per Day</b>',
        xaxis_title='Day of the Week',
        yaxis_title='Registrations per Day',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    eb_vs_day.update_yaxes(
        title_text='Registration Rate %',
        secondary_y=True
    )    
    eb_vs_day.update_yaxes(
        title_text='Registered Users per Day',
        secondary_y=False
    )
    eb_vs_day.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y2', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=True
    )
    eb_vs_day.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=False
    )

    st.write(eb_vs_day)
    st.markdown('---')

# cvr vs day of the week--------------------------------------------------------------------------------
    
    st.subheader('This plot shows how CVR behaves depending on the day users submit their contact information')
    
    alumn_x_day= pd.pivot_table(data=df_select, index=['dia'],     
                    values=['inscrito','leads_hubspot'],
                    aggfunc={'inscrito':np.sum,'leads_hubspot':np.sum},
                    fill_value=0
    )
    alumn_x_day= alumn_x_day.reset_index()
    alumn_x_day['cvr']= round((alumn_x_day['inscrito'] / alumn_x_day['leads_hubspot']*100),1)

    alumn_vs_day = make_subplots(specs=[[{'secondary_y':True}]])

    alumn_vs_day.add_trace(
        go.Scatter(
            x= alumn_x_day['dia'],
            y= alumn_x_day['cvr'],
            name= 'Conversion Rate %'),
            secondary_y=True
    )
    alumn_vs_day.add_trace(
        go.Bar(
            x= alumn_x_day['dia'],
            y= alumn_x_day['inscrito'],
            name= 'Alumns'),
            secondary_y= False
    )
    alumn_vs_day.update_layout(
        title='<b>Alumns vs Day of Submission</b>',
        xaxis_title='Day of the Week',
        yaxis_title='Alumns vs Submission Day',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    alumn_vs_day.update_yaxes(
        title_text='Conversion Rate %',
        secondary_y=True
    )    
    alumn_vs_day.update_yaxes(
        title_text='Alumns',
        secondary_y=False
    )
    alumn_vs_day.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y2', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=True
    )
    alumn_vs_day.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=False
    )

    st.write(alumn_vs_day)
    st.markdown('---')

    # eb registration vs hour of the day--------------------------------------------------------------------------------
    
    st.subheader('This plot shows how assistance rate behaves depending on the hour users submit their contact information')
    
    eb_x_hour= df_select[df_select['paid']==0]
    
    eb_x_hour= pd.pivot_table(data=eb_x_hour, index=['hora'],     
                    values=['registro_eb','leads_hubspot'],
                    aggfunc={'registro_eb':np.sum,'leads_hubspot':np.sum},
                    fill_value=0
    )
    eb_x_hour= eb_x_hour.reset_index()
    eb_x_hour['eb_rate']= round((eb_x_hour['registro_eb'] / eb_x_hour['leads_hubspot']*100),1)

    eb_vs_hour = make_subplots(specs=[[{'secondary_y':True}]])

    eb_vs_hour.add_trace(
        go.Scatter(
            x= eb_x_hour['hora'],
            y= eb_x_hour['eb_rate'],
            name= 'EB Registration Rate %'),
            secondary_y=True
    )
    eb_vs_hour.add_trace(
        go.Bar(
            x= eb_x_hour['hora'],
            y= eb_x_hour['registro_eb'],
            name= 'EB Registrations'),
            secondary_y= False
    )
    eb_vs_hour.update_layout(
        title='<b>EB Registration Rate per Hour</b>',
        xaxis_title='Hour of the Day',
        yaxis_title='Registrations per Hour',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    eb_vs_hour.update_yaxes(
        title_text='Registration Rate %',
        secondary_y=True
    )    
    eb_vs_hour.update_yaxes(
        title_text='Registered Users per Hour',
        secondary_y=False
    )
    eb_vs_hour.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y2', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=True
    )
    eb_vs_hour.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=False
    )

    st.write(eb_vs_hour)
    st.markdown('---')

# cvr vs day of the week--------------------------------------------------------------------------------
    
    st.subheader('This plot shows how CVR behaves depending on the hour users submit their contact information')
    
    alumn_x_hour= df_select[df_select['paid']==0]
    
    alumn_x_hour= pd.pivot_table(data=alumn_x_hour, index=['hora'],     
                    values=['inscrito','leads_hubspot'],
                    aggfunc={'inscrito':np.sum,'leads_hubspot':np.sum},
                    fill_value=0
    )
    alumn_x_hour= alumn_x_hour.reset_index()
    alumn_x_hour['cvr']= round((alumn_x_hour['inscrito'] / alumn_x_hour['leads_hubspot']*100),1)

    alumn_vs_hour = make_subplots(specs=[[{'secondary_y':True}]])

    alumn_vs_hour.add_trace(
        go.Scatter(
            x= alumn_x_hour['hora'],
            y= alumn_x_hour['cvr'],
            name= 'Conversion Rate %'),
            secondary_y=True
    )
    alumn_vs_hour.add_trace(
        go.Bar(
            x= alumn_x_hour['hora'],
            y= alumn_x_hour['inscrito'],
            name= 'Alumns'),
            secondary_y= False
    )
    alumn_vs_hour.update_layout(
        title='<b>Alumns vs Hour of Submission</b>',
        xaxis_title='Hour of the Day',
        yaxis_title='Alumns vs Submission Day',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=(dict(showgrid=False)),
    )
    alumn_vs_hour.update_yaxes(
        title_text='Conversion Rate %',
        secondary_y=True
    )    
    alumn_vs_hour.update_yaxes(
        title_text='Alumns',
        secondary_y=False
    )
    alumn_vs_hour.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y2', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=True
    )
    alumn_vs_hour.update_yaxes(
        rangemode='tozero', 
        scaleanchor='y', 
        scaleratio=1, 
        constraintoward='bottom', 
        secondary_y=False
    )

    st.write(alumn_vs_hour) 
