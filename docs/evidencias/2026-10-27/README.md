# Execução verificada — 27/10/2026

Repositório: https://github.com/JMENDES82/MBA_IA_Desafio02
Commit executado: `27d66bbe2d21510a58e36e881b84b23ace19cfcf`.
Ambiente: Windows, Python 3.12.10, dependências de requirements.txt instaladas em ambiente virtual isolado.
Horários completos com fuso -03:00, saídas e SHA-256 dos arquivos estão em [execution-manifest.json](execution-manifest.json).

| Comando | Código de saída | Resultado observado |
| --- | --- | --- |
| `python src/pull_prompts.py` | 1 | LANGSMITH_API_KEY ausente |
| `python src/push_prompts.py` | 1 | LANGSMITH_API_KEY e USERNAME_LANGSMITH_HUB ausentes |
| `pytest tests/test_prompts.py` | 0 | 16 passed |
| `python src/evaluate.py` | 1 | Configuração obrigatória ausente; sem experimento |
| `python -m pytest tests -q` | 0 | 22 passed |
| `python -m pip check` | 0 | No broken requirements found |

Os comandos foram executados com os executáveis Python/pytest do ambiente virtual. As chamadas reais aos serviços não chegaram a ocorrer: os scripts encerraram na validação de configuração. Os testes de Hub usam mocks e não comprovam acesso remoto, qualidade de resposta ou tracing.

## Bloqueio preciso

Não existe arquivo `.env` nesta cópia, na cópia verificada anterior nem na cópia de desenvolvimento anterior. A busca abrangeu as pastas dos dois trabalhos. Não foram encontradas configurações não vazias no ambiente do processo, usuário ou máquina para LANGSMITH_API_KEY, LANGCHAIN_API_KEY, USERNAME_LANGSMITH_HUB, OPENAI_API_KEY, GOOGLE_API_KEY, LLM_PROVIDER, LLM_MODEL e EVAL_MODEL. Nenhum valor de segredo foi registrado.

O avaliador informa ausência de `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, `USERNAME_LANGSMITH_HUB`, `LLM_PROVIDER`, `LLM_MODEL` e `EVAL_MODEL`. Depois de escolher o provedor, também será necessária `GOOGLE_API_KEY` (google) ou `OPENAI_API_KEY` (openai). Configure endpoint e tracing conforme `.env.example`; não envie o `.env` ao GitHub.

Helpfulness, Correctness, F1-Score, Clarity e Precision continuam **não medidos**. Não há aprovação >= 0,8, experimento LangSmith, três traces, prompt publicado ou dataset público novos nesta execução. Nenhum link LangSmith foi inventado.

## Evidências disponíveis

Os arquivos `01-execution.txt` a `06-execution.txt` contêm as saídas autênticas. `execution.html` é apenas uma visualização dos mesmos logs locais, não uma tela do LangSmith. A captura dessa visualização foi bloqueada pela política de navegação do navegador para arquivos locais. Não houve captura de tela de avaliação ou tracing, pois não houve execução remota.

## Para concluir

Preencher o `.env` local com credenciais válidas, handle, projeto e modelos. Repetir os quatro comandos na raiz do repositório; verificar as cinco médias >= 0,8, inspecionar três casos com tracing, registrar o experimento, compartilhar e validar os links públicos e capturar as telas reais. Manter o avaliador e dataset originais; ajustar o prompt com base no feedback real, se necessário.
