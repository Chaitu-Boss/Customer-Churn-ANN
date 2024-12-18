import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder   
import pandas as pd
import pickle

model=tf.keras.models.load_model(r'Sequetialmodel.h5')

with open('label_encoder_gender.pkl', 'rb') as file:
    label_encoder_gender = pickle.load(file)

with open('onehot_encoder_geo.pkl', 'rb') as file:
    onehot_encoder_geo = pickle.load(file)

with open('standardscaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

st.title('Customer Churn Prediction')

name=st.text_input('Customer Name')
geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
tenure = st.number_input('Tenure')
num_of_products = st.number_input('Number of Products')
has_cr_card = st.selectbox('Has Credit Card',[0,1])
is_active_member = st.selectbox('Is Active Member',[0,1])
estimated_salary = st.number_input('Estimated Salary')

input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

geo_encoded = onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=onehot_encoder_geo.get_feature_names_out(['Geography']))

input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

input_data_scaled = scaler.transform(input_data)

prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]

st.write(f'Churn Probability of {name} is {prediction_proba:.2f}')
