import streamlit as st
import pickle
import numpy as np
from PIL import Image

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()


regressor = data["model"]
le_location = data["le_location"]
le_size = data["le_size"]
le_ownership = data["le_ownership"]
le_sector = data["le_sector"]
le_title = data["le_title"]
le_seniority = data["le_seniority"]

image = Image.open('salary.jpg')

def show_predict_page():
    st.title("Data Scientist Salary Prediction")

    # st.write("""### We need some information to predict the salary""")

    Location = (
       "New York, NY",
        "San Francisco, CA",
        "Cambridge, MA ",
        "Chicago, IL" ,
        "Boston, MA" 
    )

    size = (
        '51 to 200 employees', '10000+ employees', '501 to 1000 employees',
       '201 to 500 employees', '1001 to 5000 employees',
       '5001 to 10000 employees', '1 to 50 employees', 'Unknown'
    )


    type_of_ownership = (
        'Private', 'Public', 'Other Organization',
       'Subsidiary or Business Segment', 'Nonprofit Organization',
       'Government'
    )

    sector = (
        'Business Services', 'Information Technology',
       'Biotech & Pharmaceuticals', 'Transportation & Logistics',
       'Real Estate', 'Insurance', 'Health Care', 'Others', 'Media',
       'Travel & Tourism', 'Retail', 'Government', 'Finance',
       'Construction, Repair & Maintenance', 'Manufacturing', 'Education',
       'Consumer Services'
    )

    job_title = (
        'data scientist', 'data analyst', 'data engineer',
       'machine learning engineer', 'manager', 'other', 'director'
    )

    job_seniority = (
        'jr', 'sr'
    )

    col1, col2 = st.columns(2)

    with col1:

        Location = st.selectbox("Location", Location)
        size = st.selectbox("Size", size)
        type_of_ownership = st.selectbox("Ownership Type", type_of_ownership)
        sector = st.selectbox("Sector", sector)
        job_title = st.selectbox("Designation", job_title)
        job_seniority = st.selectbox("Job Seniority", job_seniority)

    with col2:
        st.image(image, clamp=True, channels='RGB', output_format='auto')

    ok = st.button("Calculate Salary",help = "Click here to see the estimated salary")
    if ok:
        X = np.array([[Location, size, type_of_ownership ,sector,job_title,job_seniority]])
        X[:, 0] = le_location.transform(X[:,0])
        X[:, 1] = le_size.transform(X[:,1])
        X[:, 2] = le_ownership.transform(X[:,2])
        X[:, 3] = le_sector.transform(X[:,3])
        X[:, 4] = le_title.transform(X[:,4])
        X[:, 5] = le_seniority.transform(X[:,5])
        X = X.astype(float)

        salary = regressor.predict(X)
        # st.balloons()
        st.subheader(f"The estimated salary is ${salary[0]:.2f}K")
