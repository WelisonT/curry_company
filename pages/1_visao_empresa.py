#Bibliotecas 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine
import streamlit as st 
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Home', page_icon='📈', layout= 'wide')

# df = pd.read_csv(r'C:\Users\Welison\Documents\repos\ftc_fast_track_courses\datasets\train.csv')


#==================================================================
# Funções
#==================================================================
def country_maps( df1 ):
    df2 = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()

    map1 = folium.Map( zoom_start = 11 )

    for index, location_info in df2.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']],
                       popup = location_info[['City', 'Road_traffic_density']]).add_to( map1 )
    folium_static( map1, width = 1024, height = 600 )


def order_share_by_week ( df1 ):
    #contando quantas entregas foram feita na semana 
    df2 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()

    #Contando a quanidade de entrega por cada entragador unico na semana 
    df3 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

    #Juntando duas tabelas com variaveis diferente

    df4 = pd.merge(df2, df3, how = 'inner')
    df4['order_by_delivery'] = df4['ID'] / df4['Delivery_person_ID']

    fig = px.line(df4, x = 'week_of_year', y = 'order_by_delivery')
    return fig

def order_by_week ( df1 ):
    #Criando uma coluna tirando o dias da semana de outra coluna 
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )

    #Pegando a quantidade de pedidos por semana 
    df2 = df1.loc[:,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()

    #Plotando no grafico

    fig = px.line(df2, x = 'week_of_year', y = 'ID')
        
    return fig

def traffic_order_city ( df1 ):
    df2 = df1.loc[:, ['ID', 'City', 'Road_traffic_density' ]].groupby(['City', 'Road_traffic_density']).count().reset_index()

    #PLotando grafico de bolhas

    fig = px.scatter( df2, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
            
    return fig


def traffic_order_share ( df1 ):
    df2 = (df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index() )
    #Calculando a porcentagem do ID E coloando numa nova coluna 
    df2['percentual_ID'] = df2['ID'] / df2['ID'].sum()

    # Plotandografico de pizza

    fig =  px.pie(df2, values= 'percentual_ID', names = 'Road_traffic_density')
    return fig


def order_metric ( df1 ):
    df2 = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()

    df2.columns = ['Order_Date', 'qtd_pedidos']

    #Plotando Grafico
    fig = px.bar(df2, x = 'Order_Date', y = 'qtd_pedidos')
    return fig

def clean_code( df1 ):

    """Essa função de tem a responsabilidade de limpar o DataFrame

    Tipos de limepza:
    - remoção dos dados NaN
    - mundança dos tipo da coluna de dados
    - remoção dos espaços das variaveis de texto
    - formatação da coluna de datas
    - lempeza da coluna de tempo (remoção de texto da variavel numerica
     
     input: DataFrame
     output: DataFrame
     
     """
    #1 - Convertendo a coluna Age de texto para numero

    linhas = (df1['Delivery_person_Age'] !='NaN ')
    df1 = df1.loc[linhas, :].copy()

    ## Removendo o NaN da coluna City
    linhas = (df1['City'] !='NaN ')
    df1 = df1.loc[linhas, :].copy()

    ## Removendo o NaN da coluna densidade
    linhas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas, :].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype('int64')

    #2 Convertendo acoluna Ratins de texto para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    #3 Coonvertendo a coluna Order_date de texto para Data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    #4 Convertendo multiple_deliveries de texto para numero inteiro (int)
    linhas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas, :].copy()

    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype('int64')

    #5 Removendo espaço de uma string usando o FOR (Jeito demorado)
    df1 = df1.reset_index( drop=True )

    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # limpando a coluna Time_taken(min)

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min)' )[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype('int64')
    
    return df1
#===================================================== Inicio da Estrutura Lógica do Código =====================================================

#Importando DataFrame
# df = pd.read_csv(r'C:\Users\Welison\Documents\repos\ftc_fast_track_courses\datasets\train.csv')
df = pd.read_csv(r'datasets/train.csv')

#Limpeza Dataframe

df1 = clean_code( df )

#==================================================================
# Barra Lateral
#==================================================================

st.header('Marketplace - Visão Cliente')

# image_path = 'C:/Users/Welison/Documents/repos/ftc_fast_track_courses/datasets/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width = 120 )


st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '### Fastest Delivery in Town' )
st.sidebar.markdown( """___""")

st.sidebar.markdown( '## Selecione uma data limite' )
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime( 2022, 4, 13),
    min_value=pd.datetime (2022, 2, 11 ),
    max_value=pd.datetime ( 2022, 4, 6 ),
    format= 'DD-MM-YYYY' )

st.sidebar.markdown( """___""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trãnsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default = 'Low' )
st.sidebar.markdown( """___""")
st.sidebar.markdown( '### Powered by Comunidade DS' )

# Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider 
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Transito 
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[ linhas_selecionadas, : ] 

#==================================================================
# Layout no Streamlit 
#==================================================================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1:
    with st.container():
        # Order Metric
        fig = order_metric ( df1 )
        st.markdown( '# Orders by Day' )
        st.plotly_chart( fig, use_container_width = True )
        
        
    with st.container():
        col1, col2 = st.columns( 2 )
        with col1:
            fig = traffic_order_share ( df1 )
            st.header( 'Traffic Order Share' )
            st.plotly_chart( fig, use_container_width = True )
            
            
        with col2:
            fig = traffic_order_city ( df1 )
            st.header( 'Traffic Order City' )
            st.plotly_chart( fig, use_container_width = True )
            
            
        
        
with tab2:
    with st.container():
        fig = order_by_week ( df1 )
        st.markdown( '# Order by Week' )
        st.plotly_chart( fig, use_container_width = True )
        
        
        
    with st.container():
        st.markdown( '# Order share by Week' )
        fig = order_share_by_week ( df1 )
        st.plotly_chart( fig, use_container_width = True )
        
        
with tab3:
    st.header( 'Country Maps' )
    country_maps( df1 )
    
    

