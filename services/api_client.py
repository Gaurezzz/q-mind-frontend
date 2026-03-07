from __future__ import annotations

import requests

from config import API_BASE_URL, API_ENDPOINT, API_LOGIN_ENDPOINT, USER_EMAIL, USER_PASSWORD
import streamlit as st


OptimizationRequest = dict
"""
Keys (all required by the backend):
    materials              : list[str]
    operating_temperature  : float       (K, default 298.15)
    population_size        : int         (default 100)
    max_iterations         : int         (default 50)
    crossover_alpha        : float       (0–1, default 0.5)
    mutation_strength      : float       (0–1, default 0.1)
    kappa                  : float       (0–1, default 0.5)
    wavelength_input_csv   : bool        (False = use range bounds)
    wavelength_left_bound  : float|None  (nm)
    wavelength_right_bound : float|None  (nm)
    wavelength_step        : float|None  (nm)
"""

OptimizationResponse = dict
"""
Keys returned by the backend:
    status                      : str
    optimal_radii_nm            : list[float]
    projected_pce               : float
    fitness_history             : list[float]
    pce_history                 : list[float]
    avg_fitness_history         : list[float]
    computation_time_ms         : float
    materials                   : list[str]
    bandgaps_eV                 : list[float]
    wavelengths_nm              : list[float]
    absorption_spectrum         : list[list[float]]  # (n_layers, n_wavelengths)
    current_mismatch_index      : float
    photon_harvesting_efficiency: list[float]
    generations_to_convergence  : int
"""


def run_study(params: OptimizationRequest) -> OptimizationResponse:
    """
    POST params to the backend and return an OptimizationResponse.
    Raises requests.RequestException if the backend is unreachable or returns an error.
    """

    payload = {k: v for k, v in params.items() if k != "run"}


    
    response = requests.post(
        f"{API_BASE_URL}{API_ENDPOINT}",
        json=payload,
        headers={"Authorization": f"Bearer {st.session_state['dev_token']}"},
        timeout=300,
    )

    if response.status_code == 401:
        response_login = requests.post(
            f"{API_BASE_URL}{API_LOGIN_ENDPOINT}",
            data={                         
                "username": USER_EMAIL,
                "password": USER_PASSWORD
            },
            timeout=10,
        )
        if response_login.status_code == 200:
            token = response_login.json().get("access_token")
            st.session_state["dev_token"] = token

            response = requests.post(
                f"{API_BASE_URL}{API_ENDPOINT}",
                json=payload,
                headers={"Authorization": f"Bearer {st.session_state['dev_token']}"},
                timeout=60,
            )
        else:
            st.error("Login failed, cannot obtain token.")
    else:
        response.raise_for_status()
    return response.json()
