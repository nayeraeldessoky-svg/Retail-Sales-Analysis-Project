

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

df_clean = pd.read_csv(
    r"C:\Users\nayer\Downloads\python course\final project stuff\retail_sales_cleaned.csv")
Navigator = st.sidebar.title('🧭Navigator')
page = st.sidebar.radio("Pages", ["Dataset", "Analytics"])

if page == 'Dataset':
    st.title("🛍️Retail Sales Analysis")
    st.subheader("Sales Trends, Product Performance & Purchasing Behavior")
    st.image('https://vidi-corp.com/wp-content/uploads/2025/05/retaildatanalytics.png')
    st.header('Retail Dataset')
    st.dataframe(df_clean)
    
    st.write("### 📋 Column Descriptions")

    cols = {
    "Transaction ID": "A unique identifier for each transaction. Always present and unique.",
    "Category": "The category of the purchased item, such as Food or Furniture.",
    "Item": "The name of the purchased item.",
    "Price Per Unit": "The price of a single unit of the purchased item.",
    "Quantity": "The number of units purchased in a transaction.",
    "Total Spent": "The total amount spent on the transaction, calculated as Quantity multiplied by Price Per Unit.",
    "Payment Method": "The payment method used for the transaction, such as Cash, Credit Card, or Digital Wallet.",
    "Location": "The location where the transaction occurred, such as In-store or Online.",
    "Transaction Date": "The date on which the transaction occurred.",
    "Discount Applied": "Indicates whether a discount was applied.",
    "Year-Month": "An engineered time feature representing the transaction year and month, used for chronological monthly sales analysis.",
    "Month-Year": "An engineered time feature displaying the transaction month and year in a readable format, such as Jan 2023, for chart labels."
     }

    for col, desc in cols.items():
        with st.expander(f" {col}"):
            st.write(desc)

            
            
elif page == 'Analytics':

    st.title("🛍️ Retail Data Analytics")
    
    # Sidebar Filters
    st.sidebar.header("🔎 Filter Your Analysis")

    # Category
    categories = ["All Categories"] + sorted(df_clean["Category"].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("🛍️ Select Category", categories)

    # Location
    locations = ["All Locations"] + sorted(df_clean["Location"].dropna().unique().tolist())
    selected_location = st.sidebar.selectbox("🌐 Select Location", locations)

    # Payment Method
    payment_methods = ["All Payment Methods"] + sorted(df_clean["Payment Method"].dropna().unique().tolist())
    selected_payment = st.sidebar.selectbox("💳 Select Payment Method", payment_methods)

    # Date Range
    df_clean["Transaction Date"] = pd.to_datetime(df_clean["Transaction Date"])

    min_date = df_clean["Transaction Date"].min().date()
    max_date = df_clean["Transaction Date"].max().date()

    date_range = st.sidebar.date_input(
        "📅 Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date)

    # Apply Filters
    filtered_df = df_clean.copy()

    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]

    if selected_location != "All Locations":
        filtered_df = filtered_df[filtered_df["Location"] == selected_location]

    if selected_payment != "All Payment Methods":
        filtered_df = filtered_df[filtered_df["Payment Method"] == selected_payment]

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[(filtered_df["Transaction Date"].dt.date >= start_date)
            & (filtered_df["Transaction Date"].dt.date <= end_date)]

    # Four Metrics
    total_revenue = filtered_df["Total Spent"].sum()
    total_transactions = len(filtered_df)
    units_sold = filtered_df["Quantity"].sum()

    avg_transaction = (
        total_revenue / total_transactions
        if total_transactions > 0 else 0
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💰 Total Revenue", f"{total_revenue:,.0f}")
        st.metric("📦 Units Sold", f"{units_sold:,.0f}")

    with col2:
        st.metric("🧾 Transactions", f"{total_transactions:,}")
        st.metric("🧮 Avg. Transaction", f"{avg_transaction:,.2f}")

    tab1, tab2, tab3 = st.tabs( ["Univariate", "Bivariate", "Multivariate"] )

    
    

    
   

    with tab1:
#Distribution of Transaction Values
        st.plotly_chart(px.histogram(filtered_df, x="Total Spent", nbins= 30,title="Distribution of Transaction Values",
    labels={"Total Spent": "Transaction Value"},color_discrete_sequence=["#3B82F6"]))
        
#Number of Transactions by Category
        st.plotly_chart(px.pie(filtered_df, names="Category", title=" Number of Transactions by Category", color_discrete_sequence=[
        "#1D4ED8", "#3B82F6", "#60A5FA", "#93C5FD", "#2563EB", "#1E40AF", "#BFDBFE", "#DBEAFE"]))
        
#Number of Transactions by Location
        st.plotly_chart(px.pie(filtered_df, names="Location", title=" Number of Transactions by Location", color_discrete_sequence=[
        "#1D4ED8", "#3B82F6"]))
            
            

#Top 10 Most Frequently Purchased Items
        item_counts = (filtered_df["Item"].value_counts().head(10).reset_index())

        item_counts.columns = ["Item", "Transactions"]

        fig = px.bar(item_counts,x="Transactions", y="Item",orientation="h",
    title="Top 10 Most Frequently Purchased Items",
    labels={"count": "Number of Transactions","Item": "Item"},text_auto=True,
    color_discrete_sequence=["#3B82F6"])

        fig.update_layout(yaxis={"categoryorder": "total ascending"})

        st.plotly_chart(fig, use_container_width=True)


      
 #Transactions by Payment Method
        payment_counts = (filtered_df["Payment Method"].value_counts().reset_index())

        payment_counts.columns = ["Payment Method", "Transactions"]

        fig = px.bar( payment_counts,x="Payment Method",y="Transactions",title=" Transactions by Payment Method",
    labels={"Payment Method": "Payment Method","count": "Number of Transactions"},
    text_auto=True,color_discrete_sequence=["#3B82F6"])

        st.plotly_chart(fig, use_container_width=True)

        
 #Distribution of Quantity per Transaction       
        quantity_counts = (filtered_df["Quantity"].value_counts().sort_index().reset_index())

        quantity_counts.columns = ["Quantity", "Transactions"]

        fig = px.bar(quantity_counts, x="Quantity",y="Transactions",title=" Distribution of Quantity per Transaction",
    labels={"Quantity": "Quantity Purchased","Transactions": "Number of Transactions"},
    text_auto=True,color_discrete_sequence=["#3B82F6"])

        st.plotly_chart(fig, use_container_width=True)
        

    
    
    
    
    
    
    with tab2:
        
 #Monthly Sales Over Time       
        monthly_sales = (filtered_df.groupby("Year-Month", as_index=False)["Total Spent"].sum() .sort_values("Year-Month"))

        monthly_sales["Year-Month"] = monthly_sales["Year-Month"].astype(str)

        fig = px.line( monthly_sales,x="Year-Month", y="Total Spent",title=" Monthly Sales Over Time",
    labels={"Year-Month": "Month-Year", "Total Spent": "Total Revenue"},markers=True,color_discrete_sequence=["#3B82F6"])

        st.plotly_chart(fig, use_container_width=True)
        
 #Top 10 Best-Selling Items by Quantity       
        item_sales = (filtered_df.groupby("Item", as_index=False)["Quantity"].sum().sort_values("Quantity", ascending=False).head(10))

        fig = px.bar(item_sales,x="Quantity",y="Item",orientation="h",title=" Top 10 Best-Selling Items by Quantity",
    labels={ "Quantity": "Total Units Sold", "Item": "Item"},
    text_auto=True,color_discrete_sequence=["#3B82F6"])

        fig.update_layout(yaxis={"categoryorder": "total ascending"})

        st.plotly_chart(fig, use_container_width=True)
        


#Total Revenue by Product Category
        category_sales = (filtered_df.groupby("Category", as_index=False)["Total Spent"].sum().sort_values("Total Spent", ascending=False))

        fig = px.bar( category_sales,x="Category",y="Total Spent",title=" Total Revenue by Product Category",
    labels={"Category": "Product Category", "Total Spent": "Total Revenue"},
    text_auto=True,color_discrete_sequence=["#3B82F6"])

        st.plotly_chart(fig, use_container_width=True)

        
 #Total Units Sold by Category       
        category_quantity = (filtered_df.groupby("Category", as_index=False)["Quantity"].sum() .sort_values("Quantity", ascending=False))

        fig = px.bar(category_quantity, x="Category", y="Quantity", title=" Total Units Sold by Category",
    labels={ "Category": "Product Category","Quantity": "Total Units Sold" },
    text_auto=True, color_discrete_sequence=["#3B82F6"])

        st.plotly_chart(fig, use_container_width=True)
        
#Total Revenue by Payment Method
        payment_sales = (filtered_df.groupby("Payment Method", as_index=False)["Total Spent"].sum().sort_values("Total Spent", ascending=False))

        fig = px.bar( payment_sales, x="Payment Method", y="Total Spent", title="Total Revenue by Payment Method",
    labels={ "Payment Method": "Payment Method","Total Spent": "Total Revenue"},
    text_auto=True,color_discrete_sequence=["#3B82F6"])

        st.plotly_chart(fig, use_container_width=True)
    
    
 #Total Revenue by Location   
        location_sales = (filtered_df.groupby("Location", as_index=False)["Total Spent"].sum().sort_values("Total Spent", ascending=False))

        fig = px.bar(location_sales, x="Location", y="Total Spent",title="Total Revenue by Location",
    labels={ "Location": "Store Location", "Total Spent": "Total Revenue"},
    text_auto=True, color_discrete_sequence=["#3B82F6"])

        st.plotly_chart(fig, use_container_width=True)

        
        
        
        
        
        
    with tab3:
        
 #Revenue by Category and Location       
        category_location = (filtered_df.groupby(["Category", "Location"], as_index=False)["Total Spent"].sum())

        fig = px.bar(category_location,x="Category",y="Total Spent",color="Location", barmode="group",title=" Revenue by Category and Location",
    labels={ "Category": "Product Category", "Location": "Location","Total Spent": "Total Revenue"},
    color_discrete_sequence=[ "#1D4ED8", "#3B82F6","#60A5FA", "#93C5FD"])

        st.plotly_chart(fig, use_container_width=True)

        
        
#Revenue by Payment Method and Location
        location_payment_revenue = (filtered_df.groupby( ["Location", "Payment Method"], as_index=False)["Total Spent"].sum())

        fig = px.bar(location_payment_revenue,x="Location", y="Total Spent", color="Payment Method", barmode="group",
    title="Revenue by Payment Method and Location",labels={"Location": "Location","Payment Method": "Payment Method","Total Spent": "Total Revenue"},
    color_discrete_sequence=["#1D4ED8", "#3B82F6", "#60A5FA","#93C5FD","#BFDBFE"])

        st.plotly_chart(fig, use_container_width=True)




