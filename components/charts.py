"""Plotly chart components — receive the full OptimizationResponse dict."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.api_client import OptimizationResponse


def render_absorption_chart(result: OptimizationResponse) -> None:
    """
    Render absorption coefficient spectra for each optimized layer.

    Uses:
        result["wavelengths_nm"]       — shared x-axis
        result["absorption_spectrum"]  — list[list[float]], one row per layer
        result["materials"]            — layer names
    """
    wavelengths = result["wavelengths_nm"]
    spectra = result["absorption_spectrum"]
    materials = result["materials"]

    fig = go.Figure()
    for i, (spectrum, material) in enumerate(zip(spectra, materials)):
        fig.add_trace(go.Scatter(
            x=wavelengths,
            y=spectrum,
            mode="lines",
            name=f"Layer {i + 1}: {material}",
            fill="tozeroy",
            hovertemplate="Wavelength: %{x} nm<br>Abs: %{y:.2e} cm⁻¹",
        ))

    fig.update_layout(
        xaxis_title="Wavelength (nm)",
        yaxis_title="Absorption Coefficient (cm⁻¹)",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=100, r=0, t=0, b=0),
        showlegend=True,
        height=400,
        legend=dict(
            yanchor="top", y=0.95,
            xanchor="right", x=0.95,
            bgcolor="rgba(255, 255, 255, 0.5)",
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_convergence_charts(result: OptimizationResponse) -> None:
    """
    Render best-fitness and mean-fitness evolution charts side by side.

    Uses:
        result["fitness_history"]       — best individual per generation
        result["avg_fitness_history"]   — mean population fitness per generation
    """
    fitness = result["fitness_history"]
    avg_fitness = result["avg_fitness_history"]
    generations = list(range(1, len(fitness) + 1))

    col_best, col_mean = st.columns(2)

    with col_best:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=generations, y=fitness,
            mode="lines+markers",
            name="Best Fitness",
            line=dict(color="#636EFA", width=2),
            marker=dict(size=4),
        ))
        fig.update_layout(
            title="<b>Fitness Winner Evolution</b>",
            xaxis_title="Generation",
            yaxis_title="Best Fitness Score",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_mean:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=generations, y=avg_fitness,
            mode="lines+markers",
            name="Mean Fitness",
            line=dict(color="#EF553B", width=2),
            marker=dict(size=4),
        ))
        fig.update_layout(
            title="<b>Fitness Mean Evolution</b>",
            xaxis_title="Generation",
            yaxis_title="Mean Fitness Score",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
