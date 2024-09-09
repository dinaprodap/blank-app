#Calculadora de Carga e Suporte

import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Calculadora de Carga e Suporte", layout="wide")

def calcular_carga_suporte(carga, suporte):
    diferenca = suporte - carga
    if diferenca >= 0:
        return True, diferenca
    else:
        return False, abs(diferenca)

# Título da aplicação
st.title('Calculadora de Carga e Suporte')

# Entradas do usuário
carga = st.number_input('Digite o valor da carga:', min_value=0.0, format="%.2f")
suporte = st.number_input('Digite o valor do suporte:', min_value=0.0, format="%.2f")

# Botão para calcular
if st.button('Calcular'):
    suficiente, diferenca = calcular_carga_suporte(carga, suporte)
    
    # Exibição dos resultados
    st.subheader('Resultado')
    if suficiente:
        st.success(f"O suporte é suficiente para a carga. Há uma margem de segurança de {diferenca:.2f} unidades.")
    else:
        st.error(f"O suporte não é suficiente para a carga. Reduza a carga em {diferenca:.2f} unidades.")
    
    # Tabela com os dados
    resultados_df = pd.DataFrame({
        'Descrição': ['Carga', 'Suporte', 'Diferença'],
        'Valor': [f"{carga:.2f}", f"{suporte:.2f}", f"{diferenca:.2f}"]
    })
    st.dataframe(resultados_df)

    # Gráfico de barras
    st.subheader('Visualização')
    chart_data = pd.DataFrame({
        'Tipo': ['Carga', 'Suporte'],
        'Valor': [carga, suporte]
    })
    st.bar_chart(chart_data.set_index('Tipo'))
