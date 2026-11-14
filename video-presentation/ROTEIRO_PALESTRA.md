# Roteiro Tecnico da Apresentacao: Engenharia Agentica Governada para Oracle

Roteiro completo de narracao e especificacao visual para a apresentacao tecnica em video (duracao estimada de 5 a 6 minutos, Full HD 1920x1080).

Este material aborda a esteira DevSecOps corporativa integrando Oracle Database 23ai, Oracle Exadata, Oracle APEX, Model Context Protocol (MCP), Harness Engineering e versionamento declarativo com SQLcl Liquibase.

---

## Cena 1: Capa e o Desafio da IA em Bancos de Dados Criticos

- **Titulo do Slide:** Engenharia Agentica Governada para Oracle Database, Exadata e APEX
- **Subtitulo:** Da Tela Visual ao Harness Engineering: Como Adotar Agentes de IA com Seguranca, Privilegio Minimo e Zero Risco Operacional
- **Elementos Visuais:**
  - Identidade visual Dark Tech (fundo escuro, tipografia limpa, acentos em ciano e laranja).
  - Diagrama conceitual: `LLM Puro (Alucinacao e Amnesia)` versus `LLM + Harness = Agente Confiavel`.
  - Badges de tecnologia: Oracle Database 23ai, Oracle APEX, SQLcl MCP, Liquibase, GitOps.
- **Narracao (pt-BR-AntonioNeural, duracao ~50s):**
  "Sejam muito bem-vindos. Nos ultimos anos, a Inteligencia Artificial transformou o desenvolvimento de software, mas a sua adocao em bancos de dados corporativos criticos como Oracle e Oracle Exadata ainda enfrenta uma barreira compreensivel: o medo legitimo de alucinacoes, comandos destrutivos acidentais, vazamento de dados sensiveis e degradacao de contexto. A palestra The APEX Dev Reinvented, apresentada por Bruno Cardoso, expos com maestria essa mudanca de paradigma: o desenvolvedor low-code tradicional precisa se reinventar como um Engenheiro de Harness. Modelos de linguagem isolados nao possuem memoria confiavel e desconhecem regras de negocio. Para torná-los seguros, e obrigatorio envolve-los em um harness rigoroso com ferramentas locais, politicas de seguranca e esteiras de entrega continua. Neste video, demonstraremos a implementacao pratica e funcional de uma esteira DevSecOps completa construida sobre o Oracle Database 23ai e ferramentas oficiais da Oracle."

---

## Cena 2: Laboratorio 01 — Governanca e Acesso Seguro via SQLcl MCP Server

- **Titulo do Slide:** Laboratorio 01: Olhos e Algemas para a IA com SQLcl MCP Server
- **Subtitulo:** Principio do Menor Privilegio, Auditoria Nativa e Conexao Segura via Model Context Protocol
- **Elementos Visuais:**
  - Diagrama de conectividade: `Cliente de IA (VS Code)` <---> `Oracle SQLcl (modo MCP)` <---> `Oracle Database 23ai (Porta 1521)`.
  - Caixa de Governanca: Usuario dedicado `MCP_AGENT_RO`, restricao `QUOTA 0M ON USERS`, sem privilegios de DML ou DDL.
  - Trecho de codigo SQL real: Trigger de auditoria de conexao `SYSTEM.TRG_AUDIT_MCP_AGENT_LOGON` gravando `OS_USER`, `MODULE` e `IP_ADDRESS`.
- **Narracao (pt-BR-AntonioNeural, duracao ~55s):**
  "No Laboratorio 01, atacamos o primeiro pilar fundamental: a governanca de acesso. Agentes de IA jamais devem se conectar a bancos corporativos utilizando contas privilegiadas como SYS, SYSTEM ou o proprio dono do schema da aplicacao. Provisionamos o Oracle Database 23ai Free em container Docker com nomes deterministas e criamos o usuario dedicado MCP_AGENT_RO. Esta conta opera com QUOTA ZERO na tablespace USERS, impedindo categoricamente a criacao de qualquer segmento de dados ou execucao de DDL e DML em tabelas de negocio. Concedemos apenas leitura no dicionario e em views de performance como V$SQL e V$SQL_PLAN, alem de sinonimos privados transparentes. Toda sessao aberta pelo agente e interceptada em tempo real pela trigger de banco TRG_AUDIT_MCP_AGENT_LOGON, persistindo metadados de auditoria. A comunicacao entre a IDE e o banco ocorre por meio do Oracle SQLcl atuando como servidor oficial de Model Context Protocol."

---

## Cena 3: Laboratorio 02 — Harness Engineering, Progressive Disclosure e Offloading

- **Titulo do Slide:** Laboratorio 02: Harness Engineering e Mitigacao de Context Rot
- **Subtitulo:** Progressive Disclosure sob Demanda e Reducao de 98% no Consumo de Tokens com Tool Call Offloading
- **Elementos Visuais:**
  - Fluxograma de decisao: `Prompt do Usuario` -> `MASTER_INDEX.md (~300 tokens)` -> `Ativacao da Skill sob Demanda`.
  - Diagrama do Offloading: Consulta SQL -> Avaliacao de Densidade (`len(JSON)/4`) -> Se >= 1.500 tokens -> Dump em Disco -> Resumo no Contexto.
  - Destaque metrico: 35.385 tokens brutos reduzidos para ~450 tokens injetados na janela de contexto.
- **Narracao (pt-BR-AntonioNeural, duracao ~55s):**
  "No Laboratorio 02, enfrentamos o fenomeno do Context Rot: quando a janela de contexto do LLM e inundada por dados massivos, o modelo se torna lento, perde atencao e comete erros graves. Para solucionar isso, implementamos dois padroes arquiteturais. O primeiro e o Progressive Disclosure: em vez de injetar dezenas de manuais de uma vez, fornecemos apenas o catalogo leve MASTER_INDEX, consumindo meros trezentos tokens. O agente carrega a skill especializada, como a de auditoria CBO, estritamente quando detecta o gatilho da solicitacao. O segundo padrao e o Tool Call Offloading: criamos um utilitario em Python que conecta via Oracle Thin Client e analisa o volume retornado. Se a consulta exceder mil e quinhentos tokens, ela e interceptada e salva em disco local. O agente recebe apenas um resumo estruturado e uma amostra de cinco linhas, comprovando na pratica uma reducao de noventa e oito por cento de tokens consumidos."

---

## Cena 4: Laboratorio 03 — Versionamento Schema-as-Code com SQLcl Liquibase

- **Titulo do Slide:** Laboratorio 03: GitOps Declarativo com SQLcl Liquibase
- **Subtitulo:** Do Diagnostico Agentico ao Changeset Declarativo com Rollback Obrigatorio e Validacao CBO
- **Elementos Visuais:**
  - Trecho do XML Liquibase: `v1.1.0-tuning-indexes.xml` destacando os blocos `<changeSet>` e a tag obrigatoria `<rollback>`.
  - Tabela comparativa real do laboratório:
    - Consulta `q1_emp_lookup`: Custo CBO caiu de 88 para 3; Buffer Gets reduzidos de 317 para 4 (-98,7% de I/O).
  - Tabela de controle corporativo: `DATABASECHANGELOG` garantindo rastreabilidade com hash MD5 e autor.
- **Narracao (pt-BR-AntonioNeural, duracao ~55s):**
  "No Laboratorio 03, resolvemos o elo final da esteira: como transformar o diagnostico da IA em uma alteracao segura no banco de dados. Abolimos completamente a execucao manual de scripts soltos via SQL*Plus. Empregamos o Oracle SQLcl integrado nativamente ao Liquibase. Extraimos a baseline declarativa completa do schema com o comando generate-schema e encapsulamos as recomendacoes de indices identificadas na auditoria em um changeset XML semantico. Uma regra inegociavel de governanca e aplicada: nenhum changeset e comitado sem o bloco de rollback correspondente devidamente testado. Apos a aplicacao automatizada pelo Liquibase, executamos as consultas novamente contra cem mil registros. O custo do otimizador CBO despencou de oitenta e oito para tres, e os Buffer Gets cairam de trezentos e dezessete para apenas quatro, alcancando noventa e oito virgula sete por cento de economia de I/O."

---

## Cena 5: Arquitetura Corporativa — Zero Agentes no Servidor Exadata

- **Titulo do Slide:** Topologia Corporativa: Seguranca Maxima sem Agentes no Servidor
- **Subtitulo:** Acesso Restrito a Rede SQL*Net e Segregacao Fisica entre Estacoes, Git, CI/CD e Producao
- **Elementos Visuais:**
  - Topologia em 4 camadas corporativas:
    1. `Estacao Engenheiro / DBA (VS Code + MCP + Skills)`
    2. `Servidor Git Corporativo (Pull Requests + Code Review)`
    3. `Runner de CI/CD (SQLcl Headless + Liquibase)`
    4. `Ambientes Homologacao e Producao (Oracle Database / Exadata Cluster)`
  - Destaque em banner: "Zero Agentes de IA, Python ou Git instalados no Servidor de Producao ou Exadata".
- **Narracao (pt-BR-AntonioNeural, duracao ~55s):**
  "Um dos pontos mais sensiveis para diretores de tecnologia e equipes de infraestrutura e entender onde os componentes residem fisicamente. No documento Proposito Unificado, consolidamos uma premissa mandatoria: nenhum agente de IA, interpretador Python, runtime Node.js ou binario Git e instalado ou executado dentro do servidor de banco de dados do cliente, seja um Oracle em Linux ou um cluster Exadata. Toda a inteligencia opera externamente: nas estacoes dos engenheiros para analise assistida, e nos runners isolados de integracao continua para execucao dos pipelines. A comunicacao com o banco ocorre exclusivamente via rede SQL*Net padrao, nas portas autorizadas quinze vinte e um ou vinte e quatro oitenta e quatro. Qualquer mudanca de schema deve obrigatoriamente nascer como um Pull Request versionado no Git, passar por revisao por pares e ser aplicada pelo runner de CI/CD durante a janela autorizada."

---

## Cena 6: Fechamento, Resultados e Creditos Tecnicos

- **Titulo do Slide:** Conclusao e Creditos da Engenharia DevSecOps
- **Subtitulo:** Confiabilidade, Reprodutibilidade e Governanca para Sistemas Criticos Oracle
- **Elementos Visuais:**
  - Sintese dos tres pilares: Governanca MCP + Harness Engineering + GitOps Liquibase.
  - Box de Creditos Formais:
    - Implementacao dos Laboratorios, Arquitetura de Banco e Governanca: Arley Ribeiro (DBA / Infraestrutura de Dados)
    - Palestra Original de Referencia: The APEX Dev Reinvented por Bruno Cardoso (Oracle ACE Associate / APEX Solutions Architect)
    - Revisao e Estruturacao da Escrita: IA (Google Gemini)
  - Link do repositorio: `oracle-apex-agentic-engineering`.
- **Narracao (pt-BR-AntonioNeural, duracao ~50s):**
  "Em sintese, comprovamos que e perfeitamente viavel adotar agentes de Inteligencia Artificial em ambientes Oracle de missao critica, unindo a velocidade da automacao moderna com o rigor de compliance corporativo que a administracao de dados exige. Os tres laboratorios praticos e a arquitetura de referencia encontram-se integralmente codificados, testados e disponiveis neste repositorio publico. O projeto conta com a implementacao pratica, arquitetura de banco e governanca desenvolvidas por Arley Ribeiro, profissional de infraestrutura de dados e DBA, tendo como inspiracao a palestra The APEX Dev Reinvented ministrada por Bruno Cardoso, com revisao tecnica e estruturacao documental realizada pela inteligencia artificial Google Gemini. Convidamos voce a clonar este repositorio, reproduzir os laboratorios e transformar o seu fluxo de engenharia de software para Oracle e APEX. Muito obrigado."
