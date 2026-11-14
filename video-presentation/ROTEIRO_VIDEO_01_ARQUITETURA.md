# Roteiro do Video 01: Visao Executiva e Arquitetura DevSecOps

Roteiro completo de narracao e especificacao visual para o Video 01 (duracao estimada de 5 a 6 minutos, 12 slides Full HD 1920x1080).

Este video aborda a tese central da palestra *The APEX Dev Reinvented*, a transicao para Engenharia de Harness, a governanca dos tres laboratorios e a topologia corporativa sem agentes no servidor de banco de dados.

---

## Cena 01: Abertura & A Ruptura de Paradigma

- **Titulo:** Engenharia Agentica Governada para Oracle e APEX
- **Subtitulo:** A Transicao de Desenvolvedor Low-Code para Engenheiro de Harness e Sistemas Autonomos
- **Fase:** ABERTURA & CONCEITO
- **Narracao (duracao ~27s):**
  "Sejam muito bem-vindos. Nos ultimos anos, a Inteligencia Artificial transformou a engenharia de software, mas a sua adocao em bancos de dados corporativos criticos como Oracle e Oracle Exadata ainda enfrenta forte resistencia. A palestra The APEX Dev Reinvented, apresentada por Bruno Cardoso, expos com maestria essa ruptura: o desenvolvedor tradicional precisa se reinventar como um Engenheiro de Harness."

---

## Cena 02: O Dilema da IA em Bancos de Dados Criticos

- **Titulo:** O Dilema da IA em Ambientes de Producao
- **Subtitulo:** Alucinacao, Amnesia e Riscos Operacionais em Bancos de Dados de Missao Critica
- **Fase:** DIAGNOSTICO DO PROBLEMA
- **Narracao (duracao ~28s):**
  "Modelos de linguagem isolados nao possuem memoria persistente confiavel e desconhecem regras de negocio. Sem amarras tecnicas, um agente de IA pode alucinar, executar comandos destrutivos acidentais, vazar dados sensiveis ou saturar sua propria janela de contexto. Em bancos corporativos de missao critica, a confianca cega em prompts e inaceitavel."

---

## Cena 03: A Equacao da Confiabilidade: Model + Harness = Agent

- **Titulo:** A Equacao da Confiabilidade: Model + Harness = Agent
- **Subtitulo:** Como Envolver o Modelo em Restricoes Deterministicas, Ferramentas Locais e CI/CD
- **Fase:** HARNESS ENGINEERING
- **Narracao (duracao ~28s):**
  "Para tornar a IA confiavel, e mandatorio envolve-la em um harness rigoroso. O harness e o arcabouco composto por ferramentas locais, controle de acesso, gestao de memoria e esteiras de integracao continua. Neste repositorio, implementamos uma esteira DevSecOps completa construida sobre o Oracle Database 23ai e ferramentas oficiais da Oracle."

---

## Cena 04: Lab 01 — Olhos e Algemas para a IA com SQLcl MCP

- **Titulo:** Lab 01: Olhos e Algemas com SQLcl MCP Server
- **Subtitulo:** Integracao Nativa da IDE com o Banco de Dados via Model Context Protocol
- **Fase:** LAB 01: SEGURANCA & PROTOCOLO
- **Narracao (duracao ~27s):**
  "No Laboratorio 01, atacamos o primeiro pilar: a seguranca. O agente de IA jamais conecta como SYS, SYSTEM ou dono do schema. Criamos um container Docker com Oracle 23ai Free e configuramos o Oracle SQLcl atuando como servidor de Model Context Protocol, permitindo que a IDE inspecione metadados de forma governada."

---

## Cena 05: Lab 01 — Menor Privilegio e Auditoria de Sessao

- **Titulo:** Lab 01: Menor Privilegio e Auditoria em Tempo Real
- **Subtitulo:** Restricao QUOTA 0M e Rastreamento de Sessoes via Trigger AFTER LOGON
- **Fase:** LAB 01: SEGURANCA & PROTOCOLO
- **Narracao (duracao ~29s):**
  "Criamos o usuario dedicado MCP_AGENT_RO com QUOTA ZERO na tablespace USERS, impedindo fisicamente qualquer criacao de tabela ou gravacao de dados. Concedemos apenas leitura no dicionario e views dinamicas como V$SQL e V$SQL_PLAN. Toda conexao do agente e registrada automaticamente pela trigger AFTER LOGON em tabela de auditoria."

---

## Cena 06: Lab 02 — O Fenomeno do Context Rot e Progressive Disclosure

- **Titulo:** Lab 02: O Fenomeno do Context Rot e Progressive Disclosure
- **Subtitulo:** Carregando Conhecimento Especializado sob Demanda para Proteger a Memoria do Modelo
- **Fase:** LAB 02: EFICIENCIA DE CONTEXTO
- **Narracao (duracao ~28s):**
  "No Laboratorio 02, enfrentamos o Context Rot: quando a janela de contexto e inundada por dados massivos, o modelo perde atencao e comete erros. Aplicamos o Progressive Disclosure: o agente inicia lendo apenas o catalogo leve MASTER_INDEX com trezentos tokens, ativando skills especializadas de tuning CBO apenas sob demanda."

---

## Cena 07: Lab 02 — Tool Call Offloading com Reducao de 98% de Tokens

- **Titulo:** Lab 02: Tool Call Offloading e Reducao de 98% de Tokens
- **Subtitulo:** Desvio Automatico de Payloads Volumosos para Disco Local com Retorno Estruturado
- **Fase:** LAB 02: EFICIENCIA DE CONTEXTO
- **Narracao (duracao ~29s):**
  "Para consultas volumosas, criamos um utilitario em Python com driver oracledb em modo thin. Se o retorno ultrapassar mil e quinhentos tokens, o payload completo e salvo em disco local e o agente recebe apenas um resumo estruturado e uma amostra de cinco linhas. Reduzimos de trinta e cinco mil para quatrocentos e cinquenta tokens: economia de noventa e oito por cento."

---

## Cena 08: Lab 03 — Schema-as-Code Declarativo com SQLcl Liquibase

- **Titulo:** Lab 03: Schema-as-Code Declarativo com SQLcl Liquibase
- **Subtitulo:** Eliminacao de Scripts Manuais com Controle de Versao e Rastreabilidade Total
- **Fase:** LAB 03: SCHEMA-AS-CODE & GITOPS
- **Narracao (duracao ~28s):**
  "No Laboratorio 03, conectamos o diagnostico da IA a entrega continua. Abolimos a execucao manual de scripts soltos via SQL*Plus. Empregamos o Oracle SQLcl integrado ao Liquibase, capturando a baseline declarativa com o comando generate-schema e versionando os indices recomendados em changesets XML rastreaveis."

---

## Cena 09: Lab 03 — Rollback Obrigatorio e Ganho de 98,7% de I/O

- **Titulo:** Lab 03: Rollback Obrigatorio e Validacao Real no CBO
- **Subtitulo:** Queda Drastica no Custo do Otimizador e Buffer Gets Reduzidos de 317 para 4
- **Fase:** LAB 03: SCHEMA-AS-CODE & GITOPS
- **Narracao (duracao ~29s):**
  "Uma regra inegociavel e aplicada: nenhum changeset e comitado sem o bloco de rollback testado previamente. Apos a aplicacao automatizada pelo Liquibase contra cem mil registros, validamos na view V$SQL: o custo do otimizador CBO despencou de oitenta e oito para tres, e os Buffer Gets cairam de trezentos e dezessete para quatro: economia de noventa e oito virgula sete por cento de I/O."

---

## Cena 10: Arquitetura Corporativa: Zero Agentes no Servidor Exadata

- **Titulo:** Arquitetura Corporativa: Seguranca sem Agentes no Servidor
- **Subtitulo:** Acesso Restrito a Rede SQL*Net e Segregacao Fisica entre Estacoes, Git e Producao
- **Fase:** TOPOLOGIA CORPORATIVA
- **Narracao (duracao ~29s):**
  "No documento Proposito Unificado, consolidamos a premissa de seguranca para comites corporativos: nenhum componente de IA, Python ou Git e instalado dentro do servidor de banco de dados ou cluster Exadata. A comunicacao ocorre exclusivamente via rede SQL*Net padrao, nas portas quinze vinte e um ou vinte e quatro oitenta e quatro."

---

## Cena 11: Estudo de Caso: Transformacao em Manufatura de Alto Volume

- **Titulo:** Estudo de Caso: Manufatura de Calcados de Alto Volume
- **Subtitulo:** Como a Esteira DevSecOps Elimina Paradas de Linha de Montagem e Locks de Producao
- **Fase:** ESTUDO DE CASO REAL
- **Narracao (duracao ~29s):**
  "Aplicamos este modelo no cenario de uma grande industria calçadista com cento e vinte mil pares por dia em APEX. No modelo tradicional, paradas fabris ocorriam por criacao manual de indices e migrações falhas na madrugada. Com a esteira, alteracoes nascem como Pull Requests versionados, sao testadas em homologacao e aplicadas sem locks de producao."

---

## Cena 12: Conclusao, Reprodutibilidade e Creditos Tecnicos

- **Titulo:** Conclusao, Reprodutibilidade e Creditos do Projeto
- **Subtitulo:** Codigo Aberto, Documentacao Completa e Atribuicoes Técnicas do Repositorio
- **Fase:** FECHAMENTO & CREDITOS
- **Narracao (duracao ~29s):**
  "Esta esteira comprova que e perfeitamente viavel unir a velocidade da IA com a seguranca corporativa que a administracao de dados exige. O projeto conta com implementacao e arquitetura de dados desenvolvidas por Arley Ribeiro, DBA de infraestrutura, inspirado na palestra de Bruno Cardoso, com revisao tecnica pela IA Google Gemini. Clone o repositorio e transforme seu fluxo de engenharia. Muito obrigado."
