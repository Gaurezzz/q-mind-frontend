import streamlit as st

st.logo(image="img/logo-horizontal-light.svg", size="large", icon_image="img/iso-light.svg")

#TODO: Connect materials
materials = ["Material 1", "Material 2", "Material 3"]

with st.sidebar:

    st.subheader("Physics Parameters")

    materials_selection = st.multiselect("Select Material", materials)

    st.write("Temperature (K)")
    col1, col2 = st.columns([2, 1])
    with col1:
        tempSlider = st.slider("Temperature (K)", min_value=-300, max_value=300, value=0, label_visibility="collapsed")
    with col2:
        tempInput = st.number_input("Temperature (K)", min_value=-300, max_value=300, value=0, label_visibility="collapsed")

    st.subheader("AI parameters")

    st.write("Population Size")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        popSizeSlider = st.slider("Population Size", min_value=0, max_value=10000, value=100, step=100, label_visibility="collapsed")
    with col2:
        popSizeInput = st.number_input("Population Size", min_value=0, max_value=10000, value=100, step=100, label_visibility="collapsed")

    st.write("Generations")
    col1, col2 = st.columns([2, 1])
    with col1:
        genSlider = st.slider("Generations", min_value=0, max_value=1000, value=100, step=10, label_visibility="collapsed")
    with col2:
        genInput = st.number_input("Generations", min_value=0, max_value=1000, value=100, step=10, label_visibility="collapsed")
    st.write("Mutation Rate (%)")
    mutInput = st.number_input("Mutation Rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1, label_visibility="collapsed")

    run_study_btn = st.button("Run Study")

