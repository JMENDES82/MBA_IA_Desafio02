# MBA IA — Desafio 02

Implementação do desafio **Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith**.
Fork de [devfullcycle/mba-ia-pull-evaluation-prompt](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt).
Autor: [JMENDES82](https://github.com/JMENDES82).
[Primeiro desafio](https://github.com/JMENDES82/MBA_IA_Desafio01).

## Status da entrega

Código implementado e validado localmente. **Avaliação real no LangSmith pendente**:
não foram fornecidos neste ambiente chave LangSmith, handle do Hub nem configuração de modelos.
Nenhuma nota de LLM, publicação no Hub, execução de pull remoto ou aprovação >= 0,8 é alegada.

Validação local em 27/10/2026: **22 testes passaram**, incluindo os seis requisitos
do enunciado, renderização do template, rejeição de YAML inválido e contratos de
pull/push simulados. Dependências instaladas com sucesso e sem conflitos detectados.

O ZIP citado na conversa anterior (`/mnt/data/fullcycle-solucao-langsmith.zip`) não estava
disponível neste computador. Esta implementação foi construída a partir do fork.
O YAML v1 é a semente incluída pelo upstream; o script de pull poderá atualizá-lo com a versão do Hub.

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

**Pendente de execução real.** Testes estruturais e simulações não medem a qualidade das respostas.

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

1. Configurar credenciais, handle e modelos; executar pull e push e verificar o prompt público no Hub.
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
