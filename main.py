"""
ViralSim - Simulador de Viralidad en Redes Sociales
Punto de entrada principal de la aplicación Streamlit
"""
import streamlit as st
import numpy as np
import pandas as pd
from services.simulator import SimulationEngine
from ui.layout import renderizar_interfaz_completa


# Configuración de página
st.set_page_config(
    page_title="ViralSim",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inicializar_session_state() -> None:
    """
    Inicializa el estado de la sesión de Streamlit si no existe.
    """
    if 'simulator' not in st.session_state:
        # Matriz de transición por defecto (3x3)
        matriz_default = np.array([
            [0.7, 0.25, 0.05],   # Desde Latente
            [0.1, 0.7, 0.2],      # Desde Viral
            [0.3, 0.1, 0.6]       # Desde Decadente
        ])
        
        # Crear simulador inicial
        st.session_state.simulator = SimulationEngine(
            matriz_transicion=matriz_default,
            lambda_base=5.0
        )
        st.session_state.simulacion_corrida = False


def renderizar_sidebar() -> dict:
    """
    Renderiza el sidebar con controles de simulación.
    
    Returns:
        Diccionario con parámetros configurados
    """
    st.sidebar.title("Configuración")
    st.sidebar.markdown("---")
    
    # Control de Lambda
    st.sidebar.subheader("Parámetro de Poisson")
    lambda_base = st.sidebar.slider(
        "Lambda Base (λ) - Tasa de llegada de likes",
        min_value=1.0,
        max_value=20.0,
        value=5.0,
        step=0.5,
        help="Tasa promedio base de likes por unidad de tiempo"
    )
    
    st.sidebar.markdown("---")
    
    # Matriz de Transición
    st.sidebar.subheader("Matriz de Transición de Markov")
    st.sidebar.markdown("**Edita las probabilidades de transición:**")
    
    # Obtener matriz actual
    matriz_actual = st.session_state.simulator.cadena_markov.matriz_transicion
    
    # Crear DataFrame editable
    df_matriz = pd.DataFrame(
        matriz_actual,
        columns=["→ Latente", "→ Viral", "→ Decadente"],
        index=["Latente ↓", "Viral ↓", "Decadente ↓"]
    )
    
    # Editor de datos
    matriz_editada = st.sidebar.data_editor(
        df_matriz,
        use_container_width=True,
        num_rows="fixed",
        disabled=False,
        key="matriz_editor"
    )
    
    # Convertir a numpy array y normalizar
    matriz_nueva = matriz_editada.to_numpy()
    
    # Normalizar filas para garantizar que sumen 1
    sumas_filas = matriz_nueva.sum(axis=1, keepdims=True)
    if np.any(sumas_filas > 0):
        matriz_nueva = matriz_nueva / sumas_filas
    
    st.sidebar.info("**Nota:** Las filas se normalizan automáticamente para sumar 1.0")
    
    st.sidebar.markdown("---")
    
    # Parámetros de simulación
    st.sidebar.subheader("Parámetros de Simulación")
    num_pasos = st.sidebar.slider(
        "Número de pasos a simular",
        min_value=10,
        max_value=200,
        value=50,
        step=10,
        help="Cantidad de iteraciones de la simulación"
    )
    
    st.sidebar.markdown("---")
    
    # Botones de control
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        boton_simular = st.button(
            "SIMULAR",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        boton_reiniciar = st.button(
            "REINICIAR",
            use_container_width=True
        )
    
    return {
        'lambda_base': lambda_base,
        'matriz_transicion': matriz_nueva,
        'num_pasos': num_pasos,
        'boton_simular': boton_simular,
        'boton_reiniciar': boton_reiniciar
    }


def main():
    """
    Función principal de la aplicación.
    """
    # Inicializar estado
    inicializar_session_state()
    
    # Renderizar sidebar y obtener parámetros
    params = renderizar_sidebar()
    
    # Procesar botón de reinicio
    if params['boton_reiniciar']:
        st.session_state.simulator.reiniciar(
            nueva_matriz=params['matriz_transicion'],
            nuevo_lambda=params['lambda_base']
        )
        st.session_state.simulacion_corrida = False
        st.rerun()
    
    # Procesar botón de simulación
    if params['boton_simular']:
        # Actualizar parámetros del simulador
        st.session_state.simulator.cadena_markov.matriz_transicion = params['matriz_transicion']
        st.session_state.simulator.lambda_base = params['lambda_base']
        
        # Ejecutar simulación
        with st.spinner('Simulando viralidad...'):
            st.session_state.simulator.simular_multiple_pasos(params['num_pasos'])
        
        st.session_state.simulacion_corrida = True
        st.success(f"Simulación completada: {params['num_pasos']} pasos ejecutados")
    
    # Renderizar interfaz
    if st.session_state.simulacion_corrida:
        renderizar_interfaz_completa(st.session_state.simulator)
    else:
        # Pantalla de bienvenida
        st.title("ViralSim - Simulador de Viralidad")
        st.markdown("### Bienvenido al Simulador de Viralidad en Redes Sociales")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("""
            ### ¿Cómo empezar?
            
            1. **Configura los parámetros** en el panel lateral:
               - Ajusta el valor de Lambda (λ) para la tasa de likes
               - Modifica la matriz de transición de Markov
               
            2. **Define el número de pasos** a simular
            
            3. **Haz clic en SIMULAR** para comenzar
            
            La simulación modelará cómo un contenido pasa por diferentes estados
            (Latente → Viral → Decadente) y cómo esto afecta la llegada de likes
            usando un Proceso de Poisson acoplado con una Cadena de Markov.
            """)
        
        st.markdown("---")
        
        # Información teórica
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
            ### Proceso de Poisson
            Modela eventos aleatorios que ocurren de manera independiente en el tiempo:
            - Llegada de likes/comentarios
            - Tasa λ variable según contexto
            - Distribución: P(k eventos) = (λᵗ)ᵏ e⁻ᵏᵗ / k!
            """)
        
        with col_b:
            st.markdown("""
            ### Cadena de Markov
            Modelo estocástico sin memoria para transiciones de estado:
            - Estados: Latente, Viral, Decadente
            - Transiciones probabilísticas
            - Matriz estocástica (filas suman 1)
            """)


if __name__ == "__main__":
    main()
