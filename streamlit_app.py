# Calculadora de Carga e Suporte

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

# Gráfico de barras
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
        
        # Atualiza as cores e larguras das barras
fig.update_traces(
            selector=dict(name='Sombra'),
            marker_color='rgba(211, 211, 211, 0.5)',  # Cinza claro semi-transparente
            width=0.6
        )
fig.update_traces(
            selector=dict(name='Valor'),
            marker_color=['#FF4B4B', '#4BB543'],  # Vermelho para Carga, Verde para Suporte
            width=0.4
        )
        
        # Adiciona rótulos de valor nas barras
for i, valor in enumerate([carga, suporte]):
            fig.add_annotation(
                x=['Carga', 'Suporte'][i],
                y=valor,
                text=f'{valor:.2f}',
                showarrow=False,
                yshift=10
            )
        
# Exibe o gráfico usando toda a largura disponível
st.plotly_chart(fig, use_container_width=True)
