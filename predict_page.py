
# coding=ISO-8859-1

import streamlit as st
import pickle
import numpy as np
import pandas as pd
#from PIL import Image

# import trained model ------------------------------------------------

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
data = load_model()

regressor = data["model"]

def load_df():

    url= 'https://raw.githubusercontent.com/BryanPonce/marketing-app/main/dataset_mkt_28_09.csv'
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

# for this page we will only use marketing information, so i select only paid media

df1=df[df['paid']==1]

df1= pd.pivot_table(data=df1,
                   index=['batch','plataforma_ad','escuela'
                   ],
                   values=['importe_gastado','leads','leads_hubspot',
                   'asistio','inscrito','ventas'
                   ],
                   aggfunc={'importe_gastado': np.sum,'leads': np.sum,
                   'leads_hubspot':np.sum,'asistio':np.sum,'inscrito':np.sum,
                   'ventas':np.sum
                   },
                   fill_value=0
)

df1=df1.reset_index()

max_batch= df1['batch'].max()
last_batch= max_batch-1

df1=df1[df1['batch']==last_batch]

df1.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

def show_predict_page():

    # ------- sidebar --------

    st.sidebar.header('Where are we investing?')
    school_s = st.sidebar.multiselect(
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

    df_select = df1.query('escuela == @school_s & plataforma_ad == @plataforma_s')

    # select for streamlit the filtered dataset

    # st.dataframe(df_select)

    st.title("Marketing Investment Predictor")
    
    st.write("""### Find out how much we need to invest to get the desired results!""")
    st.write(f'Tip: Filter the channel and the school you are advertising and receive dynamic insights based on the last batch.')
    st.write(f'Depending on your forecasted metrics and the selected filters on the sidebar, the predicted numbers for each customer funnel stage will change')
    #image = Image.open('Zona_Rio_Tijuana.jpg')
    #st.image(image, caption = 'Zona Rio is one of the most popular areas of Tijuana')

    lead_ass_rate= df_select['asistio'].sum() / df_select['leads'].sum()
    lead_hb_rate= round((df_select['leads_hubspot'].sum() / df_select['leads'].sum()), 2)
    lead_hb_ass_rate= round((df_select['asistio'].sum() / df_select['leads_hubspot'].sum()), 2)
    hb_cvr= round((df_select['inscrito'].sum() / df_select['leads_hubspot'].sum()), 2)
    paid_cvr= round((df_select['inscrito'].sum() / df_select['leads'].sum()), 2)
    assistants= df_select['asistio'].sum()

    # first, let's find out our assistants objective

    st.subheader(f'How many assistants do we need?')
    st.write(f'This is the number of assistants obtained in Batch {last_batch}: {assistants:,}')

    asistio = st.slider("Assistants:",100,800, step= 20)
    
    ass_leads_rate= int(asistio/lead_ass_rate)

    st.write(f'Your Campaign lead to assistant rate in the last batch was {(lead_ass_rate*100):,.0f} %. Recommendation: Always consider an improvement for this new cycle.')
    st.write(f'With this assitants and your Campaign lead to assistant rate in the last batch, you will get around {ass_leads_rate:,} leads.')

    # now, let's find how many leads do we need 
    
    st.subheader(f'How many leads can we get?')
    leads = st.slider("Leads:",250,7000, step= 50)

    leads_hb_rate= int(leads*lead_hb_rate)

    st.write(f'Your Campaign lead to Hubspot lead rate in the last batch was {(lead_hb_rate*100):,.0f} %. Recommendation: Always consider an improvement for this new cycle.')
    st.write(f'With this Campaign leads and your campaign lead to Hubspot lead rate in the last batch, you will get around {leads_hb_rate:,} Hubspot leads.')

    # how many leads we want to get in hubspot

    st.subheader(f'How many leads in Hubspot are we expecting?')
    leads_hubspot = st.slider("Hubspot Leads:",250,7000, step= 50)

    exp_alumns= int(leads_hubspot*hb_cvr)

    st.write(f'In the last batch, the conversion rate of Hubspot leads was {(hb_cvr*100):,.0f} %. Recommendation: Always consider an improvement for this new cycle.')
    st.write(f'With this Hubspot leads and your conversion rate in the last batch, you will get around {exp_alumns:,} new alumns.')
    
    mes_cat = st.selectbox('On which month are we advertising? (select one)', 
    ('January',
     'February', 
     'March', 
     'April',
     'May',
     'June',
     'July',
     'August',
     'September',
     'October',
     'November',
     'December'
    ))
    if mes_cat == 'January':
        mes_cat =4
    elif mes_cat == 'February':
        mes_cat =3
    elif mes_cat == 'March':
        mes_cat =7
    elif mes_cat == 'April':
        mes_cat =0
    elif mes_cat == 'May':
        mes_cat =8
    elif mes_cat == 'June':
        mes_cat =6
    elif mes_cat == 'July':
        mes_cat =5
    elif mes_cat == 'August':
        mes_cat =1
    elif mes_cat == 'September':
        mes_cat =11
    elif mes_cat == 'October':
        mes_cat =10
    elif mes_cat == 'November':
        mes_cat =9
    elif mes_cat == 'December':
        mes_cat =2    


    #st.subheader(f'Which school are we advertising? (select one)')
    #st.write(f'Selected School = 1 Not Selected = 0')
    #school_is_coding = st.slider("Coding:", 0,1)
    #school_is_data = st.slider("Data:",  0,1)
    #school_is_marketing = st.slider("Marketing:",  0,1)
    #school_is_ux = st.slider("UX/UI:",  0,1)
    #school_is_unknown = 0

    escuela_cat = st.selectbox('Which school are we advertising? (select one)', 
    ('Coding',
     'Data', 
     'UX/UI', 
     'Marketing'
    ))
    if escuela_cat == 'Coding':
        escuela_cat =0
    elif escuela_cat == 'Data':
        escuela_cat =1
    elif escuela_cat == 'UX/UI':
        escuela_cat =4 
    elif escuela_cat == 'Marketing':
        escuela_cat =2

    #st.subheader(f'Which platform are we advertising on? (select one)')
    #st.write(f'Selected Platform = 1 Not Selected = 0')
    #platform_is_facebook_ads = st.slider("Facebook:", 0,1)
    #platform_is_google_ads = st.slider("Google:",  0,1)
    #platform_is_linkedin_ads = st.slider("Linked In:",  0,1)
    #platform_is_tiktok_ads = st.slider("Tik Tok:",  0,1)

    plataforma_ad_cat = st.selectbox('Which platform are we advertising on? (select one)', 
    ('Facebook',
     'Google', 
     'Linked In', 
     'Tik Tok'
    ))
    if plataforma_ad_cat == 'Facebook':
        plataforma_ad_cat =0
    elif plataforma_ad_cat == 'Google':
        plataforma_ad_cat =1
    elif plataforma_ad_cat == 'Linked In':
        plataforma_ad_cat =2 
    elif plataforma_ad_cat == 'Tik Tok':
        plataforma_ad_cat =3

    ok = st.button("Calculate my investment suggestion")
    if ok:
        
        # columns: 'asistio','leads','leads_hubspot', 'school_is_coding', 
        #          'school_is_data','school_is_marketing', 'school_is_unknown', 
        #          'school_is_ux','platform_is_facebook_ads', 'platform_is_google_ads',
        #          'platform_is_linkedin_ads', 'platform_is_tiktok_ads'

        #x = np.array([[leads,leads_hubspot, 
        #              school_is_coding, school_is_data, 
        #              school_is_marketing,school_is_unknown,
        #              school_is_ux,
        #              platform_is_facebook_ads,platform_is_google_ads,
        #              platform_is_linkedin_ads,platform_is_tiktok_ads
        #              ]])

        # columns: 'leads','leads_hubspot','asistio',
        # 'escuela_cat','plataforma_ad_cat','mes_cat'

        x = np.array([['leads','leads_hubspot','asistio',
                       'plataforma_ad_cat','escuela_cat',
                       'mes_cat']])
        
        x = x.astype(float)
        
        investment_sugg = regressor.predict(x)
        exp_cpa= investment_sugg / asistio

        st.subheader(f'Your investment suggestion is $ {investment_sugg[0]:,.2f} MXN')
        pred_cac= int(investment_sugg/exp_alumns)
        st.subheader(f'These are the expected metrics with this investment suggestion:')
        st.write(f'You will get around {exp_alumns:,} new alumns')
        st.write(f'Your CAC would be around $ {pred_cac:,} MXN.')
        st.write(f'Your campaigns will get around {ass_leads_rate:,} paid leads')
        st.write(f'We can expect around {leads_hb_rate:,} Hubspot leads')
        st.write(f'Our assistants goal is: {asistio:,} assistants')
        st.write(f'The expected cost per assistant is: $ {exp_cpa[0]:,.2f} MXN')

        # hide streamlit style---------------

    hide_style= """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

    st.markdown(hide_style, unsafe_allow_html=True)
