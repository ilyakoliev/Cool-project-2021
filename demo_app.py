import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ТАК А Я МОГУ КОМИТНУТЬ ЭТО?
# streamlit run demo_app.py
with st.echo(code_location='below'):
    st.title("Демография и кое-что ещё")
    """
    Визуализация демографических данных с 1990 до 2017 года в России.
    Источник данных можно найти [тут](https://www.kaggle.com/dwdkills/russian-demography). Давайте на них посмотрим:
    """
    df = pd.read_csv('russian_demography.csv')
    df
    """
    Начнем с чего-нибудь простого. 
    
    Посмотрим, как изменялся уровень урбанизации за данный период.
    """
    fig = plt.figure(figsize = (10, 4))
    fig.set_facecolor('linen')
    plt.ylabel("% городского населения")
    plt.plot(df.groupby('year')['urbanization'].mean())
    plt.title("Средний уровень урбанизации")
    st.pyplot(fig)

# wkvlbjasdkvasdvsv








    """
    # Дальше дичь и заметки
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 4), sharey = True)
    fig.set_facecolor('linen')
    ax1.plot(df['year'].unique(), df.groupby('year')['birth_rate'].mean())
    ax2.plot(df['year'].unique(), df.groupby('year')['death_rate'].mean())
    ax1.grid()
    ax2.grid()
    #ax1.set_ylabel('количество рождений')
    #ax2.set_ylabel('количество смертей')
    st.pyplot(fig)
    
    
    
    
    # А вот так обстоят дела с рождаемостью и смертностью (на 1000 человек).
    
    fig = plt.figure()
    ax_1 = fig.add_subplot(2, 2, 3)
    ax_2 = fig.add_subplot(2, 2, 4)

    ax_1.plot(df['year'].unique(), df.groupby('year')['birth_rate'].mean())
    ax_1.set_title('Рождаемость')

    ax_2.plot(df['year'].unique(), df.groupby('year')['death_rate'].mean())
    ax_2.set_title('Смертность')
    st.pyplot(fig)
    """


