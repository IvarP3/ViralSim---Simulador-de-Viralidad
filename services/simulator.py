"""
Motor de simulación que integra Poisson y Markov
"""
import numpy as np
from typing import List, Dict, Tuple
from core.poisson import generar_eventos_poisson, calcular_multiplicador_estado
from core.markov import CadenaMarkov
from core.network import RedSocial


class SimulationEngine:
    """
    Motor principal que orquesta la simulación de viralidad.
    Integra Cadena de Markov para estados y Proceso de Poisson para eventos.
    """
    
    def __init__(self, matriz_transicion: np.ndarray, lambda_base: float):
        """
        Inicializa el motor de simulación.
        
        Args:
            matriz_transicion: Matriz de probabilidades de transición entre estados
            lambda_base: Tasa base de llegada de likes (parámetro lambda de Poisson)
        """
        self.cadena_markov = CadenaMarkov(matriz_transicion, estado_inicial=0)
        self.red_social = RedSocial(num_nodos=30)
        self.lambda_base = lambda_base
        
        # Contadores y historiales
        self.time_step = 0
        self.historial_likes: List[int] = []
        self.historial_estados: List[int] = [0]
        self.historial_tiempo: List[int] = [0]
        self.likes_acumulados = 0
        
    def step(self) -> Dict[str, any]:
        """
        Ejecuta un paso de la simulación.
        
        Returns:
            Diccionario con los resultados del paso actual
        """
        # 1. Obtener estado actual
        estado_actual = self.cadena_markov.estado_actual
        
        # 2. Calcular multiplicador según estado
        multiplicador = calcular_multiplicador_estado(estado_actual)
        
        # 3. Calcular lambda efectivo
        lambda_efectivo = self.lambda_base * multiplicador
        
        # 4. Generar eventos (likes) usando Poisson
        likes_generados = generar_eventos_poisson(lambda_efectivo)
        self.likes_acumulados += likes_generados
        
        # 5. Transición a siguiente estado usando Markov
        siguiente_estado = self.cadena_markov.siguiente_estado()
        
        # 6. Actualizar red social
        self.red_social.actualizar_estados(siguiente_estado)
        
        # 7. Guardar en historiales
        self.time_step += 1
        self.historial_tiempo.append(self.time_step)
        self.historial_likes.append(likes_generados)
        self.historial_estados.append(siguiente_estado)
        
        # 8. Retornar métricas del paso
        return {
            'time_step': self.time_step,
            'estado_actual': siguiente_estado,
            'likes_generados': likes_generados,
            'likes_acumulados': self.likes_acumulados,
            'lambda_efectivo': lambda_efectivo,
            'multiplicador': multiplicador
        }
    
    def simular_multiple_pasos(self, num_pasos: int) -> None:
        """
        Ejecuta múltiples pasos de simulación.
        
        Args:
            num_pasos: Cantidad de pasos a simular
        """
        for _ in range(num_pasos):
            self.step()
    
    def obtener_metricas_globales(self) -> Dict[str, any]:
        """
        Calcula métricas agregadas de toda la simulación.
        
        Returns:
            Diccionario con KPIs de la simulación
        """
        if len(self.historial_likes) == 0:
            return {
                'total_likes': 0,
                'promedio_likes': 0,
                'max_likes': 0,
                'tiempo_viral': 0,
                'estado_actual_nombre': 'Latente'
            }
        
        # Contar tiempo en estado viral
        tiempo_viral = sum(1 for estado in self.historial_estados if estado == 1)
        
        estado_actual = self.cadena_markov.estado_actual
        nombres_estados = self.cadena_markov.obtener_nombres_estados()
        
        return {
            'total_likes': self.likes_acumulados,
            'promedio_likes': np.mean(self.historial_likes) if self.historial_likes else 0,
            'max_likes': max(self.historial_likes) if self.historial_likes else 0,
            'tiempo_viral': tiempo_viral,
            'estado_actual_nombre': nombres_estados[estado_actual]
        }
    
    def obtener_distribucion_estados(self) -> Tuple[List[int], List[int], List[int]]:
        """
        Retorna los historiales separados por tipo de estado para gráficos apilados.
        
        Returns:
            Tupla con tres listas (latente, viral, decadente) alineadas al tiempo
        """
        latente = [1 if estado == 0 else 0 for estado in self.historial_estados]
        viral = [1 if estado == 1 else 0 for estado in self.historial_estados]
        decadente = [1 if estado == 2 else 0 for estado in self.historial_estados]
        
        return latente, viral, decadente
    
    def reiniciar(self, nueva_matriz: np.ndarray = None, nuevo_lambda: float = None) -> None:
        """
        Reinicia la simulación.
        
        Args:
            nueva_matriz: Nueva matriz de transición (opcional)
            nuevo_lambda: Nuevo valor de lambda base (opcional)
        """
        if nueva_matriz is not None:
            self.cadena_markov = CadenaMarkov(nueva_matriz, estado_inicial=0)
        else:
            self.cadena_markov.reiniciar(estado_inicial=0)
        
        if nuevo_lambda is not None:
            self.lambda_base = nuevo_lambda
        
        self.red_social = RedSocial(num_nodos=30)
        self.time_step = 0
        self.historial_likes = []
        self.historial_estados = [0]
        self.historial_tiempo = [0]
        self.likes_acumulados = 0
