import pickle
import pandas as pd

df = pd.read_csv("cleaned_ecommerce_data.csv")

with open("trained_model.pkl", "rb") as file:
    recommendation_model = pickle.load(file)

def recommend_products(customer_id, num_recommendations=5):
    if "Description" not in df.columns or "StockCode" not in df.columns:
        return {"error": "Required columns missing in dataset."}

    customer_data = df[df["CustomerID"] == customer_id]
    purchased_items = customer_data[["StockCode", "Description"]].drop_duplicates().to_dict(orient='records')

    if customer_data.empty:
        return {"error": "No purchase history found for this customer."}

    purchased_stockcodes = customer_data["StockCode"].unique()

    if customer_id in recommendation_model.index:
        customer_predictions = recommendation_model.loc[customer_id]
        recommended_stockcodes = (
            customer_predictions.sort_values(ascending=False)
            .index.tolist()
        )

        recommended_items = []
        for stock_code in recommended_stockcodes:
            if stock_code not in purchased_stockcodes:
                item = df[df["StockCode"] == stock_code]["Description"].unique()
                if len(item) > 0:
                    recommended_items.append({"StockCode": stock_code, "Description": item[0]})
                if len(recommended_items) >= num_recommendations:
                    break
    else:
        recommended_items = [{"StockCode": "N/A", "Description": "No recommendations found for this Customer ID."}]

    return {
        "Purchased Items": purchased_items,
        "Recommended Items": recommended_items
    }
