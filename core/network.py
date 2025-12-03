"""
Módulo para visualización de red social usando NetworkX
"""
import networkx as nx
import numpy as np
from typing import List


class RedSocial:
    """
    Representa una red social como un grafo y permite su visualización.
    """
    
    def __init__(self, num_nodos: int = 30, probabilidad_conexion: float = 0.15):
        """
        Inicializa la red social.
        
        Args:
            num_nodos: Número de usuarios en la red
            probabilidad_conexion: Probabilidad de conexión entre nodos (Erdős-Rényi)
        """
        self.num_nodos = num_nodos
        
        # Crear grafo usando modelo Erdős-Rényi
        np.random.seed(42)  # Seed fijo para reproducibilidad
        self.grafo = nx.erdos_renyi_graph(n=num_nodos, p=probabilidad_conexion, seed=42)
        
        # Calcular layout fijo (para que los nodos no se muevan)
        self.pos = nx.spring_layout(self.grafo, seed=42, k=0.5, iterations=50)
        
        # Estados de nodos (inicialmente todos en Latente)
        self.estados_nodos = [0] * num_nodos
    
    def actualizar_estados(self, estado_predominante: int) -> None:
        """
        Actualiza los estados de los nodos según el estado predominante de la simulación.
        
        Args:
            estado_predominante: Estado actual de la cadena de Markov
        """
        # Asignar estados de manera probabilística
        for i in range(self.num_nodos):
            prob = np.random.random()
            
            if estado_predominante == 0:  # Latente
                self.estados_nodos[i] = 0 if prob < 0.7 else np.random.choice([1, 2])
            elif estado_predominante == 1:  # Viral
                self.estados_nodos[i] = 1 if prob < 0.8 else np.random.choice([0, 2])
            else:  # Decadente
                self.estados_nodos[i] = 2 if prob < 0.7 else np.random.choice([0, 1])
    
    def obtener_colores_nodos(self) -> List[str]:
        """
        Retorna lista de colores para cada nodo según su estado.
        
        Returns:
            Lista de colores en formato hexadecimal
        """
        mapa_colores = {
            0: "#808080",  # Gris - Latente
            1: "#FF6B2B",  # Naranja - Viral
            2: "#2C3E50"   # Azul oscuro - Decadente
        }
        return [mapa_colores[estado] for estado in self.estados_nodos]
    
    def dibujar(self, fig, ax) -> None:
        """
        Dibuja la red social en los ejes proporcionados.
        
        Args:
            fig: Figura de matplotlib
            ax: Ejes de matplotlib donde dibujar
        """
        ax.clear()
        
        # Configurar aspecto
        ax.set_facecolor('#FAF3E1')
        ax.axis('off')
        
        # Obtener colores según estados
        colores_nodos = self.obtener_colores_nodos()
        
        # Dibujar aristas
        nx.draw_networkx_edges(
            self.grafo,
            self.pos,
            ax=ax,
            edge_color="#D3D3D3",
            width=0.5,
            alpha=0.6
        )
        
        # Dibujar nodos
        nx.draw_networkx_nodes(
            self.grafo,
            self.pos,
            ax=ax,
            node_color=colores_nodos,
            node_size=300,
            alpha=0.9,
            edgecolors="#1F1F1F",
            linewidths=1.0
        )
        
        ax.set_title("Red Social - Estados de Usuarios", 
                     fontsize=14, 
                     fontweight='bold', 
                     color='#1F1F1F',
                     pad=10)
