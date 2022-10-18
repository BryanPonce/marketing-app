# -*- coding: utf-8 -*-
"""model_testing_marketing_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14vp6voCgJTMCRtyVStTRP7lhqulIQEt9
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_df():

    url= 'https://raw.githubusercontent.com/BryanPonce/marketing-app/main/dataset_mkt_28_09.csv'
    df =  pd.read_csv(url, encoding='ISO-8859-1')

    df.columns = df.columns.str.replace(' ', '_')
    
    
    return df

df= load_df()

df['importe_gastado'].value_counts()

df.info()

# filtering df to use only paid metrics

df1= df[df['paid']==1]

# filtering df to ignore campaigns not properly tagged

# values=['0']
# df1 = df1[df1.campaign_name.isin(values) == False]

# values_2=['redes sociales de pago']
# df1 = df1[df1.desglose_de_fuente_original_2.isin(values_2) == False]

# values_3=[0]
# df1 = df1[df1.importe_gastado.isin(values_3) == False]

# grouping dataset by labels to cross platform data

df1= pd.pivot_table(data=df1,
                    index=['escuela','plataforma_ad','fecha_de_creacion','mes'
                          ],
                    values=['leads','clics','impresiones','importe_gastado',
                            'leads_hubspot','registro_eb','asistio','ensayo',
                            'ventas','inscrito'
                           ],
                    aggfunc={'leads': np.sum,'clics': np.sum ,
                             'impresiones': np.sum,'importe_gastado':np.sum,
                             'leads_hubspot':np.sum,'registro_eb':np.sum,
                             'asistio':np.sum,'ensayo':np.sum,'ventas':np.sum,
                             'inscrito':np.sum
                             },
                    fill_value=0
)

df1=df1.reset_index()

# trying to find new metrics that has better correlations scores to predict
# with my models. not very succesful...

# df1['cpl_hubspot']= round(df1['importe_gastado'] / df1['leads_hubspot'],2)
# df1['cpl_campaigns']= round(df1['importe_gastado'] / df1['leads'],2)
# df1['costo_registro']= round(df1['importe_gastado'] / df1['registro_eb'],2)
# df1['costo_asistente']= round(df1['importe_gastado'] / df1['asistio'],2)
# df1['costo_ensayo']= round(df1['importe_gastado'] / df1['ensayo'],2)
# df1['cac']= round(df1['importe_gastado'] / df1['inscrito'],2)
# df1['roas']= round(df1['ventas'] / df1['importe_gastado'],2)
# df1['cvr']= round(df1['inscrito'] / df1['leads'],2)
# df1['paid_hs_rate']= round(df1['leads_hubspot'] / df1['leads'],2)
# df1['hs_eb_rate']= round(df1['registro_eb'] / df1['leads_hubspot'],2)
# df1['eb_ass_rate']= round(df1['asistio'] / df1['registro_eb'],2)
# df1['paid_ass_rate']= round(df1['asistio'] / df1['leads'],2)

df1 = df1.reindex(columns=[
    'fecha_de_creacion','mes','escuela','plataforma_ad','importe_gastado',
    'leads','leads_hubspot','asistio'
    ]
)

df1

sns.pairplot(df1)

# turning categoric columns' dtypes

df1['escuela'] = df1['escuela'].astype('category')
df1['plataforma_ad'] = df1['plataforma_ad'].astype('category')
df1['mes'] = df1['mes'].astype('category')
# df1['campaign_name'] = df1['campaign_name'].astype('category')
# df1['desglose_de_fuente_original_2'] = df1[
#     'desglose_de_fuente_original_2'].astype('category')

# # encoding labels

df1['escuela_cat'] = df1['escuela'].cat.codes

# # escuela      ---------
# # coding       0
# # data         1
# # marketing    2
# # unknown      3
# # ux           4

df1['plataforma_ad_cat'] = df1['plataforma_ad'].cat.codes

# # plataforma_ad   ---------
# # facebook_ads    0
# # google_ads      1
# # linkedin_ads    2
# # tiktok_ads      3

df1['mes_cat'] = df1['mes'].cat.codes

# # mes   ---------
# April      0 
# August     1 
# December   2 
# February   3 
# January    4  
# July       5
# June       6 
# March      7 
# May        8
# November   9         
# October    10         
# September  11         
         
# df1['desglose_de_fuente_original_2_cat'] = df1[
#     'desglose_de_fuente_original_2'].cat.codes

# # desglose_de_fuente_original_2
# # becas - gen 6                                         0
# # becas - traffic - gen 10                              1
# # coding-isa                                            2
# # conversions-coding                                    3
# # conversions-coding-puebla                             4
# # conversions-marketing                                 5
# # conversions-marketing-rtg                             6
# # conversions-ux-ui                                     7
# # conversions-ux-ui-rtg                                 8
# # data-isa                                              9
# # discovery-coding                                     10
# # discovery-data                                       11
# # discovery-marketing                                  12
# # discovery-ux-ui                                      13
# # display inteligente -master-data science/ai gen 7    14
# # display inteligente- master ux/ui gen 7              15
# # display inteligente-mastercoding-gen 7               16
# # facebook / none                                      17
# # home-conversiones                                    18
# # inmail-coding                                        19
# # inmail-data                                          20
# # inmail-marketing                                     21
# # inmail-ux-ui                                         22
# # linkedin-traffic-coding                              23
# # linkedin-traffic-data                                24
# # linkedin-traffic-ux-ui                               25
# # m-coding-leads-gen 10+                               26
# # m-data-autochat-gen 10+                              27
# # m-data-conversions-gen 10                            28
# # m-data-conversions-rtg-gen 10                        29
# # m-data-leads-gen 10                                  30
# # m-marketing-leads-gen 10+                            31
# # m-uxui-autochat-gen 10+                              32
# # m-uxui-leads-gen 10+                                 33
# # master ux/ui gen 6                                   34
# # master- data science / ai                            35
# # mx-conversions-data                                  36
# # mx-conversions-ux-ui                                 37
# # mx2-conversions-data                                 38
# # mx2-conversions-ux-ui-8-aniversario                  39
# # mx2_conversions-coding                               40
# # mx2_conversions-coding-lal-asistentes-1              41
# # mx2_conversions-coding-lal-ensayos-1                 42
# # mx2_conversions-coding-lal-insc-3                    43
# # mx2_conversions-coding-rtg                           44
# # mx_conversions-coding                                45
# # search- marketing digital - gen 10                   46
# # search-branded                                       47
# # search-coding                                        48
# # search-coding-isa                                    49
# # search-competencia                                   50
# # testimonios                                          51
# # tik-tok-conversions-coding                           52
# # tik-tok-conversions-data                             53
# # tik-tok-lead-gen-coding                              54
# # tik-tok-lead-gen-data                                55
# # tik-tok-traffic-coding                               56
# # tik-tok-traffic-data                                 57
# # tik-tok-traffic-marketing                            58
# # tik-tok-traffic-ux-ui                                59
# # traffic-data                                         60
# # traffic-hackerfest                                   61
# # traffic-marketing                                    62
# # traffic-quiz-typeform                                63
# # traffic-ux-ui                                        64

# df1['campaign_name_cat'] = df1['campaign_name'].cat.codes

# # campaign_name
# # Becas - Conversiones - Gen 10+                          0
# # Becas - Search                                          1
# # Becas - Traffic - Gen 10+                               2
# # Discovery - Master en Marketing -G10+                   3
# # Discovery -Master-Data Science/AI Gen 10 +              4
# # Discovery- Master UX/UI Gen 10+                         5
# # Discovery-MasterCoding-Gen 10+                          6
# # Display Inteligente -Master-Data Science/AI Gen 10+     7
# # Display Inteligente- Master UX/UI Gen 10+               8
# # Display Inteligente-MasterCoding-Gen 10+                9
# # InMail_Coding_Lead Gen                                 10
# # InMail_Data_Lead Gen                                   11
# # InMail_Marketing_Lead Gen                              12
# # InMail_UX/UI_Lead Gen                                  13
# # M-Coding - Traffic- Gen 10+                            14
# # M-Coding-Conversions ISA-Gen 10+                       15
# # M-Coding-Conversions-Gen 10+                           16
# # M-Coding-Conversions-Gen 15+                           17
# # M-Coding-Conversions-Gen 15+\n                         18
# # M-Coding-Conversions-Puebla-Gen 15+                    19
# # M-Coding-LeadGen-Gen 10+                               20
# # M-Coding-Leads-Gen 10+                                 21
# # M-Coding-Traffic-Gen 10+                               22
# # M-DATA-Conversions-Gen 10+                             23
# # M-DATA-Conversions-RTG-Gen 10+                         24
# # M-Data-Autochat-Gen 10+                                25
# # M-Data-Conversiones-Gen 15+                            26
# # M-Data-Conversions ISA-Gen 16+                         27
# # M-Data-LeadGen-Gen 10+                                 28
# # M-Data-Leads-Gen 10                                    29
# # M-Data-Traffic-Gen 10+                                 30
# # M-HackFest-Trafico_25/03                               31
# # M-Home_Conversions - Gen 10+                           32
# # M-Marketing-Conversions Gen 10+                        33
# # M-Marketing-Conversions-RTG Gen 10+                    34
# # M-Marketing-Leads-Gen 10+                              35
# # M-Marketing-Traffic-Gen 10+                            36
# # M-Marketing-Traffic-Gen10                              37
# # M-UX/UI-Traffic-Gen 10+                                38
# # M-UXUI-Autochat-Gen 10+                                39
# # M-UXUI-Conversions-Gen 10+                             40
# # M-UXUI-Conversions-RTG-Gen 10+                         41
# # M-UXUI-Leads-Gen 10+                                   42
# # M-UXUI-Traffic-Gen 10+                                 43
# # MX2_M-Coding-Conversions-Gen 18+                       44
# # MX2_M-DATA-Conversions-Gen 18+                         45
# # MX2_M-UXUI-Conversions-Gen 18+                         46
# # MX_M-Coding-Conversions-Gen 16+                        47
# # MX_M-DATA-Conversions-Gen 16+                          48
# # MX_M-UXUI-Conversions-Gen 16+                          49
# # M_Coding_Traffic_Gen16+                                50
# # M_DATA_Traffic_G16+                                    51
# # M_Quiz_Trafico_04/05                                   52
# # M_Quiz_Trafico_05/04                                   53
# # M_UX/UI_Traffic_Gen16+                                 54
# # Search -Master-Data Science/AI Gen 10+                 55
# # Search- Marketing Digital - Gen 10+                    56
# # Search- Master UX/UI Gen 10+                           57
# # Search-Branded DEV.F                                   58
# # Search-Coding-ISA-Gen 10+                              59
# # Search-Competencia-Gen 10+                             60
# # Search-MasterCoding-Gen 10+                            61

plat_cat=df1[['plataforma_ad','plataforma_ad_cat']]
esc_cat=df1[['escuela','escuela_cat']]
mes_cat=df1[['mes','mes_cat']]
mes_cat.value_counts()

# from sklearn.preprocessing import OneHotEncoder

# # creating instance of one-hot-encoder
# enc = OneHotEncoder(handle_unknown='ignore')
# # passing bridge-types-cat column (label encoded values of bridge_types)
# enc_esc = pd.DataFrame(enc.fit_transform(df1[['escuela']]).toarray())
# enc_plat = pd.DataFrame(enc.fit_transform(df1[['plataforma_ad']]).toarray())

# # merge with main df bridge_df on key values
# df1_enc= df1.join(enc_esc)
# df1_enc= df1.join(enc_plat)

# dum_df1 = pd.get_dummies(df1, 
#                          columns=["escuela"], 
#                          prefix=["school_is"])
# dum_df1 = pd.get_dummies(dum_df1, 
#                          columns=["plataforma_ad"], 
#                          prefix=["platform_is"])

# dum_df1.dtypes

# finding correlation coefficients between columns
# i'm not including encoded columns. there's no correlation
# and the plot gets too big

#df1.corr(method ='pearson')
#df1.corr(method ='kendall')
#df1.corr(method='spearman')

corr = df1.corr(method='pearson')

kot = corr[corr>=0.5]
plt.figure(figsize=(12,8))
sns.heatmap(kot, annot=True, cmap="Greens")

# looking for the most important features in Dataset for prediction

#df1.corr(method='pearson').loc['asistio'].sort_values(ascending=False)
# assistants has a correlation coefficient of .89 with eventbrite registrations

#df1.corr(method='pearson').loc['registro_eb'].sort_values(ascending=False)
# eventbrite registrations has a correlation coefficient of .91 with hubspot leads

#df1.corr(method='pearson').loc['leads_hubspot'].sort_values(ascending=False)
# hubspot leads has a correlation coefficient of .58 with campaign leads

#df1.corr(method='pearson').loc['leads'].sort_values(ascending=False)
# campaign leads has a correlation coefficient of .78 with investment

df1.corr(method='pearson').loc['importe_gastado'].sort_values(ascending=False)

# i'm converting my categoric columns (uint8) into int64 because i think
# i'm having trouble with the input of the models 

# dum_df1['school_is_coding'] = dum_df1['school_is_coding'].astype(int)
# dum_df1['school_is_data'] = dum_df1['school_is_data'].astype(int)
# dum_df1['school_is_marketing'] = dum_df1['school_is_marketing'].astype(int)
# dum_df1['school_is_unknown'] = dum_df1['school_is_unknown'].astype(int)
# dum_df1['school_is_ux'] = dum_df1['school_is_ux'].astype(int)

# dum_df1['platform_is_facebook_ads'] = dum_df1[
#                                              'platform_is_facebook_ads'
#                                              ].astype(int)
# dum_df1['platform_is_google_ads'] = dum_df1[
#                                            'platform_is_google_ads'
#                                            ].astype(int)
# dum_df1['platform_is_linkedin_ads'] = dum_df1[
#                                              'platform_is_linkedin_ads'
#                                              ].astype(int)
# dum_df1['platform_is_tiktok_ads'] = dum_df1[
#                                            'platform_is_tiktok_ads'
#                                            ].astype(int)

# imagining the question i'm doing to my model:

# i'm gonna tell my assistants objective, my hubspot leads and campaign 
# leads forecasted, school and platform.

# and i want you to tell me how much i need to invest in this campaign to reach
# my objective 

# x= dum_df1[['asistio','leads','leads_hubspot',
#             'school_is_coding','school_is_data',
#             'school_is_marketing','school_is_unknown', 
#             'school_is_ux',
#             'platform_is_facebook_ads', 
#             'platform_is_google_ads',
#             'platform_is_linkedin_ads', 
#             'platform_is_tiktok_ads'
#             ]]     
# y= dum_df1[['importe_gastado']]


x= df1[['leads','leads_hubspot','asistio','plataforma_ad_cat','escuela_cat',
        'mes_cat'
        ]]     
y= df1[['importe_gastado']]

x

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, 
                                                    test_size = 0.2, 
                                                    random_state = 0)

x_test_df = pd.DataFrame(x_test)
x_test_df

from sklearn import metrics
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

# Ordinary Least Square

ols = linear_model.LinearRegression()
ols.fit(x_train,y_train)
np.mean(cross_val_score(ols, x_train, y_train, cv = 7, scoring = "r2"))

model = linear_model.Lasso()
print("Lasso regression score: ", np.round(
    np.mean(cross_val_score(model, 
                            x_train, 
                            y_train, 
                            cv = 7, 
                            scoring = "r2")), 5))

from sklearn.model_selection import GridSearchCV

# Lasso regression

alphas = [0.01, 0.1,0.5,0.75,1]
model = linear_model.Lasso()
grid_lasso = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas), cv=5)
grid_lasso.fit(x_train, y_train)
print("Lasso regression best alpha value: ", grid_lasso.best_estimator_.alpha)
print("Lasso regression with hyperparameter tuning best score: ", 
      np.round(grid_lasso.best_score_, 5))
print("Lasso regression improvement after hyperparameter tuning: {0}%".format(
    np.round((1 - ((np.round(np.mean(cross_val_score(model, 
                                                     x_train, 
                                                     y_train, 
                                                     cv = 5, 
                                                     scoring = "r2")), 5))
    / np.round(grid_lasso.best_score_, 5))) * 100, 5)))

# Ridge regression

model = linear_model.Ridge()
print("Ridge regression score: ", 
      np.round(np.mean(cross_val_score(model, 
                                       x_train, 
                                       y_train, 
                                       cv = 7, 
                                       scoring = "r2")), 5))

alphas = [int(x) for x in np.linspace(1, 10, num = 20)]
model = linear_model.Ridge()
grid_ridge = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas))
grid_ridge.fit(x_train, y_train)
print("Ridge regression best alpha value: ", grid_ridge.best_estimator_.alpha)
print("Ridge regression with hyperparameter tuning best score: ", 
      np.round(grid_ridge.best_score_, 5))
print("Ridge regression improvement after hyperparameter tuning: {0}%".format(
    np.round((1 - ((np.round(np.mean(cross_val_score(model, 
                                                     x_train,
                                                     y_train, 
                                                     cv = 5, 
                                                     scoring = "r2")), 5))
    / np.round(grid_ridge.best_score_, 5))) * 100, 5)))

# Elastic net regression

model = linear_model.ElasticNet()
print("Elastic Net regression score: ", np.round(np.mean(cross_val_score(
    model, 
    x_train, 
    y_train, 
    cv = 7, 
    scoring = "r2")), 5))

alphas = np.array([0.01, 0.02, 0.025, 0.05,0.1,0.5,1])
model = linear_model.ElasticNet()
grid_elastic = GridSearchCV(estimator=model, param_grid=dict(alpha=alphas))
grid_elastic.fit(x_train, y_train)

print("Elastic Net regression best alpha value: ", grid_elastic.best_estimator_.alpha)
print("Elastic Net regression with hyperparameter tuning best score: ", 
      np.round(grid_elastic.best_score_, 5))
print("Elastic Net regression improvement after hyperparameter tuning: {0}%".format(
    np.round((
        1 - ((np.round(np.mean(cross_val_score(model, 
                                               x_train, 
                                               y_train, 
                                               cv = 7, 
                                               scoring = "r2")), 5))
        / np.round(grid_elastic.best_score_, 5))) * 100, 5)))

from sklearn.ensemble import RandomForestRegressor

# Random forest regression

rf_Model = RandomForestRegressor()
print("Random Forest regression score: ", 
      np.round(np.mean(cross_val_score(rf_Model, 
                                       x_train, 
                                       y_train.values.ravel(), 
                                       cv = 7, 
                                       scoring = "r2")), 5))

param_grid = {'n_estimators': [int(x) for x in np.linspace(25, 75, num = 3)],
               'max_features': ['auto', 'sqrt'],
               'max_depth': [2, 4, 8],
               'min_samples_split': [2, 5,10],
               'min_samples_leaf': [1, 2, 4],
               'bootstrap': [True, False]}
print(param_grid)

from sklearn.ensemble import RandomForestRegressor

rf_Model = RandomForestRegressor()
rf_Grid = GridSearchCV(estimator = rf_Model, 
                       param_grid = param_grid, 
                       cv = 7, 
                       verbose=2, 
                       n_jobs = 4)
rf_Grid.fit(x_train, y_train.values.ravel())
print(rf_Grid.best_params_)
print("Random Forest regression with hyperparameter tuning best score: ", 
      np.round(rf_Grid.best_score_, 5))
print("Random Forest regression improvement after hyperparameter tuning: {0}%".format(
    np.round((1 - ((np.round(np.mean(cross_val_score(rf_Model, 
                                                     x_train, 
                                                     y_train.values.ravel(), 
                                                     cv = 7, 
                                                     scoring = "r2")), 5))
    / np.round(rf_Grid.best_score_, 5))) * 100, 5)))

from sklearn.ensemble import GradientBoostingRegressor

# Gradient Booster regression

gbr = GradientBoostingRegressor()
print("Gradient Booster regression score: ", 
      np.round(np.mean(cross_val_score(gbr, 
                                       x_train, 
                                       y_train.values.ravel(), 
                                       cv = 7, 
                                       scoring = "r2")), 5))

param_grid = {'n_estimators': [400, 500, 600],
               'learning_rate': [0.005, 0.01, 0.02],
               'max_depth': [1, 2, 4, 8],
               'subsample': [0.6, 0.8, 1]}
print(param_grid)

model = GradientBoostingRegressor()
grid_gbr = GridSearchCV(estimator = model, 
                        param_grid = param_grid, 
                        cv = 7, 
                        verbose=2, 
                        n_jobs = 4)
grid_gbr.fit(x_train, y_train.values.ravel())
print(grid_gbr.best_params_)
print("Gradient Booster regression with hyperparameter tuning best score: ", 
      np.round(grid_gbr.best_score_, 5))
print("Gradient Booster regression improvement after hyperparameter tuning: {0}%".format(
    np.round((1 - ((np.round(np.mean(cross_val_score(gbr,
                                                     x_train,
                                                     y_train.values.ravel(),
                                                     cv = 7,
                                                     scoring = "r2")), 5))
    /np.round(grid_gbr.best_score_, 5))) * 100, 5)))

import xgboost

# XGBoost regression

xgb = xgboost.XGBRegressor(objective ='reg:squarederror', 
                           colsample_bytree = 0.3, 
                           learning_rate = 0.1, 
                           max_depth = 5, 
                           alpha = 10, 
                           n_estimators = 10)
np.mean(cross_val_score(xgb, 
                        x_train, 
                        y_train, 
                        cv = 7, 
                        scoring = "r2"))

param_grid = {'n_estimators': [int(x) for x in np.linspace(250, 500, num = 5)],
               'learning_rate': [0.01, 0.02, 0.03],
               'max_depth': [2, 4, 8],
               'colsample_bytree': [0.5,0.75, 1],
               'subsample': [0.6,0.8, 1]}
print(param_grid)

model = xgboost.XGBRegressor(objective ='reg:squarederror')
grid_xgb = GridSearchCV(estimator = model, 
                        param_grid = param_grid, 
                        cv = 7, 
                        verbose=2, 
                        n_jobs = 4)
grid_xgb.fit(x_train, y_train)
print(grid_xgb.best_params_)
print("XGBoost regression with hyperparameter tuning best score: ",
      np.round(grid_xgb.best_score_, 5))
print("XGBoost Forest regression improvement after hyperparameter tuning: {0}%".format(
    np.round((1 - ((np.round(np.mean(cross_val_score(xgb,
                                                     x_train,
                                                     y_train,
                                                     cv = 7,
                                                     scoring = "r2")), 5))
    /np.round(grid_xgb.best_score_, 5))) * 100, 5)))

from sklearn.preprocessing import PolynomialFeatures

# Polynomial regression

def create_polynomial_regression_model(degree):
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(x_train)
    poly = LinearRegression()
    return np.mean(cross_val_score(poly, 
                                   X_poly, 
                                   y_train, 
                                   cv=7, 
                                   scoring = "r2"))
cv_scores=[]
degrees =[2,3,4,5]
for degree in degrees:
    cv_scores.append(create_polynomial_regression_model(degree))
    
print(max(cv_scores))

fig,ax=plt.subplots(figsize=(6,6))
ax.plot(degrees,cv_scores)
ax.set_xlabel('Degree',fontsize=20)
ax.set_ylabel('R2',fontsize=20)
ax.set_title('R2 VS Degree',fontsize=25)

poly_features = PolynomialFeatures(degree=2)
X_poly = poly_features.fit_transform(x_train)
poly = LinearRegression()
poly.fit(x_train, y_train)

ols_yhat = ols.predict(x_test)
lasso_yhat  = grid_lasso.best_estimator_.predict(x_test)
ridge_yhat = grid_ridge.best_estimator_.predict(x_test)
elastic_yhat = grid_elastic.best_estimator_.predict(x_test)
forest_yhat = rf_Grid.best_estimator_.predict(x_test)
gbr_yhat = grid_gbr.predict(x_test)
xgb_yhat = grid_xgb.predict(x_test)
poly_yhat = poly.predict(x_test)

from sklearn.metrics import r2_score

print("Ordinary Least Square accuracy: %.2f" % r2_score(y_test, ols_yhat))
print("Lasso regression accuracy: %.2f" % r2_score(y_test, lasso_yhat))
print("Ridge regression accuracy: %.2f" % r2_score(y_test, ridge_yhat))
print("Elastic net regression accuracy: %.2f" % r2_score(y_test, elastic_yhat))
print("Random forest regression accuracy: %.2f" % r2_score(y_test, forest_yhat))
print("Gradient Booster regression accuracy: %.2f" % r2_score(y_test, gbr_yhat))
print("XGBoost regression accuracy: %.2f" % r2_score(y_test, xgb_yhat))
print("Polynomial regression accuracy: %.2f" % r2_score(y_test, poly_yhat))

from sklearn.metrics import mean_squared_error

print("Ordinary Least Square accuracy: %.2f" % mean_squared_error(y_test, ols_yhat)) 
print("Lasso regression accuracy: %.2f" % mean_squared_error(y_test, lasso_yhat))
print("Ridge regression accuracy: %.2f" % mean_squared_error(y_test, ridge_yhat))
print("Elastic net regression accuracy: %.2f" % mean_squared_error(y_test, elastic_yhat))
print("Random forest regression accuracy: %.2f" % mean_squared_error(y_test, forest_yhat))
print("Gradient Booster regression accuracy: %.2f" % mean_squared_error(y_test, gbr_yhat))
print("XGBoost regression accuracy: %.2f" % mean_squared_error(y_test, xgb_yhat))
print("Polynomial regression accuracy: %.2f" % mean_squared_error(y_test, poly_yhat))

gbr_ytest =  y_test.reset_index(drop=True)
gbr_ypred = pd.DataFrame(gbr_yhat)
dfs = [gbr_ytest, gbr_ypred ]
gbr_df = pd.concat(dfs, axis = 1)
gbr_df.rename(columns = {0:'predictions'}, inplace = True)
gbr_df

x_test_DF =pd.DataFrame(x_test)
x_test_DF

from sklearn.ensemble import StackingRegressor

estimators = [('xgb',xgboost.XGBRegressor(objective ='reg:squarederror',
                                          colsample_bytree = 1,
                                          learning_rate = 0.01,
                                          max_depth =8,
                                          n_estimators = 500,
                                          subsample = 0.6)),
              ('gbr', GradientBoostingRegressor(learning_rate = 0.02,
                                                max_depth = 8, 
                                                n_estimators = 500, 
                                                subsample = 0.6)
                                                )]
stack= StackingRegressor(estimators = estimators,
                         final_estimator = RandomForestRegressor(
                             bootstrap = 'False',
                             max_depth = 8,
                             max_features = 'auto',
                             min_samples_leaf = 2,
                             min_samples_split = 2,
                             n_estimators = 75
                             ))

stack.fit(x_train, y_train.values.ravel())
stack_yhat = stack.predict(x_test)  
print("Stack regression accuracy: %.2f" % r2_score(y_test, stack_yhat))

# best performing model is random forest regression with a r2 accuracy 
# of 0.73

# 'asistio','leads','leads_hubspot', 'school_is_coding', 'school_is_data',
# 'school_is_marketing', 'school_is_unknown', 'school_is_ux',
# 'platform_is_facebook_ads', 'platform_is_google_ads', 
# 'platform_is_linkedin_ads', 'platform_is_tiktok_ads'

# # escuela   ---------
# coding     0          
# data       1
# marketing  2
# unknown    3                 
# ux         4              
            
# # plataforma_ad   ---------
# # facebook_ads    0
# # google_ads      1

# # mes   ---------
# April      0 
# August     1 
# December   2 
# February   3 
# January    4  
# July       5
# June       6 
# March      7 
# May        8
# November   9         
# October    10         
# September  11  

x = [[4250,4000,125,
      0,1,11
     ]]

x = pd.DataFrame(x, columns=['leads','leads_hubspot','asistio',
                             'escuela_cat','plataforma_ad_cat',
                             'mes_cat'
                            ])

# -------------------------------------------------
# x = pd.DataFrame(x, columns=['importe_gastado','registro_eb','leads','leads_hubspot',
#                              'escuela_cat','plataforma_ad_cat'
#                              ])  
# XGBoost regression accuracy: 0.83
# -------------------------------------------------   

# x = pd.DataFrame(x, columns = ['asistio','leads','leads_hubspot', 
#                                'school_is_coding','school_is_data',
#                                'school_is_marketing','school_is_unknown', 
#                                'school_is_ux',
#                                'platform_is_facebook_ads', 
#                                'platform_is_google_ads',
#                                'platform_is_linkedin_ads', 
#                                'platform_is_tiktok_ads'
#                                ])

#x

y_pred = rf_Grid.predict(x)
y_pred

import pickle

data = {"model": grid_gbr}
with open('saved_steps.pkl', 'wb') as file:
    pickle.dump(data, file)

with open('saved_steps.pkl', 'rb') as file:
    data = pickle.load(file)

regressor_loaded = data["model"]

y_pred = regressor_loaded.predict(x)
y_pred

# NEURAL NETWORK

# let's try to improve the model performance using a neural network

df2 = df1[['leads','leads_hubspot','asistio',
           'escuela_cat','plataforma_ad_cat',
           'mes_cat','importe_gastado'
        ]]
df2.reset_index()
dataset= df2.values

x = dataset[:,0:5]
y = dataset[:,6]
print(y.shape, x.shape)

from sklearn import preprocessing

min_max_scaler = preprocessing.MinMaxScaler()
x_scale = min_max_scaler.fit_transform(x)

x_scale

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_scale,y,
                                                    test_size=0.2)

# x_val, x_test, y_val, y_test = train_test_split(x_val_and_test, 
#                                                 y_val_and_test, 
#                                                 test_size=0.5)

# print(x_train.shape, x_val.shape, x_test.shape, y_train.shape, 
#       y_val.shape, y_test.shape)

print(x_train.shape, y_train.shape, x_test.shape, y_test.shape, )

import tensorflow.keras as keras 
from keras import regularizers

model = keras.models.Sequential([
    keras.layers.Input((5,)),
    keras.layers.Dense(32, activation="relu", 
                       kernel_regularizer=regularizers.l2(0.01)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(64, activation="relu",
                       kernel_regularizer=regularizers.l2(0.01)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(16, activation="relu",
                       kernel_regularizer=regularizers.l2(0.01)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer= keras.optimizers.Adam(lr=0.05), 
    loss="binary_crossentropy", 
    metrics=["accuracy"])

history = model.fit(x_train, y_train, 
                    validation_data=(x_test, y_test), 
                    batch_size=128, 
                    epochs=100)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper right')
plt.ylim(top=1.2, bottom=0)
plt.show()