subtree는 "브랜치 자동 전환" 개념이 없습니다.
git subtree add --prefix=fastapi/app repo1(등록한리모트이름) dev(가져올 브랜치) --squash
git subtree pull --prefix=fastapi/app repo1 release --squash


submodule : 포인터 저장으로 저장소 크기 최소화, 정확한 commit reference, 완전한 독립성
subtree : 실제 코드를 전체 복사, 단순한 clone, 무거운 크기 증가, merge 충돌 복잡


repo1에서 image build
Dockerfile 추가  image registry에 저장 (.dockerignore)
GitHub Container Registry (GHCR)