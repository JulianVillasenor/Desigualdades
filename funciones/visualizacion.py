"""Visualizaciones del proyecto de desigualdades."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def graficar_comparacion(tabla: pd.DataFrame, titulo: str):
    """Grafica la probabilidad exacta y las versiones informativas de las cotas."""
    fig, ax = plt.subplots(figsize=(9, 5))
    estilos = {
        "exacta": ("o-", "Probabilidad exacta"),
        "Markov_info": ("s--", "Markov"),
        "Chebyshev_info": ("^--", "Chebyshev"),
        "Chernoff_info": ("D--", "Chernoff"),
    }
    for columna, (estilo, etiqueta) in estilos.items():
        ax.plot(tabla["umbral"], tabla[columna], estilo, label=etiqueta)
    ax.set(title=titulo, xlabel="Umbral", ylabel="Probabilidad / cota")
    ax.set_yscale("log")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig, ax
