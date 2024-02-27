# Queda livre de um objeto - análise estatística


## Introdução

Neste trabalho, fazemos uma breve análise estatística do tempo de queda de um objeto solto do repouso. Simulamos os dados a partir de uma aplicação. Com o conjunto de dados obtido, calculamos a evolução dos valores médios, do histograma de frequência e comparamos a incerteza do valor médio do conjunto com a resolução de um cronômetro de celular.

Segue o link para a aplicação em streamlit:

[queda-livre](https://queda-livre.streamlit.app/)

## Objetivos

O objetivo principal é analisar estatisticamente um conjunto de N medidas do tempo de queda de um objeto solto do repouso. Na aplicação, os tempos são gerados em segundos com duas casas decimais, simulando a resolução de um cronômetro de celular.

Os parâmetros iniciais para a geração do conjunto de dados são:

- altura da queda em metros;
- número de lançamentos (quantidade de medidas do conjunto);
- desvio padrão para o conjunto de medidas.

Os dados da aplicação são gerados a partir de uma distribuição gaussiana com o valor médio sendo o valor de referência calculado a partir da altura fornecida. O desvio padrão pode ser escolhido na entrada do programa. O valor 0.1 dado como *default* é baseado em um conjunto de dados reais analisado abaixo. 

Devido ao sorteio de dados de tempo em uma distribuição gaussiana, a aplicação simula erros aleatórios, não simulando erros sistemáticos nem na medida do tempo nem na medida da altura. Toda a análise estatística da aplicação é feita baseada somente nos erros aleatórios.

A análise fornecida pela aplicação consiste em quatro gráficos.

O primeiro gráfico mostra os dados simulados a partir dos parâmetros de entrada comparado ao valor esperado, calculado como:

$$ t = \sqrt{\frac{2h}{g}} $$

O segundo gráfico mostra o valor médio e a respectiva incerteza (dada pelo desvio padrão dividido pela raiz do número de medidas) para subconjuntos de dados contendo 10%, 20%, 30% ... 100% dos dados. Podemos observar a evolução do valor médio em função da quantidade de medidas do conjunto.

É esperado que valor médio se aproxime do valor de referência quanto maior o conjunto de dados estudado. Se notarmos que os valores médios tendem para um valor diferente do esperado, provavelmente há a presença de erros sistemáticos. No caso da queda livre, o maior erro sistemático pode vir da medida da altura. Esse erro não é levado em conta na aplicação porém, pode ser visto em um conjunto real que usamos para teste (descrição na próxima sessão).

O terceiro gráfico mostra os histogramas de frequência para subconjuntos de dados usando 25%, 50%, 75% e 100% dos dados. Podemos observar a evolução da largura e altura dos histogramas em função da quantidade de dados.

O quarto gráfico mostra a incerteza do valor médio comparada à resolução de um cronômetro de celular. Podemos observar quantas medidas são necessárias para obter um valor médio mais preciso que a resolução do cronômetro.


## Dados para a validação da simulação

A aplicação foi testada a partir de um conjunto real de dados fornecido pelo professor doutor Marcelo M. Sant'Anna da UFRJ. O conjunto é composto de 600 medidas para uma altura de 1.5 m advindas de 5 relatórios de alunos. Com os dados, pude calcular os valores médios e respectivas incertezas, o desvio padrão e os histogramas de frequência para variados subconjuntos de dados. 

No primeiro gráfico, mostrado abaixo, podemos comparar as 600 medidas com o valor esperado. Já é notável que os dados não se distribuem igualmente em torno do valor esperado. É um primeiro indicativo da presença de um erro sistemático.

![gráfico dos dados comparado ao valor esperado](dados.png)

O segundo gráfico, mostrado abaixo, sugere que o valor médio não tende ao valor de referência, tendendo a um valor ligeiramente menor. Isso é altamente sugestivo da presença de um erro sistemático. Na aplicação, não consideramos incerteza na medida da altura, que certamente aparece nos dados reais. É possível que essa diferença seja devido a erros sistemáticos na medida da altura.

![gráfico da evolução do valor médio em função da quantidade de medidas do conjunto](medias.png)

O terceiro gráfico mostra a evolução dos histogramas. Podemos ver, no último, uma concentração de dados um uma coluna mais alta. Mais de 90% dos dados desta coluna correspondem a um único relatório dos 5 estudados.

![histogramas de frequência para 4 frações da quantidade total dos dados](hist.png)

O quarto gráfico mostra que menos de 20% dos dados já são suficientes para ter uma incerteza do valor médio menor que a resolução do cronômetro do celular. Note que isso não significa acurácia. Apesar da boa precisão, os dados dão um resultado pouco acurado, evidenciando a presença de erros sistemáticos nas medições.

![gráfico comparando a resolução do cronômetro com a incerteza dos valores méddo para várias frações do conjunto de dados](desvio.png)

Considerando que o tempo de reação de acionamento do cronômetro é, em média 0.25s e que acionamos 2 vezes para a medição, podemos associar uma incerteza de 0.5 segundo para cada medida feita. Esse valor é praticamente igual ao valor esperado! Com esse trabalho, vemos que a incerteza do valor médio pode ser muito menor que a incerteza individual da medida e até mesmo menor que a resolução do instrumento utilizado. 

Com essa breve análise de dados reais podemos entender a diferença entre erros aleatórios e sistemáticos (não presentes na aplicação) aprendendo a reconhecer o tipo de erro presente no experimento olhando apenas para os resultados.


## Referências bibliográficas

- Apostila de Física Experimental 1 da UFRJ.
- Relatórios anônimos fornecidos pelo professor da disciplina Física Experimental 1 da UFRJ, Marcelo M. Sant'Anna.

-----------------------------------------------------------------------------
MP-resuldados
Dos dados aos resultados. Um pouco de física, matemática, negócios e finanças.
