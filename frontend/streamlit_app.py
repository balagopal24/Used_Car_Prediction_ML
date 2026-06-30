# # """
# # frontend/streamlit_app.py
# # Live dashboard: auto-refreshes to show new listings as the simulator
# # inserts them, plus a manual prediction form.

# # Run with: streamlit run frontend/streamlit_app.py
# # """
# # import os
# # import sys
# # import time
# # import requests
# # import pandas as pd
# # import streamlit as st

# # API_URL = os.getenv("API_URL", "http://localhost:8000")

# # st.set_page_config(page_title="Used Car Price Predictor", layout="wide")
# # st.title("🚗 Used Car Price Prediction — Live Dashboard")

# # st_autorefresh_interval = 5000  # ms

# # tab1, tab2, tab3 = st.tabs(["Live Feed", "Predict a Price", "Ask the Agent"])

# # with tab1:
# #     st.subheader("Recent listings (simulated live feed)")
# #     placeholder = st.empty()

# #     try:
# #         resp = requests.get(f"{API_URL}/listings/recent", params={"limit": 20})
# #         listings = resp.json()
# #         df = pd.DataFrame(listings)
# #         if not df.empty:
# #             df["error_pct"] = (
# #                 (df["price_actual"] - df["price_predicted"]).abs()
# #                 / df["price_actual"] * 100
# #             ).round(1)
# #             placeholder.dataframe(df, use_container_width=True)
# #         else:
# #             st.info("No listings yet — start the simulator: `python src/simulator.py`")
# #     except requests.exceptions.ConnectionError:
# #         st.error("API not reachable. Start it with: `uvicorn app.main:app --reload`")

# #     if st.button("Refresh now"):
# #         st.rerun()

# # with tab2:
# #     st.subheader("Predict a price")
# #     col1, col2 = st.columns(2)
# #     with col1:
# #         brand = st.text_input("Brand", "Maruti")
# #         fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "CNG", "Electric"])
# #         transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
# #         owner = st.selectbox(
# #             "Owner", ["First Owner", "Second Owner", "Third Owner"]
# #         )
# #     with col2:
# #         year = st.number_input("Year", min_value=1990, max_value=2026, value=2018)
# #         km_driven = st.number_input("KM Driven", min_value=0, value=40000)
# #         engine_cc = st.number_input("Engine CC", min_value=0, value=1200)
# #         mileage_kmpl = st.number_input("Mileage (kmpl)", min_value=0.0, value=18.0)

# #     if st.button("Predict Price"):
# #         payload = {
# #             "brand": brand, "fuel": fuel, "transmission": transmission,
# #             "owner": owner, "year": int(year), "km_driven": int(km_driven),
# #             "engine_cc": float(engine_cc), "mileage_kmpl": float(mileage_kmpl),
# #         }
# #         try:
# #             r = requests.post(f"{API_URL}/predict", json=payload)
# #             r.raise_for_status()
# #             st.success(f"Predicted price: ₹{r.json()['predicted_price']:,.0f}")
# #         except Exception as e:
# #             st.error(f"Prediction failed: {e}")

# # with tab3:
# #     st.subheader("Ask a question about the listings data")
# #     question = st.text_input(
# #         "e.g. What's the average price of diesel SUVs over 5 years old?"
# #     )
# #     if st.button("Ask"):
# #         try:
# #             r = requests.post(f"{API_URL}/ask", params={"question": question})
# #             r.raise_for_status()
# #             st.write(r.json()["answer"])
# #         except Exception as e:
# #             st.error(f"Agent query failed: {e}")


# """
# frontend/streamlit_app.py
# Live dashboard: auto-refreshes to show new listings as the simulator
# inserts them, plus a manual prediction form.

# Run with: streamlit run frontend/streamlit_app.py
# """
# import os
# import sys
# import time
# import requests
# import pandas as pd
# import streamlit as st

# API_URL = os.getenv("API_URL", "http://localhost:8000")

# st.set_page_config(page_title="Used Car Price Predictor", layout="wide")
# st.title("🚗 Used Car Price Prediction — Live Dashboard")

# st_autorefresh_interval = 5000  # ms

# tab1, tab2, tab3 = st.tabs(["Live Feed", "Predict a Price", "Ask the Agent"])

# with tab1:
#     st.subheader("Recent listings (simulated live feed)")
#     placeholder = st.empty()

#     try:
#         resp = requests.get(f"{API_URL}/listings/recent", params={"limit": 20})
#         listings = resp.json()
#         df = pd.DataFrame(listings)
#         if not df.empty:
#             df["error_pct"] = (
#                 (df["price_actual"] - df["price_predicted"]).abs()
#                 / df["price_actual"] * 100
#             ).round(1)
#             placeholder.dataframe(df, use_container_width=True)
#         else:
#             st.info("No listings yet — start the simulator: `python src/simulator.py`")
#     except requests.exceptions.ConnectionError:
#         st.error("API not reachable. Start it with: `uvicorn app.main:app --reload`")

#     if st.button("Refresh now"):
#         st.rerun()

# with tab2:
#     st.subheader("Predict a price")
#     col1, col2 = st.columns(2)
#     with col1:
#         brand = st.text_input("Brand", "Maruti")
#         fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "CNG", "Electric"])
#         transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
#         seller_type = st.selectbox(
#             "Seller Type", ["Individual", "Dealer", "Trustmark Dealer"]
#         )
#     with col2:
#         year = st.number_input("Year", min_value=1990, max_value=2026, value=2018)
#         km_driven = st.number_input("KM Driven", min_value=0, value=40000)
#         engine_cc = st.number_input("Engine CC", min_value=0, value=1200)
#         mileage_kmpl = st.number_input("Mileage (kmpl)", min_value=0.0, value=18.0)

#     if st.button("Predict Price"):
#         payload = {
#             "brand": brand, "fuel": fuel, "transmission": transmission,
#             "seller_type": seller_type, "year": int(year), "km_driven": int(km_driven),
#             "engine_cc": float(engine_cc), "mileage_kmpl": float(mileage_kmpl),
#         }
#         try:
#             r = requests.post(f"{API_URL}/predict", json=payload)
#             r.raise_for_status()
#             st.success(f"Predicted price: ₹{r.json()['predicted_price']:,.0f}")
#         except Exception as e:
#             st.error(f"Prediction failed: {e}")

# with tab3:
#     st.subheader("Ask a question about the listings data")
#     question = st.text_input(
#         "e.g. What's the average price of diesel SUVs over 5 years old?"
#     )
#     if st.button("Ask"):
#         try:
#             r = requests.post(f"{API_URL}/ask", params={"question": question})
#             r.raise_for_status()
#             st.write(r.json()["answer"])
#         except Exception as e:
#             st.error(f"Agent query failed: {e}")

"""
frontend/streamlit_app.py
Live dashboard: auto-refreshes to show new listings as the simulator
inserts them, plus a manual prediction form.

Run with: streamlit run frontend/streamlit_app.py
"""
import os
import sys
import time
import requests
import pandas as pd
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Used Car Price Predictor", layout="wide")
st.title("🚗 Used Car Price Prediction — Live Dashboard")

st_autorefresh_interval = 5000  # ms

tab1, tab2, tab3 = st.tabs(["Live Feed", "Predict a Price", "Ask the Agent"])

with tab1:
    st.subheader("Recent listings (simulated live feed)")
    placeholder = st.empty()

    try:
        resp = requests.get(f"{API_URL}/listings/recent", params={"limit": 20})
        listings = resp.json()
        df = pd.DataFrame(listings)
        if not df.empty:
            df["error_pct"] = (
                (df["price_actual"] - df["price_predicted"]).abs()
                / df["price_actual"] * 100
            ).round(1)
            placeholder.dataframe(df, use_container_width=True)
        else:
            st.info("No listings yet — start the simulator: `python src/simulator.py`")
    except requests.exceptions.ConnectionError:
        st.error("API not reachable. Start it with: `uvicorn app.main:app --reload`")

    if st.button("Refresh now"):
        st.rerun()

with tab2:
    st.subheader("Predict a price")
    col1, col2 = st.columns(2)
    with col1:
        brand = st.text_input("Brand", "Maruti")
        fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "CNG", "Electric"])
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
        seller_type = st.selectbox(
            "Seller Type", ["Individual", "Dealer", "Trustmark Dealer"]
        )
    with col2:
        year = st.number_input("Year", min_value=1990, max_value=2026, value=2018)
        km_driven = st.number_input("KM Driven", min_value=0, value=40000)
        engine_cc = st.number_input("Engine CC", min_value=0, value=1200)
        mileage_kmpl = st.number_input("Mileage (kmpl)", min_value=0.0, value=18.0)

    if st.button("Predict Price"):
        payload = {
            "brand": brand, "fuel": fuel, "transmission": transmission,
            "seller_type": seller_type, "year": int(year), "km_driven": int(km_driven),
            "engine_cc": float(engine_cc), "mileage_kmpl": float(mileage_kmpl),
        }
        try:
            r = requests.post(f"{API_URL}/predict", json=payload)
            r.raise_for_status()
            st.success(f"Predicted price: ₹{r.json()['predicted_price']:,.0f}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

with tab3:
    st.subheader("Ask a question about the listings data")
    question = st.text_input(
        "e.g. What's the average price of diesel SUVs over 5 years old?"
    )
    if st.button("Ask"):
        try:
            r = requests.post(f"{API_URL}/ask", params={"question": question})
            r.raise_for_status()
            st.write(r.json()["answer"])
        except Exception as e:
            st.error(f"Agent query failed: {e}")