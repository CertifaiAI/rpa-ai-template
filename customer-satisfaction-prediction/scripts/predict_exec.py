# importing libraries
import sys
# sys.version = '3.7.3 | packaged by conda-forge | (default, Jul  1 2019, 21:52:21)\n[GCC 7.3.0]'

import joblib
import datetime as dt
from workalendar.america import Brazil
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import keras
import tensorflow as tf

#data_path = r'C:\Users\zulhu\Desktop\Customer Satisfaction Prediction\SampleOrder-10.csv'
data_path = r'C:\Users\zulhu\Desktop\Customer Satisfaction Prediction\translated.csv'
model_path = r'C:\Users\zulhu\Desktop\Customer Satisfaction Prediction\my_model2.h5'
workspace_path = r'C:\Users\zulhu\Desktop\Customer Satisfaction Prediction'

# needed when dealing with multi threading
sess = tf.Session()
keras.backend.set_session(sess)

orders = pd.read_csv(data_path)
print('Loading data path ' + data_path)

# converting dates to datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders.order_purchase_timestamp)
orders['order_aproved_at'] = pd.to_datetime(orders.order_aproved_at).dt.date  
orders['order_estimated_delivery_date'] = pd.to_datetime(orders.order_estimated_delivery_date).dt.date  
orders['order_delivered_customer_date'] = pd.to_datetime(orders.order_delivered_customer_date).dt.date

# modifying the data to provide more information
cal = Brazil()
from sklearn.base import BaseEstimator, TransformerMixin

class AttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass    
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        df = X.copy()
        
        # Calculate the estimated delivery time and actual delivery time in working days. 
        # This would allow us to exclude hollidays that could influence delivery times.
        # If the order_delivered_customer_date is null, it returns 0.
        df['wd_estimated_delivery_time'] = df.apply(lambda x: cal.get_working_days_delta(x.order_aproved_at, 
                                                                                      x.order_estimated_delivery_date), axis=1)
        df['wd_actual_delivery_time'] = df.apply(lambda x: cal.get_working_days_delta(x.order_aproved_at, 
                                                                                   x.order_delivered_customer_date), axis=1)

        # Calculate the time between the actual and estimated delivery date. If negative was delivered early, if positive was delivered late.
        df['wd_delivery_time_delta'] = df.wd_actual_delivery_time - df.wd_estimated_delivery_time


        # Calculate the time between the actual and estimated delivery date. If negative was delivered early, if positive was delivered late.
        df['is_late'] = df.order_delivered_customer_date > df.order_estimated_delivery_date
        
        # Calculate the average product value.
        df['average_product_value'] = df.order_products_value / df.order_items_qty

        # Calculate the total order value
        df['total_order_value'] = df.order_products_value + df.order_freight_value
        
        # Calculate the order freight ratio.
        df['order_freight_ratio'] = df.order_freight_value / df.order_products_value
        
        # Calculate the order freight ratio.
        df['purchase_dayofweek'] = df.order_purchase_timestamp.dt.dayofweek
                       
        # With that we can remove the timestamps from the dataset
        cols2drop = ['order_purchase_timestamp', 'order_aproved_at', 'order_estimated_delivery_date', 
                     'order_delivered_customer_date']
        df.drop(cols2drop, axis=1, inplace=True)
        
        return df

# executing the estimator we just created
attr_adder = AttributesAdder()
modded = attr_adder.transform(orders)

# encoding categorical data
le_status = LabelEncoder()
le_state = LabelEncoder()
le_category = LabelEncoder()
le_late = LabelEncoder()

le_status.classes_ = np.load(workspace_path + r'\Encoder\le_status.npy', allow_pickle=True)
le_state.classes_ = np.load(workspace_path + r'\Encoder\le_state.npy', allow_pickle=True)
le_category.classes_ = np.load(workspace_path + r'\Encoder\le_category.npy', allow_pickle=True)
le_late.classes_ = np.load(workspace_path + r'\Encoder\le_late.npy', allow_pickle=True)

modded['status_encoded'] = le_status.transform(modded.order_status)
modded['state_encoded'] = le_state.transform(modded.customer_state)
modded['category_encoded'] = le_category.transform(modded.product_category_name_english)
modded['late_encoded'] = le_late.transform(modded.is_late)

status_ohe = joblib.load(workspace_path + r'\Encoder\status_ohe.joblib')
state_ohe = joblib.load(workspace_path + r'\Encoder\state_ohe.joblib')
category_ohe = joblib.load(workspace_path + r'\Encoder\category_ohe.joblib')
late_ohe = joblib.load(workspace_path + r'\Encoder\late_ohe.joblib')

x_status = status_ohe.transform(modded.status_encoded.values.reshape(-1,1)).toarray()
x_state = state_ohe.transform(modded.state_encoded.values.reshape(-1,1)).toarray()
x_category = category_ohe.transform(modded.category_encoded.values.reshape(-1,1)).toarray()
x_late = late_ohe.transform(modded.late_encoded.values.reshape(-1,1)).toarray()

# concatenating the new columns
dfOneHot = pd.DataFrame(x_status, columns = ["status"+str(int(i)) for i in range(x_status.shape[1])])
modded = pd.concat([modded, dfOneHot], axis=1)

dfOneHot = pd.DataFrame(x_state, columns = ["state"+str(int(i)) for i in range(x_state.shape[1])])
modded = pd.concat([modded, dfOneHot], axis=1)

dfOneHot = pd.DataFrame(x_category, columns = ["category"+str(int(i)) for i in range(x_category.shape[1])])
modded = pd.concat([modded, dfOneHot], axis=1)

dfOneHot = pd.DataFrame(x_late, columns = ["late"+str(int(i)) for i in range(x_late.shape[1])])
modded = pd.concat([modded, dfOneHot], axis=1)

# removing categorical columns
cols2drop = ['order_status', 'customer_state', 'product_category_name_english', 
                     'is_late', 'status_encoded', 'state_encoded', 'category_encoded',
       'late_encoded']
modded.drop(cols2drop, axis=1, inplace=True)

# inferencing the data
print('Running inference')
prediction_model = keras.models.load_model(model_path)
presult = prediction_model.predict_classes(modded)
np.set_printoptions(threshold=sys.maxsize)
result = str(presult)