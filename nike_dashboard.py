
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("nike_sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filter Options")
regions = st.sidebar.multiselect("Select Region(s):", df["Region"].unique(), default=df["Region"].unique())
products = st.sidebar.multiselect("Select Product Line(s):", df["ProductLine"].unique(), default=df["ProductLine"].unique())

filtered_df = df[(df["Region"].isin(regions)) & (df["ProductLine"].isin(products))]

# Dashboard title
st.title("Nike Business Performance Dashboard")
st.markdown("Explore sales trends, customer satisfaction, and regional performance.")

# KPI Cards
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Average Rating", f"{filtered_df['CustomerRating'].mean():.2f} / 5")

# Chart 1: Sales by Product Line
st.subheader("Sales by Product Line")
fig1 = px.bar(filtered_df.groupby("ProductLine")["Sales"].sum().reset_index(),
              x="ProductLine", y="Sales", text_auto=True)
st.plotly_chart(fig1)

# Chart 2: Monthly Sales Trend
st.subheader("Monthly Sales Trend")
fig2 = px.line(filtered_df.groupby(["Date", "Region"])["Sales"].sum().reset_index(),
               x="Date", y="Sales", color="Region")
st.plotly_chart(fig2)

# Chart 3: Rating Distribution
st.subheader("Customer Rating Distribution")
fig3 = px.histogram(filtered_df, x="CustomerRating", nbins=10)
st.plotly_chart(fig3)

# Optional: Geo plot if 'Latitude' and 'Longitude' present
if "Latitude" in df.columns and "Longitude" in df.columns:
    st.subheader("Regional Sales Distribution (Map)")
    geo_df = filtered_df.groupby(["Region", "Latitude", "Longitude"])["Sales"].mean().reset_index()
    fig_map = px.scatter_geo(geo_df,
                             lat="Latitude", lon="Longitude",
                             size="Sales", text="Region",
                             projection="natural earth")
    st.plotly_chart(fig_map)

# Download button
st.download_button("Download filtered data", filtered_df.to_csv(index=False), file_name="filtered_data.csv")
