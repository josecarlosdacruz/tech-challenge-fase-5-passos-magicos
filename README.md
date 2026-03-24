# Tech Challenge Fase 5 - Datathon Passos Mágicos

<div align="center">
  <img src="https://img.shields.io/badge/FIAP-Pós%20Tech-brightgreen" alt="FIAP Pós-Tech">
  <img src="https://img.shields.io/badge/Status-Concluído-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Data%20Analytics-Fase%205-blue" alt="Fase 5">
</div>

## 📋 Projeto

**Objetivo**: Análise preditiva e storytelling para Associação Passos Mágicos, respondendo 11 perguntas de negócio com dados educacionais 2022-2024.

**Entregas**:
- [x] Storytelling analítico (PDF/PPT)
- [x] Modelo preditivo risco de defasagem (87% acurácia)
- [x] Aplicação Streamlit deployada
- [x] Notebook análise completa
- [x] Vídeo apresentação (4:30min)

---

## 📊 Estrutura do Projeto

tech-challenge-fase-5-passos-magicos/
├── README.md # Este arquivo
├── data/ # Dataset DATATHON
├── notebooks/ # Análise + Modelo
│ ├── 01_analise_exploratoria.ipynb
│ └── 02_modelo_preditivo.ipynb
├── src/ # Streamlit App
│ └── streamlit_app.py
├── docs/ # Apresentações
│ ├── apresentacao_storytelling.pdf
│ └── roteiro_apresentacao.md
├── requirements.txt # Dependências
└── streamlit_app.py # Deploy principal


---

## 🚀 Como Executar

### 1. Clonar Repositório
git clone https://github.com/josecarlosdacruz/tech-challenge-fase-5-passos-magicos
cd tech-challenge-fase-5-passos-magicos

### 2. Ambiente Virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

### 3. Instalar Dependências
pip install -r requirements.txt

### 4.Executar Streamlit
streamlit run src/streamlit_app.py

| Pergunta   | Insight Principal     | Impacto                   |
| ---------- | --------------------- | ------------------------- |
| IAN (1)    | 65% defasagem inicial | 42% recuperação           |
| IDA (2)    | +18% nas 4 fases      | Correlação IEG 0.72       |
| IPS (5)    | Precede 78% perdas    | Alerta precoce            |
| Modelo (9) | 87% acurácia          | Intervenção 30 dias antes |


🛠️ Tecnologias Utilizadas
<div style="display: flex; flex-wrap: wrap; gap: 10px;"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" /> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" /> <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" /> <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" /> <img src="https://img.shields.io/badge/Jupyter-E37628?style=for-the-badge&logo=jupyter&logoColor=white" /> </div>


