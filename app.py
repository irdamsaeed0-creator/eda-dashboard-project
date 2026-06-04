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
    # Reading sheets from the combined Excel document
    excel_path = 'data/combined_sheets.xlsx'
    try:
        return pd.read_excel(excel_path, sheet_name=None)
    except FileNotFoundError:
        return pd.read_excel('../data/combined_sheets.xlsx', sheet_name=None)

try:
    all_sheets = load_all_sheets()
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
    st.error(f"Waiting for dataset: {str(e)}")
    st.info("Ensure Excel workbook 'data/combined_sheets.xlsx' is saved successfully.")
