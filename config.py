"""App-wide constants and configuration."""

import streamlit as st

# Sensitive values come from .streamlit/secrets.toml
API_BASE_URL       = st.secrets["api"]["base_url"]
API_ENDPOINT       = st.secrets["api"]["endpoint"]
API_LOGIN_ENDPOINT = st.secrets["api"]["login_endpoint"]

PAGE_CONFIG = {
    "page_title": "Q-Mind Dashboard",
    "page_icon": "img/iso-light.svg",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

SESSION_DEFAULTS = {
    "temp_slider": 298,  "temp_input": 298,   # operating_temperature (K)
    "pop_slider":  100,  "pop_input":  100,   # population_size
    "iter_slider":  50,  "iter_input":  50,   # max_iterations
}

AVAILABLE_MATERIALS = ["InSb", "GaAs", "CdS", "ZnO", "CdSe", "InP", "PbS"]

USER_EMAIL    = st.secrets["credentials"]["email"]
USER_PASSWORD = st.secrets["credentials"]["password"]