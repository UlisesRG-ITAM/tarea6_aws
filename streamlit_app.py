import streamlit as st
import pandas as pd
import configparser
import awswrangler as wr
import matplotlib.pyplot as plt
import statsmodels.api as sm
import boto3
from queries import QUERY

def load_data():
    config = configparser.ConfigParser()
    config.read('config.ini')

    profile_name = config['aws']['profile_name']
    db_name = config['aws']['db_name']

    session = boto3.Session(profile_name=profile_name)

    df = wr.athena.read_sql_query(
        QUERY, 
        database=db_name, 
        ctas_approach=False, 
        boto3_session=session
    )

    return df

def main():
    st.title("Análisis Económico: Tipo de cambio, Tasa de Interés, Inflación")
    df = load_data()
    
    st.subheader("Vista previa de datos")
    st.write(df.head())

    # Botón para mostrar gráficas
    if st.button("Mostrar regresiones"):
        
        # 1) tipo_cambio ~ cetes_365
        st.subheader("Regresión: tipo_cambio ~ cetes_365")
        X = df[['cetes_365']]
        X = sm.add_constant(X)
        y = df['tipo_cambio']
        model_tc_ti = sm.OLS(y, X).fit()
        st.write(model_tc_ti.summary())

        fig1, ax1 = plt.subplots()
        ax1.scatter(df['cetes_365'], df['tipo_cambio'])
        pred_line = model_tc_ti.predict(sm.add_constant(df[['cetes_365']]))
        ax1.plot(df['cetes_365'], pred_line)
        ax1.set_xlabel('cetes_365')
        ax1.set_ylabel('tipo_cambio')
        ax1.set_title('tipo_cambio ~ cetes_365')
        st.pyplot(fig1)

        # 2) cetes_365 ~ inflacion_inpc
        st.subheader("Regresión: cetes_365 ~ inflacion_inpc")
        X2 = df[['inflacion_inpc']]
        X2 = sm.add_constant(X2)
        y2 = df['cetes_365']
        model_ti_inf = sm.OLS(y2, X2).fit()
        st.write(model_ti_inf.summary())

        fig2, ax2 = plt.subplots()
        ax2.scatter(df['inflacion_inpc'], df['cetes_365'])
        pred_line2 = model_ti_inf.predict(sm.add_constant(df[['inflacion_inpc']]))
        ax2.plot(df['inflacion_inpc'], pred_line2)
        ax2.set_xlabel('inflacion_inpc')
        ax2.set_ylabel('cetes_365')
        ax2.set_title('cetes_365 ~ inflacion_inpc')
        st.pyplot(fig2)

        # 3) tipo_cambio ~ inflacion_inpc
        st.subheader("Regresión: tipo_cambio ~ inflacion_inpc")
        X3 = df[['inflacion_inpc']]
        X3 = sm.add_constant(X3)
        y3 = df['tipo_cambio']
        model_tc_inf = sm.OLS(y3, X3).fit()
        st.write(model_tc_inf.summary())

        fig3, ax3 = plt.subplots()
        ax3.scatter(df['inflacion_inpc'], df['tipo_cambio'])
        pred_line3 = model_tc_inf.predict(sm.add_constant(df[['inflacion_inpc']]))
        ax3.plot(df['inflacion_inpc'], pred_line3)
        ax3.set_xlabel('inflacion_inpc')
        ax3.set_ylabel('tipo_cambio')
        ax3.set_title('tipo_cambio ~ inflacion_inpc')
        st.pyplot(fig3)

if __name__ == "__main__":
    main()
