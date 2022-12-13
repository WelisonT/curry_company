#Bibliotecas 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine
import streamlit as st 
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Home', page_icon='🚚', layout= 'wide')

# df = pd.read_csv(r'C:\Users\Welison\Documents\repos\ftc_fast_track_courses\datasets\train.csv')

#==================================================================
# Funções
#==================================================================

def top_delivery(df1, top_asc):
    df2 = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
               .groupby(['City', 'Delivery_person_ID'])
               .min()
               .sort_values( ['City', 'Time_taken(min)'], ascending=top_asc ).reset_index() )

    top10_01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    top10_02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    top10_03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    
    df3 = pd.concat( [top10_01, top10_02, top10_03] ).reset_index(drop=True)
    return df3

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

st.header('Marketplace - Visão Entregadores')

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

# Primeira Criar a Abas
tab1, tab2 , tab3 = st.tabs( ['Visão Gerencial', '-', '-'] )

with tab1:
    with st.container():
        st.title( 'Overall Metric' )
        col1, col2, col3, col4 = st.columns( 4, gap = 'large' )
        with col1:
            maior_idade = df1.loc[:,'Delivery_person_Age'].max()
            col1.metric( 'Maior idadde é:', maior_idade )
        
        with col2:
            menor_idade = df1.loc[:,'Delivery_person_Age'].min()
            col2.metric( 'Menor idade é:', menor_idade )
            
        with col3:
            melhor_condicao = df1.loc[:,'Vehicle_condition'].max()
            col3.metric( 'Melhor condição é:', melhor_condicao )
            
        with col4:
            pior_condicao = df1.loc[:,'Vehicle_condition'].min()
            col4.metric( 'Pior condição é:', pior_condicao )
    
    with st.container():
        st.markdown( """___""" )
        st.title ( 'Avaliações' )
        
        col1, col2 = st.columns ( 2 )
        
        with col1:
            st.markdown( '##### Avalição média por entregador ' )
            avaliacao_media_entreg = ( df1.loc[:,['Delivery_person_Ratings', 'Delivery_person_ID']]
                                        .groupby('Delivery_person_ID')
                                        .mean()
                                        .reset_index() )
            st.dataframe( avaliacao_media_entreg )
            
        with col2:
            st.markdown( '##### Avalição média por trânsito' )
            avaliacao_media_trans = df_media_e_devio = ( df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']]
                                                          .groupby('Road_traffic_density')
                                                          .agg({'Delivery_person_Ratings': ['mean', 'std']} ) )

        
            avaliacao_media_trans = df_media_e_devio.columns = ['Delivery_mean', 'Delivery_std']


            avaliacao_media_trans = df_media_e_devio.reset_index()
            st.dataframe( avaliacao_media_trans )
            
            
            
            st.markdown( '##### Avalição media por clima' )
            avaliacao_media_clima = df_media_e_devio = ( df1.loc[:,['Delivery_person_Ratings', 'Weatherconditions']]
                                                          .groupby('Weatherconditions')
                                                          .agg({'Delivery_person_Ratings': ['mean', 'std']} ) )

            avaliacao_media_clima = df_media_e_devio.columns = ['Conditions_mean', 'Conditions_std']

            avaliacao_media_clima = df_media_e_devio.reset_index()
            st.dataframe( avaliacao_media_clima )
            
    with st.container():
        st.markdown( """___""" )
        st.title( 'Velocidade de Entrega' )
        
        col1, col2 = st.columns ( 2 )
        
        
        with col1:
            st.markdown( '##### Top Entregadores mais rapidos' )
            df3 = top_delivery( df1, top_asc = True )
            st.dataframe ( df3 )
            
        with col2:
            st.markdown( '##### Top Entregadores mais lentos' )
            df3 = top_delivery( df1, top_asc = False )
            st.dataframe( df3 )
            
             
            
        
            