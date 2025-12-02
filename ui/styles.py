"""
Configuración de estilos para gráficos Plotly
"""


def get_plotly_template() -> dict:
    """
    Retorna la configuración de template personalizada para Plotly.
    
    Returns:
        Diccionario con configuración de layout
    """
    return {
        'plot_bgcolor': '#FAF3E1',
        'paper_bgcolor': '#FAF3E1',
        'font': {
            'color': '#1F1F1F',
            'family': 'sans-serif',
            'size': 12
        },
        'xaxis': {
            'gridcolor': '#D3D3D3',
            'gridwidth': 0.5,
            'showline': True,
            'linewidth': 1,
            'linecolor': '#1F1F1F',
            'mirror': False
        },
        'yaxis': {
            'gridcolor': '#D3D3D3',
            'gridwidth': 0.5,
            'showline': True,
            'linewidth': 1,
            'linecolor': '#1F1F1F',
            'mirror': False
        },
        'title_font': {
            'size': 16,
            'color': '#1F1F1F'
        },
        'legend': {
            'bgcolor': 'rgba(244, 232, 193, 0.8)',
            'bordercolor': '#1F1F1F',
            'borderwidth': 1
        }
    }


def get_estado_color(estado: int) -> str:
    """
    Retorna el color correspondiente a un estado.
    
    Args:
        estado: Número de estado (0=Latente, 1=Viral, 2=Decadente)
    
    Returns:
        Color en formato hexadecimal
    """
    colores = {
        0: "#808080",  # Gris - Latente
        1: "#FF6B2B",  # Naranja - Viral
        2: "#2C3E50"   # Azul oscuro - Decadente
    }
    return colores.get(estado, "#808080")
