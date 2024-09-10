import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Calculadora de Carga e Suporte", layout="wide")

def calcular_capacidade_suporte(num_animais, peso_medio, area_efetiva, altura_media):
    # Ajuste na produção de MS por hectare
    producao_ms_por_cm = 100  # kg de MS por cm de altura por hectare
    
    # Cálculo da produção de MS baseada na altura média do pasto
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
area_efetiva = st.number_input('Área efetiva do pasto (ha):', min_value=0.1, value=1.0)
altura_media = st.number_input('Altura média do pasto (cm):', min_value=1.0, value=20.0)

# Botão para calcular
if st.button('Calcular'):
    capacidade_suporte, carga_atual, animais_por_hectare_atual, animais_por_hectare_suportado = calcular_capacidade_suporte(num_animais, peso_medio, area_efetiva, altura_media)
    
    # Exibição dos resultados
    st.subheader('Resultado')
    st.success(f"A capacidade de suporte estimada é de {capacidade_suporte:.0f} UA/ha.")
    st.info(f"A carga animal atual é de {carga_atual:.0f} UA.")
    
    # Comparação e insight
    st.subheader('Análise da Lotação')
    st.write(f"Número atual de animais por hectare: {animais_por_hectare_atual:.0f}")
    st.write(f"Número de animais por hectare suportado pelo pasto: {animais_por_hectare_suportado:.0f}")
    
    if animais_por_hectare_atual > animais_por_hectare_suportado:
        st.warning(f"O número de animais está inadequado para o pasto. Há um excesso de {(animais_por_hectare_atual * area_efetiva) - (animais_por_hectare_suportado * area_efetiva):.0f} animais no pasto.")
        st.write("Recomendação: Considere reduzir o número de animais ou aumentar a área de pastagem para evitar sobrecarga e degradação do pasto.")
    elif animais_por_hectare_atual < animais_por_hectare_suportado:
        st.success(f"O número de animais está adequado ao pasto. Há uma margem para adicionar até {animais_por_hectare_suportado - animais_por_hectare_atual:.0f} animais por hectare ou você poderá manter estes animais neste pasto por 60 dias.")
        st.write("Recomendação: O pasto está sendo subutilizado. Você pode considerar aumentar o número de animais ou reduzir a área de pastagem para otimizar o uso do recurso.")
    else:
        st.success("O número de animais está perfeitamente adequado à capacidade de suporte do pasto.")

    # Tabela com os dados
    resultados_df = pd.DataFrame({
        'Descrição': ['Carga Unidade Animal', 'Animais/ha', 'Animais/ha Suportado'],
        'Valor': [f"{carga_atual:.0f} UA/ha", 
                  f"{animais_por_hectare_atual:.0f}", f"{animais_por_hectare_suportado:.0f}"]
    })
    st.dataframe(resultados_df)

    # Gráfico de barras
    st.subheader('Visualização')
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['Capacidade de Suporte', 'Carga Animal Atual'],
        y=[capacidade_suporte, carga_atual],
        name='UA/ha',
        marker_color=['#4BB543', '#FF4B4B']
    ))

    fig.update_layout(
        title='Comparação entre Capacidade de Suporte e Carga Animal Atual',
        xaxis_title='Métrica',
        yaxis_title='UA/ha'
    )

    st.plotly_chart(fig, use_container_width=True)
