
import streamlit as st
import pickle
import numpy as np
import pandas as pd
from PIL import Image

# import metrics data

url= 'https://raw.githubusercontent.com/BryanPonce/marketing-app/main/dataset_mkt_19_09.csv'
df =  pd.read_csv(url, encoding='ISO-8859-1')

# replace characters to avoid problems with the streamlit filter

df.columns = df.columns.str.replace(' ', '_')

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

# import trained model ------------------------------------------------

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
data = load_model()

regressor = data["model"]

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
    #image = Image.open('Zona_Rio_Tijuana.jpg')
    #st.image(image, caption = 'Zona Rio is one of the most popular areas of Tijuana')

    lead_ass_rate= round((df_select['asistio'].sum() / df_select['leads'].sum()),2)
    lead_hb_rate= round((df_select['leads_hubspot'].sum() / df_select['leads'].sum()), 2)
    lead_hb_ass_rate= round((df_select['asistio'].sum() / df_select['leads_hubspot'].sum()), 2)
    hb_cvr= round((df_select['inscrito'].sum() / df_select['leads_hubspot'].sum()), 2)
    paid_cvr= round((df_select['inscrito'].sum() / df_select['leads'].sum()), 2)

    # first, let's find out our assistants objective

    st.subheader(f'How many assistants do we need?')
    assistants = st.slider("Assistants:", 100,800, step= 25)
    
    ass_leads_rate= int(assistants/lead_ass_rate)

    st.write(f'Your Campaign lead to assistant rate in the last batch was {lead_ass_rate*100}%. Recommendation: Always consider an improvement for this new cycle.')
    st.write(f'With this assitants and your Campaign lead to assistant rate in the last batch, you will get around {ass_leads_rate:,} leads.')

    # now, let's find how many leads do we need 
    
    st.subheader(f'How many leads can we get?')
    leads = st.slider("Leads:", 250,5000, step= 50)

    leads_hb_rate= int(leads*lead_hb_rate)

    st.write(f'Your Campaign lead to Hubspot lead rate in the last batch was {lead_hb_rate*100}%. Recommendation: Always consider an improvement for this new cycle.')
    st.write(f'With this Campaign leads and your campaign lead to Hubspot lead rate in the last batch, you will get around {leads_hb_rate:,} Hubspot leads.')

    # how many leads we want to get in hubspot

    st.subheader(f'How many leads in Hubspot are we expecting?')
    leads_hb = st.slider("Hubspot Leads:", 250,5000, step= 50)

    exp_alumns= int(leads_hb*hb_cvr)

    st.write(f'In the last batch, the conversion rate of Hubspot leads was {hb_cvr*100}%. Recommendation: Always consider an improvement for this new cycle.')
    st.write(f'With this Hubspot leads and your conversion rate in the last batch, you will get around {exp_alumns:,} new alumns.')

    st.subheader(f'Which school are we advertising? (select one)')
    st.write(f'Selected School = 1 Not Selected = 0')
    sch_cod = st.slider("Coding:", 0,1)
    sch_dat = st.slider("Data:",  0,1)
    sch_mkt = st.slider("Marketing:",  0,1)
    sch_ux = st.slider("UX/UI:",  0,1)
    sch_unk= 0

    st.subheader(f'Which platform are we advertising on? (select one)')
    st.write(f'Selected Platform = 1 Not Selected = 0')
    plat_fb = st.slider("Facebook:", 0,1)
    plat_gads = st.slider("Google:",  0,1)
    plat_in = st.slider("Linked In:",  0,1)
    plat_tt = st.slider("Tik Tok:",  0,1)

    ok = st.button("Calculate my investment suggestion")
    if ok:

        # columns: 'asistio','leads','leads_hubspot', 'school_is_coding', 
        #          'school_is_data','school_is_marketing', 'school_is_unknown', 
        #          'school_is_ux','platform_is_facebook_ads', 'platform_is_google_ads',
        #          'platform_is_linkedin_ads', 'platform_is_tiktok_ads'

        x = np.array([[assistants,leads,leads_hb, sch_cod, sch_dat, 
                      sch_mkt,sch_ux,sch_unk,plat_fb,plat_gads,plat_in,
                      plat_tt
                      ]])
        x = x.astype(float)
        
        investment_sugg = regressor.predict(x)

        st.subheader(f'Your investment suggestion is $ {investment_sugg[0]:,.2f} MXN')
        pred_cac= int(investment_sugg/exp_alumns)
        st.write(f'With this investment and your forecasted alumns, your CAC would be around $ {pred_cac:,} MXN.')