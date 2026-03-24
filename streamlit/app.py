import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurações globais da aplicação
st.set_page_config(page_title="Projeto Datathon - Passos Mágicos", layout="wide")

@st.cache_resource
def load_model():
    """Carrega o modelo preditivo treinado"""
    return joblib.load('modelo_passos_magicos.pkl')

@st.cache_data
def load_data():
    """Carrega e realiza o pré-processamento das bases 2022, 2023 e 2024"""
    file_path = os.path.join('data', 'BASE DE DADOS PEDE 2024 - DATATHON.xlsx')
    
    if not os.path.exists(file_path):
        st.error(f"Erro: Arquivo não localizado em {file_path}")
        return pd.DataFrame()

    xls = pd.ExcelFile(file_path)
    df_list = []
    abas = ['PEDE2022', 'PEDE2023', 'PEDE2024']
    
    for sheet in abas:
        temp = pd.read_excel(xls, sheet_name=sheet)
        temp['ANO_REFERENCIA'] = sheet
        temp.columns = [c.strip() if isinstance(c, str) else c for c in temp.columns]
        df_list.append(temp)
        
    df = pd.concat(df_list, ignore_index=True)

    # Padronização da coluna de fases
    df['Fase'] = df['Fase'].astype(str).str.strip().str.upper()

    # Mapeamento de Ciclos Escolares para análise agregada
    def mapear_ciclo(fase):
        if 'ALFA' in fase: return 'Alfabetização'
        if any(f in fase for f in ['1', '2', '3']): return 'Fundamental I'
        if any(f in fase for f in ['4', '5', '6']): return 'Fundamental II'
        if any(f in fase for f in ['7', '8']): return 'Ensino Médio'
        if any(f in fase for f in ['QUARTZO', 'ÁGATA', 'AMETISTA', 'TOPÁZIO']): return 'Especial (Pedras)'
        return 'Outros'

    df['Ciclo'] = df['Fase'].apply(mapear_ciclo)
    return df

# Inicialização dos recursos
df = load_data()
model = load_model()

st.title("Sistema de Análise Estratégica - Passos Mágicos")
st.markdown("---")

if not df.empty:
    # Sidebar para controle de escopo da análise
    st.sidebar.header("Parâmetros de Filtro")
    anos_disponiveis = df['ANO_REFERENCIA'].unique()
    ano_sel = st.sidebar.multiselect("Ciclos de Referência", anos_disponiveis, default=anos_disponiveis)
    df_filtered = df[df['ANO_REFERENCIA'].isin(ano_sel)]

    tab1, tab2, tab3 = st.tabs(["Análise de Desempenho", "Modelo Preditivo", "Base de Dados"])

    with tab1:
        st.subheader("Indicadores de Evolução Acadêmica")
        
        # Grid superior: Linha e Dispersão
        c1, c2 = st.columns(2)
        
        with c1:
            # Evolução temporal do IDA
            df_evolucao = df_filtered.groupby('ANO_REFERENCIA')['IDA'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(6, 3.5)) # Tamanho reduzido
            sns.lineplot(data=df_evolucao, x='ANO_REFERENCIA', y='IDA', marker='o', color='#1f77b4', ax=ax)
            ax.set_ylim(0, 10)
            ax.set_title("Média IDA por Ano", fontsize=10)
            st.pyplot(fig)

        with c2:
            # Correlação Engajamento x Social
            fig2, ax2 = plt.subplots(figsize=(6, 3.5)) # Tamanho reduzido
            sns.scatterplot(data=df_filtered, x='IEG', y='IPS', hue='Ciclo', alpha=0.5, palette='tab10', ax=ax2)
            ax2.set_title("Correlação IEG vs IPS", fontsize=10)
            ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small')
            st.pyplot(fig2)

        st.markdown("---")
        
        # Grid inferior centralizado para o ranking
        _, col_mid, _ = st.columns([1, 4, 1])
        with col_mid:
            st.subheader("Desempenho por Ciclo Escolar")
            df_ciclo = df_filtered.groupby('Ciclo')['IDA'].mean().sort_values(ascending=False).reset_index()
            
            fig3, ax3 = plt.subplots(figsize=(7, 3.5)) # Tamanho otimizado
            sns.barplot(data=df_ciclo, y='Ciclo', x='IDA', palette='viridis', ax=ax3)
            
            for i, v in enumerate(df_ciclo['IDA']):
                ax3.text(v + 0.1, i, f'{v:.2f}', va='center', fontsize=8, fontweight='bold')
                
            ax3.set_xlim(0, 11)
            ax3.set_title("Média IDA por Ciclo", fontsize=10)
            st.pyplot(fig3)

    with tab2:
        st.subheader("Predição de Risco de Defasagem (IAN)")
        st.write("Cálculo de probabilidade baseado nos indicadores psicopedagógicos e acadêmicos.")

        with st.form("form_ml"):
            col_a, col_b, col_c = st.columns(3)
            f_ida = col_a.number_input("Nota IDA", 0.0, 10.0, 7.0)
            f_ieg = col_b.number_input("Nota IEG", 0.0, 10.0, 7.0)
            f_ips = col_c.number_input("Nota IPS", 0.0, 10.0, 7.0)
            
            col_d, col_e = st.columns(2)
            f_ipp = col_d.number_input("Nota IPP", 0.0, 10.0, 7.0)
            f_iaa = col_e.number_input("Nota IAA", 0.0, 10.0, 7.0)
            
            f_fase = st.selectbox("Fase Atual", sorted(df['Fase'].unique()))
            btn_pred = st.form_submit_button("Executar Predição")

        if btn_pred:
            # Estrutura de entrada para o pipeline
            input_df = pd.DataFrame([[f_ida, f_ieg, f_ips, f_ipp, f_iaa, f_fase, "PEDE2024"]],
                                    columns=['IDA', 'IEG', 'IPS', 'IPP', 'IAA', 'Fase', 'ANO_REFERENCIA'])
            
            input_df['Fase'] = input_df['Fase'].astype(str)
            probs = model.predict_proba(input_df)[0]
            prob_risco = probs[1] if len(probs) > 1 else (1.0 if model.classes_[0] == 1 else 0.0)
            
            st.markdown("---")
            if prob_risco > 0.5:
                st.error(f"**Resultado: Risco Elevado ({prob_risco:.1%})**")
                st.info("Recomenda-se acompanhamento preventivo e reforço pedagógico.")
            else:
                st.success(f"**Resultado: Risco Baixo ({prob_risco:.1%})**")

    with tab3:
        st.subheader("Visualização de Dados Consolidados")
        st.dataframe(df_filtered.head(500), use_container_width=True)