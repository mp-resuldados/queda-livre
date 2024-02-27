import datetime
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from random import seed
from random import gauss
import streamlit as st

st.set_page_config(layout="wide")

if 'clicked' not in st.session_state:
    st.session_state.clicked = {0: True, 1: False, 2: False, 3: False}

if 'timestamp' not in st.session_state:
    timestamp = datetime.datetime.now().timestamp()
    st.session_state.timestamp = timestamp
else:
    timestamp = st.session_state.timestamp
    
seed(timestamp)
    
def clicked(botao):
    for bot in [0, 1, 2, 3]:
        st.session_state.clicked[bot] = False
    st.session_state.clicked[botao] = True

#############################################################
# PARÂMETROS DE ENTRADA

cols = st.columns([1, 2])

with cols[0]:
    st.subheader('MP-resuldados', divider=True)
    st.caption('Tempo de queda livre de um objeto')

    h = st.number_input('altura do lançamento metros',
                  value = 1.5,
                  min_value = 1.,
                  max_value = 100.,
                  step=0.1,
                  )    

    N_medidas = st.number_input('número de lançamentos',
                  value = 100,
                  min_value = 1,
                  max_value = 10000
                  )
    
    desvio_padrao = st.number_input('desvio padrão do conjunto do de medidas',
                  value = 0.1,
                  min_value = 0.01,
                  max_value = 10.,
                  step=0.01,
                  )


    info = st.empty()

    botao_dados = st.button('dados', on_click=clicked, args=[0])
    botao_medias = st.button('valores médios', on_click=clicked, args=[1])
    botao_hist = st.button('histogramas', on_click=clicked, args=[2])
    botao_crono = st.button('resolução do cronômetro', on_click=clicked, args=[3])

#############################################################

# simulação das medidas

def medidas(N_conj, N_medidas, h, desvio_padrao):
    t = (2*h/9.787899) **(0.5)
        
    medidas = pd.Series([gauss(t,desvio_padrao) for i in range(N_medidas)])
        
    estatistica = pd.DataFrame(columns=['media', 'desvio', 'incerteza'])
    for i in range(1, N_conj+1):
        medidas_frac = medidas.iloc[:int(i*N_medidas/N_conj)]
        estatistica_frac = pd.DataFrame({
            'media':[medidas_frac.mean()],
            'desvio':[medidas_frac.std()],
            'incerteza':[medidas_frac.std()/(medidas_frac.size)**0.5],
        })
        estatistica = pd.concat([estatistica, estatistica_frac])
    
    return medidas, estatistica.reset_index()

# Assign o conjunto

m1, e1 = medidas(10, N_medidas, h, desvio_padrao)

with cols[1]:
    
# Dados

    if st.session_state.clicked[0]:
        fig, ax = plt.subplots()
        
        m1.plot(
            ax=ax,
            color='orange',
            marker='o',
            ls=':',
        )
        
        t = (2*h/9.787899) **(0.5)
        
        ax.axhline(
            t,
            color='blue',
            ls='--',
            label='valor de referência',
        )
        ax.set_title('Conjunto de dados')
        #ax.set_xlabel('dados')
        ax.set_ylabel('tempo de queda (s)')
        ax.legend(ncols=1)
    
        ax.text(
            0.5,
            0.5,
            "MP-resuldados",
            transform=ax.transAxes,
            fontsize=40,
            color="gray",
            alpha=0.1,
            ha="center",
            va="center",
            rotation=45,
            )
    
        
        st.pyplot(fig)
        

# Médias
    if st.session_state.clicked[1]:
    
        fig, ax = plt.subplots()

        t = (2*h/9.787899) **(0.5)

        # valor de referência
        ax.axhline(t,
        color='blue',
        linestyle='dashed',
        label='valor de referência'
        )
            
        # média e incerteza
        ax.errorbar(
            10*(1+e1.index),
            e1['media'],
            yerr = e1['incerteza'],
            color='orange',
            marker='.',
            linestyle='none',
            label='valores médios'
        )
    
        ax.set_title('Evolução do valor médio')
        ax.set_xlabel('% dos dados')
        ax.set_ylabel('tempo de queda (s)')
        ax.legend(ncols=1)
    
        ax.text(
            0.5,
            0.5,
            "MP-resuldados",
            transform=ax.transAxes,
            fontsize=40,
            color="gray",
            alpha=0.1,
            ha="center",
            va="center",
            rotation=45,
            )
    
        st.pyplot(fig)
    
#############################################################

# Histograma

    if st.session_state.clicked[2]:
    
        fig, axs_arr = plt.subplots(2, 2, sharex=True, sharey=True)

        axs = [ax for axs in axs_arr for ax in axs]
        fracs = [.25, .50, .75, 1]
        colors = ['orange', 'r', 'g', 'b']

        for ax, frac, color in zip(axs, fracs, colors):
    
            a = m1[:int(frac*N_medidas)]
    
            sns.histplot(a, alpha=0.4, ax=ax, label=f'{int(100*frac)}%', color=color)

            ax.set_xlabel('tempo de queda (s)')
            ax.set_ylabel('contagem')
            ax.legend(loc='upper right')
    
        fig.text(
            0.5,
            0.5,
            "MP-resuldados",
            fontsize=50,
            color="gray",
            alpha=0.1,
            ha="center",
            va="center",
            rotation=45,
    )
    
        st.pyplot(fig)
        
        
            
#############################################################

# Comparação do desvio padrão com a resolução do cronômetro

    if st.session_state.clicked[3]:

        fig, ax = plt.subplots()

        # resolução do cronômetro
        ax.axhline(0.01,
            color='green',
            linestyle='dotted',
            label='resolução do cronômetro'
            )

        # desvio para diversos conjuntos com quantidade de medidas diferentes
        ax.plot(
            10*(1+e1.index),
            e1['incerteza'],
            color='orange',
            marker='o',
            linestyle='none',
            label='Incerteza do valor médio'
            )


        ax.set_title('Evolução da incerteza do valor médio')
        ax.set_xlabel('% dos dados')
        ax.set_ylabel('tempo de queda (s)')
        ax.legend(ncols=1)
    
        ax.text(
            0.5,
            0.5,
            "MP-resuldados",
            transform=ax.transAxes,
            fontsize=40,
            color="gray",
            alpha=0.1,
            ha="center",
            va="center",
            rotation=45,
            )
    
        st.pyplot(fig)