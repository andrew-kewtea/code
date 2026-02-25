from ..prompt_engine import PromptTemplate


def test_prompt_binding():

    template = PromptTemplate("Hello ${name}")
    result = template.bind({"name": "Andrew"})

    assert result == "Hello Andrew"