import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pickle
import plotly.graph_objects as go

st.title('Ibovespa Forecast')

resumo, intro ,eda, split, modelos, resultados = st.tabs(['Resumo', 'Introdução', 'Análise Exploratória', 'Split and Cross Validation', 'Modelos', 'Resultados'])

with resumo:

    st.subheader('Resumo')

    '''
    Este projeto, parte do programa de Pós-Graduação em Data Analytics da FIAP, visa desenvolver um modelo preditivo para prever os preços de fechamento diário do IBOVESPA, com uma meta de acurácia mínima de 70%. A aplicação de conhecimentos em análise estatística, ciência de dados e modelagem preditiva foi essencial para atingir esse objetivo.

    A análise envolveu uma investigação exploratória dos dados da IBOVESPA para identificar padrões e tendências, seguida pela implementação de várias técnicas de previsão. Antes da aplicação da validação cruzada, o modelo ETS apresentou um MAPE de 0.01 (ou 1%), o que indicou uma previsão bastante precisa e que a acurácia do modelo estava acima da meta de 70%. Após a validação cruzada, o MAPE do modelo ETS aumentou para 0.03 (ou 3%), mas ainda permaneceu dentro da faixa que indica uma acurácia aceitável acima de 70%.

    Conclusivamente, a análise destaca a importância de uma abordagem integrada, combinando habilidades técnicas e analíticas com comunicação eficaz, para desenvolver modelos preditivos robustos. O estudo sugere que o modelo ETS, embora tenha mostrado um desempenho consistente antes e depois da validação cruzada, pode se beneficiar de ajustes adicionais e melhorias para garantir a precisão ideal e sua aplicabilidade no mundo real.

    '''

with intro:

    st.subheader('Introdução')

    '''
    Este projeto de Pós-Graduação em Data Analytics, desenvolvido para a FIAP, tem como objetivo construir um modelo preditivo utilizando dados da IBOVESPA para prever o fechamento diário dos preços. Adicionalmente, é necessário justificar a técnica utilizada através de um storytelling claro e convincente, com a meta de alcançar uma acurácia mínima de 70%.

    Para cumprir esses objetivos, várias etapas são necessárias. Primeiramente, aplicar os conhecimentos adquiridos nas disciplinas do curso é crucial, abrangendo desde estatísticas básicas até técnicas avançadas de ciência de dados e modelagem preditiva. A análise exploratória dos dados da IBOVESPA será realizada para identificar padrões e tendências, informando a escolha do modelo preditivo mais adequado. Os dados serão coletados do site [Investing](https://br.investing.com/indices/bovespa-historical-data).

    Diversas técnicas de previsão, como ETS, Auto ARIMA e Prophet, serão implementadas e comparadas em termos de desempenho preditivo. A justificativa das escolhas metodológicas será apresentada de maneira estruturada, destacando a análise dos dados e os insights obtidos.

    A participação nas lives com os docentes será aproveitada para obter orientações e garantir que todas as exigências do desafio sejam cumpridas. Essas sessões oferecem uma oportunidade valiosa para refinar as técnicas utilizadas e melhorar a precisão do modelo.

    Em resumo, este projeto requer a aplicação integrada de habilidades técnicas e analíticas, bem como uma comunicação eficaz, para atingir a acurácia mínima de 70% e proporcionar uma compreensão profunda das escolhas metodológicas realizadas durante o processo.

    '''

with eda:

    raw_data = pd.read_csv('../data/raw/Dados Históricos - Ibovespa (2020-2024).csv', converters={'Data': pd.to_datetime}, thousands='.')

    st.subheader('Raw Data')

    st.write(raw_data.tail())

    '''
    O portal Investing apresenta restrições na quantidade de dados que podem ser importados simultaneamente.

    Para obter a totalidade das informações disponibilizadas sobre o índice IBOVESPA, abrangendo o período de 1992 até a atualidade,
    torna-se necessário a realização de downloads segmentados em três bases de dados distintas.
    '''

    st.subheader('Limpeza dos dados')
    
    '''
    Os dados presentes no dataset original continham informações de data sem a formatação adequada
    e também estavam com os divisores de milhares separados por pontos (.). Necessitando ajustes para prosseguir com as análises
    necessárias.
    '''

    st.subheader('Comportamento das Váriaveis do Dataset')

    '''
    
    '''
    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_feature_behaviors.html', 'r') as f:
        ibov_feature_behaviors = f.read()
    
    # st.html(ibov_feature_behaviors)
    components.html(ibov_feature_behaviors, height=800, width=700)

    '''
    Os dados aparentam ser semelhantes e com uma tendência de alta no longo prazo.
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/distribution_boxplot.html', 'r') as f:
        ibov_distribution_boxplot = f.read()
    
    components.html(ibov_distribution_boxplot, height=400, width=700)

    '''
    A distribuição dos dados não tem diferenças consideráveis dado que a dispersão entre os valores das variáveis são pequenos em relação a amplitude e magnitude dos preços em geral.
    Para efeito de forecast utilizaremos então o preço de fechamento do IBOVESPA, sendo essa uma análise univariada.
    '''

    st.subheader('Comportamento do dataset em diferentes Janelas Temporais')

    '''
    Como o dataset possui informações desde 1992 é interessante avaliar o comportamento dos preços em diferentes janelas temporais
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_timeframe_behaviors.html', 'r') as f:
        ibov_timeframe_behaviors = f.read()

    components.html(ibov_timeframe_behaviors, height=1200, width=700)

    '''
    Conforme visto acima o comportamento dos dados em diferentes janelas temporais são bem diferentes, para realizar um forecast de fechamento do IBOVESPA, provavelmente
    não seja tão interessante utilizar dados muito antigos, dado que as características relacionadas a composição do IBOVESPA de anos atrás já não refletem nos parâmetros atuais.
    Seguindo esse raciocínio, para realizar o modelo utilizaremos os dados de 01 de Janeiro de 2023 até 20 de Junho de 2024

    '''

    st.subheader('Decomposição de Sazonalidade dos Dados')

    '''
    Os dados foram decompostos para melhor entendimento dos componentes subjacentes dos dados.
    De acordo com as visualizações é possível observar alguns comportamentos dos dados:

    De forma geral a tendência indica ser positiva, porém com um comportamento semelhante a de uma escada devido as altas serem relativamente mais expressivas que as
    quedas nos período analisado.

    Os dados apresentam certa sazonalidade entre 500 e -1.000 de acordo com a decomposição e que duram cerca de aproximadamente 45 dias.

    E existe uma cerca constância de ruídos que variam entre 4.300 e -5.000, mas que parecem ter reduzido de forma considerável desde janeiro de 2024.

    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/seasonal_decomposition.html', 'r') as f:
        seasonal_decomposition = f.read()

    components.html(seasonal_decomposition, height=800, width=700)

    st.subheader('Lidando com dados faltantes')
    '''
    Por último antes de iniciar os preparativos para forecasting dos modelos, é necessário ajustar os dados faltantes, já que o mercado de capitais não abre em finais de semana e
    feriados, e manter essas datas sem valores pode compremeter a análise dos nossos modelos.

    Como queremos prever com base em valores anteriores, faz sentido utilizar o ffil (preencher os valores vazios com o último valor disponível), dado que se fossemos fazer
    um modelo de aplicação contínua não teriamos acesso a valores posteriores conforme fossemos atualizando o modelo.

    Com isso podemos seguir com a seleção de modelos de forecast.
    '''

with split:

    st.subheader('Seleção de modelos para Forecast')
    
    '''
    O primeiro passo é selecionar os modelos que utilizaremos para fazer as predições.

    Nessa análise utilizaremos alguns dos sete modelos mais conhecidos, sendo eles: Naive, Theta, Auto Arima, Prophet, Auto ETS, Bayesian Ridge e Decision Tree.
    '''

    st.subheader('Dividindo dataset entre dados de teste e treino')

    '''
    Para a análise foi decidido separar 15 dias para o dataset de treino, devido a alta volatilidade e imprevisibilidade da bolsa de valores (utilizar muitos dados para realizar a previsão se torna inviável sem avaliar fatores
    externos e utilizar poucos dados pode indicar um modelo que não seja tão consistente).
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_train_test_split.html', 'r') as f:
        ibov_train_test_split = f.read()

    st.components.v1.html(ibov_train_test_split, height=400, width=700)

    st.subheader('Cross Validation Splits')

    '''
    Fizemos então uma distribuição de validação cruzada nos dados de teste para assegurar que o modelo seja robusto, capaz de generalizar bem e fornecer previsões precisas ao longo de diferentes períodos temporais.
    Permitindo uma avaliação mais completa e confiável do desempenho do modelo, levando em consideração as variações e tendências inerentes aos dados temporais.
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_train_cross_validation.html', 'r') as f:
        ibov_train_cross_validation = f.read()

    st.components.v1.html(ibov_train_cross_validation, height=400, width=700)

with modelos:

    st.subheader('Justificativa dos Modelos')

    '''
    A escolha dos modelos utilizados nesta análise de previsão do fechamento diário dos preços do IBOVESPA foi guiada por várias considerações técnicas e práticas. Cada modelo foi selecionado com base em suas características únicas e capacidades de capturar diferentes aspectos dos dados financeiros. A seguir, detalhamos a justificativa para a escolha de cada modelo:

    **Naive Forecaster:** Utilizado como benchmark, o modelo Naive faz previsões simples baseadas no último valor observado. Ele é fundamental para comparar a performance de modelos mais complexos e verificar se estão realmente agregando valor preditivo. Apesar de sua simplicidade, ele fornece uma base sólida para avaliar melhorias em modelos mais sofisticados.

    **Theta Forecaster:** O modelo Theta é conhecido por combinar decomposição de séries temporais com técnicas de suavização, sendo eficiente para capturar tendências e padrões sazonais. Isso é particularmente útil para dados financeiros que frequentemente exibem comportamento sazonal e tendências a longo prazo, permitindo uma modelagem mais precisa dessas características.

    **Auto ARIMA:** Este modelo é amplamente utilizado em previsões financeiras devido à sua capacidade de capturar a autocorrelação nos dados de séries temporais de forma automática. O Auto ARIMA ajusta os parâmetros ARIMA (Auto-Regressive Integrated Moving Average) de forma otimizada, oferecendo flexibilidade e robustez na modelagem de dados financeiros complexos.

    **Prophet:** Desenvolvido pelo Facebook, o Prophet é eficaz em lidar com séries temporais que possuem sazonalidade diária, semanal e anual. Ele é capaz de ajustar feriados e eventos especiais, o que é adequado para dados financeiros frequentemente influenciados por tais fatores. Sua facilidade de uso e capacidade de incorporar conhecimento especializado o tornam uma escolha valiosa para previsões financeiras.

    **Auto ETS:** O modelo Exponential Smoothing State Space (ETS) é ideal para capturar componentes de nível, tendência e sazonalidade nos dados. A versão automatizada do ETS seleciona o melhor modelo baseado nos dados fornecidos, tornando-o especialmente útil para previsões financeiras que requerem modelagem de componentes complexos de forma eficiente e precisa.

    **Bayesian Ridge com Desazonalização Condicional e Detrending:** Este modelo combina regressão bayesiana com técnicas de desazonalização e detrending, permitindo capturar relações lineares robustas mesmo em presença de sazonalidade e tendências. Esta abordagem é valiosa para dados financeiros que frequentemente apresentam esses padrões complexos, proporcionando uma modelagem mais robusta.

    **Decision Tree com Desazonalização Condicional e Detrending:** As árvores de decisão são modelos não paramétricos que particionam os dados com base em atributos preditivos. Quando combinadas com desazonalização e detrending, podem capturar interações complexas nos dados financeiros, oferecendo uma abordagem alternativa às técnicas tradicionais. Sua capacidade de lidar com não-linearidades e interações complexas torna-as uma escolha interessante para este tipo de análise.

    A seleção desses modelos visa explorar uma ampla gama de técnicas preditivas, desde abordagens simples e interpretáveis até métodos mais complexos e robustos, permitindo uma análise abrangente e comparativa do desempenho preditivo em dados financeiros.

    '''

    '''
    Inicialmente foram realizadas análises dos modelos sem a validação cruzada para entender o comportamento e resultados no período indicado de previsão.
    '''

    st.subheader('Naive')
    '''
    O modelo Naive é um método simples de previsão onde a previsão para um determinado período é igual ao valor observado no período anterior. 
    É frequentemente usado como um benchmark para avaliar a eficácia de modelos mais complexos devido à sua simplicidade e facilidade de implementação.
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_model_naive.html', 'r') as f:
        ibov_model_naive = f.read()

    st.components.v1.html(ibov_model_naive, height=400, width=700)

    '''
    O desempenho do Naive Forecaster mostrou um MAPE de 0.02 e um R² negativo (-3.06).
    Isso indica que usar o valor observado anterior como previsão não é suficiente para capturar a dinâmica dos preços do Ibovespa.
    '''


    st.subheader('Theta')
    '''
    O modelo Theta decompõe a série temporal em duas ou mais séries Theta e aplica modelos lineares a elas, combinando as previsões dessas séries para gerar a previsão final. 
    É conhecido por seu bom desempenho em séries temporais com tendência e sazonalidade, tornando-o uma escolha robusta para essas características.
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_model_theta.html', 'r') as f:
        ibov_model_theta = f.read()

    st.components.v1.html(ibov_model_theta, height=400, width=700)

    '''
    O Theta Forecaster teve um desempenho inferior, com um MAPE de 0.02 e um R² de -4.49. 
    Esses resultados indicam que este modelo pode não ser a melhor escolha para prever os preços de fechamento do Ibovespa neste contexto.
    '''


    st.subheader('Auto ARIMA')   
    '''
    O Auto ARIMA (AutoRegressive Integrated Moving Average) ajusta automaticamente os parâmetros do modelo ARIMA para melhor se adequar à série temporal. 
    É eficaz em séries temporais que mostram dependências autocorrelacionadas e pode capturar tendências e sazonalidades, sendo amplamente utilizado em diversas aplicações de previsão.
    '''
    
    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_model_auto_arima.html', 'r') as f:
        ibov_model_auto_arima = f.read()

    st.components.v1.html(ibov_model_auto_arima, height=400, width=700)

    '''
    O Auto ARIMA teve um MAPE de 0.02, mas seu R² negativo (-3.06) indica que ele não conseguiu explicar a variância dos dados de teste adequadamente. 
    Este desempenho sugere que, para este caso específico, o Auto ARIMA pode não ser a melhor escolha.
    '''

    
    st.subheader('Prophet')
    '''
    Desenvolvido pelo Facebook, o Prophet é um modelo aditivo que lida bem com séries temporais que têm fortes sazonalidades e períodos de dados ausentes. 
    É ideal para séries temporais com tendências não lineares e múltiplas sazonalidades, oferecendo uma abordagem flexível e robusta para previsões de longo prazo.
    '''    

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_model_prophet.html', 'r') as f:
        ibov_model_prophet = f.read()

    st.components.v1.html(ibov_model_prophet, height=400, width=700)

    ''''
    O Prophet teve um MAPE de 0.04 e um R² de -16.15, demonstrando um desempenho fraco na previsão dos preços de fechamento do Ibovespa. 
    Mesmo sendo um modelo conhecido por lidar bem com sazonalidades, ele não se mostrou adequado para este conjunto de dados.
    '''


    st.subheader('Auto ETS')    
    '''
    O modelo Auto ETS (Exponential Smoothing State Space Model) ajusta automaticamente os parâmetros dos modelos de suavização exponencial (ETS) para melhor se adequar à série temporal. 
    É bom para séries temporais que podem ser decompostas em componentes de nível, tendência e sazonalidade, oferecendo previsões precisas em diversas condições.
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_model_ets.html', 'r') as f:
        ibov_model_ets = f.read()

    st.components.v1.html(ibov_model_ets, height=400, width=700)

    '''
    Este modelo teve o melhor desempenho entre os analisados, com o menor MAPE de 0.01 e um R² de 0.43, indicando que explica 43% da variância dos dados de teste. 
    Esses resultados sugerem que o modelo ETS é promissor e pode ser uma boa escolha para prever o fechamento do preço do Ibovespa.
    '''


    st.subheader('Bayesian Ridge')
    '''
    O Bayesian Ridge é um modelo de regressão linear que utiliza a abordagem bayesiana para calcular a distribuição posterior dos parâmetros do modelo. 
    É útil para séries temporais onde se deseja incorporar incerteza e controle de regularização, proporcionando uma abordagem equilibrada entre precisão e complexidade.
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_model_br_cds.html', 'r') as f:
        ibov_model_br_cds = f.read()

    st.components.v1.html(ibov_model_br_cds, height=400, width=700)

    '''
    Este modelo apresentou um MAPE de 0.03 e um R² de -14.44, indicando um desempenho fraco. A incorporação de desazonalização e detrending condicional não foi eficaz neste caso.
    '''


    st.subheader('Decision Tree')
    '''
    O Decision Tree (Árvore de Decisão) é um modelo preditivo que divide a série temporal em segmentos baseados em critérios de decisão para prever o valor futuro. 
    É eficaz para séries temporais com padrões complexos e interações não lineares entre variáveis, permitindo uma interpretação clara e lógica das decisões de previsão.
    '''

    with open('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/ibov_model_decision_trees.html', 'r') as f:
        ibov_model_decision_trees = f.read()

    st.components.v1.html(ibov_model_decision_trees, height=400, width=700)

    '''
    O desempenho deste modelo foi o pior entre todos, com um MAPE de 0.04 e um R² de -31.79. 
    Isso indica que a árvore de decisão, mesmo com desazonalização e detrending condicional, não é adequada para este problema de previsão.
    '''

    st.subheader('Resultados sem validação cruzada')

    accuracy_without_cross = pd.read_csv('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/accuracy_without_cross.csv')

    st.write(accuracy_without_cross)

    '''
    A análise dos modelos de previsão para o fechamento do preço do IBOVESPA revelou que o modelo ETS apresentou o melhor desempenho inicial, com um MAPE de 0.01 (1%), o que corresponde a uma acurácia de 99%. Este desempenho superior foi complementado por um R² de 0.43, indicando uma boa capacidade de captura da variabilidade dos dados.

    Os modelos Auto ARIMA, Naive Forecaster e Theta Forecaster também tiveram desempenhos notáveis, com MAPE de 0.02 (2%) e acurácia de 98%. No entanto, esses modelos apresentaram R² negativos, sugerindo uma captura limitada da dinâmica dos preços. Modelos como Bayesian Ridge, Prophet e Decision Tree tiveram desempenhos menos satisfatórios, com MAPE variando entre 0.03 e 0.04 (3% a 4%) e acurácia entre 96% e 97%, além de R² fortemente negativos.

    Apesar das altas porcentagens de acurácia, os valores dos preços do IBOVESPA são elevados, e as diferenças percentuais podem representar variações significativas em termos absolutos. Portanto, mesmo com boas porcentagens de acurácia, as previsões ainda precisam ser interpretadas com cuidado devido ao impacto financeiro das variações nos preços.

    '''

    st.subheader('Resultados com validação cruzada')

    accuracy_with_cross = pd.read_csv('/Users/andersonpacheco/Documents/Estudos/01 - Pós Graduacao/Tech Challenge/Ibovespa/ibovespa-prediction/reports/figures/accuracy_with_cross.csv')

    st.write(accuracy_with_cross)

    '''
    A validação cruzada revelou que todos os modelos tiveram um aumento nos erros de previsão em comparação com os resultados iniciais. O modelo ETS, que inicialmente apresentou o melhor desempenho, teve um MAPE de 0.03 (3%) após a validação cruzada, correspondendo a uma acurácia de 97%. Apesar da queda em relação aos resultados iniciais, o ETS ainda manteve uma acurácia bem acima do critério de 70%.

    Os modelos Naive Forecaster, Theta Forecaster e Auto ARIMA também mostraram aumentos no MAPE, mas continuaram com acurácia entre 96% e 97%. Modelos como Bayesian Ridge, Decision Tree e Prophet, que já tinham desempenho inferior, mantiveram acurácia acima de 70%, mas não conseguiram melhorar com a validação cruzada.

    Em resumo, a validação cruzada indicou que todos os modelos, incluindo o ETS, conseguiram manter uma acurácia superior a 70%. No entanto, as variações percentuais, apesar de parecerem pequenas, podem representar diferenças significativas em termos absolutos devido aos altos valores dos preços do IBOVESPA. Isso sugere a necessidade de possíveis ajustes adicionais ou a consideração de técnicas mais avançadas para melhorar a precisão das previsões e garantir a aplicabilidade prática dos modelos.
    '''

with resultados:

    st.subheader('Conclusão')

    '''

    Nesta análise de previsão do preço de fechamento do Ibovespa, diversos modelos foram avaliados quanto ao desempenho preditivo e capacidade de explicação da variância dos dados. Os modelos foram inicialmente testados sem validação cruzada e, posteriormente, sua robustez foi verificada com a aplicação desta técnica.

    **Resultados Sem Validação Cruzada:** O modelo ETS apresentou o melhor desempenho preliminar, com um MAPE de 0.01 e um R² de 0.43, sugerindo boa precisão e capacidade de explicar a variância dos dados. Modelos como Auto ARIMA, Naive Forecaster e Theta Forecaster mostraram um MAPE de 0.02, mas com R² negativos, indicando um desempenho insatisfatório. Modelos mais complexos, incluindo Bayesian Ridge com desazonalização condicional e detrending, Prophet e Decision Tree, tiveram desempenhos inferiores, com MAPE variando entre 0.03 e 0.04 e R² altamente negativos.

    **Resultados Com Validação Cruzada:** A validação cruzada revelou que todos os modelos tiveram um aumento nos erros de previsão em comparação com os resultados iniciais. O modelo ETS, que inicialmente mostrou a melhor performance, apresentou um MAPE de 0.03 (3%) após a validação cruzada, resultando em uma acurácia de 97%. Embora tenha ocorrido uma queda, o modelo ainda manteve uma acurácia acima do critério de 70%. Os modelos Naive Forecaster, Theta Forecaster e Auto ARIMA também mostraram aumentos no MAPE, mas continuaram a ter acurácia entre 96% e 97%. Modelos como Bayesian Ridge, Decision Tree e Prophet, que já apresentavam desempenho inferior, não conseguiram melhorar com a validação cruzada, mas mantiveram acurácia superior a 70%.

    Em resumo, a validação cruzada evidenciou que todos os modelos, incluindo o ETS, mantiveram uma acurácia acima de 70%, apesar do aumento dos erros de previsão. Embora as porcentagens de acurácia sejam relativamente boas, a natureza dos preços elevados do IBOVESPA significa que essas variações percentuais ainda podem representar valores absolutos significativos. Portanto, ajustes adicionais e técnicas mais sofisticadas podem ser necessários para aprimorar a precisão das previsões e garantir a robustez dos modelos em cenários reais.

    **Melhor Modelo e Recomendações para Melhorias:**
    Apesar da queda de desempenho após a validação cruzada, o modelo ETS ainda emergiu como o melhor entre os analisados. No entanto, para aumentar sua acurácia e robustez, várias estratégias podem ser recomendadas:

    1. **Otimização de Hiperparâmetros:** Realizar uma busca mais exaustiva e sistemática de hiperparâmetros utilizando técnicas avançadas como Random Search ou Bayesian Optimization.
    2. **Inclusão de Variáveis Exógenas:** Incorporar variáveis exógenas relevantes, como indicadores econômicos, notícias de mercado, ou outras séries temporais correlacionadas, que possam influenciar os preços do Ibovespa.
    3. **Engenharia de Features:** Desenvolver novas features derivadas dos dados históricos, tais como médias móveis, volatilidade, ou transformações não lineares, para capturar padrões mais complexos nos dados.
    4. **Modelagem Híbrida:** Explorar combinações de modelos, como o ETS com redes neurais recorrentes (LSTM) ou modelos de mistura de Gaussianas, para capturar diferentes aspectos dos dados.
    5. **Regularização e Ensembling:** Aplicar técnicas de regularização para prevenir overfitting e utilizar métodos de ensemble para combinar previsões de múltiplos modelos, melhorando a robustez das previsões.

    A implementação dessas estratégias pode potencialmente melhorar a precisão e a aplicabilidade prática do modelo ETS, ajudando a melhorar a acuracidade dos valores analisados. Futuros trabalhos podem se concentrar em validar estas abordagens e explorar outros modelos e técnicas para continuar melhorando as previsões dos preços de fechamento do Ibovespa.

    '''

    st.subheader('Disclaimer')

    '''
    É importante destacar que a previsão de preços financeiros com base em dados históricos enfrenta limitações significativas. Diversas pesquisas acadêmicas sugerem que tentar prever preços futuros com base em preços passados pode não ser efetivo devido à natureza aleatória dos mercados financeiros.

    Paul A. Samuelson, em seu artigo "Proof That Properly Anticipated Prices Fluctuate Randomly" (1965), argumenta que os preços em mercados eficientes seguem um passeio aleatório. De acordo com a hipótese dos mercados eficientes (EMH), se todos os participantes do mercado têm acesso à mesma informação e agem racionalmente, os preços refletirão toda a informação disponível, tornando impossível prever movimentos futuros com base em dados passados. Samuelson demonstrou matematicamente que, em mercados eficientes, as variações de preços são essencialmente aleatórias e imprevisíveis.

    Além disso, estudos subsequentes corroboram a ideia de que os preços financeiros são influenciados por uma vasta gama de fatores exógenos, incluindo eventos econômicos, políticos, e até mesmo comportamentais, que não podem ser capturados apenas pelos dados históricos de preços. Portanto, a capacidade de modelos preditivos baseados exclusivamente em séries temporais de preços passados é intrinsecamente limitada.

    Embora os modelos analisados nesta pesquisa, como ETS, Auto ARIMA, Prophet, entre outros, tenham mostrado algum grau de eficácia na previsão de preços do Ibovespa, é crucial entender essas limitações. Os resultados obtidos indicam a necessidade de uma abordagem cautelosa ao utilizar esses modelos para previsões financeiras, reconhecendo que a aleatoriedade e a eficiência do mercado impõem desafios significativos à precisão preditiva.

    Portanto, ao considerar a aplicação prática de modelos preditivos para preços financeiros, é fundamental combinar abordagens de modelagem com insights qualitativos e uma compreensão abrangente do contexto de mercado, além de explorar continuamente novas metodologias e técnicas para melhorar a robustez e a precisão das previsões.

    '''

    st.subheader('Bibliografia e Aprofundamento')

    '''     
    Samuelson, P. A. (1965). Proof that Properly Anticipated Prices Fluctuate Randomly. *Industrial Management Review*, 6(2), 41-49. https://www.jstor.org/stable/3003046

    Fama, E. F. (1965). Random Walks in Stock Market Prices. *Financial Analysts Journal*, 21(5), 55-59. https://www.jstor.org/stable/4479810

    Malkiel, B. G. (1973). A Random Walk Down Wall Street. *Financial Analysts Journal*, 29(6), 45-50. https://yourknowledgedigest.org/wp-content/uploads/2020/04/a-random-walk-down-wall-street.pdf
    '''