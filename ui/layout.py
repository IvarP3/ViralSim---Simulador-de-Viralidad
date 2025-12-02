"""
Layout principal de la interfaz de usuario
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from typing import Dict
from streamlit_agraph import agraph, Node, Edge, Config
from services.simulator import SimulationEngine
from ui.styles import get_plotly_template, get_estado_color


def renderizar_metricas(metricas: Dict[str, any]) -> None:
    """
    Renderiza las métricas principales en tarjetas (KPIs).
    
    Args:
        metricas: Diccionario con métricas calculadas
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total de Likes",
            value=f"{metricas['total_likes']:,}"
        )
    
    with col2:
        st.metric(
            label="Promedio de Likes",
            value=f"{metricas['promedio_likes']:.1f}"
        )
    
    with col3:
        st.metric(
            label="Pico Máximo",
            value=f"{metricas['max_likes']:,}"
        )
    
    with col4:
        st.metric(
            label="Estado Actual",
            value=metricas['estado_actual_nombre']
        )


def renderizar_grafico_viralidad(simulator: SimulationEngine) -> None:
    """
    Renderiza el gráfico de línea con la curva de viralidad (likes en el tiempo).
    
    Args:
        simulator: Motor de simulación con datos
    """
    if len(simulator.historial_likes) > 0 and len(simulator.historial_tiempo) > 0:
        # Asegurar que ambas listas tengan la misma longitud
        min_length = min(len(simulator.historial_tiempo), len(simulator.historial_likes))
        tiempos = simulator.historial_tiempo[:min_length]
        likes = simulator.historial_likes[:min_length]
        estados = simulator.historial_estados[:min_length]
        
        if len(tiempos) > 1:
            # Crear figura de Plotly
            fig = go.Figure()
            
            # Añadir trazas por segmentos según el estado
            for i in range(len(tiempos) - 1):
                estado = estados[i]
                color = get_estado_color(estado)
                nombre_estado = ['Latente', 'Viral', 'Decadente'][estado]
                
                # Solo mostrar en leyenda la primera aparición de cada estado
                mostrar_leyenda = bool(i == 0 or estados[i] != estados[i-1])
                
                fig.add_trace(go.Scatter(
                    x=tiempos[i:i+2],
                    y=likes[i:i+2],
                    mode='lines+markers',
                    line=dict(color=color, width=3),
                    marker=dict(size=8, color=color, line=dict(color='#1F1F1F', width=1)),
                    name=nombre_estado,
                    showlegend=mostrar_leyenda,
                    legendgroup=nombre_estado,
                    hovertemplate=f'<b>Estado: {nombre_estado}</b><br>Tiempo: %{{x}}<br>Likes: %{{y}}<extra></extra>'
                ))
            
            # Aplicar template personalizado
            layout_config = get_plotly_template()
            fig.update_layout(
                **layout_config,
                title='Curva de Viralidad - Likes en el Tiempo',
                xaxis_title='Tiempo (pasos)',
                yaxis_title='Likes Generados',
                hovermode='closest',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)


def renderizar_grafico_estados(simulator: SimulationEngine) -> None:
    """
    Renderiza el gráfico de barras apiladas con la evolución de estados.
    
    Args:
        simulator: Motor de simulación con datos
    """
    if len(simulator.historial_tiempo) > 1:
        latente, viral, decadente = simulator.obtener_distribucion_estados()
        
        # Crear figura de Plotly
        fig = go.Figure()
        
        # Añadir barras apiladas
        fig.add_trace(go.Bar(
            x=simulator.historial_tiempo,
            y=latente,
            name='Latente',
            marker=dict(color='#808080', line=dict(color='#1F1F1F', width=1)),
            hovertemplate='<b>Latente</b><br>Tiempo: %{x}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=simulator.historial_tiempo,
            y=viral,
            name='Viral',
            marker=dict(color='#FF6B2B', line=dict(color='#1F1F1F', width=1)),
            hovertemplate='<b>Viral</b><br>Tiempo: %{x}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=simulator.historial_tiempo,
            y=decadente,
            name='Decadente',
            marker=dict(color='#2C3E50', line=dict(color='#1F1F1F', width=1)),
            hovertemplate='<b>Decadente</b><br>Tiempo: %{x}<extra></extra>'
        ))
        
        # Aplicar template personalizado
        layout_config = get_plotly_template()
        fig.update_layout(
            **layout_config,
            title='Evolución de Estados (Cadena de Markov)',
            xaxis_title='Tiempo (pasos)',
            yaxis_title='Estado Activo',
            barmode='stack',
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)


def renderizar_red_social(simulator: SimulationEngine) -> None:
    """
    Renderiza la visualización de la red social con streamlit-agraph.
    
    Args:
        simulator: Motor de simulación con red social
    """
    # Crear nodos
    nodes = []
    for i in range(simulator.red_social.num_nodos):
        estado = simulator.red_social.estados_nodos[i]
        color = get_estado_color(estado)
        nombre_estado = ['Latente', 'Viral', 'Decadente'][estado]
        
        nodes.append(Node(
            id=str(i),
            label=str(i),
            size=15,
            color=color,
            title=f"Usuario {i} - {nombre_estado}"
        ))
    
    # Crear aristas
    edges = []
    for edge in simulator.red_social.grafo.edges():
        edges.append(Edge(
            source=str(edge[0]),
            target=str(edge[1]),
            color='#D3D3D3',
            width=0.5
        ))
    
    # Configuración del grafo
    config = Config(
        width="100%",
        height=600,
        directed=False,
        physics={
            "enabled": True,
            "barnesHut": {
                "gravitationalConstant": -2000,
                "centralGravity": 0.3,
                "springLength": 95,
                "springConstant": 0.04,
                "damping": 0.09,
                "avoidOverlap": 0.1
            },
            "stabilization": {
                "enabled": True,
                "iterations": 200
            }
        },
        interaction={
            "hover": True,
            "navigationButtons": True,
            "zoomView": True,
            "dragNodes": True
        }
    )
    
    # Renderizar grafo
    agraph(nodes=nodes, edges=edges, config=config)
    
    # Leyenda manual
    st.markdown("""
    <div style='display: flex; justify-content: center; gap: 30px; padding: 10px; background-color: #F4E8C1; border-radius: 5px; margin-top: 10px;'>
        <div><span style='color: #808080;'>●</span> Usuario Latente</div>
        <div><span style='color: #FF6B2B;'>●</span> Usuario Viral</div>
        <div><span style='color: #2C3E50;'>●</span> Usuario Decadente</div>
    </div>
    """, unsafe_allow_html=True)


def renderizar_interfaz_completa(simulator: SimulationEngine) -> None:
    """
    Renderiza la interfaz completa de la aplicación.
    
    Args:
        simulator: Motor de simulación
    """
    # Título principal
    st.title("ViralSim - Simulador de Viralidad en Redes Sociales")
    st.markdown("*Modelado con Procesos de Poisson y Cadenas de Markov*")
    st.markdown("---")
    
    # Métricas principales
    metricas = simulator.obtener_metricas_globales()
    renderizar_metricas(metricas)
    
    st.markdown("---")
    
    # Gráficos principales en columnas
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("Curva de Viralidad")
        renderizar_grafico_viralidad(simulator)
    
    with col_der:
        st.subheader("Evolución de Estados")
        renderizar_grafico_estados(simulator)
    
    st.markdown("---")
    
    # Red social
    st.subheader("Red Social - Propagación de Estados")
    renderizar_red_social(simulator)
    
    st.markdown("---")
    
    # Información adicional
    with st.expander("Información del Modelo"):
        st.markdown("""
        ### Modelo Matemático
        
        **Estados de Markov:**
        - **Estado 0 - Latente**: Contenido sin tracción, tasa normal de likes (λ × 1.0)
        - **Estado 1 - Viral**: Contenido explotando, tasa multiplicada (λ × 10.0)
        - **Estado 2 - Decadente**: Contenido en caída, tasa reducida (λ × 0.5)
        
        **Proceso de Poisson:**
        - Modela la llegada aleatoria de likes en el tiempo
        - La tasa λ efectiva depende del estado actual de Markov
        - Eventos generados: Poisson(λ_efectivo)
        
        **Acoplamiento:**
        - El estado de Markov modifica la intensidad del proceso de Poisson
        - Simula cómo el "momentum" viral afecta la llegada de interacciones
        """)
