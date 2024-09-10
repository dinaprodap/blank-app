# Calculadora de Capacidade de Suporte de Pastagem

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Calculadora de Carga e Suporte", layout="wide")

def calcular_capacidade_suporte(num_animais, peso_medio, area_efetiva, altura_media):
    # Estimativa da produção de MS baseada na altura média do pasto (exemplo simplificado)
    producao_ms_por_cm = 200  # kg de MS por cm de altura por hectare
    producao_ms = producao_ms_por_cm * altura_media * area_efetiva
    
    consumo_anual_ua = 18000  # kg de MS por ano para 1 UA
    capacidade_suporte = producao_ms / consumo_anual_ua
    
    carga_atual = (num_animais * peso_medio) / 450  # 450 kg = 1 UA
    animais_por_hectare_atual = num_animais / area_efetiva
    animais_por_hectare_suportado = (capacidade_suporte * area_efetiva * 450) / peso_medio
    
    return capacidade_suporte, carga_atual, animais_por_hectare_atual, animais_por_hectare_suportado

# Título da aplicação
st.title('Calculadora de Capacidade de Suporte de Pastagem')

# Entradas do usuário
num_animais = st.number_input('Número de animais:', min_value=1, value=1)
peso_medio = st.number_input('Peso médio dos animais (kg):', min_value=0.0, value=450.0)
area_efetiva = st.number_input('Área efetiva do pasto (ha):', min_value=0.1, value=12.0)
altura_media = st.number_input('Altura média do pasto (cm):', min_value=1.0, value=25.0)

# Botão para calcular
if st.button('Calcular'):
    capacidade_suporte, carga_atual, animais_por_hectare_atual, animais_por_hectare_suportado = calcular_capacidade_suporte(num_animais, peso_medio, area_efetiva, altura_media)
    
    # Exibição dos resultados
    st.subheader('Resultado')
    st.success(f"A capacidade de suporte estimada é de {capacidade_suporte:.2f} UA/ha.")
    st.info(f"A carga animal atual é de {carga_atual:.2f} UA/ha.")
    
    # Comparação e insight
    st.subheader('Análise da Lotação')
    st.write(f"Número atual de animais por hectare: {animais_por_hectare_atual:.2f}")
    st.write(f"Número de animais por hectare suportado pelo pasto: {animais_por_hectare_suportado:.2f}")
    
    if animais_por_hectare_atual > animais_por_hectare_suportado:
        st.warning(f"O número de animais está inadequado para o pasto. Há um excesso de {animais_por_hectare_atual - animais_por_hectare_suportado:.2f} animais por hectare.")
        st.write("Recomendação: Considere reduzir o número de animais ou aumentar a área de pastagem para evitar sobrecarga e degradação do pasto.")
    elif animais_por_hectare_atual < animais_por_hectare_suportado:
        st.success(f"O número de animais está adequado ao pasto. Há uma margem para adicionar até {animais_por_hectare_suportado - animais_por_hectare_atual:.2f} animais por hectare.")
        st.write("Recomendação: O pasto está sendo subutilizado. Você pode considerar aumentar o número de animais ou reduzir a área de pastagem para otimizar o uso do recurso.")
    else:
        st.success("O número de animais está perfeitamente adequado ao pasto.")
        st.write("Recomendação: Mantenha o manejo atual, pois está otimizando o uso do pasto.")
    
    # Tabela com os dados
    resultados_df = pd.DataFrame({
        'Descrição': ['Capacidade de Suporte', 'Carga Animal Atual', 'Animais/ha Atual', 'Animais/ha Suportado'],
        'Valor': [f"{capacidade_suporte:.2f} UA/ha", f"{carga_atual:.2f} UA/ha", f"{animais_por_hectare_atual:.2f}", f"{animais_por_hectare_suportado:.2f}"]
    })
    st.dataframe(resultados_df)

    # Gráfico de barras
    fig = go.Figure()

    # Adiciona as barras de sombra (mais grossas e cinzas)
    fig.add_trace(go.Bar(
                x=['Carga', 'Suporte'],
                y=[carga_atual, capacidade_suporte],
                name='Sombra',
                marker_color='lightgrey',
                width=0.5
            ))

    # Adiciona as barras coloridas (mais finas) na frente
    fig.add_trace(go.Bar(
                x=['Carga', 'Suporte'],
                y=[carga_atual, capacidade_suporte],
                name='Valor',
                marker_color=['#FF4B4B', '#4BB543'],
                width=0.3
            ))

    fig.update_layout(
                barmode='overlay',
                title='Comparação entre Carga e Suporte',
                xaxis_title='Tipo',
                yaxis_title='Valor'
            )

    # Ajusta o layout do gráfico
    fig.update_layout(
                height=500,  # Altura do gráfico
                margin=dict(l=50, r=50, t=50, b=50),  # Margens
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),  # Legenda horizontal no topo
                title_text='Comparação entre Carga e Suporte',  # Título do gráfico
                title_font_size=20,  # Tamanho da fonte do título
                xaxis_title='Tipo',  # Título do eixo X
                yaxis_title='Valor',  # Título do eixo Y
                barmode='overlay'  # Modo de sobreposição das barras
            )

    # Adiciona rótulos de valor nas barras
    for i, valor in enumerate([carga_atual, capacidade_suporte]):
        fig.add_annotation(
            x=['Carga', 'Suporte'][i],
            y=valor,
            text=f'{valor:.2f}',
            showarrow=False,
            yshift=10
        )
        
    # Exibe o gráfico usando toda a largura disponível
    st.plotly_chart(fig, use_container_width=True)
