# Auditoria Técnica e Arquitetural: The APEX Dev Reinvented

> **Palestra Original:** The APEX Dev Reinvented  
> **Palestrante:** Bruno Cardoso (Oracle ACE Associate / Oracle APEX Solutions Architect)  
> **Implementação dos Laboratórios, Arquitetura de Banco e Governança:** Arley Ribeiro (DBA / Infraestrutura de Dados)  
> **Revisão e Estruturação da Escrita:** IA (Google Gemini)  
> **Status da Auditoria:** 100% Concluída (40 de 40 Slides Auditados Sequencialmente)  

---

## 1. Resumo Executivo

A palestra **"The APEX Dev Reinvented"**, ministrada por **Bruno Cardoso**, marca uma ruptura paradigmática na forma como aplicações corporativas são construídas em **Oracle APEX**. Historicamente, o desenvolvimento em APEX foi rotulado como uma prática centrada em interfaces visuais pontuais (*low-code click-and-run*), com desafios crônicos em controle de versão (*Git diffs* poluídos por IDs numéricos internos), testes automatizados frágeis e isolamento do ciclo de vida tradicional de engenharia de software (*SDLC*).

A tese central defendida pelo palestrante é a transição mandatória do **"Desenvolvedor APEX Construtor de Telas"** para o **"Desenvolvedor APEX Reinventado: Engenheiro de Harness & Sistemas Autônomos"**.

Nesse novo paradigma:
1. **Engenharia de Harness (Harness Engineering):** O desenvolvedor deixa de executar tarefas braçais repetitivas e passa a projetar o *harness* — um arcabouço rigoroso de especificações, restrições arquiteturais, memória estruturada e ferramentas externas que guiam agentes de Inteligência Artificial autônomos na geração e manutenção de código.
2. **Mitigação do *Context Rot*:** O palestrante detalha como a sobrecarga e degradação da janela de contexto de LLMs (*Context Rot*) impede o desenvolvimento sério em projetos grandes. A resposta arquitetural é a decomposição em **Sub-Agentes Especializados** com papéis isolados (Arquiteto, Desenvolvedor PL/SQL, QA/Tester) e a técnica de **Tool Call Offloading**, onde o processamento volumoso de dados ocorre fora da janela de contexto.
3. **APEXlang e o Fim do Bloqueio de Versionamento:** A introdução do **APEXlang** (especificação declarativa legível e determinística) como elo entre humanos, Git e LLMs, superando o antigo problema de conflitos de merge e IDs numéricos voláteis gerados pelo exportador tradicional do APEX.
4. **Governança com SQLcl e MCP (Model Context Protocol):** A integração do banco de dados com agentes de IA via servidores MCP conectando o **Oracle SQLcl**, permitindo que o modelo inspecione o dicionário de dados da Oracle com governança e segurança, sem expor dados sensíveis.
5. **Automação de Testes E2E com Playwright & IA:** A elevação da qualidade das aplicações APEX por meio de testes ponta a ponta automatizados via **Playwright**, com agentes gerando e validando cenários de testes diretamente no navegador contra os componentes do *Universal Theme*.


---

## 2. Mapeamento Slide a Slide (1 a 40)

### Slide 1: A Reinvenção do Desenvolvedor Oracle APEX

- **Arquivo de Origem:** [`slides/01-the-apex-dev-reinvented.png`](slides/01-the-apex-dev-reinvented.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `Git`, `Workflow`, `Harness Engineering`, `CI/CD`, `Automation`

#### Conteúdo Extraído
O slide apresenta o título da palestra 'THE APEX DEV Reinvented' de Bruno Cardoso. Visualmente, exibe um desenvolvedor interagindo com um ecossistema de ferramentas modernas, representado por ícones de banco de dados, fluxogramas (Workflows), automação (AI Assistant) e código. Na parte inferior, destaca quatro pilares fundamentais: Workflow, Git, Automações e Harness Engineering. Inclui QR Codes para o 'APEX HUB' e perfil no LinkedIn.

#### Insight Técnico (Arquitetura & DBA)
Este slide sinaliza uma mudança de paradigma no ecossistema APEX: a transição do desenvolvimento puramente low-code para uma abordagem de engenharia de software profissional. A menção a 'Git' e 'Harness Engineering' aponta para a adoção de práticas de DevOps, CI/CD e controle de versão (APEX Export/Import, APEX CLI), essenciais para governança em larga escala. A integração com 'Workflows' e 'Automações' sugere o uso de APEX Automations e APEX Workflows, permitindo que o desenvolvedor APEX atue como um orquestrador de processos de negócio complexos, elevando a produtividade e a manutenibilidade das aplicações.

---

### Slide 2: Perfil Profissional e Credenciais do Palestrante

- **Arquivo de Origem:** [`slides/02-speaker-profile-credentials.png`](slides/02-speaker-profile-credentials.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `SQL`, `PL/SQL`, `JavaScript`, `ORDS`, `REST APIs`, `AI-assisted development`

#### Conteúdo Extraído
O slide apresenta o perfil de Bruno Cardoso, destacando: 1) Título: Oracle ACE Associate e Oracle APEX Solutions Architect com mais de 7 anos de experiência em software corporativo. 2) Competências principais: Design e entrega de aplicações APEX escaláveis, REST APIs, integrações, SQL, PL/SQL, JavaScript, ORDS, database engineering, performance, governança, maintainability e suporte em produção. 3) Especializações: Experiência nos setores de energia e comércio exterior (COMEX), além de foco em AI-assisted development e integração de AI em fluxos de trabalho corporativos. 4) Certificações: Oracle APEX Cloud Developer Professional e Oracle ACE Associate.

#### Insight Técnico (Arquitetura & DBA)
O perfil reflete a evolução do desenvolvedor APEX moderno: não apenas um construtor de telas, mas um arquiteto de soluções full-stack que domina a camada de persistência (Database Engineering), a camada de integração (REST/ORDS) e a nova fronteira de produtividade (AI-assisted development). A ênfase em governança e maintainability é crucial para ambientes enterprise, onde a escalabilidade do APEX depende diretamente de boas práticas de modelagem de dados e da correta orquestração de APIs, indo além do low-code básico.

---

### Slide 3: Evolução da Engenharia de Software com IA

- **Arquivo de Origem:** [`slides/03-ai-software-engineering-evolution.png`](slides/03-ai-software-engineering-evolution.png)
- **Tecnologias / Recursos Citados:** `GPT-3`, `ChatGPT`, `IDE`, `AGENTS.md`, `MCP (Model Context Protocol)`, `CI/CD`, `Multi-agent workflows`

#### Conteúdo Extraído
O slide apresenta uma linha do tempo da evolução do desenvolvimento assistido por IA, dividida em quatro fases: Fase 1 (2020-2021) 'Copy & Paste': GPT-3 gerando código via prompts para colagem manual. Fase 2 (2021-2024) 'IDE Autocomplete + Agents': Uso de AGENTS.md para contexto de projeto e aceleração de entrega. Fase 3 (2024-2025) 'Vibe Coding': Modelos de fronteira orquestrando projetos com 'Ralph loops'. Fase 4 (2025-2026) 'Autonomous Engineering': Uso de MCP (Model Context Protocol) e fluxos multi-agentes onde humanos governam arquitetura e segurança, com ciclo de vida: BACKLOG -> WORKTREE -> PR -> REVIEW.

#### Insight Técnico (Arquitetura & DBA)
Para um Arquiteto APEX, a transição para a 'Autonomous Engineering' implica uma mudança de paradigma: o Page Designer deixa de ser apenas uma ferramenta de arrastar e soltar para se tornar uma interface de orquestração de agentes. A integração de MCP no ecossistema Oracle permitirá que o APEX interaja nativamente com LLMs, transformando o desenvolvimento de aplicações em um processo de governança de fluxos de trabalho. O desafio para o DBA será garantir a integridade dos dados e a segurança em um ambiente onde agentes autônomos geram e aplicam alterações no schema e na lógica de negócio via CI/CD.

---

### Slide 4: Definição e Arquitetura de Harness Engineering

- **Arquivo de Origem:** [`slides/04-harness-engineering-architecture.png`](slides/04-harness-engineering-architecture.png)
- **Tecnologias / Recursos Citados:** `LLM`, `AI Assistant`, `Vector Search`, `PL/SQL`, `REST Data Sources`, `Autonomous Database`

#### Conteúdo Extraído
O slide define a fórmula 'MODEL + HARNESS = AGENT'. O componente 'MODEL' é descrito como a entidade que interpreta o contexto e gera a saída. O componente 'HARNESS' (Execution layer) é composto por quatro pilares: Instructions, Tools, Memory & State e Execution Cycle. O resultado da combinação é o 'AGENT', definido como o modelo em ação, coordenado pelo harness, operando sob o ciclo 'Observe -> Decide -> Act'.

#### Insight Técnico (Arquitetura & DBA)
Sob a ótica de um Arquiteto APEX, o 'Harness' representa a camada de orquestração necessária para transformar LLMs genéricos em agentes produtivos dentro do ecossistema Oracle. No APEX, isso se traduz em utilizar o 'AI Assistant' e 'Vector Search' integrados ao banco de dados, onde o 'Harness' é implementado via PL/SQL (para lógica de negócio e segurança), REST Data Sources (para integração com ferramentas externas) e o estado gerenciado em tabelas do banco. A transição de um modelo estático para um agente autônomo exige que o desenvolvedor APEX foque na governança das 'Instructions' (System Prompts) e na robustez do 'Execution Cycle' para garantir que as ações do agente sejam auditáveis e seguras, evitando alucinações e acessos indevidos aos dados.

---

### Slide 5: O Conceito de Harness Engineering na IA

- **Arquivo de Origem:** [`slides/05-harness-engineering-capabilities.png`](slides/05-harness-engineering-capabilities.png)
- **Tecnologias / Recursos Citados:** `Git`, `Bash`, `MCPs (Model Context Protocols)`, `LLM`, `Ralph Loops`

#### Conteúdo Extraído
O slide define 'Harness Engineering' como o conjunto de capacidades adicionadas a um modelo de IA para suprir suas limitações intrínsecas. O conteúdo é estruturado em uma tabela comparativa entre 'Desired behavior' e 'What the harness adds': 1. Work with real data persistently -> File system + Git; 2. Write and run code -> Bash + code execution; 3. Secure execution + standard tools -> Isolated environments + tools; 4. Remember and access new knowledge -> Memory files + web search + MCPs; 5. Maintain performance in long contexts -> Context compaction + tool delegation + skills; 6. Complete long-term work -> Ralph Loops + planning + verification. Nota de rodapé: 'Each harness capability corresponds to a behavior the model cannot perform on its own.'

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, vejo o 'Harness Engineering' como a evolução natural da integração entre LLMs e o ecossistema Oracle. Ao trazer persistência (Git/File system), execução isolada e MCPs (Model Context Protocols) para o fluxo de desenvolvimento, estamos essencialmente criando um 'agente de desenvolvimento' capaz de interagir com o Page Designer ou gerar PL/SQL de forma mais robusta. Para um DBA, a parte de 'Context compaction' e 'Tool delegation' é crucial para evitar alucinações e garantir que o modelo respeite as restrições de segurança do banco de dados e as melhores práticas de performance ao gerar código para o APEX.

---

### Slide 6: Definição e Conceitos de Harness Engineering

- **Arquivo de Origem:** [`slides/06-harness-skills-and-memory.png`](slides/06-harness-skills-and-memory.png)
- **Tecnologias / Recursos Citados:** `Markdown`, `AI Assistant`, `Git`, `Oracle APEX`, `LLM`, `Harness Engineering`

#### Conteúdo Extraído
O slide define 'Harness Engineering' como um método onde 'Skills' são arquivos Markdown (.md). As características principais são: 1) Skills podem conter referências a código determinístico; 2) Uma skill pode ser referenciada dentro de outra. É apresentado um exemplo de interação com um assistente chamado 'CODEX' através do prompt: 'Use $get-investments and make a graph showing my expenses x revenue', resultando em um gráfico de barras comparativo. O slide também menciona os conceitos de 'UNSLOP', 'GRILL-ME' e 'AI MEMORY' ilustrados por um ícone de robô.

#### Insight Técnico (Arquitetura & DBA)
A abordagem de 'Harness Engineering' proposta sugere uma abstração de lógica de negócio em arquivos Markdown, o que facilita a versionabilidade via Git e a modularização de componentes. Para um Arquiteto APEX, isso representa uma mudança de paradigma: em vez de codificar lógica puramente em PL/SQL dentro do Page Designer, utiliza-se uma camada de orquestração baseada em LLM que invoca 'Skills' (código determinístico). Isso aumenta a produtividade e a manutenibilidade, mas exige governança rigorosa sobre as 'Skills' para evitar 'alucinações' de IA, garantindo que o código executado seja seguro e performático no Oracle Database.

---

### Slide 7: Arquitetura de Memória para Agentes de IA

- **Arquivo de Origem:** [`slides/07-agent-memory-architecture.png`](slides/07-agent-memory-architecture.png)
- **Tecnologias / Recursos Citados:** `AI Memory`, `LLM`, `RAG`, `Vector Search`, `Oracle Database`

#### Conteúdo Extraído
O slide apresenta o conceito de 'AI Memory' com os seguintes pontos: 1. Store multiple patterns (Armazenar múltiplos padrões); 2. Changing providers and keep the knowledge (Trocar provedores de LLM mantendo o conhecimento); 3. To Observe and learn with choices and trade-offs (Observar e aprender com escolhas e trade-offs); 4. Knowledge becomes a wiki (O conhecimento torna-se uma base de conhecimento estruturada).

#### Insight Técnico (Arquitetura & DBA)
Do ponto de vista de um Arquiteto APEX, este slide aborda a necessidade de persistência de contexto (RAG - Retrieval-Augmented Generation) fora do escopo volátil da sessão do LLM. Para implementar isso no Oracle Database, o uso de Vector Search e tabelas de metadados é crucial. A capacidade de 'trocar provedores' sugere uma camada de abstração (Service Layer) no PL/SQL que desacopla a aplicação APEX da API específica do provedor (ex: OCI Generative AI, OpenAI, Cohere), permitindo que o 'conhecimento' (embeddings) resida de forma agnóstica no banco de dados, garantindo governança e persistência a longo prazo.

---

### Slide 8: Orquestração de Releases e Automação de CI/CD

- **Arquivo de Origem:** [`slides/08-release-orchestration-cicd.png`](slides/08-release-orchestration-cicd.png)
- **Tecnologias / Recursos Citados:** `AI Assistant`, `CI/CD`, `Git`, `APEX CLI`, `Release Orchestrator`, `Pull Requests (PR)`

#### Conteúdo Extraído
O slide ilustra um fluxo automatizado de orquestração de releases via IA. O processo inicia com o prompt: 'Use $release-orchestrator and deploy tasks 1, 2, and 3 to production'. O fluxo segue quatro etapas: 1. CHERRY-PICK: Seleção de PRs para as tarefas 1, 2 e 3. 2. CONFLICTS: Resolução automatizada de conflitos com documentação. 3. QUALITY GATES: Execução de testes e geração de relatório qualitativo. 4. RELEASE PR: Finalização em 10 minutos, deixando o PR pronto para aprovação com todas as tarefas e soluções documentadas. O slide traz o lema 'MENOS É MAIS!' reforçando a eficiência operacional.

#### Insight Técnico (Arquitetura & DBA)
Este slide propõe uma mudança de paradigma no ciclo de vida de aplicações APEX, movendo-se de deploys manuais ou baseados em scripts simples para uma orquestração inteligente. Para um Arquiteto APEX, isso implica a necessidade de integrar o APEX Export/Import (via APEX CLI ou OCI DevOps) com ferramentas de IA que gerenciem o versionamento no Git. A automação de 'Quality Gates' é crítica para garantir que as mudanças no Page Designer não quebrem dependências de banco de dados. A capacidade de resolver conflitos automaticamente em arquivos JSON de exportação do APEX é o 'santo graal' da produtividade em equipes grandes, reduzindo drasticamente o tempo de ciclo (lead time) e o risco de regressão em ambientes de produção.

---

### Slide 9: O Fenômeno de Context Rot em LLMs

- **Arquivo de Origem:** [`slides/09-context-rot-phenomenon.png`](slides/09-context-rot-phenomenon.png)
- **Tecnologias / Recursos Citados:** `LLMs`, `Vector Search`, `Oracle Database`, `RAG`, `AI Assistant`

#### Conteúdo Extraído
O slide ilustra o conceito de 'Context Rot' em LLMs, destacando que o uso excessivo da 'Context Window' (~250.000 tokens) degrada a qualidade das respostas. O diagrama divide a janela de contexto em três zonas: 1. SMART ZONE (0-40%): Alta qualidade. 2. Warning (40-60%): Zona de degradação. 3. DUMB ZONE (60-100%): Baixa qualidade, onde o autor indica que o desenvolvedor geralmente está operando. Mensagens chave: 'The problem isn't AI. It's how you're using the context window.', 'LLMs are STATELESS (goldfish memory)', 'LIMITED Context Window (~250.000 tokens / ~950.000 tokens new)', e '>40% = DUMB ZONE (Quality drops dramatically)'.

#### Insight Técnico (Arquitetura & DBA)
Para um Arquiteto APEX integrando IA, este slide é um alerta crítico sobre a implementação de RAG (Retrieval-Augmented Generation). Ao injetar metadados, esquemas de banco de dados ou logs de aplicação no prompt, o desenvolvedor deve priorizar a relevância sobre o volume. O uso de Vector Search no Oracle Database deve ser otimizado para enviar apenas os 'chunks' mais pertinentes ao LLM, evitando o 'Context Rot'. Em arquiteturas de CI/CD ou agentes de IA no APEX, é vital implementar estratégias de sumarização e filtragem de contexto para manter a performance e a precisão, evitando que o modelo entre na 'Dumb Zone' ao processar grandes volumes de dados de negócio.

---

### Slide 10: Gerenciamento de Context Window em LLMs

- **Arquivo de Origem:** [`slides/10-context-window-management.png`](slides/10-context-window-management.png)
- **Tecnologias / Recursos Citados:** `LLM`, `Context Window`, `Oracle Database Vector Search`, `APEX AI Assistant`, `REST Data Sources`

#### Conteúdo Extraído
O slide aborda estratégias para evitar o 'Context Rot' (degradação de contexto) em interações com LLMs. Apresenta duas técnicas principais: 1. COMPACTION: Uso de comandos como '/compact' ou compactação automática quando o uso da janela de contexto atinge 90%+. Nota que é útil, mas não a única opção. 2. HANDOFF: Técnica de solicitar um resumo (summary) da conversa atual, iniciar uma nova sessão e colar o resumo para manter a continuidade. O rodapé alerta que ambas as técnicas mantêm a qualidade, mas podem resultar em perda de detalhes do contexto.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, essa estratégia é vital ao integrar LLMs via APEX AI Assistant ou REST Data Sources. O 'Context Rot' é um desafio real em aplicações complexas que mantêm histórico de chat. O 'Handoff' é preferível para manter a precisão em fluxos de trabalho de longa duração, enquanto o 'Compaction' é mais eficiente para sessões rápidas. Do ponto de vista de governança, é crucial implementar lógica de truncamento ou sumarização no backend (PL/SQL) para evitar exceder limites de tokens e custos desnecessários, garantindo que o prompt enviado ao Oracle Database Vector Search ou LLM externo seja sempre otimizado.

---

### Slide 11: Evitando o Context Rot através de Progressive Disclosure

- **Arquivo de Origem:** [`slides/11-progressive-disclosure-strategy.png`](slides/11-progressive-disclosure-strategy.png)
- **Tecnologias / Recursos Citados:** `AI Assistant`, `Context Window`, `Progressive Disclosure`, `Codex`, `Claude Code`, `Markdown`

#### Conteúdo Extraído
O slide aborda a estratégia de 'Progressive Disclosure' para gerenciar o 'Context Rot' em assistentes de IA. O problema identificado é o carregamento excessivo de habilidades (skills) em uma 'limited context window', causando sobrecarga. A solução proposta é o uso de um índice de ferramentas e habilidades carregadas sob demanda. O fluxo de trabalho é dividido em três etapas: 1. DISCOVER (identificar a habilidade necessária), 2. ACTIVATE (ativar a habilidade específica), 3. EXECUTE (executar a tarefa). É recomendado o uso de um 'MASTER INDEX' centralizado no arquivo 'skills.md', mantido no diretório de habilidades do 'Codex' ou 'Claude Code'.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, esta abordagem é fundamental para otimizar o uso de LLMs integrados ao ciclo de vida de desenvolvimento. Ao aplicar 'Progressive Disclosure', reduzimos o consumo de tokens e evitamos alucinações causadas por excesso de ruído no prompt. Em um contexto de APEX, isso se traduz em criar 'Skill Sets' modulares (ex: um arquivo para Page Designer, outro para REST Data Sources, outro para Security Policies) que são injetados no contexto da IA apenas quando necessário, garantindo que o assistente mantenha o foco na tarefa atual sem perder a coerência arquitetural.

---

### Slide 12: Evitando o Context Rot através de Progressive Disclosure

- **Arquivo de Origem:** [`slides/12-progressive-disclosure-deepdive.png`](slides/12-progressive-disclosure-deepdive.png)
- **Tecnologias / Recursos Citados:** `Progressive Disclosure`, `CI/CD`, `Git`, `Automation`, `Oracle APEX`

#### Conteúdo Extraído
O slide apresenta uma estratégia de organização de conhecimento e automação dividida em três etapas: 1. TOOLS CATALOG: Um repositório centralizado contendo 'What it is', 'When to use' e 'How it works' para ferramentas como 'Local Search' e 'release-orchestrator'. 2. Request selects the skill: Um agente (representado por um robô) que recebe uma instrução (ex: 'Deploy tasks 1, 2, and 3 to production') e seleciona a ferramenta adequada do catálogo. 3. SKILL FOLDER: A estrutura de diretórios específica da ferramenta selecionada (ex: release-orchestrator/), contendo SKILL.md, scripts/, refs/ e assets/, permitindo acesso a detalhes e recursos sob demanda.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, vejo este slide como uma aplicação prática de 'Cognitive Load Management' para equipes de desenvolvimento. Ao aplicar Progressive Disclosure, evitamos que o desenvolvedor seja sobrecarregado por documentação excessiva ou complexidade desnecessária. No ecossistema Oracle APEX, isso se traduz em manter uma documentação técnica centralizada (via APEX Application Documentation ou repositórios Git) que se integra com ferramentas de CI/CD e automação. A estrutura de 'SKILL FOLDER' é um padrão excelente para organizar scripts de automação, APEX export files e documentação técnica, facilitando a governança e a manutenção em ambientes de larga escala.

---

### Slide 13: Estratégia de Tool Call Offloading para Otimização de Contexto em LLMs

- **Arquivo de Origem:** [`slides/13-tool-call-offloading.png`](slides/13-tool-call-offloading.png)
- **Tecnologias / Recursos Citados:** `LLM`, `JSON`, `Tool Call Offloading`, `Oracle Database`, `Vector Search`, `JSON Relational Duality Views`

#### Conteúdo Extraído
O slide apresenta uma comparação entre duas abordagens para lidar com o limite de contexto em LLMs: 1) 'Without Offloading': Onde chamadas de ferramentas retornam grandes volumes de dados (ex: 500 linhas de JSON), resultando em 'Context Nearly Full' e sobrecarga do modelo. 2) 'With Offloading': Onde o sistema realiza o offload da saída, retornando apenas um 'Summary + File Pointer' para o modelo, enquanto os detalhes completos são armazenados em banco de dados e acessados 'on demand', resultando em 'More Context Available'.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, esta técnica é crucial para integrar LLMs com o Oracle Database. Ao usar APEX, em vez de injetar grandes payloads JSON diretamente no prompt, devemos persistir os dados em tabelas (usando JSON Relational Duality Views ou colunas JSON) e passar apenas metadados ou resumos para o modelo. Isso evita o 'Context Rot', reduz custos de tokens e latência, e aproveita a capacidade do Oracle de realizar buscas eficientes via Vector Search ou SQL, mantendo o contexto do LLM limpo e focado na tarefa principal.

---

### Slide 14: Estratégia para evitar Context Rot em aplicações de IA

- **Arquivo de Origem:** [`slides/14-context-rot-mitigation-rules.png`](slides/14-context-rot-mitigation-rules.png)
- **Tecnologias / Recursos Citados:** `LLM`, `JSON`, `Cloud Storage`, `Oracle APEX`, `OCI`, `Tokenization`

#### Conteúdo Extraído
O slide apresenta um fluxo de 3 etapas para gerenciar grandes volumes de dados gerados por ferramentas de IA (Tool-call output) para evitar o esgotamento da janela de contexto (Context Rot): 1. INTERCEPT OUTPUT: Medir o tamanho da saída. Se exceder 3.000 tokens, o fluxo é desviado para persistência. 2. PERSIST THE OUTPUT: Salvar o conteúdo completo (ex: arquivos JSON) em armazenamento persistente (filesystem ou cloud storage). 3. RETURN A POINTER: Retornar ao modelo de IA apenas um resumo descritivo, metadados e um link/ponteiro para o arquivo completo. O objetivo final é garantir que 'The AI knows what it found—and where to get the details'.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, esta é uma técnica fundamental para otimizar o uso de LLMs em aplicações Oracle APEX. Ao integrar APEX com serviços de IA (via OCI Generative AI ou OpenAI API), o gerenciamento de tokens é crítico para performance e custo. A implementação ideal no ecossistema Oracle envolve armazenar os outputs volumosos em tabelas com colunas BLOB/CLOB ou OCI Object Storage, utilizando o APEX_JSON para manipular os metadados e gerar URLs assinadas ou links de download. Isso mantém o prompt do modelo leve, reduz latência e evita erros de 'Context Window Exceeded', garantindo uma arquitetura escalável e resiliente.

---

### Slide 15: Estratégia de Offloading de Ferramentas em PL/SQL para LLM Agents

- **Arquivo de Origem:** [`slides/15-tool-offloading-plsql.png`](slides/15-tool-offloading-plsql.png)
- **Tecnologias / Recursos Citados:** `PL/SQL`, `Oracle Database`, `DBMS_LOB`, `UTL_FILE`, `ORDS`, `LLM Agents`, `RAG`

#### Conteúdo Extraído
O slide apresenta um fluxo de processamento para evitar o estouro da janela de contexto (context window) de LLMs. 1. RUN QUERY: Executa uma função fnc_executa_consulta retornando um CLOB. 2. ESTIMATE SIZE: Calcula tokens usando 'l_tokens := CEIL(DBMS_LOB.GETLENGTH(l_result) / 4)' com um limite configurável de 1500. 3A. DIRECT RETURN: Se l_tokens < 1500, retorna o CLOB diretamente. 3B. RESPONSE THE AGENT RECEIVES: Se exceder o limite, o sistema salva o resultado em disco e retorna uma notificação ao agente contendo metadados, o caminho do arquivo (filepath) e uma amostra das primeiras 5 linhas, instruindo o agente a usar ferramentas como 'grep_file' ou 'read_file' para interagir com o conteúdo. Rodapé técnico: Token count usa estimativa (não substitui cl100k_base) e File Access utiliza UTL_FILE via DIRECTORY/GRANT e ORDS.

#### Insight Técnico (Arquitetura & DBA)
Esta é uma arquitetura essencial para sistemas RAG (Retrieval-Augmented Generation) robustos em Oracle APEX. Ao implementar 'Tool Offloading', o desenvolvedor contorna a limitação de tokens de modelos de IA, mantendo a governança de dados dentro do banco. O uso de UTL_FILE para persistir grandes payloads e expor via ORDS é uma prática de engenharia de software inteligente, pois evita o envio de volumes massivos de dados via JSON/REST, reduzindo latência e custos de inferência. A abordagem de fornecer metadados e amostras permite que o agente atue de forma autônoma e iterativa, o que é um padrão de design superior para agentes de IA corporativos.

---

### Slide 16: Mitigação de Context Rot através de Sub-Agents

- **Arquivo de Origem:** [`slides/16-sub-agents-architecture.png`](slides/16-sub-agents-architecture.png)
- **Tecnologias / Recursos Citados:** `LLMs`, `AI Assistant`, `REST Data Sources`, `Oracle APEX`, `Autonomous Database`

#### Conteúdo Extraído
O slide aborda a estratégia de 'Sub-Agents' para gerenciar a complexidade em tarefas de desenvolvimento. Lado esquerdo: Ilustra o problema de 'Context Rot' e 'Loss of Focus' quando um agente único tenta processar tarefas longas e complexas. Lado direito: Propõe a delegação para sub-agentes especializados (RESEARCH, BUILD, QA), permitindo que modelos de menor custo (lower-cost models) executem tarefas específicas que não exigem raciocínio de alto nível. Rodapé: Alerta para não fragmentar excessivamente as tarefas, mantendo escopos pequenos e trabalho fortemente acoplado.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, esta abordagem é fundamental para a integração de LLMs no ciclo de vida de desenvolvimento (SDLC). Ao utilizar Oracle APEX com AI Assistant ou integrações via REST Data Sources, a estratégia de sub-agentes evita que o prompt de contexto exceda o token limit ou perca a coerência (context rot). Para o DBA, isso otimiza o consumo de recursos de inferência, permitindo o uso de modelos menores para tarefas repetitivas (como geração de unit tests ou documentação) enquanto reserva modelos de alta capacidade para arquitetura e design de esquemas complexos.

---

### Slide 17: Estratégias para evitar a degradação do contexto (Context Rot) em sistemas de IA

- **Arquivo de Origem:** [`slides/17-context-degradation-strategies.png`](slides/17-context-degradation-strategies.png)
- **Tecnologias / Recursos Citados:** `AI Assistant`, `Autonomous Database`, `OCI Generative AI`, `APEX`

#### Conteúdo Extraído
O slide apresenta diretrizes para o uso de sub-agents em arquiteturas de IA. 'When use sub-agents?': 1. Fluxos de trabalho que podem prosseguir independentemente. 2. Tarefas grandes ou altamente complexas. 3. Quando o custo da paralelização é menor que o custo atual. 'When not use sub-agents?': 1. Tarefas simples ou lineares. 2. Respostas rápidas/tempo real. 3. Uso de arquivos em paralelo ou com escrita paralela pesada. 4. Quando existem dependências entre tarefas.

#### Insight Técnico (Arquitetura & DBA)
Sob a ótica de um Arquiteto APEX, este slide é fundamental para o design de integrações com LLMs via APEX AI Assistant ou OCI Generative AI. O 'Context Rot' ocorre quando o prompt se torna muito longo ou fragmentado, perdendo a coerência. Ao delegar tarefas para sub-agents, o desenvolvedor deve garantir que o estado (state management) seja mantido de forma eficiente, preferencialmente utilizando APEX Application Items ou tabelas de estado no Autonomous Database. A recomendação de não usar sub-agents para tarefas lineares evita latência desnecessária (overhead de chamadas de API), o que é crucial para manter a performance da UI em aplicações APEX que dependem de respostas rápidas.

---

### Slide 18: Uso de Sub-Agents para evitar Context Rot

- **Arquivo de Origem:** [`slides/18-sub-agents-isolation.png`](slides/18-sub-agents-isolation.png)
- **Tecnologias / Recursos Citados:** `AI Assistant`, `JWT`, `SDLC`, `Oracle APEX`, `Autonomous Database`

#### Conteúdo Extraído
O slide ilustra um fluxo de trabalho de IA para evitar 'Context Rot' (degradação de contexto) ao delegar tarefas complexas. O processo começa com uma solicitação ('Add JWT validation to login'), que é recebida por um 'PEER AGENT' central. Este agente atua como orquestrador, planejando e delegando a tarefa para três sub-agentes especializados: 1) RESEARCH (pesquisa padrões de autenticação existentes), 2) BUILD (implementa a validação JWT) e 3) QA (testa tokens válidos e inválidos). O fluxo termina com a consolidação dos resultados em um 'Review results' com um resumo conciso.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, vejo este modelo como a evolução da automação no ciclo de vida de desenvolvimento (SDLC). Em vez de um único prompt monolítico que perde o contexto, a decomposição em sub-agentes permite que o AI Assistant interaja com componentes específicos do APEX (como Authentication Schemes ou PL/SQL Packages) de forma modular. Isso reduz drasticamente o risco de alucinações em tarefas críticas de segurança e melhora a governança, permitindo que cada sub-agente valide suas saídas contra padrões de codificação estabelecidos antes da integração final no Page Designer ou no banco de dados.

---

### Slide 19: Comunicação entre Sub-Agentes para evitar Context Rot

- **Arquivo de Origem:** [`slides/19-sub-agents-communication.png`](slides/19-sub-agents-communication.png)
- **Tecnologias / Recursos Citados:** `AI Assistant`, `Oracle APEX`, `Autonomous Database`, `Vector Search`, `LLM`, `REST Data Sources`

#### Conteúdo Extraído
O slide ilustra um padrão de arquitetura de agentes de IA onde um 'Peer Agent' (orquestrador) delega tarefas para sub-agentes especializados: RESEARCH, BUILD e QA. O fluxo de trabalho segue o princípio 'Focused tasks out. Concise results back'. Cada interação envia 'TASK + RELEVANT CONTEXT' para o sub-agente e recebe 'SUMMARY + FINDINGS + FILES'. O processo final envolve 'Review, combine, respond'. A mensagem central é que cada 'handoff' deve carregar apenas o briefing focado e o contexto estritamente necessário para a tarefa, evitando a degradação do contexto (Context Rot).

#### Insight Técnico (Arquitetura & DBA)
Sob a ótica de um Arquiteto APEX, este modelo é fundamental para a implementação de agentes de IA integrados ao Oracle APEX via AI Assistant ou APEX AI. Ao lidar com LLMs, o gerenciamento de tokens é crítico; enviar todo o contexto da aplicação causa 'Context Rot' e aumenta custos. A estratégia de segregar tarefas em sub-agentes permite que o orquestrador (ex: um procedimento PL/SQL orquestrando chamadas de REST Data Sources para LLMs) mantenha o prompt enxuto. Para o DBA, isso reforça a necessidade de usar Vector Search no Autonomous Database para fornecer apenas os 'chunks' de dados relevantes, otimizando a performance e a precisão das respostas do agente.

---

### Slide 20: Otimização do Fluxo de Desenvolvimento com Git Worktrees

- **Arquivo de Origem:** [`slides/20-git-worktrees-workflow.png`](slides/20-git-worktrees-workflow.png)
- **Tecnologias / Recursos Citados:** `Git`, `Git Worktrees`, `AI Assistant`, `CI/CD`, `APEX CLI`

#### Conteúdo Extraído
O slide apresenta o conceito de 'Git Worktrees' como uma estratégia para gerenciar múltiplos branches simultaneamente a partir de um único repositório. O diagrama mostra um diretório .git centralizado alimentando múltiplos diretórios de trabalho (feature, urgent bug, feature), cada um com seu próprio contexto de desenvolvimento e interação com IA. O fluxo converge para um ambiente 'main / PR'. Inclui um meme com a frase 'You're not a meat proxy, you're an AI assisted senior software engineer', destacando que o gargalo do processo é o contexto do desenvolvedor, não a execução técnica.

#### Insight Técnico (Arquitetura & DBA)
Para um Arquiteto APEX, o uso de Git Worktrees é uma mudança de paradigma essencial para o desenvolvimento moderno. Como o APEX é baseado em metadados armazenados no banco de dados, a integração com Git (via APEX Export/APEX CLI) muitas vezes sofre com a troca de contexto entre branches. Worktrees permitem manter múltiplos ambientes de desenvolvimento locais sincronizados com diferentes branches sem a necessidade de clonar o repositório várias vezes ou realizar 'git stash' constantes. Isso acelera o ciclo de CI/CD e permite que o desenvolvedor alterne entre correções de bugs urgentes e novas funcionalidades sem perder o estado do ambiente, otimizando a produtividade ao trabalhar com ferramentas de IA para geração de código.

---

### Slide 21: O desafio do Git Diff em versões anteriores do Oracle APEX

- **Arquivo de Origem:** [`slides/21-git-diff-legacy-apex-challenge.png`](slides/21-git-diff-legacy-apex-challenge.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `Git`, `SQL`, `CI/CD`, `APEXLANG`

#### Conteúdo Extraído
O slide ilustra as dificuldades de versionamento de código em versões do APEX anteriores à 26 (ou pré-APEX 26). Problemas identificados: 1. Noisy Diffs: IDs gerados dinamicamente, timestamps e ordenação arbitrária de componentes ocultam alterações reais. 2. Trust-me-bro Reviews: O excesso de ruído nos arquivos de exportação torna a revisão de código lenta ou superficial. 3. CI/CD Gates: A falta de um diff limpo impede a criação de quality gates confiáveis. O slide destaca que tanto exportações monolíticas quanto exportações baseadas em componentes em SQL eram difíceis de revisar.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto, este slide endereça a maior dor do ciclo de vida de desenvolvimento (SDLC) no APEX: a falta de legibilidade em sistemas de controle de versão (VCS). A natureza declarativa do APEX, armazenada em metadados no banco de dados, gera arquivos de exportação (SQL scripts) que não são naturalmente amigáveis ao Git. A dependência de IDs internos e a estrutura não determinística das exportações antigas inviabilizavam o Code Review automatizado e o uso de ferramentas de análise estática. A transição para APEXLANG promete resolver isso ao tratar a definição da aplicação como código legível, permitindo diffs semânticos e integrando o APEX ao fluxo moderno de DevOps.

---

### Slide 22: Introdução do APEXLANG e a nova estrutura de arquivos no APEX 26

- **Arquivo de Origem:** [`slides/22-apexlang-file-structure-apex26.png`](slides/22-apexlang-file-structure-apex26.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX 26`, `APEXLANG`, `Git`, `SQL`, `CI/CD`, `GitOps`

#### Conteúdo Extraído
O slide apresenta o APEXLANG, uma especificação declarativa legível por humanos introduzida no APEX 26. O fluxo mostra a transição de arquivos SQL tradicionais para um conjunto de arquivos de texto com extensão '.apx'. Cada artefato lógico (PAGE, REGION, PROCESS, COMPUTATION, LOV) é representado por um arquivo individual. O slide destaca a melhoria na experiência de versionamento com Git, onde alterações granulares (como a mudança de um valor 'Default' de 'Yes' para 'No') tornam-se facilmente rastreáveis e legíveis em diffs de código.

#### Insight Técnico (Arquitetura & DBA)
Esta é uma mudança de paradigma fundamental para o ecossistema Oracle APEX. Ao migrar de grandes arquivos de exportação monolíticos para uma estrutura modular baseada em arquivos .apx, o APEX resolve o maior gargalo histórico para CI/CD: a dificuldade de realizar code reviews e merge de conflitos em arquivos de exportação gigantescos. Isso permite que equipes de desenvolvimento adotem fluxos de trabalho de GitOps reais, facilitando a auditoria de mudanças, a automação de testes e a integração contínua, elevando o APEX ao mesmo nível de maturidade de frameworks de desenvolvimento de software modernos.

---

### Slide 23: APEXlang: O Futuro do Desenvolvimento APEX com Git

- **Arquivo de Origem:** [`slides/23-apexlang-git-future.png`](slides/23-apexlang-git-future.png)
- **Tecnologias / Recursos Citados:** `APEXlang`, `Oracle APEX`, `Git`, `SQLcl`, `VS Code`, `AI Agents`, `CI/CD`

#### Conteúdo Extraído
O slide apresenta o APEXlang, uma linguagem projetada para modernizar os workflows de desenvolvimento no Oracle APEX. Os pilares fundamentais são: 1. VERSIONABLE: Permite Git diffs úteis e compatíveis com workflows padrão. 2. HUMAN-READABLE: Especificações em texto claro usando convenções familiares. 3. VALIDATABLE: Capacidade de validação via SQLcl e linters. 4. WORKS OUTSIDE THE BROWSER: Foco no desenvolvimento via VS Code, posicionado como a IDE oficial. 5. AI-REPRODUCIBLE: Especificações estruturadas para serem reproduzidas por AI agents.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto, vejo o APEXlang como a solução definitiva para o maior gargalo do APEX: a dificuldade de versionamento de metadados em formato binário/JSON complexo. Ao mover a definição da aplicação para um formato textual, o APEXlang viabiliza o 'True CI/CD', permitindo code reviews reais via Pull Requests, rastreabilidade de alterações e automação de testes via SQLcl. A integração com VS Code e a capacidade de serem interpretadas por AI agents transformam o APEX de uma ferramenta 'low-code' isolada em uma plataforma de engenharia de software de nível empresarial, alinhada com as melhores práticas de DevOps moderno.

---

### Slide 24: Definição e papel do APEXLANG no ecossistema APEX

- **Arquivo de Origem:** [`slides/24-apexlang-spec-vs-database.png`](slides/24-apexlang-spec-vs-database.png)
- **Tecnologias / Recursos Citados:** `APEXLANG`, `Git`, `Database Metadata`, `CI/CD`, `Oracle APEX`

#### Conteúdo Extraído
O slide define o APEXLANG como uma especificação declarativa, não como o código da aplicação em si. O diagrama central mostra o 'APEXLANG SPEC' (.apx) como o componente que descreve o comportamento dos elementos. O fluxo é dividido em duas fontes de verdade: 1) DATABASE METADATA, que é a fonte de verdade para a execução da aplicação; 2) GIT .apx FILES, que é a fonte de verdade para versionamento. A nota final reforça que a especificação é uma abstração, enquanto o banco de dados continua armazenando os metadados da aplicação.

#### Insight Técnico (Arquitetura & DBA)
Esta abordagem resolve o 'calcanhar de Aquiles' do desenvolvimento APEX tradicional: a dificuldade de versionamento e code review. Ao tratar o .apx como uma especificação declarativa, o desenvolvedor ganha a capacidade de utilizar fluxos de CI/CD modernos, permitindo que o Git seja o repositório oficial de mudanças, enquanto o banco de dados mantém a integridade dos metadados em tempo de execução. Isso promove uma governança de código superior e facilita a colaboração em equipe, alinhando o APEX com práticas de DevOps de nível empresarial.

---

### Slide 25: Ciclo de Desenvolvimento e Fluxo Git para APEX (APEXlang)

- **Arquivo de Origem:** [`slides/25-apexlang-git-development-cycle.png`](slides/25-apexlang-git-development-cycle.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `Git`, `CI/CD`, `APEXlang`, `Pull Request`, `Linters`, `Interactive Report`

#### Conteúdo Extraído
O slide detalha um fluxo de trabalho de 7 etapas para desenvolvimento em APEX utilizando a metodologia APEXlang: 1. EDIT: Atualização da aplicação ou arquivos .apx; 2. LOCAL CHECKS: Execução de linters e testes locais; 3. EXPORT: Exportação do APEXlang para a working copy; 4. OPEN A PR: Commit, push e abertura de Pull Request; 5. REVIEW: Revisão de especificações estruturadas e diffs limpos; 6. CI QUALITY GATES: Execução de validações e testes automatizados no pipeline; 7. RELEASE: Merge para ambientes de teste e produção. Inclui exemplos de revisão: 'Page X -> uses LOV Y' e 'Region A (Interactive Report) -> search query changed'.

#### Insight Técnico (Arquitetura & DBA)
Este fluxo resolve o maior gargalo do desenvolvimento em Oracle APEX: a dificuldade de versionamento e code review de metadados binários/XML. Ao utilizar 'APEXlang' (uma representação textual/declarativa dos componentes), o desenvolvedor transforma o APEX em um artefato 'Git-friendly'. Isso permite que equipes de engenharia apliquem práticas de CI/CD, Quality Gates e Code Review real, eliminando a dependência de exportações monolíticas e facilitando a rastreabilidade de mudanças em componentes como Interactive Reports e LOVs, o que é fundamental para governança e estabilidade em ambientes corporativos.

---

### Slide 26: O Custo dos Static IDs no Oracle APEX

- **Arquivo de Origem:** [`slides/26-static-ids-tax-and-clean-diffs.png`](slides/26-static-ids-tax-and-clean-diffs.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `Git`, `CI/CD`, `APEXlang`, `App Builder`

#### Conteúdo Extraído
O slide aborda a importância de utilizar 'Static IDs' em componentes do APEX para facilitar o versionamento e controle de mudanças. 'BEFORE': IDs gerados automaticamente mudam a cada exportação, gerando 'diffs' ruidosos em ferramentas de versionamento (ex: C4F9A7D1 vs 8E2B1F03). 'AFTER': Static IDs (ex: P1_SAVE_BUTTON) permanecem estáveis entre re-exportações, resultando em 'diffs' limpos e legíveis. 'THE TAX': O custo (taxa) é o esforço manual ou via AI Assistant para atribuir esses IDs significativos. Conclusão: 'One App Builder line changed = one APEXlang line changed', promovendo melhor qualidade semântica no codebase.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto, este é um pilar fundamental para CI/CD em APEX. O uso de IDs gerados pelo sistema torna o controle de versão (Git) praticamente inútil, pois qualquer alteração trivial gera um 'noise' imenso nos arquivos de exportação (SQL/APEXlang). Ao forçar o uso de Static IDs, garantimos que o histórico do Git reflita apenas mudanças reais de lógica ou layout, facilitando Code Reviews e auditorias. Embora exija disciplina (o 'tax'), o retorno sobre o investimento é a viabilidade de pipelines de automação e a redução drástica de conflitos de merge em equipes de desenvolvimento.

---

### Slide 27: O Desafio da Versionamento de Objetos de Banco de Dados no APEX

- **Arquivo de Origem:** [`slides/27-database-objects-versioning-liquibase.png`](slides/27-database-objects-versioning-liquibase.png)
- **Tecnologias / Recursos Citados:** `APEXlang`, `Git`, `GitHub Actions`, `Docker`, `Liquibase`, `CI/CD`

#### Conteúdo Extraído
O slide aborda a lacuna no versionamento de objetos de banco de dados ao utilizar APEXlang. O fluxo de trabalho proposto inclui: 1. Database Objects, 2. Separate Git Repository, 3. GitHub Actions CI, 4. Docker + Liquibase, 5. Build Validation. O slide enfatiza que o APEXlang não gerencia o versionamento de objetos de banco de dados automaticamente e alerta que a tecnologia está em evolução, mencionando uma curva de aprendizado e problemas potenciais como falhas de exportação na versão 26.2.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto, este slide destaca a necessidade crítica de separar a camada de metadados do APEX da camada de persistência (schema objects). Embora o APEX facilite o desenvolvimento declarativo, a governança de dados e a integridade do schema exigem ferramentas externas como Liquibase para garantir que o versionamento seja idempotente e rastreável via Git. A menção ao APEXlang reforça que, apesar da automação, a responsabilidade pela arquitetura de CI/CD e pelo ciclo de vida do schema (Schema-as-Code) permanece com a equipe de engenharia, não sendo uma solução 'out-of-the-box' completa para o banco de dados.

---

### Slide 28: Ciclo de Vida de Desenvolvimento com Agentes de IA

- **Arquivo de Origem:** [`slides/28-ai-agents-development-lifecycle.png`](slides/28-ai-agents-development-lifecycle.png)
- **Tecnologias / Recursos Citados:** `AI Agents`, `MCP (Model Context Protocol)`, `Loop Engineering`, `Oracle APEX`, `PL/SQL`, `POCs`

#### Conteúdo Extraído
O slide apresenta um fluxo de trabalho iterativo para desenvolvimento de software assistido por agentes de IA, dividido em quatro fases principais: 1. RESEARCH: Entrada de dados composta por 'Relevant files', 'Project structure', 'Business analysis', 'Docs/skills/MCPs' e 'Scripts/POCs'. 2. PLAN: O agente organiza a pesquisa e define os passos. 3. IMPLEMENT: O agente implementa a solução. 4. VERIFY: O agente executa um loop de verificação da implementação. Há um ciclo de feedback 'Fix and test again' que retorna de VERIFY para IMPLEMENT. Notas adicionais: 'Research' define o caminho e decisões; 'Plan' refina a pesquisa via agente; 'Implement e Verify' utilizam o conceito de 'loop engineering'.

#### Insight Técnico (Arquitetura & DBA)
Este modelo representa a transição do desenvolvimento manual para o 'Agentic Workflow' no ecossistema Oracle APEX. Do ponto de vista de arquitetura, a integração de MCPs (Model Context Protocol) com o Oracle Database permite que agentes de IA acessem metadados do dicionário de dados e lógica de negócio (PL/SQL) com maior precisão. A implementação de 'loop engineering' é crucial para reduzir alucinações em geração de código APEX, garantindo que o código gerado passe por validações de sintaxe e testes unitários antes da integração no Page Designer. Para um DBA/Arquiteto, isso exige governança sobre os prompts e o contexto fornecido ao agente para evitar riscos de segurança (SQL Injection) e garantir que o código gerado siga as melhores práticas de performance do Oracle Database.

---

### Slide 29: Dev APEX Reinvented Toolkit

- **Arquivo de Origem:** [`slides/29-dev-apex-reinvented-toolkit.png`](slides/29-dev-apex-reinvented-toolkit.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `Database Actions`, `REST Data Sources`, `CI/CD`, `DevOps`

#### Conteúdo Extraído
O slide apresenta o conceito de um 'Toolkit' para o desenvolvedor APEX moderno. Visualmente, exibe um personagem segurando uma maleta contendo quatro ícones representativos: 1. Ícone de código (</>) representando desenvolvimento e lógica; 2. Ícone de banco de dados representando persistência e modelagem; 3. Ícone de engrenagem representando automação e configurações; 4. Ícone de rede/nós representando integração e conectividade. O título principal é 'Dev APEX reinvented toolkit'.

#### Insight Técnico (Arquitetura & DBA)
Este slide sintetiza a mudança de paradigma no desenvolvimento APEX: a transição do desenvolvedor focado apenas em Page Designer para um perfil de 'Full-Stack Low-Code Engineer'. A maleta simboliza a necessidade de integrar práticas de DevOps, automação de banco de dados (Database Actions), integração via REST Data Sources e orquestração de fluxos. Para um Arquiteto, isso reforça a importância de adotar uma abordagem de 'Infrastructure as Code' e CI/CD para manter a governança em ambientes APEX complexos, garantindo que o toolkit não seja apenas uma coleção de ferramentas, mas um ecossistema de produtividade.

---

### Slide 30: Evolução de Gestão de Conhecimento para IA: De AGENTS.md para AI-Memory

- **Arquivo de Origem:** [`slides/30-knowledge-management-agentsmd-to-memory.png`](slides/30-knowledge-management-agentsmd-to-memory.png)
- **Tecnologias / Recursos Citados:** `AI`, `LLM`, `Vector Search`, `Custom Embeddings`, `SQLite`, `Markdown`, `Context Window`

#### Conteúdo Extraído
O slide apresenta a transição de um arquivo estático (AGENTS.md) para um sistema de memória inteligente (AI-Memory). 1. PROBLEM: AGENTS.md centraliza padrões, mas cresce indefinidamente, consumindo o context window da IA. 2. SOLUTION: ai-memory (OKF - Open Knowledge File) que registra DECISIONS, PATTERNS e LIMITS. Utiliza CUSTOM EMBEDDINGS - V2 para busca eficiente e de baixo custo. 3. CONTINUITY: Conceito de Portable memory usando SQLite para permitir a troca de modelos ou ambientes (Notebook/PC) mantendo o contexto, facilitando o TEAM - DOCUMENTED HANDOFF.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto APEX, esta abordagem resolve o gargalo de 'context window' em aplicações baseadas em LLM. A transição de arquivos Markdown para uma estrutura baseada em Vector Search (Custom Embeddings) é crucial para a escalabilidade. O uso de SQLite como 'Portable memory' é uma estratégia excelente para garantir a persistência local e portabilidade do contexto, permitindo que o estado da sessão de desenvolvimento seja compartilhado entre diferentes instâncias de agentes ou ambientes de trabalho, reduzindo a latência e o custo de tokens em chamadas de API recorrentes.

---

### Slide 31: Estrutura do Conjunto de Habilidades APEXLANG

- **Arquivo de Origem:** [`slides/31-apexlang-skills-structure.png`](slides/31-apexlang-skills-structure.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `SQLcl`, `APEXLANG`, `CI/CD`, `Infrastructure as Code`

#### Conteúdo Extraído
O slide apresenta o 'APEXLANG SKILL SET', dividido em um núcleo compartilhado e quatro habilidades especializadas: 1. CORE: 'apexlang-inventory' (Catálogo de componentes, propriedades, definições de sintaxe e organização de arquivos). 2. SPECIALIZED SKILLS: 'apexlang-generation' (Planejamento, regras e validações para suporte à geração de aplicações), 'apexlang-example-applications' (Aplicações de exemplo para referência), 'apexlang-compile' (Validação da aplicação usando SQLcl) e 'apexlang-deploy' (Importação da aplicação usando SQLcl).

#### Insight Técnico (Arquitetura & DBA)
Esta proposta de 'APEXLANG' sugere uma abordagem de 'Infrastructure as Code' (IaC) para o desenvolvimento em Oracle APEX. Ao formalizar um inventário de componentes e utilizar o SQLcl para compilação e deploy, o autor promove a padronização do ciclo de vida de desenvolvimento (SDLC). Isso resolve gargalos comuns de governança e CI/CD em APEX, permitindo que aplicações sejam tratadas como artefatos versionáveis, reduzindo a dependência exclusiva do Page Designer e facilitando a automação de pipelines de entrega contínua.

---

### Slide 32: Integração entre SQLcl MCP e APEXlang para Desenvolvimento Assistido por IA

- **Arquivo de Origem:** [`slides/32-sqlcl-mcp-apexlang-integration.png`](slides/32-sqlcl-mcp-apexlang-integration.png)
- **Tecnologias / Recursos Citados:** `SQLcl`, `MCP (Model Context Protocol)`, `APEXlang`, `AI Agents`, `Database`, `CI/CD`

#### Conteúdo Extraído
O slide apresenta o 'SQLcl MCP Server' como uma nova ferramenta que provê recursos de banco de dados para agentes de IA. O fluxo de trabalho do agente (Agent Workflow) é dividido em quatro etapas: 1. REQUEST (Testar função X e buscar falhas); 2. TOOLS (MCP expõe ferramentas do SQLcl); 3. CONNECTION (Usa credenciais configuradas para autenticar com o SQLcl); 4. ANALYSIS & TESTING (Lê código-fonte, queries, testes e compila). O slide conclui que a combinação de 'APEXlang skills' (Front-end) com 'SQLcl MCP' (Database) permite um desenvolvimento end-to-end impulsionado por IA.

#### Insight Técnico (Arquitetura & DBA)
A adoção do Model Context Protocol (MCP) para expor o SQLcl como um servidor de ferramentas para LLMs representa uma mudança de paradigma na automação de tarefas de DBA e desenvolvedor APEX. Ao permitir que agentes de IA interajam diretamente com o ciclo de vida do código (compilação, análise e testes) via SQLcl, reduz-se drasticamente o 'context switching' e o erro humano em tarefas repetitivas de CI/CD. Para um Arquiteto, isso significa que a governança de código e a execução de scripts de banco de dados podem ser delegadas a agentes com maior segurança, desde que as credenciais e o escopo do MCP sejam estritamente controlados no nível de infraestrutura.

---

### Slide 33: Integração do VS Code com Oracle APEX e Banco de Dados

- **Arquivo de Origem:** [`slides/33-vscode-oracle-apex-integration.png`](slides/33-vscode-oracle-apex-integration.png)
- **Tecnologias / Recursos Citados:** `VS Code`, `SQL Developer`, `APEXlang`, `Oracle APEX`, `Git`, `CI/CD`, `APEX 26.2`

#### Conteúdo Extraído
O slide apresenta o 'DEV APEX REINVENTED TOOLKIT', focando na sinergia entre VS Code e SQL Developer. Destaques: 1. .apx COMPILER: Plugin oficial para VS Code que integra o desenvolvimento APEX com o banco de dados. 2. Funcionalidades do Plugin: DATABASE (UX aprimorada para interação com o banco), IMPORT/EXPORT (gerenciamento de componentes, com menção ao 'live import' no APEX 26.2), e COMPARE (comparação de versões locais vs. remotas com visualização de diffs). 3. Conceito central: 'APEXlang in VS Code', unificando app, banco de dados e controle de versão em um único workflow.

#### Insight Técnico (Arquitetura & DBA)
Esta abordagem marca uma mudança de paradigma no desenvolvimento APEX, migrando da dependência exclusiva do Page Designer no browser para um modelo 'File-based' ou 'Code-centric'. Para arquitetos e DBAs, isso resolve o gargalo histórico de versionamento (Git) e CI/CD, permitindo que o código APEX seja tratado como código-fonte real. A introdução de 'live import' e diffs nativos reduz drasticamente o risco de conflitos em ambientes de desenvolvimento colaborativo e acelera o ciclo de vida de entrega (SDLC).

---

### Slide 34: Automação de Gestão de Tarefas com Model Context Protocol (MCP)

- **Arquivo de Origem:** [`slides/34-task-management-automation-mcp.png`](slides/34-task-management-automation-mcp.png)
- **Tecnologias / Recursos Citados:** `Model Context Protocol (MCP)`, `Jira`, `Azure DevOps`, `Oracle APEX`, `Kanban`

#### Conteúdo Extraído
O slide apresenta o conceito 'Dev APEX Reinvented Toolkit' com foco na automação de fluxos de trabalho de desenvolvimento. A mensagem central é 'FUCK JIRA. FUCK AZURE. Let MCP handle the boring work'. Visualmente, mostra um desenvolvedor codificando, onde o código flui através de um componente central chamado 'MCP' (Model Context Protocol) que atualiza automaticamente um quadro Kanban (To Do, In Progress, Done). O card de exemplo mostra a tarefa 'Implement login' com detalhes de esforço (5h), datas e status de PR (Pull Request) concluído.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto, vejo aqui uma proposta disruptiva de integração entre o ambiente de desenvolvimento (IDE/APEX) e ferramentas de gestão de projetos via MCP. A ideia é eliminar a carga administrativa manual (overhead) de atualizar tickets em ferramentas como Jira ou Azure DevOps. Para o ecossistema Oracle APEX, isso sugere a criação de agentes inteligentes que, ao detectar commits ou alterações em metadados de aplicações via APIs, atualizam automaticamente o status das tarefas, reduzindo o contexto de troca (context switching) e aumentando a produtividade do desenvolvedor focado em 'Low-Code'.

---

### Slide 35: Fluxo de Trabalho de Agente de IA para Jira

- **Arquivo de Origem:** [`slides/35-ai-agent-workflow-jira.png`](slides/35-ai-agent-workflow-jira.png)
- **Tecnologias / Recursos Citados:** `Jira`, `AI Agents`, `Orchestrator`, `PR (Pull Request)`, `Git`, `REST Data Sources`, `APEX Automations`

#### Conteúdo Extraído
O slide apresenta um workflow automatizado de 6 etapas para gestão de tarefas via agentes de IA: 1) Scan the Board (Jira); 2) A skill defines what counts as simple (classificação de complexidade); 3) Orchestrator assigns each task (distribuição de tarefas); 4) Agents test + document (execução e documentação); 5) Open a detailed PR (integração com Git); 6) Update the card + send a chat report (atualização de status e notificação). O resumo do processo é: 'One agent coordinates the work; task agents deliver it.'

#### Insight Técnico (Arquitetura & DBA)
Este slide ilustra a aplicação prática de AI Agents e Orchestration dentro do ciclo de vida de desenvolvimento (SDLC). Para um Arquiteto APEX, isso representa a evolução da automação de tarefas repetitivas através da integração via REST Data Sources com APIs de terceiros (Jira/GitHub). A arquitetura proposta sugere o uso de um 'Orchestrator' que pode ser implementado via APEX Automations ou PL/SQL, consumindo LLMs para tomada de decisão. O impacto é a redução drástica de 'toil' (trabalho manual), permitindo que desenvolvedores foquem em lógica de negócio complexa, enquanto a governança e o rastreamento de mudanças (PRs) são automatizados.

---

### Slide 36: Estratégia de Testes em Camadas para Desenvolvimento APEX

- **Arquivo de Origem:** [`slides/36-layered-testing-strategy-pyramid.png`](slides/36-layered-testing-strategy-pyramid.png)
- **Tecnologias / Recursos Citados:** `utPLSQL`, `CI/CD`, `Playwright`, `Agents`, `APEX`

#### Conteúdo Extraído
O slide apresenta o framework 'Testing: Build Confidence in Layers' com o lema 'Compilation is only the start'. O fluxo é dividido em três etapas: 1. Write Unit Tests While Building (utilizando Agents + utPLSQL); 2. Run Feature Tests in CI (processo de CI/CD); 3. Run Regression Tests + Track Coverage. O slide finaliza com uma recomendação prática: 'Can't build the full pipeline yet? Start with end-to-end tests' utilizando Playwright.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto, vejo este slide como uma mudança de paradigma necessária no ecossistema APEX. A transição de testes manuais para automação via utPLSQL (para lógica de banco) e Playwright (para a camada de UI/E2E) é o que separa aplicações corporativas resilientes de protótipos. A integração de 'Agents' sugere o uso de IA para acelerar a escrita de testes unitários, reduzindo o atrito do desenvolvedor. A ênfase em 'Coverage' e 'Regression' é crucial para governança em ambientes de CI/CD, garantindo que mudanças no Page Designer ou em pacotes PL/SQL não quebrem funcionalidades existentes.

---

### Slide 37: Automação de Testes E2E com Playwright e MCP

- **Arquivo de Origem:** [`slides/37-playwright-mcp-e2e-testing.png`](slides/37-playwright-mcp-e2e-testing.png)
- **Tecnologias / Recursos Citados:** `Playwright`, `MCP (Model Context Protocol)`, `Headless Browser`, `AI Agent`, `CI/CD`, `Oracle APEX`

#### Conteúdo Extraído
O slide apresenta um fluxo de trabalho para automação de testes utilizando um agente de IA integrado ao Playwright via MCP (Model Context Protocol). O processo segue as etapas: 1. PLAN: O agente planeja os testes. 2. PLAYWRIGHT MCP: Execução dos testes em um headless browser. 3. INSPECT RESULTS: Análise dos resultados. 4. FIX + RETEST: Ciclo de correção e reteste. O sistema gera evidências como 'TRACE: ACTIONS + LOGS' e 'TEST VIDEO'. A mensagem central destaca: 'An agent can plan and run end-to-end checks' e 'When a test fails, the agent has evidence to diagnose the issue'.

#### Insight Técnico (Arquitetura & DBA)
A integração de agentes de IA com o Playwright via MCP representa uma mudança de paradigma no QA para aplicações Oracle APEX. Tradicionalmente, testes E2E em APEX são frágeis devido à natureza dinâmica dos IDs de elementos (DOM). O uso de agentes capazes de 'raciocinar' sobre o DOM, aliado a artefatos de diagnóstico (traces e vídeos), reduz drasticamente o MTTR (Mean Time To Repair). Para um Arquiteto APEX, isso viabiliza a implementação de CI/CD robusto, permitindo que o pipeline não apenas reporte falhas, mas forneça contexto suficiente para que o próprio agente ou o desenvolvedor identifique a causa raiz (ex: uma Dynamic Action que falhou ou um erro de PL/SQL disparado via AJAX).

---

### Slide 38: Automação de Testes E2E com IA e Playwright no Ciclo de Vida APEX

- **Arquivo de Origem:** [`slides/38-playwright-ai-e2e-lifecycle.png`](slides/38-playwright-ai-e2e-lifecycle.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `Playwright`, `CI/CD`, `Git`, `AI Agents`, `LLM`

#### Conteúdo Extraído
O slide apresenta um fluxo de trabalho para automação de testes em aplicações APEX: 1. Map each feature scenario (Mapeamento de cenários); 2. Agents write the tests (Uso de agentes de IA para gerar código Playwright); 3. Review + commit the suite (Revisão humana e versionamento); 4. CI runs it on every PR (Execução automatizada em pipelines de CI). Inclui um snippet de código Playwright: 'import { test } from '@playwright'; test('feature', () => { await page.click(); });'. O fluxo enfatiza ser 'Deterministic', 'Repeatable' e 'Lower Token Cost'.

#### Insight Técnico (Arquitetura & DBA)
A adoção de Playwright para testes E2E em APEX resolve um dos maiores gargalos de governança e qualidade: a dependência de testes manuais. Ao integrar agentes de IA para gerar os scripts de teste, reduz-se o custo cognitivo e o tempo de desenvolvimento. Do ponto de vista de arquitetura, isso viabiliza a implementação de um pipeline de CI/CD robusto, garantindo que mudanças no Page Designer ou alterações em Dynamic Actions não quebrem funcionalidades críticas. A abordagem 'Lower Token Cost' sugere que, ao manter uma suíte de testes versionada no Git, evita-se o consumo excessivo de tokens de LLM para re-explorar cenários que já foram validados anteriormente.

---

### Slide 39: Estabelecendo um Ciclo de Qualidade em Pull Requests (PR)

- **Arquivo de Origem:** [`slides/39-pull-request-quality-gates-docker.png`](slides/39-pull-request-quality-gates-docker.png)
- **Tecnologias / Recursos Citados:** `APEX`, `SQLcl`, `APEXLANG`, `Docker`, `CI/CD`, `Git`, `AI Agents`

#### Conteúdo Extraído
O slide apresenta um framework para automação e governança de código em APEX. Componentes principais: 1. Ciclo de Feedback: 'Read Review Comments + CI Coverage' -> 'Implement Fixes' -> 'Rerun The Gates'. 2. Automação de Pipeline: Fluxo sequencial composto por APEXLANG + SQLCL, Linter, Security Scan, Isolated APEX in Docker e Regression Tests. 3. Estratégia de IA: Uso de 'Agentic review' para filtrar mudanças rotineiras e 'Specialized reviews' para PRs de alto risco. 4. Regra de Ouro: 'Merge only after the checks pass'.

#### Insight Técnico (Arquitetura & DBA)
Como Arquiteto, este slide propõe a transição do desenvolvimento APEX tradicional para um modelo de 'Engineering-first'. A integração de SQLcl com ferramentas de CI/CD é o divisor de águas para garantir que o metadata do APEX seja validado antes do merge. O uso de 'Isolated APEX in Docker' resolve o problema histórico de ambientes de teste efêmeros, permitindo que o pipeline valide mudanças sem depender de instâncias compartilhadas. A automação via agentes reduz a carga cognitiva do revisor humano, permitindo foco em lógica de negócio complexa enquanto a máquina garante padrões de segurança e performance.

---

### Slide 40: Encerramento e Canais de Contato da Palestra

- **Arquivo de Origem:** [`slides/40-conclusion-community-contacts.png`](slides/40-conclusion-community-contacts.png)
- **Tecnologias / Recursos Citados:** `Oracle APEX`, `Oracle ACE Program`, `Oracle Cloud World Tour`, `APEX HUB`

#### Conteúdo Extraído
O slide funciona como uma tela de encerramento contendo: 1. QR Code para LinkedIn do palestrante (Bruno Cardoso). 2. QR Code para o APEX HUB. 3. Foto do palestrante com badge de 'Oracle ACE Associate' no evento Oracle Cloud World Tour São Paulo. 4. Texto central de agradecimento em três idiomas: 'Thank you! Obrigado! Gracias!'. 5. Rodapé com links (via QR Code) para: Slides, Referências e Mentorias (WhatsApp).

#### Insight Técnico (Arquitetura & DBA)
Do ponto de vista de um Arquiteto APEX, este slide consolida a importância da comunidade e do networking no ecossistema Oracle. O uso de QR Codes para centralizar recursos (Slides, Referências, Mentorias) é uma prática recomendada para disseminação de conhecimento técnico e governança de conteúdo pós-evento. A menção ao 'APEX HUB' reforça a centralização de melhores práticas e componentes reutilizáveis, essenciais para o ciclo de vida de desenvolvimento em APEX, garantindo que a comunidade tenha acesso a padrões de arquitetura validados.

---

## 3. Inventário de Recursos e Tecnologias Citadas

### 1. Ferramentas e Ambientes de Desenvolvimento (IDEs & CLIs)
- **Oracle APEX (versões modernas com suporte declarativo e IA)**: Page Designer, Shared Components, Universal Theme.
- **Visual Studio Code (VS Code)**: IDE central para edição de código, extensões Oracle e orquestração de agentes.
- **Oracle SQLcl**: Interface CLI moderna da Oracle utilizada como motor de automação e ponte de comunicação via MCP.
- **Git & GitHub**: Versionamento de código, rastreamento de branchings, pull requests e gatilhos de CI/CD.

### 2. Especificações e Linguagens
- **APEXlang**: Representação declarativa legível para humanos e LLMs, estruturada para versionamento no Git sem ruído de metadados internos.
- **SQL e PL/SQL**: Lógica de negócios em banco de dados, pacotes transacionais, triggers e APIs nativas do APEX (`APEX_UTIL`, `APEX_APPLICATION`).
- **JavaScript & Node.js**: Automação externa de scripts, clientes MCP e suites de testes.
- **JSON & YAML**: Formatos de intercâmbio de contexto, configurações de harness e definição de tarefas.

### 3. Inteligência Artificial, Model Context Protocol e Orquestração
- **Model Context Protocol (MCP)**: Protocolo padronizado de comunicação entre assistentes de IA (ex: Claude, Gemini, GPT) e recursos locais (servidor SQLcl MCP).
- **Sub-Agentes Autônomos**: Decomposição em agentes com papéis segregados (Planner, Coder, Reviewer, Tester) comunicando-se via barramento de mensagens.
- **Técnicas de Prompt Engineering & Context Management**: Mitigação de *Context Rot*, offloading de ferramentas e arquitetura de memória externa (vetores e cache).

### 4. Qualidade de Software, Testes & CI/CD
- **Playwright**: Framework de automação de testes de ponta a ponta (E2E) para navegadores modernos (Chromium, Firefox, WebKit).
- **Testes em Camadas (Pyramid Testing)**: Testes unitários no banco (utPLSQL), testes de integração de REST Data Sources e testes E2E com Playwright.
- **Automação de Task Tracking**: Integração de agentes com GitHub Issues e boards de tarefas para resolução automatizada de bugs e novas features.


---

## 4. Plano de Ação e Exploração Prática (PoCs / Laboratórios)

### Prova de Conceito 1: Implementação de Servidor MCP com SQLcl para Assistente de IA
- **Objetivo:** Permitir que agentes e assistentes de IA (no VS Code ou CLI) consultem o esquema do Oracle Database e o repositório do APEX de forma segura e governada através do Model Context Protocol (MCP).
- **Tecnologias Utilizadas:** Oracle SQLcl, VS Code (com Claude Code ou Roo/Cline), protocolo MCP, Oracle Database 19c/23ai.
- **Passo a Passo de Execução:**
  1. Configurar o Oracle SQLcl localmente e registrar o servidor MCP nativo.
  2. Configurar o cliente MCP na IDE apontando para o binário do SQLcl com credenciais de desenvolvedor (mínimo privilégio).
  3. Realizar consultas de dicionário (`USER_TABLES`, `APEX_APPLICATION_PAGES`) através do agente para geração assistida de consultas SQL conformes ao padrão corporativo.

---

### Prova de Conceito 2: Ciclo Git & Automação Declarativa com APEXlang
- **Objetivo:** Eliminar conflitos de merge e a poluição de IDs internos do APEX através da conversão e versionamento no padrão APEXlang.
- **Tecnologias Utilizadas:** Git, GitHub Actions, APEXlang Toolkit, Oracle APEX.
- **Passo a Passo de Execução:**
  1. Exportar uma aplicação APEX piloto decomposta em arquivos granulares.
  2. Converter as páginas para a representação textual APEXlang.
  3. Criar uma branch de feature, solicitar que um desenvolvedor ou agente realize uma alteração pontual (ex: adicionar um item ou validação) no arquivo APEXlang.
  4. Executar o `git diff` e validar a legibilidade das alterações antes de disparar o re-empacotamento e deploy no ambiente de desenvolvimento.

---

### Prova de Conceito 3: Automação de Testes E2E com Playwright em Componentes APEX
- **Objetivo:** Criar uma suite automatizada de testes funcionais contra telas críticas do APEX (login, relatórios interativos e formulários modais).
- **Tecnologias Utilizadas:** Node.js, Playwright, Oracle APEX (Universal Theme).
- **Passo a Passo de Execução:**
  1. Inicializar um projeto Playwright na raiz de um repositório de testes (`npm init playwright@latest`).
  2. Implementar helpers específicos para o APEX: tratamento de autenticação por sessão, manipulação de seletores com classes semânticas (`.t-Form-input`, `.a-IRR-table`) em substituição a IDs dinâmicos.
  3. Criar um fluxo de validação de CRUD completo (inserção de registro em formulário modal, validação no Interactive Grid e exclusão).
  4. Integrar a execução do Playwright em modo headless em um pipeline de CI/CD.

---

### Prova de Conceito 4: Arquitetura de Sub-Agentes para Resolução de Chamados / Issues
- **Objetivo:** Estabelecer um fluxo autônomo baseado no conceito de *Harness* onde um agente lê uma issue no GitHub, diagnostica o código PL/SQL correspondente e submete um Pull Request com testes.
- **Tecnologias Utilizadas:** GitHub Issues, Python/Agentic Framework, SQLcl MCP, Playwright.
- **Passo a Passo de Execução:**
  1. Definir o *harness* de restrições (arquivos de regras, convenções de código PL/SQL e esquemas autorizados).
  2. Submeter uma issue descritiva (ex: "Validação incorreta de limite de crédito na página 12").
  3. O Agente de Diagnóstico inspeciona a especificação do APEX e o pacote PL/SQL via SQLcl MCP.
  4. O Agente Desenvolvedor aplica o patch no código PL/SQL.
  5. O Agente Testador gera e executa o teste Playwright para garantir que a regressão não foi introduzida.

