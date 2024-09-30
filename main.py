import streamlit as st
import pandas as pd

# Dados das corretoras
data = {
    'Corretora': [
        'XP Investimentos', 'Rico Investimentos', 'Clear Corretora',
        'Modalmais', 'Nu Invest', 'BTG Pactual Digital',
        'Toro Investimentos', 'Ágora Investimentos',
        'Itaú Corretora', 'Banco do Brasil Corretora'
    ],
    'Taxa de Corretagem Ações (R$)': [
        4.90, 0.0, 0.0, 2.49, 0.0, 2.50, 0.0, 4.50, 10.00, 10.00
    ],
    'Taxa de Corretagem FIIs (R$)': [
        4.90, 0.0, 0.0, 2.49, 0.0, 2.50, 0.0, 4.50, 10.00, 10.00
    ],
    'Taxa de Custódia (R$)': [
        0.0 for _ in range(10)
    ],
    'Outras Taxas (R$)': [
        0.0 for _ in range(10)
    ]
}

df_corretoras = pd.DataFrame(data)

# Taxas da B3 (valores aproximados)
TAXA_EMOLUMENTOS = 0.003  # 0,003%
TAXA_LIQUIDACAO = 0.0275  # 0,0275%

# Título do aplicativo
st.title('Comparação de Custos entre Corretoras')

# Entrada do usuário
valor_investimento = st.number_input('Digite o valor que deseja investir (R$):', min_value=0.0, value=1000.0, step=100.0)
tipo_investimento = st.selectbox('Selecione o tipo de investimento:', ['Ações', 'Fundos Imobiliários'])

# Botão para calcular
if st.button('Calcular'):
    # Cálculo das taxas da B3
    def calcular_taxas_b3(valor):
        taxa_emolumentos = valor * (TAXA_EMOLUMENTOS / 100)
        taxa_liquidacao = valor * (TAXA_LIQUIDACAO / 100)
        return taxa_emolumentos + taxa_liquidacao

    # Lista para armazenar os resultados
    resultados = []

    for index, row in df_corretoras.iterrows():
        # Taxa de corretagem
        if tipo_investimento == 'Ações':
            taxa_corretagem = row['Taxa de Corretagem Ações (R$)']
        else:
            taxa_corretagem = row['Taxa de Corretagem FIIs (R$)']

        taxa_custodia = row['Taxa de Custódia (R$)']
        outras_taxas = row['Outras Taxas (R$)']

        # Taxas da B3
        taxas_b3 = calcular_taxas_b3(valor_investimento)

        # Custos totais
        custo_total = taxa_corretagem + taxa_custodia + outras_taxas + taxas_b3

        # Valor líquido a ser investido
        valor_liquido = valor_investimento - custo_total

        resultados.append({
            'Corretora': row['Corretora'],
            'Taxa de Corretagem (R$)': taxa_corretagem,
            'Taxa de Custódia (R$)': taxa_custodia,
            'Outras Taxas (R$)': outras_taxas,
            'Taxas B3 (R$)': taxas_b3,
            'Custos Totais (R$)': custo_total,
            'Valor Líquido Investido (R$)': valor_liquido
        })

    # Criação do DataFrame com os resultados
    df_resultados = pd.DataFrame(resultados)

    # Ordenar as corretoras pelo maior valor líquido investido
    df_resultados = df_resultados.sort_values(by='Valor Líquido Investido (R$)', ascending=False)

    # Melhor opção com destaque
    melhor_opcao = df_resultados.iloc[0]

    # Exibir o perfil da melhor corretora com destaque visual e cor verde
    st.subheader('Melhor opção para investir:')
    st.markdown(f"""
        <div style="border-radius: 15px; border: 2px solid #4CAF50; background-color: #f9f9f9; padding: 20px; margin-top: 30px; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2); color: #4CAF50;">
            <h3 style="color: #4CAF50;">{melhor_opcao['Corretora']}</h3>
            <p><strong>Taxa de Corretagem (R$):</strong> {melhor_opcao['Taxa de Corretagem (R$)']:.2f}</p>
            <p><strong>Taxa de Custódia (R$):</strong> {melhor_opcao['Taxa de Custódia (R$)']:.2f}</p>
            <p><strong>Outras Taxas (R$):</strong> {melhor_opcao['Outras Taxas (R$)']:.2f}</p>
            <p><strong>Taxas B3 (R$):</strong> {melhor_opcao['Taxas B3 (R$)']:.2f}</p>
            <p><strong>Custos Totais (R$):</strong> {melhor_opcao['Custos Totais (R$)']:.2f}</p>
            <p><strong>Valor Líquido a Investir (R$):</strong> {melhor_opcao['Valor Líquido Investido (R$)']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
