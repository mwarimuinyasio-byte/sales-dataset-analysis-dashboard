import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("Sales Dataset Analysis Dashboard")
st.write("Interactive analysis of sales performance and customer purchasing data.")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("sales.csv")

    # Convert date column
    if "Sale_Date" in df.columns:
        df["Sale_Date"] = pd.to_datetime(
            df["Sale_Date"],
            errors="coerce"
        )

    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "The file 'sales.csv' was not found. "
        "Place the CSV file in the same folder as this Streamlit file."
    )
    st.stop()

# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

numeric_columns = [
    "Sales_Amount",
    "Quantity_Sold",
    "Unit_Cost",
    "Unit_Price",
    "Discount"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

# Region filter
if "Region" in df.columns:
    regions = df["Region"].dropna().unique().tolist()

    selected_regions = st.sidebar.multiselect(
        "Select Region",
        options=regions,
        default=regions
    )
else:
    selected_regions = []

# Product category filter
if "Product_Category" in df.columns:
    categories = (
        df["Product_Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Select Product Category",
        options=categories,
        default=categories
    )
else:
    selected_categories = []

# Sales representative filter
if "Sales_Rep" in df.columns:
    sales_reps = (
        df["Sales_Rep"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_reps = st.sidebar.multiselect(
        "Select Sales Representative",
        options=sales_reps,
        default=sales_reps
    )
else:
    selected_reps = []

# Customer type filter
if "Customer_Type" in df.columns:
    customer_types = (
        df["Customer_Type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_customer_types = st.sidebar.multiselect(
        "Customer Type",
        options=customer_types,
        default=customer_types
    )
else:
    selected_customer_types = []

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if "Region" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(selected_regions)
    ]

if "Product_Category" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Product_Category"].isin(selected_categories)
    ]

if "Sales_Rep" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Sales_Rep"].isin(selected_reps)
    ]

if "Customer_Type" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Customer_Type"].isin(selected_customer_types)
    ]

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_sales = (
    filtered_df["Sales_Amount"].sum()
    if "Sales_Amount" in filtered_df.columns
    else 0
)

total_quantity = (
    filtered_df["Quantity_Sold"].sum()
    if "Quantity_Sold" in filtered_df.columns
    else 0
)

average_sale = (
    filtered_df["Sales_Amount"].mean()
    if "Sales_Amount" in filtered_df.columns
    else 0
)

number_of_sales = len(filtered_df)

col1.metric(
    "Total Sales",
    f"{total_sales:,.2f}"
)

col2.metric(
    "Quantity Sold",
    f"{total_quantity:,.0f}"
)

col3.metric(
    "Average Sale",
    f"{average_sale:,.2f}"
)

col4.metric(
    "Number of Sales",
    f"{number_of_sales:,}"
)

# --------------------------------------------------
# SALES BY REGION
# --------------------------------------------------

st.subheader("Sales Analysis")

col1, col2 = st.columns(2)

with col1:

    if (
        "Region" in filtered_df.columns
        and "Sales_Amount" in filtered_df.columns
    ):

        region_sales = (
            filtered_df
            .groupby("Region", as_index=False)["Sales_Amount"]
            .sum()
            .sort_values(
                "Sales_Amount",
                ascending=False
            )
        )

        fig_region = px.bar(
            region_sales,
            x="Region",
            y="Sales_Amount",
            title="Total Sales by Region",
            text_auto=".2s"
        )

        fig_region.update_layout(
            template="plotly_white",
            xaxis_title="Region",
            yaxis_title="Sales Amount"
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

with col2:

    if (
        "Product_Category" in filtered_df.columns
        and "Sales_Amount" in filtered_df.columns
    ):

        category_sales = (
            filtered_df
            .groupby(
                "Product_Category",
                as_index=False
            )["Sales_Amount"]
            .sum()
            .sort_values(
                "Sales_Amount",
                ascending=False
            )
        )

        fig_category = px.bar(
            category_sales,
            x="Product_Category",
            y="Sales_Amount",
            title="Total Sales by Product Category",
            text_auto=".2s"
        )

        fig_category.update_layout(
            template="plotly_white",
            xaxis_title="Product Category",
            yaxis_title="Sales Amount"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

# --------------------------------------------------
# SALES TREND
# --------------------------------------------------

if (
    "Sale_Date" in filtered_df.columns
    and "Sales_Amount" in filtered_df.columns
):

    st.subheader("Sales Trend Over Time")

    daily_sales = (
        filtered_df
        .dropna(subset=["Sale_Date"])
        .groupby("Sale_Date", as_index=False)["Sales_Amount"]
        .sum()
    )

    fig_trend = px.line(
        daily_sales,
        x="Sale_Date",
        y="Sales_Amount",
        title="Sales Amount Over Time",
        markers=True
    )

    fig_trend.update_layout(
        template="plotly_white",
        xaxis_title="Sale Date",
        yaxis_title="Sales Amount"
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

# --------------------------------------------------
# SALES REPRESENTATIVE ANALYSIS
# --------------------------------------------------

if (
    "Sales_Rep" in filtered_df.columns
    and "Sales_Amount" in filtered_df.columns
):

    st.subheader("Sales Representative Performance")

    rep_sales = (
        filtered_df
        .groupby("Sales_Rep", as_index=False)["Sales_Amount"]
        .sum()
        .sort_values(
            "Sales_Amount",
            ascending=False
        )
    )

    fig_rep = px.bar(
        rep_sales,
        x="Sales_Rep",
        y="Sales_Amount",
        title="Sales by Sales Representative",
        text_auto=".2s"
    )

    fig_rep.update_layout(
        template="plotly_white",
        xaxis_title="Sales Representative",
        yaxis_title="Sales Amount"
    )

    st.plotly_chart(
        fig_rep,
        use_container_width=True
    )

# --------------------------------------------------
# CUSTOMER TYPE ANALYSIS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    if (
        "Customer_Type" in filtered_df.columns
        and "Sales_Amount" in filtered_df.columns
    ):

        customer_sales = (
            filtered_df
            .groupby(
                "Customer_Type",
                as_index=False
            )["Sales_Amount"]
            .sum()
        )

        fig_customer = px.pie(
            customer_sales,
            names="Customer_Type",
            values="Sales_Amount",
            title="Sales by Customer Type"
        )

        fig_customer.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_customer,
            use_container_width=True
        )

with col2:

    if (
        "Payment_Method" in filtered_df.columns
        and "Sales_Amount" in filtered_df.columns
    ):

        payment_sales = (
            filtered_df
            .groupby(
                "Payment_Method",
                as_index=False
            )["Sales_Amount"]
            .sum()
        )

        fig_payment = px.pie(
            payment_sales,
            names="Payment_Method",
            values="Sales_Amount",
            title="Sales by Payment Method"
        )

        fig_payment.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )

# --------------------------------------------------
# SALES CHANNEL
# --------------------------------------------------

if (
    "Sales_Channel" in filtered_df.columns
    and "Sales_Amount" in filtered_df.columns
):

    st.subheader("Sales Channel Performance")

    channel_sales = (
        filtered_df
        .groupby(
            "Sales_Channel",
            as_index=False
        )["Sales_Amount"]
        .sum()
        .sort_values(
            "Sales_Amount",
            ascending=False
        )
    )

    fig_channel = px.bar(
        channel_sales,
        x="Sales_Channel",
        y="Sales_Amount",
        title="Sales by Sales Channel",
        text_auto=".2s"
    )

    fig_channel.update_layout(
        template="plotly_white",
        xaxis_title="Sales Channel",
        yaxis_title="Sales Amount"
    )

    st.plotly_chart(
        fig_channel,
        use_container_width=True
    )

# --------------------------------------------------
# QUANTITY SOLD BY CATEGORY
# --------------------------------------------------

if (
    "Product_Category" in filtered_df.columns
    and "Quantity_Sold" in filtered_df.columns
):

    st.subheader("Quantity Sold by Product Category")

    category_quantity = (
        filtered_df
        .groupby(
            "Product_Category",
            as_index=False
        )["Quantity_Sold"]
        .sum()
        .sort_values(
            "Quantity_Sold",
            ascending=False
        )
    )

    fig_quantity = px.bar(
        category_quantity,
        x="Product_Category",
        y="Quantity_Sold",
        title="Quantity Sold by Product Category",
        text_auto=True
    )

    fig_quantity.update_layout(
        template="plotly_white",
        xaxis_title="Product Category",
        yaxis_title="Quantity Sold"
    )

    st.plotly_chart(
        fig_quantity,
        use_container_width=True
    )

# --------------------------------------------------
# UNIT PRICE VS SALES
# --------------------------------------------------

if (
    "Unit_Price" in filtered_df.columns
    and "Sales_Amount" in filtered_df.columns
):

    st.subheader("Unit Price vs Sales Amount")

    fig_scatter = px.scatter(
        filtered_df,
        x="Unit_Price",
        y="Sales_Amount",
        color="Region" if "Region" in filtered_df.columns else None,
        size="Quantity_Sold"
        if "Quantity_Sold" in filtered_df.columns
        else None,
        hover_data=[
            column
            for column in [
                "Product_ID",
                "Sales_Rep",
                "Product_Category",
                "Quantity_Sold",
                "Discount"
            ]
            if column in filtered_df.columns
        ],
        title="Unit Price vs Sales Amount"
    )

    fig_scatter.update_layout(
        template="plotly_white",
        xaxis_title="Unit Price",
        yaxis_title="Sales Amount"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

# --------------------------------------------------
# PROFIT ANALYSIS
# --------------------------------------------------

if all(
    column in filtered_df.columns
    for column in [
        "Unit_Cost",
        "Unit_Price",
        "Quantity_Sold"
    ]
):

    st.subheader("Profit Analysis")

    filtered_df["Profit_Per_Unit"] = (
        filtered_df["Unit_Price"]
        - filtered_df["Unit_Cost"]
    )

    filtered_df["Total_Profit"] = (
        filtered_df["Profit_Per_Unit"]
        * filtered_df["Quantity_Sold"]
    )

    profit_col1, profit_col2 = st.columns(2)

    total_profit = filtered_df["Total_Profit"].sum()

    average_profit = filtered_df["Total_Profit"].mean()

    profit_col1.metric(
        "Total Profit",
        f"{total_profit:,.2f}"
    )

    profit_col2.metric(
        "Average Profit per Sale",
        f"{average_profit:,.2f}"
    )

    if "Product_Category" in filtered_df.columns:

        profit_category = (
            filtered_df
            .groupby(
                "Product_Category",
                as_index=False
            )["Total_Profit"]
            .sum()
            .sort_values(
                "Total_Profit",
                ascending=False
            )
        )

        fig_profit = px.bar(
            profit_category,
            x="Product_Category",
            y="Total_Profit",
            title="Profit by Product Category",
            text_auto=".2s"
        )

        fig_profit.update_layout(
            template="plotly_white",
            xaxis_title="Product Category",
            yaxis_title="Total Profit"
        )

        st.plotly_chart(
            fig_profit,
            use_container_width=True
        )

# --------------------------------------------------
# DATASET
# --------------------------------------------------

st.subheader("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# --------------------------------------------------
# DOWNLOAD FILTERED DATA
# --------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_sales_dataset.csv",
    mime="text/csv"
)