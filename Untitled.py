#!/usr/bin/env python
# coding: utf-8

# In[1]:


import seaborn as sns
import pandas as pd

df = pd.DataFrame({"country":["IE", "UK"], "population": [5.5, 50]})
suicide_data = pd.read_csv(r"C:\\Users\\ciward\\MyFolder\\MyFolder\\suiciderateall.csv") 

Covid_date = pd.read_csv(r"C:\\Users\\ciward\\MyFolder\\MyFolder\\worldometer_data.csv")

sns.barplot(x="population", y="country", data=df)

print('hello')

print('hello world')


