"""Results metrics and materials table components."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from services.api_client import OptimizationResponse


def render_metrics(result: OptimizationResponse) -> None:
    """
    Render the four top-level KPI metric cards.

    Uses:
        result["projected_pce"]
        result["current_mismatch_index"]
        result["computation_time_ms"]
        result["generations_to_convergence"]
    """
    col_pce, col_cmi, col_rt, col_gen = st.columns(4)
    col_pce.metric("Projected PCE", value=f"{result['projected_pce'] * 100:.2f}%", border=True)
    col_cmi.metric("Current Mismatch Index", value=f"{result['current_mismatch_index']:.4f}", border=True)
    col_rt.metric("Computation Time", value=f"{result['computation_time_ms']:.1f} ms", border=True)
    col_gen.metric("Generations to Convergence", value=str(result["generations_to_convergence"]), border=True)


def render_materials_table(result: OptimizationResponse) -> None:
    """
    Render the optimized materials summary table.

    Uses:
        result["materials"]
        result["optimal_radii_nm"]
        result["bandgaps_eV"]
        result["photon_harvesting_efficiency"]
    """
    df = pd.DataFrame({
        "Material": result["materials"],
        "Radius (nm)": result["optimal_radii_nm"],
        "$E_{g}$ (eV)": result["bandgaps_eV"],
        "PHE": result["photon_harvesting_efficiency"],
    })
    st.table(df.set_index("Material"))
