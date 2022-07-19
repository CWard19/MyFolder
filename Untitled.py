#!/usr/bin/env python
# coding: utf-8

# In[1]:


import seaborn as sns
import pandas as pd

df = pd.DataFrame({"country":["IE", "UK"], "population": [5.5, 50]})

sns.barplot(x="population", y="country", data=df)

print('hello')

print('hello world')
