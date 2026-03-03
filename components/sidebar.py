import streamlit as st

from config import SESSION_DEFAULTS


def _init_session_state() -> None:
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _sync(source: str, target: str) -> None:
    st.session_state[target] = st.session_state[source]


def _slider_with_input(
    label: str,
    key_prefix: str,
    min_val: int,
    max_val: int,
    step: int = 1,
) -> None:
    """Render a synchronized slider + number_input pair."""
    st.write(label)
    col_slider, col_input = st.columns([2, 1])
    with col_slider:
        st.slider(
            label,
            min_value=min_val,
            max_value=max_val,
            step=step,
            label_visibility="collapsed",
            key=f"{key_prefix}_slider",
            on_change=lambda: _sync(f"{key_prefix}_slider", f"{key_prefix}_input"),
        )
    with col_input:
        st.number_input(
            label,
            min_value=min_val,
            max_value=max_val,
            step=step,
            label_visibility="collapsed",
            key=f"{key_prefix}_input",
            on_change=lambda: _sync(f"{key_prefix}_input", f"{key_prefix}_slider"),
        )


def render_sidebar(available_materials: list[str]) -> dict:
    """
    Render the sidebar and return a dict that maps 1-to-1 to OptimizationRequest.

    Returns:
        {
            # --- OptimizationRequest fields ---
            "materials"             : list[str],
            "operating_temperature" : float,   (K)
            "population_size"       : int,
            "max_iterations"        : int,
            "crossover_alpha"       : float,
            "mutation_strength"     : float,
            "kappa"                 : float,
            "wavelength_input_csv"  : bool,
            "wavelength_left_bound" : float | None,
            "wavelength_right_bound": float | None,
            "wavelength_step"       : float | None,
            # --- UI control ---
            "run"                   : bool,
        }
    """
    _init_session_state()
    params: dict = {}

    with st.sidebar:

        with st.expander("General Physics Parameters", expanded=True):
            params["materials"] = [str(m) for m in st.multiselect(
                "Select Materials", available_materials
            )]
            _slider_with_input("Operating Temperature (K)", "temp", 0, 500)
            params["operating_temperature"] = float(st.session_state["temp_input"])

        with st.expander("Wavelength Configuration"):
            st.write("Choose between uploading your own data or an auto-generated range.")
            wavelength_mode = st.radio(
                "Wavelength Input Method",
                options=["Upload CSV", "Auto-Generate Range"],
                index=1,
            )
            if wavelength_mode == "Auto-Generate Range":
                params["wavelength_input_csv"] = False
                params["wavelength_left_bound"] = st.number_input(
                    "Wavelength Start (nm)", min_value=280.0, max_value=2499.9,
                    value=280.0, step=1.0,
                )
                params["wavelength_right_bound"] = st.number_input(
                    "Wavelength End (nm)", min_value=280.1, max_value=2500.0,
                    value=1300.0, step=1.0,
                )
                params["wavelength_step"] = st.number_input(
                    "Wavelength Step (nm)", min_value=0.01, max_value=15.0,
                    value=10.0, step=0.1,
                )
            else:
                params["wavelength_input_csv"] = True
                params["wavelength_left_bound"] = None
                params["wavelength_right_bound"] = None
                params["wavelength_step"] = None
                st.file_uploader(
                    "Upload Wavelength CSV", type=["csv"],
                    key="wavelength_csv", label_visibility="collapsed",
                )

        with st.expander("AI Optimization Parameters"):
            _slider_with_input("Population Size", "pop", 2, 1000, step=10)
            params["population_size"] = st.session_state["pop_input"]

            _slider_with_input("Max Iterations", "iter", 2, 500, step=10)
            params["max_iterations"] = st.session_state["iter_input"]

            st.write("Crossover Alpha")
            params["crossover_alpha"] = st.number_input(
                "Crossover Alpha", min_value=0.0, max_value=1.0,
                value=0.5, step=0.01, label_visibility="collapsed",
            )

            st.write("Mutation Strength")
            params["mutation_strength"] = st.number_input(
                "Mutation Strength", min_value=0.0, max_value=1.0,
                value=0.1, step=0.01, label_visibility="collapsed",
            )

            st.write("Kappa (Current Mismatch Index weight)")
            params["kappa"] = st.number_input(
                "Kappa", min_value=0.0, max_value=1.0,
                value=0.5, step=0.01, label_visibility="collapsed",
            )

        params["run"] = st.button("Run Study", use_container_width=True)

    return params
