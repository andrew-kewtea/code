

pytest
pytest -m integration
pytest -m provider
pytest -m "provider and integration"
pytest tests/unit
pytest tests/test_openai_provider.py::test_openai_provider
pytest -k openai #파일명, 함수명에 openai 포함된 것만 실행