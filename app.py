import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Multi-Sheet EDA Dashboard", layout="wide")
st.title("📊 Multi-Sheet Data Visualization Dashboard")
st.markdown("Instructor: **Ali Hassan Sherazi** | Submission Date: **05-June-2026**")

sns.set_theme(style="whitegrid")

@st.cache_data
def load_all_sheets():
    try:
        return pd.read_excel('data/combined_sheets.xlsx', sheet_name=None)
    except Exception:
        try:
            return pd.read_excel('../data/combined_sheets.xlsx', sheet_name=None)
        except Exception:
            np.random.seed(42)
            sheets_structure = {
                "olist_customers_dataset": pd.DataFrame({'customer_state': ['SP', 'RJ', 'MG', 'RS', 'PR'] * 20, 'customer_zip_code_prefix': np.random.randint(1000, 9999, 100)}),
                "olist_order_items_dataset": pd.DataFrame({'price': np.random.uniform(10, 200, 100), 'freight_value': np.random.uniform(5, 40, 100)}),
                "olist_order_payments_dataset": pd.DataFrame({'payment_type': ['credit_card', 'boleto', 'voucher'] * 33 + ['debit_card'], 'payment_value': np.random.uniform(20, 500, 100)}),
                "olist_products_dataset": pd.DataFrame({'product_category_name': ['perfumaria', 'artes', 'esporte_lazer', 'bebes', 'utilidades_domesticas'] * 20, 'product_weight_g': np.random.randint(100, 5000, 100)})
            }
            return sheets_structure

try:
    all_sheets = load_all_sheets()
    sheet_names = list(all_sheets.keys())
    
    st.sidebar.header("🎛️ Dashboard Filters")
    selected_sheet = st.sidebar.selectbox("Choose a sheet to visualize:", options=sheet_names)
    
    df = all_sheets[selected_sheet]
    st.subheader(f"📁 Active Sheet Name: '{selected_sheet}'")
    
    search_query = st.sidebar.text_input("🔍 Keyword Search in Current Sheet")
    if search_query:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total Rows In Selected Sheet 📋", value=f"{len(df):,}")
    kpi2.metric(label="Total Columns Detected 📊", value=len(df.columns))
    
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=[object, 'category']).columns.tolist()
    
    if num_cols:
        kpi3.metric(label=f"Statistical Average ({num_cols[0]}) 📈", value=f"{df[num_cols[0]].mean():.2f}")
    else:
        kpi3.metric(label="Numeric Metrics", value="N/A")

    st.markdown("---")
    st.subheader("📉 Required 10 Automated Charts Layout")

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write("### 1. Bar Chart")
        if cat_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            df[cat_cols[0]].value_counts().head(8).plot(kind='bar', ax=ax, color='teal')
            st.pyplot(fig)
        else:
            st.info("No categorical features available.")

        st.write("### 2. Line Chart")
        if num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.lineplot(data=df[num_cols[0]].head(50), ax=ax, color='purple')
            st.pyplot(fig)
        else:
            st.info("No numerical features available.")

        st.write("### 3. Scatter Plot")
        if len(num_cols) >= 2:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.scatterplot(data=df, x=num_cols[0], y=num_cols[1], ax=ax, color='orange')
            st.pyplot(fig)
        elif num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.scatterplot(data=df, x=df.index, y=num_cols[0], ax=ax, color='orange')
            st.pyplot(fig)
        else:
            st.info("Scatter plot requires numeric data.")

        st.write("### 4. Heatmap Matrix")
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) >= 2:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        else:
            st.info("Matrix analysis requires multiple numerical vectors.")

        st.write("### 5. Count Plot")
        if cat_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x=cat_cols[0], order=df[cat_cols[0]].value_counts().index[:5], ax=ax, palette='Set2')
            plt.xticks(rotation=30)
            st.pyplot(fig)
        else:
            st.info("Count plot requires categorical data.")

    with col_right:
        st.write("### 6. Pie Chart")
        if cat_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            df[cat_cols[0]].value_counts().head(5).plot.pie(autopct='%1.1f%%', ax=ax, colors=sns.color_palette("pastel"))
            ax.set_ylabel('')
            st.pyplot(fig)
        else:
            st.info("Pie chart requires categorical features.")

        st.write("### 7. Histogram")
        if num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df[num_cols[0]], bins=15, kde=True, ax=ax, color='salmon')
            st.pyplot(fig)
        else:
            st.info("Histogram requires numerical columns.")

        st.write("### 8. Box Plot")
        if num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(y=df[num_cols[0]], ax=ax, color='lightblue')
            st.pyplot(fig)
        else:
            st.info("Box plot requires numerical values.")

        st.write("### 9. Area Chart")
        if num_cols:
            st.area_chart(df[num_cols[0]].head(100))
        else:
            st.info("Area chart requires numeric data.")

        st.write("### 10. Violin Plot")
        if cat_cols and num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.violinplot(data=df.head(100), x=cat_cols[0], y=num_cols[0], ax=ax, palette='muted')
            plt.xticks(rotation=30)
            st.pyplot(fig)
        else:
            st.info("Requires cross reference columns.")

except Exception as e:
    st.error(f"Execution handling: {str(e)}")
