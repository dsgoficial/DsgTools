![DSGTools](https://github.com/dsgoficial/DsgTools/assets/6131641/fc2511a4-607b-4ce6-a24c-96b390be2739)

#

[![Join the chat at https://gitter.im/DsgTools/Lobby](https://badges.gitter.im/DsgTools/Lobby.svg)](https://gitter.im/DsgTools/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![DOI](https://zenodo.org/badge/25019920.svg)](https://zenodo.org/badge/latestdoi/25019920)

|branch|status|version|
|-------|--------|--------|
|master|[![unittests](https://github.com/dsgoficial/DsgTools/actions/workflows/test_plugin_on_qgis.yml/badge.svg?branch=master)](https://github.com/dsgoficial/DsgTools/actions/workflows/test_plugin_on_qgis.yml)|4.18.1|
|dev|[![unittests](https://github.com/dsgoficial/DsgTools/actions/workflows/test_plugin_on_qgis.yml/badge.svg?branch=dev)](https://github.com/dsgoficial/DsgTools/actions/workflows/test_plugin_on_qgis.yml)|4.19.6|

------------------------------------
# Complemento DSGTools

O DSGTools é um complemento para o QGIS (http://qgis.org/pt_BR/site/) que permite aos usuários a criação e utilização de produtos cartográficos de acordo com as especificações da ET-EDGV. O DSGTools visa atender não apenas o Exército Brasileiro, mas também produtores e usuários de geoinformação da sociedade.

## Enquadramento Estratégico Atual

Este projeto visa cumprir a missão estabelecida no Plano Estratégico do Exército 2024-2027 (PEEx 2024-2027), relativo ao seguinte Objetivo Estratégico do Exército (OEE):
* OEE 6 - Aperfeiçoar os Sistemas de Informação e de Comando e Controle do Exército
* Estratégia 6.3 - Ampliação das capacidades de produção e disseminação de geoinformação
* Iniciativa 6.3.1.1 - Ampliar a capacidade de uso de geoinformação digital da F Ter
* Iniciativa 6.3.2.1 - Obter sistemas de produção de geoinformação com o uso de Inteligência Artificial

## Principais Funcionalidades

O plugin está na versão 4.17.27 e possui as seguintes funcionalidades:

### Gestão de Bancos de Dados
- Criação de bancos de dados em Spatialite e PostGIS de acordo com os modelos EDGV 2.1.3, EDGV 3.0, EDGV 3.0 Pro, EDGV 3.0 Orto e EDGV 3.0 Topo
- Criação, armazenamento e remoção de configuração de servidores PostGIS
- Conversão entre formatos de bancos de dados (PostGIS para Spatialite e vice-versa)
- Conversão de dados entre modelagens de banco no formato PostGIS utilizando o json de mapeamento
- Validação da estrutura do banco de dados em relação ao masterfile

### Carregamento e Gestão de Camadas
- Carregamento de camadas por classe, categoria, primitiva geométrica e esquema
- Ferramentas para carregar shapefiles, camadas PostGIS Raster e temas

### Edição e Manipulação de Feições
- Manipulação de feições complexas (criação, edição, remoção, zoom, associação e desassociação)
- Menu de classificação para aquisição de feições
- Menu de aquisição de feições
- Ferramentas de aquisição com ângulos retos e à mão livre
- Ferramenta para inverter sentido de linhas (flip)
- Ferramentas para indicar tamanho da feição durante aquisição

### Validação e Controle de Qualidade
- Ferramentas de validação geométrica (identificação e correção)
- Ferramentas para identificar geometrias inválidas, vértices duplicados, Z, ângulos e densidades incorretas
- Controle de Qualidade e Workflow Toolbox com ferramentas de validação específicas
- Identificação de feições fechadas, não unidas, entrelaçadas e próximas
- Validação de atributos e verificação de atributos Unicode

### Integração de Dados
- Acesso a serviços WM(T)S do BDGEx
- Acesso ao mapa índice de produtos vetoriais e matriciais do BDGEx
- Ferramenta de Inventário de Dados Geoespaciais suportados pela GDAL/OGR

### Processamento Topológico
- Ferramentas de Snap Hierárquico
- Ferramentas de construção de polígonos por linha e centroide
- Ferramentas para adicionar vértices em intersecções e segmentos compartilhados

### Processamento de Dados Específicos
- Ferramentas para processamento de redes de drenagem e terreno
- Direcionamento de fluxo de drenagens e identificação de inconsistências
- Ferramentas para extração de pontos cotados e validação do terreno
- Ferramentas para numeração de polígonos e generalização

### Gerenciamento de Usuários e Segurança
- Gerenciamento de permissões de usuários
- Criação/Remoção de usuários no PostgreSQL
- Alteração de senha de usuários no PostgreSQL

### Outros
- Visualizador de valores de códigos da EDGV para auxiliar em consultas por atributos
- Ferramenta para preparação de arquivos para empacotamento no BDGEx
- Ferramentas para simulação e filtros espaciais

O plugin foi todo desenvolvido em Python e está disponível para download pelo próprio QGIS ou pelo endereço http://plugins.qgis.org/plugins/DsgTools/.

Para acessar o histórico completo de mudanças, visite: https://github.com/dsgoficial/DsgTools/wiki/Changelog-4.3

Para maiores informações, acesse https://github.com/dsgoficial/DsgTools/wiki ou https://bdgex.eb.mil.br/portal/index.php?option=com_content&view=article&id=96&Itemid=380&lang=pt

## Requisitos para Linux (Ubuntu/Debian)

Instalar os seguintes pacotes de acordo com o código abaixo:
```
sudo apt-get install libqt5sql5-psql
sudo apt-get install libqt5sql5-sqlite
```

------------------------------------
# DSGTools Plugin

DSGTools is a QGIS plugin that allows users to create and manipulate Geospatial Data according to Brazilian standards (ET-EDGV). DSGTools aims to provide tools not only to the Brazilian Army but to the GIS community in general.

## Strategic Framework

This project fulfills the mission established in the Brazilian Army Strategic Plan 2024-2027 (PEEx 2024-2027), related to the following Army Strategic Objective (OEE):
* OEE 6 - Improving the Army's Information and Command and Control Systems
* Strategy 6.3 - Expanding geoinformation production and dissemination capabilities
* Initiative 6.3.1.1 - Expand the capability of using digital geoinformation for the Land Force
* Initiative 6.3.2.1 - Obtain geoinformation production systems using Artificial Intelligence

## Main Features

The plugin is in version 4.17.27 and has the following features:

### Database Management
- Database creation using Spatialite and PostGIS according to EDGV 2.1.3, EDGV 3.0, EDGV 3.0 Pro, EDGV 3.0 Orto, and EDGV 3.0 Topo models
- Creation, storage, and deletion of PostGIS server configurations
- Conversion between database formats (PostGIS to Spatialite and vice versa)
- Database structure validation against the masterfile

### Layer Loading and Management
- Layer loading by class, category, geometric primitive, and schema
- Tools for loading shapefiles, PostGIS Raster layers, and themes

### Feature Editing and Manipulation
- Complex features manipulation (creation, editing, deletion, zoom, association, disassociation)
- Classification menu for feature acquisition
- Feature reclassification tools
- Right-angle and freehand acquisition tools
- Line direction flip tool
- Tools to indicate feature size during acquisition

### Validation and Quality Control
- Geometric validation tools (identification and correction)
- Tools to identify invalid geometries, duplicate vertices, Z values, angles, and incorrect densities
- Quality Control and Workflow Toolbox with specific validation tools
- Identification of closed, unmerged, intertwined, and nearby features
- Attribute validation and Unicode attribute verification

### Data Integration
- Access to BDGEx WM(T)S services
- Access to BDGEx vector and raster product index map
- Geospatial Data Inventory Tool supported by GDAL/OGR

### Topological Processing
- Hierarchical Snap tools
- Polygon construction from lines and centroids
- Tools to add vertices at intersections and shared segments

### Specific Data Processing
- Drainage networks and terrain processing tools
- Drainage flow direction and inconsistency identification
- Tools for spot elevation extraction and terrain validation
- Tools for polygon numbering and generalization

### User and Security Management
- User permissions management
- User creation/removal in PostgreSQL
- Password changing for PostgreSQL users

### Others
- EDGV code list viewer to aid attribute queries
- Tool for preparing files for packaging in BDGEx
- Simulation tools and spatial filters

The plugin was fully developed in Python and is available for download through QGIS or from http://plugins.qgis.org/plugins/DsgTools/.

For the complete changelog, visit: https://github.com/dsgoficial/DsgTools/wiki/Changelog-4.3

For further information, go to https://github.com/dsgoficial/DsgTools/wiki or https://bdgex.eb.mil.br/portal/index.php?option=com_content&view=article&id=96&Itemid=380&lang=pt

## Requirements for LINUX (Ubuntu/Debian)

Install the following packages as follows:
```
sudo apt-get install libqt5sql5-psql
sudo apt-get install libqt5sql5-sqlite
```
