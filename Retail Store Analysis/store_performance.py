import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("./data/dh_transactions.csv")

stores = data["store"].unique()
stores.sort()

def report(store_id):

	store_data = data[data["store"] == store_id]
	store_baskets = store_data.groupby("basket")

	total_sales = store_data["dollar_sales"].sum()
	num_customers = len(store_data["basket"].unique())

	st.write(f"Total Sales: {total_sales}")
	st.write(f"Number of Customers: {num_customers}")

	sale_per_baskets = store_baskets['dollar_sales'].sum()
	weeks = (store_baskets['week'].sum()/store_baskets.size())

	sale_each_weeks = np.zeros(105)
	for idx,val in sale_per_baskets.items():
		sale_each_weeks[int(weeks[idx])] += val

	plt.figure(figsize = (10,15))

	plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.2)


	plt.subplot(2, 1, 1)
	plt.barh(np.arange(1,105,1),sale_each_weeks[1:])
	plt.title(f"Total Sales at Store {store_id} Each Week")
	plt.xlabel("Sales (Dollar)")
	plt.ylabel("week")



	basket_per_weeks = weeks.value_counts().sort_index()

	plt.subplot(2, 1, 2)
	plt.barh(np.arange(1,105,1),basket_per_weeks)
	plt.title(f"Number of Customers at Store {store_id} Each Week")
	plt.xlabel("Number of Customers (household)")
	plt.ylabel("week")

	st.pyplot(plt.gcf())



st.title("Store Report")
st.write("This is a report to show how each store performs over the last 2 years")

with st.form("my_form"):
	st.write("Please choose an id of store you want a report")
	store_id = st.selectbox('Store ID', stores)
	submitted = st.form_submit_button('Submit')

if submitted:
	report(store_id)
