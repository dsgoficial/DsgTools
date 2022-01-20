# CHANGELOG

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
