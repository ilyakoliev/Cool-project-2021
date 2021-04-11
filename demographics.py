import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
from regions import regions_ru


translation = {'Урбанизация':['urbanization', 'урбанизации', "% городского населения"],
           'Рождаемость':['birth_rate', 'рождаемости', 'Рождений на 1000 человек'],
           'Смертность':['death_rate', 'смертности', 'Смертей на 1000 человек'],
               'Естественный прирост населения':['npg', 'естественного прироста', 'Естественный прирост на 1000 человек']}

# streamlit run demo_app.py
with st.echo(code_location='below'):
    st.title("Демография")
    """
    Визуализация демографических данных с 1990 до 2017 года в России.
    Источник данных можно найти [тут](https://www.kaggle.com/dwdkills/russian-demography). Давайте на них посмотрим:
    """
    df = pd.read_csv('russian_demography.csv')
    df
    """ 
    ### **Как изменялся средний уровень любой из характеристик по России за весь период?**
    """
    desired_x = st.selectbox('Выберите характеристику:',
                             ['Урбанизация', 'Рождаемость', 'Смертность', 'Естественный прирост населения'])
    """
    """
    fig = plt.figure(figsize = (10, 6))
    fig.set_facecolor('linen')
    plt.ylabel(translation[desired_x][2])
    plt.plot(df.groupby('year')[translation[desired_x][0]].mean())
    plt.title(f"Средний уровень {translation[desired_x][1]} в России")
    st.pyplot(fig)
    """ 
    ### **Сравнение регионов**
    """
    desired_3 = st.multiselect('Выберите регионы, которые хотите сравнить:', list(regions_ru.keys()), default=[list(regions_ru.keys())[33],
                               list(regions_ru.keys())[84], list(regions_ru.keys())[54]])
    if len(desired_3) >= 1:
        reg = []
        for i in desired_3:
            reg.append(regions_ru[i])
        def fun1(r, x):
            df_reg = df[(df['region'] == r) & (df['year'] >= 2012)]
            return round(df_reg[x].mean(), 2)
        """
        В таблице представлены средние значения за 2012-2017.
        """
        a = f"""
        |Регион| Урбанизация        |  Смертность          | Рождаемость  | Естественный прирост |
        | ------------- | :-------------: |:-------------:| :-----:|:-----:|
        | {desired_3[0]} | {fun1(reg[0], 'urbanization')}%    | {fun1(reg[0], 'death_rate')} | {fun1(reg[0], 'birth_rate')} | {fun1(reg[0], 'npg')} |
        """
        for i in range(1, len(desired_3)):
            a = a + f"""| {desired_3[i]} | {fun1(reg[i], 'urbanization')}%    | {fun1(reg[i], 'death_rate')} | {fun1(reg[i], 'birth_rate')} | {fun1(reg[i], 'npg')}|
            """
        a
        """
        """
        desired_x2 = st.selectbox('Характеристика:',
                                 ['Урбанизация', 'Рождаемость', 'Смертность', 'Естественный прирост населения'], index=2)

        df1 = df.loc[df['region'].isin(reg)]

        fig = px.line(df1, x="year", y=translation[desired_x2][0], color='region')
        st.plotly_chart(fig)
    else:
        """
        **Выберите хотя бы один регион**
        """
    """
    
    ### **Посмотрим как изменялся "ящик с усами"**
    """
    need_year = st.slider('Выберите год:', min_value=1990, max_value=2017)

    df1 = df[df['year'] == need_year]
    df1 = df1.drop(['year', 'region', 'urbanization', 'gdw', 'npg'], axis=1)

    fig = plt.figure()
    ax = sns.boxplot(data=df1, orient="h", palette="Set1")
    st.pyplot(fig)
    """
    ## **Что мы имеем на 2017 год**
    """
    ans = st.radio('Выберите:', ['Смертность', 'Рождаемость', 'Естественный прирост'])
    df3 = df[df['year'] == 2017]
    df3 = df3.sort_values('death_rate', ascending=False)
    source = df3
    fig1 = alt.Chart(source).mark_bar(opacity=1, height=7, color='darkmagenta').encode(
        x='death_rate:Q',
        y=alt.Y('region:N', sort='-x', title='Регионы')
    ).properties(
        width=700,
        height=900,
    )
    fig2 = alt.Chart(source).mark_bar(opacity=1, height=7, color='blue').encode(
        x='birth_rate:Q',
        y=alt.Y('region:N', sort='-x', title='Регионы')
    ).properties(
        width=700,
        height=900,
    )
    # color='green'
    fig3 = alt.Chart(source).mark_bar(opacity=1, height=7).encode(
        x='npg:Q',
        y=alt.Y('region:N', sort='-x', title='Регионы'),
        color = alt.condition(
            alt.datum.npg > 0,
            alt.value("darkgreen"),  # The positive color
            alt.value("crimson")
        )
    ).properties(
        width=700,
        height=900,
    )
    if ans == 'Смертность':
        st.altair_chart(fig1)
    elif ans == 'Рождаемость':
        st.altair_chart(fig2)
    elif ans == 'Естественный прирост':
        st.altair_chart(fig3)
    balloons = st.button('👍')
    if balloons:
        st.balloons()
