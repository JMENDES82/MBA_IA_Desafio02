"""Validação estrutural; não substitui a avaliação real por LLM."""
import sys
from pathlib import Path
import pytest
import yaml
from langchain_core.prompts import ChatPromptTemplate
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from push_prompts import validate_prompt

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def prompt():
    return yaml.safe_load((ROOT / "prompts/bug_to_user_story_v2.yml").read_text(encoding="utf-8"))["bug_to_user_story_v2"]

def test_prompt_has_system_prompt(prompt):
    assert isinstance(prompt["system_prompt"], str) and prompt["system_prompt"].strip()

def test_prompt_has_role_definition(prompt):
    assert "Você é um Product Manager" in prompt["system_prompt"]

def test_prompt_mentions_format(prompt):
    text = prompt["system_prompt"]
    assert "Markdown" in text
    assert "Como [persona], eu quero" in text and "para que [benefício]" in text
    assert "Dado/Quando/Então" in text

def test_prompt_has_few_shot_examples(prompt):
    text = prompt["system_prompt"]
    assert text.count("— Entrada:") >= 2
    assert text.count("Saída:") >= 2
    assert text.count("## Critérios de aceitação") >= 3

def test_prompt_no_todos(prompt):
    assert "TODO" not in yaml.safe_dump(prompt).upper()

def test_minimum_techniques(prompt):
    techniques = prompt["techniques_applied"]
    assert len(set(techniques)) >= 2
    assert "few-shot" in techniques
    assert "role-prompting" in techniques

def test_template_renders_only_bug_report(prompt):
    assert validate_prompt(prompt) == (True, [])
    template = ChatPromptTemplate.from_messages([
        ("system", prompt["system_prompt"]), ("human", prompt["user_prompt"])
    ])
    assert template.input_variables == ["bug_report"]
    messages = template.format_messages(bug_report="Falha {literal} ao salvar")
    assert len(messages) == 2
    assert "Falha {literal}" not in messages[0].content
    assert "Falha {literal}" in messages[1].content

@pytest.mark.parametrize("field,value", [
    ("system_prompt", ""), ("user_prompt", "{unknown}"),
    ("techniques_applied", ["few-shot", "few-shot"]),
    ("techniques_applied", None), ("tags", "not-a-list"), ("version", "v1"),
    ("system_prompt", "TODO"), ("user_prompt", "{bug_report} {"),
])
def test_reject_invalid_prompt(prompt, field, value):
    prompt[field] = value
    assert validate_prompt(prompt)[0] is False

def test_reject_non_mapping():
    assert validate_prompt(None)[0] is False
