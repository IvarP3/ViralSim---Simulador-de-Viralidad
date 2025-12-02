"""
Módulo para Cadena de Markov - Transición entre estados
"""
import numpy as np
from typing import List


class CadenaMarkov:
    """
    Representa una Cadena de Markov discreta de tiempo para modelar estados virales.
    """
    
    def __init__(self, matriz_transicion: np.ndarray, estado_inicial: int = 0):
        """
        Inicializa la cadena de Markov.
        
        Args:
            matriz_transicion: Matriz de probabilidades de transición (n x n)
            estado_inicial: Estado en el que comienza la cadena (default=0)
        """
        self.matriz_transicion = np.array(matriz_transicion)
        self.estado_actual = estado_inicial
        self.num_estados = len(matriz_transicion)
        self.historial_estados = [estado_inicial]
        
        # Validar matriz estocástica
        self._validar_matriz()
    
    def _validar_matriz(self) -> None:
        """
        Valida que la matriz de transición sea estocástica (filas suman 1).
        """
        sumas_filas = np.sum(self.matriz_transicion, axis=1)
        if not np.allclose(sumas_filas, 1.0):
            # Normalizar filas para garantizar propiedad estocástica
            self.matriz_transicion = self.matriz_transicion / sumas_filas[:, np.newaxis]
    
    def siguiente_estado(self) -> int:
        """
        Calcula y retorna el siguiente estado según la matriz de transición.
        
        Returns:
            Próximo estado de la cadena
        """
        # Obtener probabilidades de transición desde el estado actual
        probabilidades = self.matriz_transicion[self.estado_actual]
        
        # Seleccionar siguiente estado según distribución de probabilidad
        siguiente = np.random.choice(
            range(self.num_estados),
            p=probabilidades
        )
        
        self.estado_actual = siguiente
        self.historial_estados.append(siguiente)
        
        return siguiente
    
    def obtener_nombres_estados(self) -> List[str]:
        """
        Retorna los nombres descriptivos de los estados.
        
        Returns:
            Lista con nombres de estados
        """
        return ["Latente", "Viral", "Decadente"]
    
    def obtener_color_estado(self, estado: int) -> str:
        """
        Retorna el color hexadecimal asociado a un estado.
        
        Args:
            estado: Número de estado
        
        Returns:
            Color en formato hexadecimal
        """
        colores = {
            0: "#808080",  # Gris para Latente
            1: "#FF6B2B",  # Naranja para Viral
            2: "#2C3E50"   # Azul oscuro para Decadente
        }
        return colores.get(estado, "#808080")
    
    def reiniciar(self, estado_inicial: int = 0) -> None:
        """
        Reinicia la cadena a un estado inicial.
        
        Args:
            estado_inicial: Estado en el que se reinicia la cadena
        """
        self.estado_actual = estado_inicial
        self.historial_estados = [estado_inicial]
