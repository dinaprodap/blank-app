import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

        # Gráfico de barras com sombra
        st.subheader('Visualização')
        fig = go.Figure()

        # Adiciona as barras de sombra (mais grossas e cinzas)
        fig.add_trace(go.Bar(
            x=['Carga', 'Suporte'],
            y=[carga, suporte],
            name='Sombra',
            marker_color='lightgrey',
            width=0.5
        ))

        # Adiciona as barras coloridas (mais finas) na frente
        fig.add_trace(go.Bar(
            x=['Carga', 'Suporte'],
            y=[carga, suporte],
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

        st.plotly_chart(fig)
