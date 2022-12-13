#Bibliotecas 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine
import streamlit as st 
from PIL import Image
from streamlit_folium import folium_static
import numpy as np

st.set_page_config(page_title='Home', page_icon='🍽', layout= 'wide')

# df = pd.read_csv(r'C:\Users\Welison\Documents\repos\ftc_fast_track_courses\datasets\train.csv')

#==================================================================
# Funções
#==================================================================
def avg_std_time_on_traffic(df1):
    df_tempo = df1.loc[:,['Time_taken(min)', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)':['mean', 'std']})

    df_tempo.columns = ['Time_mean', 'Time_std']

    df_tempo = df_tempo.reset_index()
            
    fig = px.sunburst(df_tempo, path = ['City', 'Road_traffic_density'], values = 'Time_mean', color = 'Time_std', color_continuous_scale = 'RdBu', color_continuous_midpoint = np.average(df_tempo['Time_std']))
    return fig



def avg_std_time_graph( df1 ):            
    df_tempo = df1.loc[:,['Time_taken(min)', 'City']].groupby('City').agg({'Time_taken(min)':['mean', 'std']})

    df_tempo.columns = ['Time_mean', 'Time_std']

    df_tempo = df_tempo.reset_index()
            
    fig = go.Figure()
    fig.add_trace( go.Bar( name = 'Control', x= df_tempo['City'], y= df_tempo['Time_mean'], error_y = dict ( type='data', array= df_tempo['Time_std'])))
            
    fig.update_layout(barmode= 'group')
    return fig


def avg_std_time_delivery( df1, Festival, op ):              
    """
    Essa função de calcula o tempo médio e desvio padrão do tempo de entrega:
    Parêmntros:
            Input:
                1. df - DataFrame com os dados necessario para realizar o calculo
                2. op - Tipo de operação que pode ser calculado:
                    Time_mean - Calcula o tempo médio 
                    Time_std - calcula o desvio padrão do tempo 
            Output:
                1. df - DataFrame com duas colunas e uma linha
                
    """
    df_tempo = (df1.loc[:,['Time_taken(min)', 'Festival']]
                    .groupby('Festival')
                    .agg({'Time_taken(min)':['mean', 'std']}))
            
    df_tempo.columns = ['Time_mean', 'Time_std']
    df_tempo = df_tempo.reset_index()
    df_tempo = np.round(df_tempo.loc[df_tempo['Festival'] == Festival, op ], 2 )
    return df_tempo


def distance( df1, fig ):
    if fig == False:
        colunas = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

        df1['distance'] = df1.loc[:, colunas].apply( lambda x:
                                 haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)

        avg_distance = np.round( df1['distance'].mean(), 2 )
        return avg_distance
    
    else:
        colunas = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['distance'] = df1.loc[:, colunas].apply( lambda x:
                                 haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)

        avg_distance = df1.loc[:, ['City','distance']].groupby('City').mean().reset_index()
        fig = go.Figure( data = [ go.Pie( labels= avg_distance['City'], values = avg_distance['distance'], pull = [0, 0.1, 0])])
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
df = pd.read_csv(r'datasets\train.csv')

#Limpeza Dataframe

df1 = clean_code( df )

#==================================================================
# Barra Lateral
#==================================================================

st.header('Marketplace - Visão Restaurantes')

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

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial','-','-'] )

with tab1:
    with st.container():
        st.title('Overall Metric')
        
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            delivery_unique = df1['Delivery_person_ID'].nunique()
            col1.metric( 'Entregadores:', delivery_unique )
            
        with col2:
            
            avg_distance = distance( df1, fig = False )
            col2.metric( 'Distância média', avg_distance )
          
        with col3:
            df_tempo = avg_std_time_delivery( df1, 'Yes', 'Time_mean' )
            col3.metric( 'Tempo médio Entregas:', df_tempo  )
                   
        with col4:
            df_tempo = avg_std_time_delivery( df1, 'Yes', 'Time_std' )
            col4.metric( 'STD tempo Entregas:', df_tempo  )
            
        with col5:
            df_tempo = avg_std_time_delivery( df1, 'No', 'Time_mean' )
            col5.metric( 'Tempo médio sem festival:', df_tempo  )
            
        with col6:
            df_tempo = avg_std_time_delivery( df1, 'No', 'Time_std' )
            col6.metric( 'STD tempo sem Festival:', df_tempo  )

            
    with st.container():
        st.markdown( """___""" )
        
        col1, col2 = st.columns( 2 )
        
        with col1:   
            fig = avg_std_time_graph( df1 )
            st.plotly_chart( fig, use_container_width = True )
                              
                
        with col2:
            df_tempo = df1.loc[:,['Time_taken(min)', 'City', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)':['mean', 'std']})
            df_tempo.columns = ['Time_mean', 'Time_std']
            df_tempo = df_tempo.reset_index()
            
            st.dataframe( df_tempo, use_container_width = True )
    
    with st.container():
        st.markdown( """___""" )
        st.title( 'Distribuição de Tempo' )
        
        col1, col2 = st.columns( 2 )
        
        with col1:
            fig = distance( df1, fig = True )
            st.plotly_chart( fig, use_container_width = True)
                     
        with col2:
            fig = avg_std_time_on_traffic( df1 )
            st.plotly_chart ( fig, use_container_width = True)
            
            
                
        