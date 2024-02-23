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

#############################################################
# PARÂMETROS DE ENTRADA

cols = st.columns([1, 2])

with cols[0]:
    st.subheader('MP-resuldados', divider=True)
    st.caption('Tempo de queda livre de um objeto')

    h = st.number_input('altura da queda em metros',
                  value = 1.5,
                  min_value = 1.,
                  max_value = 100.,
                  step=0.1,
                  )
    
    N_conj = st.number_input('número de conjunto de dados',
                  value = 6,
                  min_value = 1,
                  max_value = 1000
                  )
    

    N_medidas = st.number_input('número de quedas em cada conjunto',
                  value = 10,
                  min_value = 1,
                  max_value = 1000
                  )
    
    desvio_padrao = st.number_input('desvio padrão do conjunto do de medidas',
                  value = 0.1,
                  min_value = 0.01,
                  max_value = 10.,
                  step=0.01,
                  )


    info = st.empty()

    botao_medias = st.button('valores médios')
    botao_hist = st.button('histogramas')
    botao_crono = st.button('resolução do cronômetro')

#############################################################

# simulação das medidas

def medidas(N_conj, N_medidas, h, desvio_padrao):
    t = (2*h/9.787899) **(0.5)
    medidas = pd.Series()
    estatistica = pd.DataFrame(columns = ['media', 'desvio', 'incerteza'])

    for i in range(N_conj):
        
        med = pd.Series([gauss(t,desvio_padrao) for i in range(N_medidas)])
        medidas = pd.concat([medidas, med])
        
        est = pd.DataFrame({'media':[medidas.mean()],'desvio':[medidas.std()], 'incerteza':[medidas.std()/((i+1)*N_medidas)**0.5]})
        estatistica = pd.concat([estatistica, est])
    
    return medidas, estatistica.reset_index()

# Assign o conjunto

m1, e1 = medidas(N_conj, N_medidas, h, desvio_padrao)

with cols[1]:
    
# Gráfico

    if botao_medias:
    
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
            e1.index,
            e1['media'],
            yerr = e1['incerteza'],
            color='orange',
            marker='.',
            linestyle='none',
            label='valores médios'
        )
    
        #ax.set_title('')
        ax.set_xlabel('conjuntos de medidas')
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

    if botao_hist:
    
        fig, ax = plt.subplots()
        for a in [m1,
          m1[:int(N_conj*N_medidas/4)],
          m1[:int(N_conj*N_medidas/2)],
          m1[:3*int(N_conj*N_medidas/4)],
          ]:      
            sns.histplot(a, alpha=0.4)
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
            rotation=0,
        )
    
    
        st.pyplot(fig)
        
        
            
#############################################################

# Comparação do desvio padrão com a resolução do cronômetro

    if botao_crono:

        fig, ax = plt.subplots()

        # resolução do cronômetro
        ax.axhline(0.01,
            color='blue',
            linestyle='dashed',
            label='resolução do cronômetro'
            )

        # desvio para diversos conjuntos com quantidade de medidas diferentes
        ax.plot(
            e1.index,
            e1['incerteza'],
            color='orange',
            marker='.',
            linestyle='none',
            label='Incerteza do valor médio'
            )


        #ax.set_title('Incerteza do valor médio')
        ax.set_xlabel('conjuntos de medidas')
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