import streamlit as st
import pandas as pd

transactions = pd.read_csv("./data/dh_transactions.csv")
products = pd.read_csv("./data/dh_product_lookup.csv")

data = transactions.join(products.set_index('upc'),on = "upc")

def remove_product_and_brands(brand_cut_off,product_cut_off,main_data = data.copy()):

	total_sales_before = main_data["dollar_sales"].sum()
	baskets_before = main_data.groupby(['basket'])
	num_customers_before = len(baskets_before.size())

	brands = data["brand"].value_counts()
	products = data["product_description"].value_counts()

	cut_brands = brands[brands < brand_cut_off].index
	cut_products = products[products < product_cut_off].index

	new_data = main_data[~main_data["brand"].isin(cut_brands)]
	new_data = new_data[~new_data["product_description"].isin(cut_products)]

	total_sales_after = new_data["dollar_sales"].sum()
	baskets_after = new_data.groupby(['basket'])
	num_customers_after = len(baskets_after.size())

	st.write(f"Number of brands that are cut: {len(cut_brands)}/{len(brands)}")
	st.write(f"Number of products that are cut: {len(cut_products)}/{len(products)}")

	return ((total_sales_before-total_sales_after)/total_sales_before,
			(num_customers_before-num_customers_after)/num_customers_before)

st.title("Simple Simulation")
st.write("This simulation purpose is to calculate how much we will lose in sales/number of customers "+
		"if we remove brands/products that sell less than the cut off over the last 2 years")

with st.form("my_form"):
	st.write("Please input the cut off you want")
	brand_cut_off = st.number_input('cut off for brands')
	product_cut_off = st.number_input('cut off for products')
	submitted = st.form_submit_button('Submit')

if submitted:
	sales_loss, customers_loss = remove_product_and_brands(brand_cut_off,product_cut_off)

	st.write(f"If we remove both products that sell less than {product_cut_off} times and "+
			f"brands that sell less than {brand_cut_off} times, we will loss {round(sales_loss*100,3)}%"+
			 f" in sales and {round(customers_loss*100,3)}% in number of customers")


