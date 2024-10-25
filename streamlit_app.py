import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Calculadora de Carga e Suporte", layout="wide")

# Função para calcular a produção de suporte com base na fertilidade selecionada
def calcular_suporte_ha(fertilidade_selecionada, area_efetiva):
    producao_por_ha = 0
    if fertilidade_selecionada == "Baixa fertilidade":
        producao_por_ha = 6000  # ton>kg/ha
    elif fertilidade_selecionada == "Fertilidade razoável":
        producao_por_ha = 7000  # ton>kg/ha
    elif fertilidade_selecionada == "Média fertilidade":
        producao_por_ha = 8000  # ton>kg/ha
    elif fertilidade_selecionada == "Alta fertilidade":
        producao_por_ha = 9000  # ton>kg/ha

    # Cálculo da produção total baseada na área efetiva
    producao_fazenda = producao_por_ha
    return producao_fazenda

# Novo cálculo da capacidade de suporte
def suporte_total(producao_fazenda, peso_medio, area_efetiva):
    # Cálculo de suporte
    suporte_kg_ms = ((producao_fazenda - 4500) / 365 / 0.025) * area_efetiva  # SUPORTE = (fertilidade_solo – 4500kg) / 365 / 2,5% PV de consumo animal * area_efetiva para calcular o suporte total da fazenda
    suporte_total_fazenda = suporte_kg_ms
    return suporte_total_fazenda

# Título da aplicação
st.title('Calculadora de Carga e Suporte')

# Inputs do usuário
num_animais = st.number_input('Número de animais:', min_value=1, value=1)
peso_medio = st.number_input('Peso médio dos animais (kg):', min_value=0.0, value=550.0)
area_efetiva = st.number_input('Área efetiva (ha):', min_value=0.1, value=1.0)

# Caixa de seleção para escolher o potencial de produção baseado na fertilidade do solo
fertilidade_selecionada = st.selectbox(
    'Selecione a fertilidade do solo:',
    ['Baixa fertilidade', 'Fertilidade razoável', 'Média fertilidade', 'Alta fertilidade']
)

# Botão para calcular
if st.button('Calcular'):
    # Cálculo da fertilidade do solo
    fertilidade_solo = calcular_suporte_ha(fertilidade_selecionada, area_efetiva)
    
    # Cálculo da capacidade de suporte
    suporte_total_fazenda = suporte_total(fertilidade_solo, peso_medio, area_efetiva)
    
    # Cálculo da carga atual em UA e animais por hectare
    carga_atual = (num_animais * peso_medio)
    animais_suportados = suporte_total_fazenda / peso_medio

    producao_fazenda = calcular_suporte_ha(fertilidade_selecionada, area_efetiva)

    # Exibição dos resultados
    st.subheader('Resultado')
    st.success(f"A produção total do solo (fertilidade) é de {producao_fazenda :.2f} toneladas de MS.")
    st.info(f"A carga animal atual é de {carga_atual:.2f} KG.")
    
    insight = carga_atual / suporte_total_fazenda
    # Comparação e insight
    st.subheader('Análise da Lotação')
    st.write(f"O valor do suporte total é de {suporte_total_fazenda:.2f} animais/ha")
    
    if animais_suportados > suporte_total_fazenda:
        st.warning(f"O número de animais está inadequado para o pasto. Há um excesso de {(animais_suportados * area_efetiva) - (suporte_total_fazenda * area_efetiva):.2f} animais a pasto.")
        st.write("Recomendação: Considere reduzir o número de animais ou aumentar a área de pastagem para evitar sobrecarga e degradação do pasto.")
    elif animais_suportados < suporte_total_fazenda:
        st.success(f"O número de animais está adequado ao pasto. Há uma margem para adicionar até {suporte_total_fazenda - animais_suportados:.2f} animais por hectare ou você poderá manter estes animais neste pasto por mais tempo.")
        st.write("Recomendação: O pasto está sendo subutilizado. Você pode considerar aumentar o número de animais ou reduzir a área de pastagem para otimizar o uso do recurso.")
    else:
        st.success("O número de animais está perfeitamente adequado à capacidade de suporte do pasto.")
    
    # Tabela com os dados
    resultados_df = pd.DataFrame({
        'Descrição': ['Produção Total do Solo (ton MS)', 'Carga Animal Atual (UA)', 'Animais/ha', 'Animais/ha Suportado'],
        'Valor': [f"{fertilidade_solo:.2f}", f"{carga_atual:.2f}", f"{animais_suportados:.2f}", f"{suporte_total_fazenda:.2f}"]
    })
    st.dataframe(resultados_df)
