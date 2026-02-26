subtree는 "브랜치 자동 전환" 개념이 없습니다.
git subtree add --prefix=fastapi/app repo1(등록한리모트이름) dev(가져올 브랜치) --squash
git subtree pull --prefix=fastapi/app repo1 release --squash


submodule : 포인터 저장으로 저장소 크기 최소화, 정확한 commit reference, 완전한 독립성
subtree : 실제 코드를 전체 복사, 단순한 clone, 무거운 크기 증가, merge 충돌 복잡


repo1에서 image build
Dockerfile 추가  image registry에 저장 (.dockerignore)
GitHub Container Registry (GHCR)

--------------------
uv init
uv venv --python 3.11
uv add
uv sync

uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
uv run python -m uvicorn src.main:app --reload

pyproject.toml
[project]
name = "tracker"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "sqlalchemy>=2.0.46",
]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
include = ["*"]

Dockerfile

FROM python:3.13-slim

# uv 설치
RUN pip install uv

WORKDIR /app

# pyproject & lock 먼저 복사 (레이어 캐싱 최적화)
COPY pyproject.toml uv.lock ./

# 의존성 설치 (.venv 생성)
RUN uv sync --frozen

# 소스 복사
COPY src ./src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

docker build -t tracker-app .
docker run -p 8000:8000 tracker-app




---------------------------

(1)alembic 환경 설정 (uv run alembic init alembic)
- alembic.ini
- alembic/ 폴더 생성
- alembic/env.py  : target_metadata = Base.metadata

(2)델타 기록
uv run alembic revision --autogenerate -m "init"
uv run alembic upgrade head
