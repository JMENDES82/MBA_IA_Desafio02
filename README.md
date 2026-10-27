# MBA IA — Desafio 02

Implementação do desafio **Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith**.
Fork de [devfullcycle/mba-ia-pull-evaluation-prompt](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt).
Autor: [JMENDES82](https://github.com/JMENDES82).
[Primeiro desafio](https://github.com/JMENDES82/MBA_IA_Desafio01).

## Status da entrega

Código validado localmente. **Avaliação real no LangSmith bloqueada por permissões da chave de tracing.**
Em 27/10/2026, os quatro comandos foram executados com credenciais temporárias:
16 testes de prompt passaram; pull, push e avaliação falharam por acesso negado.
LangSmith retornou HTTP 403 para `datasets:read` e `prompts:read`, não permitidos para tracing keys.

A chave OpenAI e `gpt-6-sol` funcionaram em chamada mínima (resposta `OK`).
O modelo rejeitou `temperature=0` usado pelo projeto; para mantê-lo, será necessário
adaptar a configuração para omitir temperature. Avaliador, métricas, utils e dataset
não foram alterados nesta execução. Nenhuma das cinco notas foi medida.

[Resultados e logs reais com credenciais](docs/evidencias/2026-10-27-com-credenciais/README.md).
A suíte completa local anterior passou com 22 testes e sem conflitos de dependências.

O ZIP citado na conversa anterior (`/mnt/data/fullcycle-solucao-langsmith.zip`) não estava
disponível neste computador. Esta implementação foi construída a partir do fork.
O YAML v1 é a semente incluída pelo upstream; o script de pull poderá atualizá-lo com a versão do Hub.

## Execução inicial sem credenciais em 27/10/2026 (histórico)

Repositório publicado clonado e verificado no commit `27d66bbe2d21510a58e36e881b84b23ace19cfcf`.
Executados os quatro comandos solicitados: **16 testes de prompt passaram**;
pull, push e avaliação encerraram com código 1 por configuração ausente.
A suíte completa passou com **22 testes**, e `pip check` não encontrou conflitos.

Faltam `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, `USERNAME_LANGSMITH_HUB`,
`LLM_PROVIDER`, `LLM_MODEL`, `EVAL_MODEL` e a chave do provedor escolhido
(`GOOGLE_API_KEY` ou `OPENAI_API_KEY`). Não foi encontrado `.env` nos trabalhos
inspecionados nem credenciais nas variáveis de processo, usuário ou máquina.

As cinco notas seguem não medidas; experimento, três traces, screenshots do
LangSmith e links públicos do Hub/dataset permanecem pendentes.
[Relatório e logs autênticos da execução](docs/evidencias/2026-10-27/README.md)
incluem horários, códigos de saída e hashes SHA-256 dos arquivos executados.

## Técnicas Aplicadas (Fase 2)

- **Few-shot Learning:** três pares entrada/saída mostram uma falha de persistência de fonte,
  validação de título e relato insuficiente com tentativa de mudar as instruções.
  Os exemplos ensinam estrutura, concisão e como pedir esclarecimentos; foram escritos
  para o prompt, sem copiar as respostas de referência do dataset.
- **Role Prompting:** persona de Product Manager experiente em requisitos e qualidade.
  Direciona a resposta para valor do usuário e critérios verificáveis, sem diagnóstico técnico inventado.
- **Skeleton of Thought:** seções fixas Título, User Story, Contexto, Critérios de aceitação,
  Lacunas e perguntas. Organiza o artefato final sem exigir exposição de raciocínio interno.

O system prompt contém regras e exemplos; o user prompt contém a única variável
`{bug_report}`. Há regras para dados ausentes, contradições, múltiplos bugs,
dados sensíveis e instruções maliciosas no relato. Essas regras orientam o modelo;
sua eficácia comportamental ainda precisa ser observada em execuções reais.

## Comparação v1 × v2

| Aspecto | v1 (upstream) | v2 |
| --- | --- | --- |
| Persona | Assistente genérico | Product Manager com contexto de requisitos |
| Entrada | Relato duplicado no system e user | Relato apenas no user |
| Instruções | Pedido aberto | Regras explícitas e fatos preservados |
| Exemplos | Ausentes | Três pares entrada/saída |
| Formato | Livre | Markdown, história e critérios Dado/Quando/Então |
| Incerteza | Sem orientação | Lacunas e perguntas, sem inventar causas |
| Qualidade medida | Sem execução nesta entrega | Avaliação real pendente |

## Como Executar

Pré-requisitos: Python 3.10+, conta LangSmith com handle público e acesso a um
provedor de LLM suportado (Google ou OpenAI).

Execute os comandos na raiz do repositório. Crie um ambiente virtual:

```bash
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
# source venv/bin/activate
python -m pip install -r requirements.txt
```

Copie `.env.example` para `.env` (PowerShell: `Copy-Item .env.example .env`;
Linux/macOS: `cp .env.example .env`). Preencha localmente:

- `LANGSMITH_API_KEY`, `LANGSMITH_ENDPOINT` e `LANGSMITH_TRACING=true`.
- `LANGSMITH_PROJECT=MBA_IA_Desafio02`.
- `USERNAME_LANGSMITH_HUB`: seu handle público, que pode diferir do login do GitHub.
- `LLM_PROVIDER=google` e `GOOGLE_API_KEY`, ou `LLM_PROVIDER=openai` e `OPENAI_API_KEY`.
- `LLM_MODEL` e `EVAL_MODEL`: modelos disponíveis na conta e compatíveis com `temperature=0`.
  Consulte a documentação de modelos do provedor antes de configurá-los.

Para criar o handle: LangSmith > Prompts > abra/crie um prompt > menu de três pontos >
Make Public > Choose your public handle. A escolha é definitiva.

```bash
# Validação local, sem chamadas ao Hub ou LLM:
python -m pytest tests -q

# Pull da semente autorizada (sobrescreve somente o YAML v1):
python src/pull_prompts.py

# Publicação PÚBLICA de <handle>/bug_to_user_story_v2:
python src/push_prompts.py

# Avaliação dos 15 exemplos e gravação de feedback no LangSmith:
python src/evaluate.py
```

O push inclui versão e técnicas nos metadados do template, além de descrição e tags
do repositório do Hub. YAML inválido é rejeitado antes da conexão.
O opt-in `dangerously_pull_public_prompt=True` é limitado à semente fixa autorizada
pelo enunciado; prompts do Hub são objetos serializados e não devem ser obtidos de fontes arbitrárias.

## Resultados Finais

**Avaliação real bloqueada por permissões LangSmith e configuração de temperatura.** Testes estruturais e simulações não medem a qualidade das respostas.

| Métrica | Resultado real | Meta |
| --- | --- | --- |
| Helpfulness | Não medido | >= 0,8 |
| Correctness | Não medido | >= 0,8 |
| F1-Score | Não medido | >= 0,8 |
| Clarity | Não medido | >= 0,8 |
| Precision | Não medido | >= 0,8 |

A avaliação original calcula F1 por LLM-as-Judge; Helpfulness é a média de Clarity e Precision,
e Correctness é a média de F1 e Precision. O relatório exige cada uma das cinco médias
>= 0,8, além da média geral. Confira também os exemplos individuais e falhas de execução.

Pendências para concluir a avaliação acadêmica:

1. Substituir a chave de tracing por uma chave com permissões para prompts, datasets e avaliações. O handle `jmendes82` já foi criado e o prompt v2 publicado pela interface. Ajustar a compatibilidade de temperatura para `gpt-6-sol` antes de repetir os scripts.
2. Rodar o avaliador original contra os 15 exemplos. Registrar modelos, commit do prompt,
   URL do experimento e as cinco notas reais.
3. Realizar 3–5 iterações conforme o enunciado: analisar feedback, modificar apenas o prompt,
   repetir push e avaliação até cumprir todas as metas. Registrar cada tentativa na tabela.
4. Verificar tracing detalhado de pelo menos três exemplos e capturar screenshots das notas.
5. Compartilhar o dataset e incluir aqui seu link público e as evidências.

| Iteração real | Commit do prompt | Modelos | Notas / experimento | Ajuste motivado pelo feedback |
| --- | --- | --- | --- | --- |
| Ainda não executada | — | — | — | — |

Após avaliar, compartilhe o dataset uma única vez, usando as credenciais locais:

```python
import os
from dotenv import load_dotenv
from langsmith import Client
load_dotenv()
print(Client().share_dataset(dataset_name=f"{os.environ['LANGSMITH_PROJECT']}-eval")["url"])
```

O link privado de experimento não substitui o link público do dataset.
Valide o link em uma sessão sem autenticação. Compartilhar novamente pode mudar o endereço.
Salve screenshots revisadas em `docs/evidencias/`, sem tokens nem dados pessoais.

## Preservação e segurança

`src/evaluate.py`, `src/metrics.py`, `src/utils.py` e
`datasets/bug_to_user_story.jsonl` permanecem idênticos ao upstream de referência
`a94ce443299b4928d0f1e08cecdacf7a36ff5fb1`. Dependências e suporte multiprovedor foram preservados.

Não envie `.env`, chaves, ambientes virtuais ou logs ao GitHub. Apenas `.env.example`
sem valores de segredo faz parte da entrega. Revise as evidências antes de publicá-las.
Os scripts implementados não imprimem o conteúdo de exceções remotas.
