"""
Módulo para generación de eventos usando Proceso de Poisson
"""
import numpy as np


def generar_eventos_poisson(lambda_rate: float, time_step: int = 1) -> int:
    """
    Genera el número de eventos (likes) en un intervalo de tiempo usando distribución de Poisson.
    
    Args:
        lambda_rate: Tasa promedio de llegada de eventos por unidad de tiempo
        time_step: Duración del intervalo de tiempo (default=1)
    
    Returns:
        Número entero de eventos generados en el intervalo
    """
    if lambda_rate < 0:
        lambda_rate = 0
    
    # Generar eventos según distribución de Poisson
    eventos = np.random.poisson(lam=lambda_rate * time_step)
    return int(eventos)


def calcular_multiplicador_estado(estado: int) -> float:
    """
    Calcula el multiplicador de lambda según el estado actual de Markov.
    
    Args:
        estado: Estado actual (0=Latente, 1=Viral, 2=Decadente)
    
    Returns:
        Multiplicador a aplicar sobre lambda base
    """
    multiplicadores = {
        0: 1.0,   # Estado Latente - Tasa normal
        1: 10.0,  # Estado Viral - Explosión de likes
        2: 0.5    # Estado Decadente - Caída de interés
    }
    return multiplicadores.get(estado, 1.0)
