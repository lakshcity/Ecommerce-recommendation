import streamlit as st
import pandas as pd
from recommend import recommend_products

df = pd.read_csv("cleaned_ecommerce_data.csv")
st.title("🛍️ E-Commerce Recommendation System")

customer_id = st.number_input(
    "Enter Customer ID:", 
    min_value=int(df['CustomerID'].min()), 
    max_value=int(df['CustomerID'].max()), 
    step=1
)

if st.button("Get Recommendations"):
    result = recommend_products(int(customer_id))  

    if "error" in result:
        st.error(result["error"])
    else:
        purchased_items = result.get("Purchased Items", [])
        recommended_items = result.get("Recommended Items", [])

        st.write("### ✅ Purchased Items:")
        if purchased_items:
            for item in purchased_items:
                st.write(f"- {item['Description']} (StockCode: {item['StockCode']})")
        else:
            st.write("No purchased items found.")

        st.write("### 🔥 Recommended Items:")
        if recommended_items and recommended_items[0]["StockCode"] != "N/A":
            for item in recommended_items:
                st.write(f"- {item['Description']} (StockCode: {item['StockCode']})")
        else:
            st.write("No recommendations available.")
