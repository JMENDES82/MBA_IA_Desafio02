"""Contrato do Hub com clientes simulados: nenhuma rede ou segredo."""
import sys
from pathlib import Path
from unittest.mock import Mock
import pytest
import yaml
from langchain_core.prompts import ChatPromptTemplate
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pull_prompts
import push_prompts

@pytest.fixture
def prompt():
    path = Path(__file__).resolve().parents[1] / "prompts/bug_to_user_story_v2.yml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))[push_prompts.NAME]

def test_pull_preserves_messages_and_authorized_source(monkeypatch, tmp_path):
    template = ChatPromptTemplate.from_messages([("system", "Instruções"), ("human", "{bug_report}")])
    client = Mock()
    client.pull_prompt.return_value = template
    monkeypatch.setattr(pull_prompts, "Client", lambda: client)
    monkeypatch.setattr(pull_prompts, "ROOT", tmp_path)
    data = pull_prompts.pull_prompts_from_langsmith()
    client.pull_prompt.assert_called_once_with(
        pull_prompts.SEED, dangerously_pull_public_prompt=True)
    stored = yaml.safe_load((tmp_path / "prompts/bug_to_user_story_v1.yml").read_text(encoding="utf-8"))
    assert stored == data
    result = stored["bug_to_user_story_v1"]
    assert result["system_prompt"] == "Instruções"
    assert result["user_prompt"] == "{bug_report}"

def test_pull_rejects_unsupported_messages_without_overwriting(monkeypatch, tmp_path):
    client = Mock()
    client.pull_prompt.return_value = ChatPromptTemplate.from_messages([("human", "Só user")])
    monkeypatch.setattr(pull_prompts, "Client", lambda: client)
    monkeypatch.setattr(pull_prompts, "ROOT", tmp_path)
    with pytest.raises(ValueError):
        pull_prompts.pull_prompts_from_langsmith()
    assert not (tmp_path / "prompts/bug_to_user_story_v1.yml").exists()

def test_push_is_public_versioned_and_has_metadata(monkeypatch, prompt):
    client = Mock()
    client.push_prompt.return_value = "https://example.invalid/prompt"
    monkeypatch.setattr(push_prompts, "Client", lambda: client)
    monkeypatch.setenv("USERNAME_LANGSMITH_HUB", "test-handle")
    assert push_prompts.push_prompt_to_langsmith(push_prompts.NAME, prompt)
    args, kwargs = client.push_prompt.call_args
    assert args == ("test-handle/bug_to_user_story_v2",)
    assert kwargs["is_public"] is True
    assert set(prompt["techniques_applied"]) <= set(kwargs["tags"])
    assert kwargs["object"].metadata["version"] == "v2"
    assert kwargs["object"].input_variables == ["bug_report"]
    assert "few-shot" in kwargs["description"]

def test_invalid_push_does_not_contact_hub(monkeypatch, prompt):
    client = Mock()
    monkeypatch.setattr(push_prompts, "Client", lambda: client)
    prompt["user_prompt"] = "{wrong}"
    assert not push_prompts.push_prompt_to_langsmith(push_prompts.NAME, prompt)
    client.push_prompt.assert_not_called()

def test_network_failure_does_not_leak_service_response(monkeypatch, prompt, capsys):
    client = Mock()
    client.push_prompt.side_effect = RuntimeError("SENSITIVE_RESPONSE")
    monkeypatch.setattr(push_prompts, "Client", lambda: client)
    monkeypatch.setenv("USERNAME_LANGSMITH_HUB", "test-handle")
    assert not push_prompts.push_prompt_to_langsmith(push_prompts.NAME, prompt)
    assert "SENSITIVE_RESPONSE" not in capsys.readouterr().out

def test_cli_missing_credentials_fails_without_client(monkeypatch):
    monkeypatch.setattr(push_prompts, "check_env_vars", lambda _: False)
    monkeypatch.setattr(pull_prompts, "check_env_vars", lambda _: False)
    def unexpected():
        raise AssertionError("Não deveria conectar")
    monkeypatch.setattr(push_prompts, "Client", unexpected)
    monkeypatch.setattr(pull_prompts, "Client", unexpected)
    assert push_prompts.main() == 1
    assert pull_prompts.main() == 1
