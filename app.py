import streamlit as st # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express 


# https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dash Receita Games",
                   page_icon="👾",
                   layout="wide"
                   )

dataframe = pd.read_csv('dados/vgsales.csv')


# ---- SIDEBAR ----
with st.sidebar:
    st.image('img/control.png')
    st.header('Dash Receita Games')

platform = st.sidebar.selectbox(
    'Selecione uma Plataforma:',
    options=['Todos'] + list(dataframe['Platform'].unique())
)


genre = st.sidebar.selectbox(
    'Selecione um Gênero:',
    options=['Todos'] + list(dataframe['Genre'].unique())
)

# df_selection = dataframe.query(
#    'Platform == @platform & Genre == @genre')

# Se a plataforma for 'Todos', use todo o dataframe, caso contrário, filtre pela plataforma
if platform != 'Todos':
    df_selection = dataframe[dataframe['Platform'] == platform]
else:
    df_selection = dataframe

# Se o gênero for 'Todos', mantenha o dataframe atual, caso contrário, filtre pelo gênero
if genre != 'Todos':
    df_selection = df_selection[df_selection['Genre'] == genre]

# ---- TOP KPIs ----
receita_global = df_selection.groupby(
    'Platform')['Global_Sales'].sum().reset_index()

receita_global_media = df_selection.groupby(
    'Platform')['Global_Sales'].mean().reset_index()

total_receita = df_selection['Global_Sales'].sum()
total_receita_formatado = "$ {:.2f}".format(total_receita)

# Agrupar por 'Genre', calcular a soma de 'Global_Sales' para cada grupo, resetar o índice e pegar os 3 maiores
top_3 = df_selection.groupby('Genre')['Global_Sales'].sum(
).reset_index().nlargest(3, 'Global_Sales')


total_receita_global = df_selection['Global_Sales'].sum()
total_receita_formatado = "$ {:.2f}".format(total_receita)

total_receita_europa = df_selection['EU_Sales'].sum()
total_receita_europa_formatado = "$ {:.2f}".format(total_receita_europa)

total_receita_Namibia = df_selection['NA_Sales'].sum()
total_receita_Namibia_formatado = "$ {:.2f}".format(total_receita_Namibia)

total_receita_japones = df_selection['JP_Sales'].sum()
total_receita_japones_formatado = "$ {:.2f}".format(total_receita_japones)

total_receita_other = df_selection['Other_Sales'].sum()
total_receita_other_formatado = "$ {:.2f}".format(total_receita_other)

porc_europa = total_receita_europa / total_receita_global * 100
porc_receita_europa_formatado = "{:.2f}%".format(porc_europa)

porc_namibia = total_receita_Namibia / total_receita_global * 100
porc_receita_Namibia_formatado = "{:.2f}%".format(porc_namibia)

porc_japones = total_receita_japones / total_receita_global * 100
porc_receita_japones_formatado = "{:.2f}%".format(porc_japones)

porc_other = total_receita_other / total_receita_global * 100
porc_receita_other_formatado = "{:.2f}%".format(porc_other)


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    fig1 = st.metric(label='Receita Global',
                     value=total_receita_formatado,
                     )

with col2:
    fig1 = st.metric(label='Receita Europa',
                     value=total_receita_europa_formatado,
                     delta=porc_receita_europa_formatado,
                     # delta_color='off'
                     )

with col3:
    fig1 = st.metric(label='Receita Namíbia',
                     value=total_receita_Namibia_formatado,
                     delta=porc_receita_Namibia_formatado,
                     # delta_color='off'
                     )

with col4:
    fig1 = st.metric(label='Receita Japonesa',
                     value=total_receita_japones_formatado,
                     delta=porc_receita_japones_formatado,
                     # delta_color='off'
                     )

with col5:
    fig1 = st.metric(label='Outros',
                     value=total_receita_other_formatado,
                     delta=porc_receita_other_formatado,
                     # delta_color='off'
                     )

col6, col7 = st.columns(2)

fig2 = px.bar(receita_global,
              x='Platform',
              y='Global_Sales',
              )

color_dict = {'Platform1': 'blue', 'Platform2': 'green', 'Platform3': 'red'}
# Criar um gráfico de pizza com o dataframe 'top_3'
figpx = px.pie(top_3,
               values='Global_Sales',
               names='Genre')


fig2.update_layout(
    xaxis=dict(tickmode='linear'),
    yaxis=(dict(showgrid=False)),
)

figpx.update_layout(
    xaxis=dict(tickmode='linear'),
    yaxis=(dict(showgrid=False)),
)

col6.plotly_chart(figpx, use_container_width=True)
col7.plotly_chart(fig2, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)
