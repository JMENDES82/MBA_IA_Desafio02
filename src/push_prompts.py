"""Valida o YAML e publica v2 no LangSmith Prompt Hub."""
import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars

ROOT = Path(__file__).resolve().parents[1]
NAME = "bug_to_user_story_v2"
load_dotenv(ROOT / ".env")

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    errors = []
    if not isinstance(prompt_data, dict):
        return False, ["Prompt deve ser um objeto YAML"]
    for field in ("description", "system_prompt", "user_prompt", "version"):
        if not isinstance(prompt_data.get(field), str) or not prompt_data[field].strip():
            errors.append(f"Campo obrigatório inválido: {field}")
    if prompt_data.get("version") != "v2":
        errors.append("version deve ser v2")
    techniques = prompt_data.get("techniques_applied")
    if (not isinstance(techniques, list) or
            any(not isinstance(t, str) or not t.strip() for t in techniques) or
            len(set(techniques)) < 2 or "few-shot" not in techniques):
        errors.append("Liste few-shot e outra técnica distinta")
    tags = prompt_data.get("tags", [])
    if not isinstance(tags, list) or any(not isinstance(t, str) for t in tags):
        errors.append("tags deve ser lista de textos")
    text = " ".join(str(prompt_data.get(f, "")) for f in ("system_prompt", "user_prompt"))
    if "TODO" in text.upper():
        errors.append("Remova marcadores TODO")
    if not errors:
        try:
            template = ChatPromptTemplate.from_messages([
                ("system", prompt_data["system_prompt"]), ("human", prompt_data["user_prompt"])
            ])
            if template.input_variables != ["bug_report"]:
                errors.append("A única variável deve ser bug_report")
            if "{bug_report}" in prompt_data["system_prompt"]:
                errors.append("Mantenha o relato somente no user_prompt")
        except (ValueError, TypeError, KeyError):
            errors.append("Template inválido")
    return not errors, errors

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    valid, errors = validate_prompt(prompt_data)
    if not valid:
        print("\n".join(errors))
        return False
    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
    if prompt_name != NAME or not re.fullmatch(r"[A-Za-z0-9_-]+", username):
        print("Configure um handle válido do Hub e use o nome v2.")
        return False
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system_prompt"]), ("human", prompt_data["user_prompt"])
    ])
    techniques = prompt_data["techniques_applied"]
    prompt.metadata = {"version": "v2", "techniques_applied": techniques}
    try:
        url = Client().push_prompt(
            f"{username}/{prompt_name}", object=prompt, is_public=True,
            description=prompt_data["description"] + " | Técnicas: " + ", ".join(techniques),
            tags=list(dict.fromkeys(prompt_data.get("tags", []) + techniques)),
        )
    except Exception as exc:
        print(f"Falha no push ({type(exc).__name__}). Confira credenciais, handle e acesso.")
        return False
    print(f"Prompt público publicado: {url}")
    return True

def main():
    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1
    data = load_yaml(str(ROOT / "prompts/bug_to_user_story_v2.yml"))
    if not isinstance(data, dict) or set(data) != {NAME}:
        print(f"O YAML deve conter exatamente a chave {NAME}")
        return 1
    return 0 if push_prompt_to_langsmith(NAME, data[NAME]) else 1

if __name__ == "__main__":
    sys.exit(main())
