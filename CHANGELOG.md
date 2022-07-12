# CHANGELOG

## 4.5.0

Melhorias:
- Melhoria de desempenho no identificar Z;

## 4.4.0

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
