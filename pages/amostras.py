import datetime

import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

from medias import create_random_sample


for k, v in st.session_state.items():
    st.session_state[k] = v

if "n_samples" not in st.session_state:
    st.session_state["n_samples"] = 5

n_samples = st.sidebar.number_input(
    "número de conjuntos amostrais", min_value=1, max_value=100, key="n_samples"
)

if "sample_size" not in st.session_state:
    st.session_state["sample_size"] = 5

sample_size = st.sidebar.number_input(
    "tamanho da amostra",
    value=5,
    min_value=2,
    max_value=100,
    key="sample_size",
)

if "seed" not in st.session_state:
    seed = int(datetime.datetime.now().timestamp())
    st.session_state["seed"] = seed
else:
    seed = st.session_state["seed"]

display_n_rows = ((n_samples - 1) // 5) + 1


sample_df = create_random_sample(n_total=n_samples * sample_size, seed=seed)[["i", "t"]]

sample_sets_list = list()
results_list = list()
for n in range(n_samples):
    sample_set = sample_df.iloc[n * sample_size : (n + 1) * sample_size]
    sample_sets_list.append(sample_set)
    results_list.append(
        [
            n + 1,
            sample_set["t"].mean(),
            sample_set["t"].std(),
            sample_set["t"].std() / np.sqrt(sample_size),
        ]
    )

results_df = pd.DataFrame(results_list, columns=["index", "avg", "std", "stderr"])

sample_sets_list_copy = sample_sets_list.copy()
with st.expander("tabelas de conjuntos amostrais"):
    for row in range(display_n_rows):
        cols = st.columns(5)
        for col in cols:
            with col:
                try:
                    st.dataframe(sample_sets_list_copy.pop(0).set_index("i"))
                except IndexError:
                    break

st.dataframe(results_df.set_index("index").transpose())

chart = alt.Chart(results_df.reset_index())

mean_values = chart.mark_point(filled=True).encode(x="index:N", y="avg").interactive()
error_bars = chart.mark_errorbar(color="blue", ticks=True).encode(
    x="index:N",
    y="avg",
    yError=("stderr"),
)
theoretical_avg_value = chart.mark_rule(color="red", strokeDash=[5, 5]).encode(
    y=alt.datum(55.4)
)

st.altair_chart(mean_values + error_bars + theoretical_avg_value)
