import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def title_cleaner(title):
    if 'data scientist' in title.lower() or 'scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'machine learning' in title.lower():
        return 'machine learning engineer'
    elif 'data analyst' in title.lower():
        return 'data analyst'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'other'

def title_seniority(title):
    if 'senior' in title.lower() or 'sr.' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'sr'
   
    else:
        return 'jr'
    
def hourly_to_yearly(minlimit, maxlimit):
  x = minlimit.strip()
  y = maxlimit.strip()
  x = int(int(minlimit)*45*52/1000)
  y = int(int(maxlimit)*45*52/1000)
  return '{}-{}'.format(x,y)

def size_simplifier(text):
  if '-1' in text.lower():
    return 'Unknown'
  else:
    return text

def ownership_simplifier(text):
    if 'private' in text.lower():
      return 'Private'
    elif 'public' in text.lower():
      return 'Public'
    elif ('-1' in text.lower()) or ('unknown' in text.lower()) or ('school / school district' in text.lower()) or ('private practice / firm' in text.lower()) or ('contract' in text.lower()) :
      return 'Other Organization'
    else:
      return text


def revenue_simplifier(text):
  if '-1' in text.lower():
    return 'Unknown / Non-Applicable'
  else:
    return text

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

@st.cache_data
def load_data():
    df = pd.read_csv("salary.csv")
    df.drop(labels=['Unnamed: 0'],axis='columns',inplace=True)
    df['Rating'] = df['Rating'].apply(lambda x: np.NaN if x==-1 else x)
    df['Rating'] = df['Rating'].fillna(df['Rating'].mean())
    df['Founded'] = df['Founded'].apply(lambda x: np.NaN if x==-1 else x)
    df['Founded'] = df['Founded'].fillna(int(df['Founded'].median()))
    df['Founded'] = df['Founded'].astype('int')
    df['job_title']= df['Job Title'].apply(title_cleaner)
    df['job_seniority'] = df['Job Title'].apply(title_seniority)
    df.drop(labels = ['Job Title'], axis=1 ,inplace =True)
    salary = df['Salary Estimate'].apply(lambda x: x.split("(")[0])
    salary = salary.apply(lambda x: np.NaN if x=='-1' else x)
    salary = salary.apply(lambda x: x if type(x)== type(3.5) else x.replace('$','').replace('K',''))
    salary = salary.apply(lambda x: x if type(x)==type(3.5) else x.lower().replace("employer provided salary:", ""))
    salary = salary.apply(lambda x: x if type(x)==type(3.5) else (hourly_to_yearly(x.lower().replace("per hour", "").split('-')[0], x.lower().replace("per hour", "").split('-')[1]) if "per hour" in x.lower() else x))
    df['Salary'] = salary.apply(lambda x:  x if type(x)==type(3.5) else (int(x.split("-")[0]) + int(x.split("-")[1].strip()))/2)
    df['Salary'] = df['Salary'].fillna(df['Salary'].median())
    df["Company Name"] = df['Company Name'].apply(lambda x: x.split("\n")[0])
    df['job_location'] = df['Location'].apply(lambda x: x if ',' not in x else x.split(',')[1].strip())
    df['Size'] = df['Size'].apply(size_simplifier)
    df['Type of ownership'] = df['Type of ownership'].apply(ownership_simplifier)
    df['Industry'] = df['Industry'].apply(lambda x: 'Others' if x=='-1' else x)
    df['Sector'] = df['Sector'].apply(lambda x: 'Others' if x=='-1' else x)
    df['Revenue'] = df['Revenue'].apply(revenue_simplifier)
    df['Competitors'] = df['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)
    df.drop(["Unnamed: 0.1","Salary Estimate","Job Description","Company Name","Rating","Headquarters","Founded"
         ,"Industry","Revenue","Competitors","job_location"],axis = 1, inplace = True)
    country_map = shorten_categories(df.Location.value_counts(), 20)
    df['Location'] = df['Location'].map(country_map)
    df = df[df['Location'] != 'Other']
    return df








df = load_data()

def show_explore_page():
    st.title("Explore Data Scientist Salaries")

    

        
    data = df["Location"].value_counts()

    fig1, ax1 = plt.subplots()
    
    g = sns.countplot(x='Sector', data=df, order = df['Sector'].value_counts()[:20].index)
    p = plt.title('Count plot for Sector (Top 20)')
    g.set_xlabel('')
    p = plt.ylabel('Count')
    p = g.set_xticklabels(g.get_xticklabels(), rotation=45, horizontalalignment='right')

    st.pyplot(fig1)
  
    fig2, ax2 = plt.subplots()
    g = sns.countplot(x='Type of ownership', data=df, order = df['Type of ownership'].value_counts().index)
    p = plt.title('Count plot for Type of ownership')
    g.set_xlabel('')
    p = plt.ylabel('Count')
    p = g.set_xticklabels(g.get_xticklabels(), rotation=45, horizontalalignment='right')

    st.pyplot(fig2)

    data = df["Location"].value_counts()
    fig3, ax3 = plt.subplots()
    ax3.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax3.axis("equal")

    st.pyplot(fig3)