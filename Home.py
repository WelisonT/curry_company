import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='🎲'
)

# image_path = 'C:/Users/Welison/Documents/repos/ftc_fast_track_courses/datasets/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width = 120 )


st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '### Fastest Delivery in Town' )
st.sidebar.markdown( """___""")

st.write( '# Curry Company Growth Dashboard' )

st.markdown(
    """
    Growth Dashboard foi contruído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como Utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento  
        - Visão Tática: Indicadores semanais de crescimento 
        - Visão Geográfica: Insights de geolocalização 
    - Visão Entregadores:
        - Acompanhamento dos indicadores semanais de crescimento 
    - Visão Restaurantes:
        - Indicadores semanais de crescimentos dos restaurantes
    ### Ask for Help
        - Time Data Science no Discord 
            -@Welison_Tavares
            
    """)