# Análise e Dashboard - Covid-19

## Descrição

Este projeto tem como objetivo realizar a extração, tratamento e visualização de dados relacionados à pandemia de Covid-19 no Brasil, com foco no ano de 2021. Os dados abrangem casos confirmados, óbitos e vacinação, sendo organizados para serem utilizados em um dashboard interativo no Looker Studio. O projeto busca compreender o impacto da pandemia e das estratégias de vacinação implementadas no Brasil, auxiliando na análise de políticas públicas e planejamento futuro.

## Funcionalidades

- **Extração de Dados:** Obtenção de dados públicos sobre Covid-19, como casos, óbitos e vacinação.

- **Limpeza e Pré-processamento:**
    - Renomeação de colunas e padronização de nomes dos estados brasileiros.
    - Criação de métricas temporais como médias móveis e tendências.
    - Preenchimento de dados ausentes e reorganização do dataset.

- **Visualizações:**
    - Evolução diária de casos confirmados, óbitos e vacinação.
    - Análise temporal detalhada com gráficos.

- **Exportação:** Criação de arquivos CSV para utilização em dashboards e análises futuras.

## Requisitos
- Python 3.x
- Bibliotecas Python:
    - pandas
    - numpy
    - matplotlib

- Você pode instalar as dependências utilizando:

```bash
pip install -r requirements.txt
```

## Como Usar
1. Clone este repositório:

```bash
git clone https://github.com/SEU_USUARIO/analise-dashboard-covid
cd analise-dashboard-covid
```

2. Certifique-se de que as bibliotecas estão instaladas:

```bash
pip install -r requirements.txt
```

3. Execute o código para gerar os arquivos CSV:

```bash
python analise_dashboard_covid.py
```

4. Utilize os arquivos gerados (covid-cases.csv e covid-vaccines.csv) para criar visualizações no Looker Studio ou em outra ferramenta de análise.

## Estrutura do Projeto

- **Extração de Dados:**
    - Dados de casos e óbitos extraídos do repositório da Johns Hopkins University.
    - Dados de vacinação extraídos do Our World in Data.

- **Limpeza e Pré-processamento:**
    - Padronização dos nomes dos estados brasileiros.
    - Criação de métricas temporais como médias móveis e tendências.
    - Organização de dados em formato tabular.

- **Visualizações:**
    - Evolução de casos confirmados e óbitos.
    - Impacto da vacinação na redução de casos e mortes.
    - Progresso da vacinação ao longo de 2021.

- **Dashboard:**
    - https://lookerstudio.google.com/reporting/edc3d964-8f1b-4f66-87fe-4f478b2f358b

## Exemplos de Insights

- **Casos Confirmados e Mortes:**
    - Redução significativa de casos e óbitos a partir de meados de 2021, correlacionada com o início da vacinação em massa.

- **Vacinação:**
    - A vacinação começou em janeiro de 2021, inicialmente nos grupos prioritários, e expandiu ao longo do ano, impactando positivamente os indicadores da pandemia.

## Personalização
- Novas Métricas: Adapte o código para incluir outras análises ou variáveis de interesse.
- Visualizações Personalizadas: Crie novos gráficos para destacar diferentes aspectos da pandemia.

## Observações
Certifique-se de que a conexão com a internet está ativa durante a execução do código, pois os dados são baixados de fontes online. Caso o formato dos dados originais mude, ajustes no código poderão ser necessários.

## Licença
Este projeto é de uso livre e pode ser modificado conforme necessário.
