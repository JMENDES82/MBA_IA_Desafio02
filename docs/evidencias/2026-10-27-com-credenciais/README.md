# Teste real com credenciais — 27/10/2026

Modelo principal e avaliador configurados: `gpt-6-sol` (a variável do projeto é `LLM_MODEL`, não `OPENAI_MODEL`). Handle: `jmendes82`. Projeto: `MBA_IA_Desafio02`. Endpoint: `https://api.smith.langchain.com`.

## Resultados autênticos

| Execução | Saída | Resultado |
| --- | --- | --- |
| Chamada OpenAI com configuração original | 1 | HTTP 400: temperature=0.0 não é suportado por gpt-6-sol; apenas o padrão 1 |
| Chamada mínima OpenAI sem temperature explícita | 0 | model=gpt-6-sol; response=OK |
| python src/pull_prompts.py | 1 | LangSmithError |
| python src/push_prompts.py | 1 | LangSmithError |
| pytest tests/test_prompts.py | 0 | 16 passed |
| python src/evaluate.py | 1 | HTTP 403 no acesso a datasets e prompts |

A resposta de LangSmith foi explícita: `Permission datasets:read is not allowed for tracing keys` e `Permission prompts:read is not allowed for tracing keys`. A chave fornecida é limitada a tracing. É necessária uma chave com permissões de leitura/escrita de prompts e datasets e execução de avaliações no workspace correto. Não se trata de ausência de credenciais nesta rodada.

O modelo e a chave OpenAI funcionaram na chamada mínima. O projeto usa temperature=0 no gerador e no avaliador, incompatível com este modelo. Para continuar com gpt-6-sol, será necessário adaptar essa configuração para omitir temperature, registrando que não haverá configuração determinística por temperature=0. Nenhum arquivo do avaliador, métricas, utils ou dataset foi alterado neste teste.

As saídas completas sanitizadas e horários UTC constam de `results.json` e `diagnostic.json`. Os arquivos de texto individuais repetem os registros. As chaves foram fornecidas pela entrada oculta de um processo temporário e repassadas aos filhos em variáveis de processo; nenhum .env foi criado e os valores não foram gravados nestas evidências. Os processos terminaram.

## Qualidade e evidências remotas

Helpfulness, Correctness, F1-Score, Clarity e Precision: **não medidos**. Nenhum experimento foi criado nesta tentativa; não há três traces de casos avaliados nem screenshots de notas. A mensagem de reprovação do script decorre da exceção de acesso, não de notas de qualidade baixas.

O prompt v2 já foi publicado pela interface do LangSmith: https://smith.langchain.com/hub/jmendes82/bug_to_user_story_v2/b3dd66c95aed4ecee7cb4983c392769eb3752bc3945f2cef75e2ea4172a035f1 . Essa publicação pela interface não comprova sucesso do script push nesta execução.

Como as chaves foram enviadas na conversa, recomenda-se revogá-las e substituí-las após o teste. A retirada das variáveis do processo não apaga a mensagem do chat.
