# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 20:31:02 2020

@author: andre
"""

import numpy as np # linear algebra
import pandas as pd

train=pd.read_csv('~/Documents/kaggle_competitions/pulmonary_fibrosis_progression/train.csv')

train.head()

#train.groupby('Patient')['FVC'].plot()

import matplotlib.pyplot as plt
fig, (ax1) = plt.subplots(nrows = 1, ncols = 1)
for key, grp in train.groupby(['Patient']): 
    ax1.plot(grp['Weeks'], grp['FVC']) #, label = "Patient in {0:02d}".format(key))
#plt.legend(loc='best')    
plt.show()
    

keep_weeks_min=train.groupby('Patient')["Weeks"].min().reset_index()
keep_weeks_max=train.groupby('Patient')["Weeks"].max()

#new1=train.sort_values("Weeks").groupby("Patient", as_index=False).first()

find_first_measurement_per_patient=train.loc[train.groupby("Patient")["Weeks"].idxmin()]

find_last_measurement_per_patient=train.loc[train.groupby("Patient")["Weeks"].idxmax()]

#Rename the columns so that we merge them
find_first_measurement_per_patient.columns=['Patient', 'Weeks', 'FVC_first', 'Percent_first', 'Age', 'Sex', 'SmokingStatus']

find_last_measurement_per_patient.columns=['Patient', 'Weeks', 'FVC_last', 'Percent_last', 'Age', 'Sex', 'SmokingStatus']

merge_data_frames=pd.merge(find_first_measurement_per_patient, find_last_measurement_per_patient,
                           left_on='Patient', right_on='Patient', how='inner')

merge_data_frames['difference:last-first_FVC']=merge_data_frames['FVC_first']-merge_data_frames['FVC_last']
merge_data_frames['difference:last-first_Percent']=merge_data_frames['Percent_first']-merge_data_frames['Percent_last']

merge_data_frames.plot(kind='scatter',x='FVC_first',y='FVC_last',color='red')
plt.show()

#thedifference=new1
#thedifference=thedifference.drop
difference_sex_plot=merge_data_frames.groupby("Sex_x")['difference:last-first_FVC'].mean().plot(kind='bar', title="Mean difference between last and first FVC")

bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
merge_data_frames['age_group'] = pd.cut(merge_data_frames['Age_x'], bins)
merge_data_frames['age_group'].value_counts().plot(kind='bar')

merge_data_frames.groupby("age_group")['difference:last-first_FVC'].mean().plot(kind='bar',
                         title="Mean difference between last and first FVC by age group")
