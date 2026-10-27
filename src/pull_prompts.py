"""Baixa somente a semente pública autorizada pelo desafio."""
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import check_env_vars, save_yaml

ROOT = Path(__file__).resolve().parents[1]
SEED = "leonanluppi/bug_to_user_story_v1"
load_dotenv(ROOT / ".env")

def pull_prompts_from_langsmith():
    prompt = Client().pull_prompt(SEED, dangerously_pull_public_prompt=True)
    if not isinstance(prompt, ChatPromptTemplate):
        raise ValueError("Esperado ChatPromptTemplate")
    messages = {}
    for message in prompt.messages:
        role = message.__class__.__name__.replace("MessagePromptTemplate", "").lower()
        field = {"system": "system_prompt", "human": "user_prompt"}.get(role)
        template = getattr(getattr(message, "prompt", None), "template", None)
        if field is None or field in messages or not isinstance(template, str):
            raise ValueError("Esperadas uma mensagem system e uma human de texto")
        messages[field] = template
    if set(messages) != {"system_prompt", "user_prompt"}:
        raise ValueError("Semente sem system ou user")
    data = {"bug_to_user_story_v1": {
        "description": "Prompt inicial obtido do LangSmith Hub",
        **messages, "version": "v1", "source": SEED,
    }}
    if not save_yaml(data, str(ROOT / "prompts/bug_to_user_story_v1.yml")):
        raise OSError("Falha ao salvar YAML")
    return data

def main():
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1
    try:
        pull_prompts_from_langsmith()
    except Exception as exc:
        print(f"Falha no pull ({type(exc).__name__}). Confira credenciais, acesso e formato.")
        return 1
    print("Semente salva em prompts/bug_to_user_story_v1.yml")
    return 0

if __name__ == "__main__":
    sys.exit(main())
