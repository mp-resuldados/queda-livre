import datetime

import altair as alt
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

for k, v in st.session_state.items():
    st.session_state[k] = v

if "N" not in st.session_state:
    st.session_state["N"] = 120

N = st.sidebar.number_input("N", min_value=1, max_value=int(1e4), key="N")


@st.cache_data
def create_random_sample(avg=55.4, std=10, n_total=int(1e4), seed=None):
    rng = np.random.default_rng(seed=seed)

    values = rng.normal(avg, std, n_total).round()

    time_values = pd.DataFrame()
    time_values["i"] = range(1, n_total + 1)
    time_values["t"] = values
    time_values["avg_time"] = time_values["t"].expanding().mean()
    time_values["std"] = time_values["t"].expanding().std()
    time_values["stderr"] = time_values["std"] / np.sqrt(time_values["i"])

    return time_values


if "time_values" not in st.session_state:
    time_values = create_random_sample()

    st.session_state["time_values"] = time_values

else:
    time_values = st.session_state["time_values"]

chart = alt.Chart(time_values.iloc[:N])

########################################################################################
cols = st.columns(2)
with cols[0]:
    st.header("resultados dos lançamentos")

########################################################################################
with cols[1]:
    st.header("histograma")
    n_bins = st.number_input("largura do agrupamento", value=6, min_value=1)

cols = st.columns(2)
with cols[0]:
    resultados = (
        chart.mark_line()
        .encode(
            x="i",
            y="t",
        )
        .interactive()
    )
    theoretical_avg_value = chart.mark_rule(color="red", strokeDash=[5, 5]).encode(
        y=alt.datum(55.4)
    )
    st.altair_chart(resultados + theoretical_avg_value)
with cols[1]:
    hist = (
        chart.mark_bar()
        .encode(alt.X("t", bin=alt.BinParams(step=n_bins)), y="count()")
        .interactive()
    )
    st.altair_chart(hist)

########################################################################################
cols = st.columns(2)

with cols[0]:
    st.header("média")
    avg_values = chart.mark_line().encode(x="i", y="avg_time").interactive()
    st.altair_chart(avg_values + theoretical_avg_value)

with cols[1]:
    st.header("desvio padrão")
    std = chart.mark_line().encode(x="i", y="std").interactive()
    theoretical_std_value = chart.mark_rule(color="red", strokeDash=[5, 5]).encode(
        y=alt.datum(10)
    )
    st.altair_chart(std + theoretical_std_value)

########################################################################################
st.header("incerteza do valor médio")
stderr = chart.mark_line().encode(x="i", y="stderr").interactive()
instr_resolution = chart.mark_rule(color="red", strokeDash=[5, 5]).encode(
    y=alt.datum(1)
)
st.altair_chart(stderr + instr_resolution)
