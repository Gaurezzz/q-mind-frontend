import streamlit as st

from components.charts import render_absorption_chart, render_convergence_charts
from components.metrics import render_materials_table, render_metrics
from components.sidebar import render_sidebar
from config import AVAILABLE_MATERIALS, PAGE_CONFIG
from services.api_client import run_study

st.session_state.setdefault("dev_token", "xxx")
st.set_page_config(**PAGE_CONFIG)
st.logo(image="img/logo-horizontal-light.svg", size="large", icon_image="img/iso-light.svg")

params = render_sidebar(available_materials=AVAILABLE_MATERIALS)

if params["run"]:
    if not params["materials"]:
        st.sidebar.error("Please select at least one material.")
    else:
        with st.spinner("Running optimization study..."):
            try:
                st.session_state["last_result"] = run_study(params)
            except Exception:
                st.error("Oops! Something crashed on the server, try later!")


result = st.session_state.get("last_result")

st.write("## Optimization Results")

if result is None:
    st.info("Configure the parameters in the sidebar and click **Run Study** to start.")
else:
    render_metrics(result)

    col_table, col_chart = st.columns([3, 5])
    with col_table:
        render_materials_table(result)
    with col_chart:
        render_absorption_chart(result)

    st.write("### AI Optimization Details")
    st.write(f"Generations to convergence: {result['generations_to_convergence']}")
    render_convergence_charts(result)