"""Cotas de Markov, Chebyshev y Chernoff para el proyecto.

Las funciones de comparacion devuelven tanto la cota teorica como su version
informativa ``min(1, cota)``. Esto evita ocultar cuando una desigualdad produce
un valor mayor que uno.
"""

from __future__ import annotations

import math
from collections.abc import Iterable

import pandas as pd
from scipy.stats import expon, poisson


def _validar_positivo(valor: float, nombre: str) -> None:
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError(f"{nombre} debe ser un numero finito y positivo.")


def cota_markov(esperanza: float, umbral: float) -> float:
    """Devuelve E[X]/a para una variable no negativa y a > 0."""
    _validar_positivo(umbral, "umbral")
    if esperanza < 0 or not math.isfinite(esperanza):
        raise ValueError("esperanza debe ser finita y no negativa.")
    return esperanza / umbral


def cota_chebyshev(esperanza: float, varianza: float, umbral: float) -> float:
    """Cota unilateral obtenida de Chebyshev para a > E[X]."""
    if umbral <= esperanza:
        raise ValueError("umbral debe ser mayor que la esperanza.")
    if varianza < 0 or not math.isfinite(varianza):
        raise ValueError("varianza debe ser finita y no negativa.")
    return varianza / (umbral - esperanza) ** 2


def cota_chernoff_poisson(lam: float, umbral: int) -> float:
    """Cota Chernoff optimizada para P(X >= k), X ~ Poisson(lam), k > lam."""
    _validar_positivo(lam, "lam")
    if int(umbral) != umbral or umbral <= lam:
        raise ValueError("umbral debe ser un entero mayor que lam.")
    k = int(umbral)
    return math.exp(-lam) * (math.e * lam / k) ** k


def cota_chernoff_exponencial(lam: float, umbral: float) -> float:
    """Cota Chernoff optimizada para P(X >= a), X ~ Exp(tasa=lam), a > 1/lam."""
    _validar_positivo(lam, "lam")
    if umbral <= 1 / lam:
        raise ValueError("umbral debe ser mayor que 1/lam.")
    return lam * umbral * math.exp(1 - lam * umbral)


def comparar_poisson(lam: float, umbrales: Iterable[int]) -> pd.DataFrame:
    """Compara cola exacta y cotas para una distribucion Poisson."""
    _validar_positivo(lam, "lam")
    filas = []
    for k in umbrales:
        if int(k) != k or k <= lam:
            raise ValueError("Cada umbral Poisson debe ser un entero mayor que lam.")
        k = int(k)
        markov = cota_markov(lam, k)
        chebyshev = cota_chebyshev(lam, lam, k)
        chernoff = cota_chernoff_poisson(lam, k)
        filas.append(
            {
                "distribucion": f"Poisson(lambda={lam:g})",
                "umbral": k,
                "exacta": poisson.sf(k - 1, mu=lam),
                "Markov": markov,
                "Chebyshev": chebyshev,
                "Chernoff": chernoff,
                "Markov_info": min(1.0, markov),
                "Chebyshev_info": min(1.0, chebyshev),
                "Chernoff_info": min(1.0, chernoff),
            }
        )
    return pd.DataFrame(filas)


def comparar_exponencial(lam: float, umbrales: Iterable[float]) -> pd.DataFrame:
    """Compara cola exacta y cotas para una exponencial con tasa lam."""
    _validar_positivo(lam, "lam")
    media = 1 / lam
    varianza = 1 / lam**2
    filas = []
    for a in umbrales:
        if a <= media:
            raise ValueError("Cada umbral exponencial debe ser mayor que 1/lam.")
        markov = cota_markov(media, a)
        chebyshev = cota_chebyshev(media, varianza, a)
        chernoff = cota_chernoff_exponencial(lam, a)
        filas.append(
            {
                "distribucion": f"Exponencial(lambda={lam:g})",
                "umbral": float(a),
                "exacta": expon.sf(a, scale=1 / lam),
                "Markov": markov,
                "Chebyshev": chebyshev,
                "Chernoff": chernoff,
                "Markov_info": min(1.0, markov),
                "Chebyshev_info": min(1.0, chebyshev),
                "Chernoff_info": min(1.0, chernoff),
            }
        )
    return pd.DataFrame(filas)
