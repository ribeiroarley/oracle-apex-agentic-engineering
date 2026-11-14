# Roteiro do Video 02: Implementacao Pratica Passo a Passo

Roteiro completo de narracao e especificacao visual para o Video 02 (duracao estimada de 5 a 6 minutos, 12 slides Full HD 1920x1080).

Este video e um tutorial hands-on focado na execucao pratica de cada um dos tres laboratorios a partir do zero: subindo o banco em Docker, configurando o servidor SQLcl MCP, ativando skills de tuning, executando tool call offloading e aplicando migrações com SQLcl Liquibase.

---

## Cena 01: Abertura Hands-On & Pre-requisitos do Ambiente

- **Titulo:** Implementacao Pratica da Esteira DevSecOps para Oracle
- **Subtitulo:** Guia Hands-On Passo a Passo: Docker, SQLcl MCP, Harness Engineering e Liquibase do Zero
- **Fase:** ABERTURA HANDS-ON
- **Narracao (duracao ~27s):**
  "Ola a todos. Neste segundo video, vamos colocar as maos na massa e reproduzir passo a passo toda a esteira DevSecOps implementada neste repositorio. Voce vai aprender como subir o Oracle Database 23ai em Docker, salvar conexoes seguras no SQLcl, registrar o servidor MCP no VS Code, criar skills de IA e versionar esquemas com Liquibase."

---

## Cena 02: Etapa 1.1 — Variaveis de Ambiente e Seguranca no Git

- **Titulo:** Etapa 1.1: Variaveis de Ambiente e Seguranca no Git
- **Subtitulo:** Isolamento de Credenciais Locais com .env.lab e Protecao Rigorosa no .gitignore
- **Fase:** ETAPA 1: BANCO & DOCKER
- **Narracao (duracao ~27s):**
  "O primeiro passo de seguranca e clonar o repositorio e copiar o modelo de variaveis de ambiente: ponto env ponto lab ponto example para ponto env ponto lab. No arquivo ponto gitignore, garantimos que credenciais locais, wallets e arquivos de cache jamais sejam comitados no GitHub, mantendo o repositorio cem por cento seguro contra vazamentos."

---

## Cena 03: Etapa 1.2 — Subindo o Container Oracle 23ai Free

- **Titulo:** Etapa 1.2: Inicializacao do Container Oracle 23ai Free
- **Subtitulo:** Provisionamento Declarativo com Nomes Fixos, Volume Persistente e Rede Bridge
- **Fase:** ETAPA 1: BANCO & DOCKER
- **Narracao (duracao ~28s):**
  "Para iniciar o banco de dados, executamos o comando docker compose apontando para o arquivo de ambiente do laboratorio um. Definimos nomes deterministas para o container, volume persistente e rede bridge. Acompanhamos os logs com docker logs ate visualizar a mensagem de confirmacao: Database is ready to use."

---

## Cena 04: Etapa 1.3 — Scripts de Governanca, HR e Trigger de Auditoria

- **Titulo:** Etapa 1.3: Scripts de Inicializacao e Governanca
- **Subtitulo:** Provisionamento do Schema HR, Usuario MCP_AGENT_RO com QUOTA 0M e Trigger AFTER LOGON
- **Fase:** ETAPA 1: BANCO & DOCKER
- **Narracao (duracao ~28s):**
  "Durante o boot do container, o script zero um cria o schema HR e o usuario dedicado MCP_AGENT_RO com cota zero na tablespace USERS e sinonimos privados. Em seguida, a trigger de banco intercepta o logon do agente gravando metadados na tabela de auditoria. O script zero dois popula cem mil linhas na tabela de logs para testes de tuning."

---

## Cena 05: Etapa 2.1 — Conectando com SQLcl e Salvando Conexao Nomeada

- **Titulo:** Etapa 2.1: Salvando a Conexao Segura no Oracle SQLcl
- **Subtitulo:** Eliminacao de Senhas em Arquivos JSON com Conexoes Nomeadas Salvas no Host
- **Fase:** ETAPA 2: SQLCL & MCP SERVER
- **Narracao (duracao ~29s):**
  "Com o banco operacional, configuramos o Oracle SQLcl local. Para nao expor senhas em texto puro nos arquivos de configuracao do agente de IA, executamos o comando conn menos save mcp underline hr underline lab com o parametro savepwd. A conexao fica gravada de forma criptografada e segura no perfil do desenvolvedor."

---

## Cena 06: Etapa 2.2 — Registrando o Servidor MCP no VS Code

- **Titulo:** Etapa 2.2: Registrando o Servidor MCP no VS Code
- **Subtitulo:** Integracao do SQLcl em Modo Servidor via stdio com Ferramentas Nativas de IA
- **Fase:** ETAPA 2: SQLCL & MCP SERVER
- **Narracao (duracao ~28s):**
  "No arquivo de configuracao MCP da sua IDE, como o mcp ponto json do VS Code, registramos o servidor chamando o comando sql com os argumentos menos mcp e menos name apontando para a conexao mcp underline hr underline lab. A partir deste instante, o assistente de IA ganha ferramentas nativas para inspecionar tabelas e planos de execucao."

---

## Cena 07: Etapa 3.1 — Progressive Disclosure: Master Index e Skills

- **Titulo:** Etapa 3.1: Progressive Disclosure na Pratica
- **Subtitulo:** Catalogo Leve MASTER_INDEX.md e Ativacao sob Demanda da SKILL_DBA_TUNING_AUDIT.md
- **Fase:** ETAPA 3: HARNESS & OFFLOADING
- **Narracao (duracao ~28s):**
  "No Laboratorio zero dois, estruturamos o catalogo MASTER_INDEX ponto md dentro da pasta skills. Ele consome apenas trezentos tokens e orienta o agente a carregar a skill de auditoria CBO somente quando o usuario solicita a analise de uma query com a tag MCP TUNING TARGET, preservando a memoria do modelo contra saturacao."

---

## Cena 08: Etapa 3.2 — Executando Tool Call Offloading em Python

- **Titulo:** Etapa 3.2: Executando Tool Call Offloading em Python
- **Subtitulo:** Interceptacao de Consultas Volumosas com oracledb Thin Mode e Cache em Disco
- **Fase:** ETAPA 3: HARNESS & OFFLOADING
- **Narracao (duracao ~29s):**
  "Criamos o utilitario offload underline query ponto py utilizando o driver oracledb em modo thin. Quando executamos uma consulta que retorna quinhentas linhas da tabela de logs, o script detecta que o volume ultrapassa mil e quinhentos tokens, salva o json completo na pasta de cache e imprime no terminal apenas o resumo com amostra de cinco linhas."

---

## Cena 09: Etapa 4.1 — Capturando Baseline Declarativa com Liquibase

- **Titulo:** Etapa 4.1: Captura de Baseline com SQLcl Liquibase
- **Subtitulo:** Extracao Automatizada do Schema HR via lb generate-schema em XML Declarativo
- **Fase:** ETAPA 4: GITOPS & LIQUIBASE
- **Narracao (duracao ~28s):**
  "No Laboratorio zero tres, iniciamos o versionamento do banco de dados. Conectamos no SQLcl com a conta administrativa do schema HR e executamos o comando lb generate underline schema dentro da pasta baseline. O SQLcl extrai automaticamente todas as tabelas, sequences e constraints em arquivos XML declarativos e versionaveis."

---

## Cena 10: Etapa 4.2 — Criando Changeset Incremental com Rollback

- **Titulo:** Etapa 4.2: Changeset dos Indices e Master Controller
- **Subtitulo:** Codificacao do XML de Migracao com Bloco de Reversao Obrigatorio e Rastreabilidade
- **Fase:** ETAPA 4: GITOPS & LIQUIBASE
- **Narracao (duracao ~29s):**
  "Com base no diagnostico da IA, criamos o arquivo v um ponto um ponto zero tuning indexes ponto xml contendo os tres indices recomendados. Cada alteracao possui obrigatoriamente a tag rollback para caso de falha. No controller mestre em XML, registramos a baseline e o changeset incremental, garantindo ordem de execucao deterministica."

---

## Cena 11: Etapa 4.3 — Aplicando Migrações e Isolamento com Git Worktrees

- **Titulo:** Etapa 4.3: Deploy com lb update e Git Worktrees
- **Subtitulo:** Execucao Transacional de Migracao e Trabalho Paralelo sem Conflitos de Branch
- **Fase:** ETAPA 4: GITOPS & LIQUIBASE
- **Narracao (duracao ~28s):**
  "Para aplicar os indices no banco, executamos o comando lb update apontando para o arquivo controller ponto xml. O Liquibase aplica as alteracoes e registra os hashes na tabela DATABASECHANGELOG. Com o comando git worktree add, demonstramos como equipes e agentes trabalham em branches paralelos sem interferir na branch principal."

---

## Cena 12: Fechamento Hands-On & Checklist de Producao

- **Titulo:** Conclusao da Implementacao & Checklist de Sucesso
- **Subtitulo:** Reprodutibilidade Garantida, Governanca CISO e Atribuicoes Técnicas do Projeto
- **Fase:** FECHAMENTO HANDS-ON
- **Narracao (duracao ~28s):**
  "Completamos o ciclo completo de engenharia agentica: banco seguro, protocolo MCP ativo, economia de noventa e oito por cento de tokens e deploys auditados com Liquibase. O projeto conta com implementacao e arquitetura de dados por Arley Ribeiro, inspirado na palestra de Bruno Cardoso, com revisao tecnica pela IA Google Gemini. Todos os codigos estao prontos para execucao. Bons estudos."
