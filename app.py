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
def generate_all_sheets():
    np.random.seed(42)
    size = 150
    
    # Automated Fallback Generator for all 9 Sheets
    sheets_data = {
        "olist_customers_dataset": pd.DataFrame({
            'customer_id': [f"cust_{i}" for i in range(size)],
            'customer_unique_id': [f"uniq_{i}" for i in range(size)],
            'customer_zip_code_prefix': np.random.randint(1000, 99999, size),
            'customer_city': np.random.choice(['Sao Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador'], size),
            'customer_state': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'PR'], size)
        }),
        "olist_geolocation_dataset": pd.DataFrame({
            'geolocation_zip_code_prefix': np.random.randint(1000, 99999, size),
            'geolocation_lat': np.random.uniform(-33, 4, size),
            'geolocation_lng': np.random.uniform(-73, -34, size),
            'geolocation_city': np.random.choice(['Sao Paulo', 'Rio', 'Curitiba'], size),
            'geolocation_state': np.random.choice(['SP', 'RJ', 'PR'], size)
        }),
        "olist_order_items_dataset": pd.DataFrame({
            'order_id': [f"order_{i}" for i in range(size)],
            'order_item_id': np.random.randint(1, 4, size),
            'product_id': [f"prod_{i}" for i in range(size)],
            'seller_id': [f"sell_{i}" for i in range(size)],
            'price': np.random.uniform(15.0, 350.0, size),
            'freight_value': np.random.uniform(5.0, 60.0, size)
        }),
        "olist_order_payments_dataset": pd.DataFrame({
            'order_id': [f"order_{i}" for i in range(size)],
            'payment_sequential': np.random.randint(1, 3, size),
            'payment_type': np.random.choice(['credit_card', 'boleto', 'voucher', 'debit_card'], size),
            'payment_installments': np.random.randint(1, 12, size),
            'payment_value': np.random.uniform(20, 500, size)
        }),
        "olist_order_reviews_dataset": pd.DataFrame({
            'review_id': [f"rev_{i}" for i in range(size)],
            'order_id': [f"order_{i}" for i in range(size)],
            'review_score': np.random.choice([1, 2, 3, 4, 5], size, p=[0.1, 0.05, 0.1, 0.3, 0.45]),
            'review_comment_title': np.random.choice(['Recomendo', 'Bom', 'Ruim', 'Muito bom'], size)
        }),
        "olist_orders_dataset": pd.DataFrame({
            'order_id': [f"order_{i}" for i in range(size)],
            'customer_id': [f"cust_{i}" for i in range(size)],
            'order_status': np.random.choice(['delivered', 'shipped', 'canceled', 'invoiced'], size, p=[0.9, 0.05, 0.03, 0.02]),
            'order_purchase_timestamp': pd.date_range(start='2025-01-01', periods=size, freq='H')
        }),
        "olist_products_dataset": pd.DataFrame({
            'product_id': [f"prod_{i}" for i in range(size)],
            'product_category_name': np.random.choice(['beleza_saude', 'informatica_acessorios', 'automotivo', 'cama_mesa_banho'], size),
            'product_name_lenght': np.random.randint(20, 60, size),
            'product_weight_g': np.random.uniform(100, 5000, size)
        }),
        "olist_sellers_dataset": pd.DataFrame({
            'seller_id': [f"sell_{i}" for i in range(size)],
            'seller_zip_code_prefix': np.random.randint(1000, 99999, size),
            'seller_city': np.random.choice(['Sao Paulo', 'Curitiba', 'Campinas'], size),
            'seller_state': np.random.choice(['SP', 'PR', 'SP'], size)
        }),
        "product_category_name_translation": pd.DataFrame({
            'product_category_name': ['beleza_saude', 'informatica_acessorios', 'automotivo', 'cama_mesa_banho'],
            'product_category_name_english': ['health_beauty', 'computers_accessories', 'auto', 'bed_bath_table']
        })
    }
    return sheets_data

try:
    all_sheets = generate_all_sheets()
    sheet_names = list(all_sheets.keys())
    
    st.sidebar.header("🎛️ Dashboard Filters")
    selected_sheet = st.sidebar.selectbox("Choose a sheet to visualize:", options=sheet_names)
    
    df = all_sheets[selected_sheet]
    st.subheader(f"📁 Currently Active Sheet: '{selected_sheet}'")
    
    search_query = st.sidebar.text_input("🔍 Keyword Search in Current Sheet")
    if search_query:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total Rows In Sheet 📋", value=f"{len(df):,}")
    kpi2.metric(label="Total Columns 📊", value=len(df.columns))
    
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=[object, 'category']).columns.tolist()
    
    if num_cols:
        kpi3.metric(label=f"Avg Value ({num_cols[0]}) 📈", value=f"{df[num_cols[0]].mean():.2f}")
    else:
        kpi3.metric(label="Numeric Metrics", value="N/A")

    st.markdown("---")
    st.subheader("📉 Required 10 Chart Visualizations")

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write("### 1. Bar Chart")
        if cat_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            df[cat_cols[0]].value_counts().head(8).plot(kind='bar', ax=ax, color='teal')
            st.pyplot(fig)
        else: st.info("No matching fields for Bar Chart.")

        st.write("### 2. Line Chart")
        if num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.lineplot(data=df[num_cols[0]].head(50), ax=ax, color='purple')
            st.pyplot(fig)
        else: st.info("Requires Numeric Fields.")

        st.write("### 3. Scatter Plot")
        if len(num_cols) >= 2:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.scatterplot(data=df, x=num_cols[0], y=num_cols[1], ax=ax, color='orange')
            st.pyplot(fig)
        else: st.info("Requires 2 numerical columns.")

        st.write("### 4. Heatmap")
        if len(num_cols) >= 2:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        else: st.info("Requires multiple numerical attributes.")

        st.write("### 5. Count Plot")
        if cat_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x=cat_cols[0], order=df[cat_cols[0]].value_counts().index[:5], ax=ax, palette='Set2')
            plt.xticks(rotation=30)
            st.pyplot(fig)
        else: st.info("Requires categorical features.")

    with col_right:
        st.write("### 6. Pie Chart")
        if cat_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            df[cat_cols[0]].value_counts().head(5).plot.pie(autopct='%1.1f%%', ax=ax, colors=sns.color_palette("pastel"))
            ax.set_ylabel('')
            st.pyplot(fig)
        else: st.info("Requires categorical features.")

        st.write("### 7. Histogram")
        if num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df[num_cols[0]], bins=15, kde=True, ax=ax, color='salmon')
            st.pyplot(fig)
        else: st.info("Requires numerical columns.")

        st.write("### 8. Box Plot")
        if num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(y=df[num_cols[0]], ax=ax, color='lightblue')
            st.pyplot(fig)
        else: st.info("Requires numerical values.")

        st.write("### 9. Area Chart")
        if num_cols:
            st.area_chart(df[num_cols[0]].head(100))
        else: st.info("Requires numeric data.")

        st.write("### 10. Violin Plot")
        if cat_cols and num_cols:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.violinplot(data=df.head(100), x=cat_cols[0], y=num_cols[0], ax=ax, palette='muted')
            plt.xticks(rotation=30)
            st.pyplot(fig)
        else: st.info("Requires categorical and numeric data.")

except Exception as e:
    st.error(f"Error loading dashboard: {str(e)}")
