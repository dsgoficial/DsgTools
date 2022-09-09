# CHANGELOG

## 4.6.0

Novas funcionalidades:
- Novo processo de estender linhas próximas da moldura;

Melhorias:
- Adicionada a opção de atribuir um id de atividade para o grid de revisão criado no processo de criar grid de edição;
- Melhorado o estilo do grid utilizado pela barra de ferramentas de revisão;

## 4.5.0 - 2022-09-08

Novas funcionalidades:
- Novo processo de identificar undershoot de polígonos;
- Novo processo de identificar erros de construção de redes (linhas que compartilham vértices não segmentadas dentro da camada, linhas não segmentadas com as camadas de filtro);
- Novo processo de identificar linhas com mesmo conjunto de atributos não unidas;
- Novo processo de carregamento de primeira camada com elemento de um csv (utilizado na construção de modelos);
- Novo processo de identificação de problemas no fluxo de drenagens;
- Novo processo de construir fatiamento do terreno segundo as regras do MTM;
- Novo processo de ativar a remoção automática de vértices nas camadas;
- Novo processo de bloquear a edição de atributos;
- Novo processo de identificar loops em drenagens;
- Novo processo de identificar problemas de direcionamento com elementos da rede (massas d'água com e sem fluxo, oceano, vala, sumidouro e vertedouro);
- Novo processo de identificar problemas nos ângulos entre os trechos de drenagem (verificar deltas);
- Nova barra de ferramentas de revisão;
- Novo processo de construir grid de revisão;

Melhorias:
- Melhoria de desempenho no identificar Z;
- Melhoria de desempenho no identificar geometrias inválidas;
- Melhoria de desempenho no identificar dangles;
- Melhoria no processo de validação do terreno (removidos os falso-positivos com a moldura);

Correção de bug:
- Tratamento de geometria nula no Identify Out Of Bounds Angles in Coverage;

## 4.4.0 - 2022-07-12

Novas funcionalidades:

- Nova ferramenta de alternar visibilidade de raster;
- Novo processo de remover camadas vazias do projeto (portado do Ferramentas Experimentais);
- Novo processo de identificar vértices duplicados;
- Novo processo de identificar feições com densidade alta de vértices;

Melhorias:
- Refatoração da interface de carregamento de camadas (remoção de funcionalidades não utilizadas e melhoria no filtro de camadas);
- Adicionadas flags de delimitador não utilizado no algoritmo Construir Polígonos com Delimitadores e Centroides;
- Adicionada a opção de verificar geometrias inválidas nos polígonos montados no algoritmo Construir Polígonos com Delimitadores e Centroides;
- Adicionada a opção de unir os polígonos com mesmo conjunto de atributos na saída do Construir Polígonos com Delimitadores e Centroides;
- Adicionado botão de mudar camada da barra de inspeção de raster pela camada ativa;
- Ferramenta de controle de qualidade agora agrupa as camadas carregadas em grupos;
- Ferramenta de contole de qualidade agora diferencia camadas carregadas nos processos de flags, por meio de parâmetro de configuração;
- Adicionada a opção de ignorar feições circulares no processo de identificar ângulos errados em edificações;
- Refatorado o processo de atribuir regras de atributação ao formulário de feições;
- Refatorado o processo de identificar overlaps. Agora ele também pega overlaps de linhas;
- Adicionada a opção de ordenar no inspetor de feições por um atributo;

Correção de Bug:

- Filtro de expressão do inspetor de feições agora é limpo quando o botão de trocar para a camada ativa é acionado;
- Corrigido o bug da ferramenta de aliases retirando os mapas de valores;

## 4.3.2 - 2022-05-30

Correção de bugs:

- Correção do proxy para os serviços https do BDGEx

## 4.3.1 - 2022-05-30

Novas funcionalidades:
- Adicionado processo de verificação de caracteres unicode;
- Adicionados parâmetros de densidade de pontos na criação de molduras;
- Adicionados novos casos no processo de identificação de geometrias inválidas (buraco intersectando fronteira de polígono);

Correção de bugs:
- Correção no template da EDGV 3.0;
- Correção nos endereços do BDGEx;
- Correção na janela de opções do DSGTools;
- Ajustado o número de casas decimais no snap hierárquico;
- Corrigido bug na SQL de filtragem do carregamento de camadas com elementos quando se utiliza o postgres mais novo;

## 4.3.0 - 2022-01-20

Novas funcionalidades:
- Novo menu de classificação

Novos algoritmos:
- Corretor ortográfico
- Verifica o UUID das feições
- Verifica a sobreposição de curvas de nível
- Identifica pequenos buracos
- Identifica interseções entre curvas de nível e linhas de drenagem
- Carrega um shapefile

Melhorias:
- Adequação dos processings de camadas para ser compatível com o SAP
- Compatibilidade com QGIS 3.22

Correção de bugs:
- Ferramenta de inspeção de feições, agora mostra a aproximação correta quando utilizado em linha ou áreas em latlong com porcentagem inferior a 100%
- O problema onde a Ferramenta de Aquisição com Ângulos Retos e a Ferramenta de Aquisição à Mão Livre não atribuíam os valores padrões nos formulários da feição foi corrigido
- Correção nos processings de geração de MI: remover MI que não existem

Changelog completo: https://github.com/dsgoficial/DsgTools/wiki/Changelog-4.3
