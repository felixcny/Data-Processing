import streamlit as st
import duckdb
import pandas as pd 
import plotly.express as px

st.set_page_config(page_title='dashboard',layout='wide')
st.title("Dashboard performance e-commerce")
st.markdown("----")

conn = duckdb.connect("/opt/dagster/app/data/local_database.duckdb")

kpi_query = """
SELECT 
    sum(revenue_net) as total_revenue,
    count(product_id) as nb_produit,
    avg(revenue_net) as avg_order,
    count(distinct user_id) as nb_clients
FROM main_marts.fct_sales
"""
kpis = conn.execute(kpi_query).fetchone()

col1, col2, col3, col4 = st.columns(4)

with col1:
    formatted_rev = f"{kpis[0]:,.2f}".replace(",", " ").replace(".", ",")
    st.metric("Revenue Total", f"{formatted_rev} $")

with col2:
    st.metric("Produits vendus", f"{int(kpis[1])}")

with col3:
    formatted_basket = f"{kpis[2]:,.2f}".replace(",", " ").replace(".", ",")
    st.metric("Panier moyen", f"{formatted_basket} $")

with col4:
    st.metric("Nombre de clients", "150")

st.markdown("----")

st.subheader("Évolution du CA Journalier")
daily_query = """
    SELECT 
        d.full_date, 
        SUM(f.revenue_net) as revenue
    FROM main_marts.fct_sales f
    JOIN main_marts.dim_date d ON f.date_id = d.date_id
    GROUP BY 1
    ORDER BY 1
"""
df_daily = conn.execute(daily_query).df()
fig_line = px.line(df_daily, x='full_date', y='revenue', title="Revenu net par jour")
st.plotly_chart(fig_line, use_container_width=True)

col_gauche, col_droit = st.columns(2)

with col_gauche:
    st.subheader("Performance par Catégorie")
    cat_query = """
        SELECT p.product_category, SUM(f.quantity) as quantity
        FROM main_marts.fct_sales f
        JOIN main_marts.dim_products p ON f.product_id = p.product_id
        GROUP BY 1 ORDER BY 2 DESC
    """
    df_cat = conn.execute(cat_query).df()
    fig_bar = px.bar(df_cat, x='quantity', y='product_category', orientation='h', color='quantity')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_droit:
    st.subheader("Profil Clients (Segments d'âge)")
    age_query = """
        SELECT age_segment, COUNT(*) as nb_users
        FROM main_marts.dim_user
        GROUP BY 1
    """
    df_age = conn.execute(age_query).df()
    fig_pie = px.pie(df_age, values='nb_users', names='age_segment', hole=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)

conn.close()