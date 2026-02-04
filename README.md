# code
coding test

각종 LLM 개발을 실험해보고 기록해 보는 코드 repo
여기서 테스트가 된것을 main projects로 이식한다

## 2602 할일
### speckit, taskmaster, openspec + claude code, opencode
=======
git fetch
git branch -r
git checkout -b 2602 origin/2602
git branch -vv

(신규 브랜치를 로컬에서 먼저 만든 경우)
git checkout -b 2603
....git add .   git commit -m "작업 내용"....
git push -u origin 2603
git branch -vv

(커밋하기전일떄 수정된것들을 돌릴려면)
git restore .  ==  git reset --hard

(최근 3개의 커밋-push되 된것을 돌릴때)
git reset --hard HEAD~3
git push -f  (force)

(remote의 history는 보존해야한다면)
git revert HEAD~1  (해당 commit만 변동없는 새 커밋으로 바꾸어줌)

(merge, rebase)
(1)git checkout dev .... git merge (--no-ff or --ff or --squash) feature...충돌난  파일수정: git add <conflicted-file>, git commit
  다 끝나면 그 브랜치 삭제도 가능 git branch -d feature  (-D), git push origin --delete feature
(2)git checkout feature.....git fetch ..git rebase origin/dev....충돌만 파일들 수정  git add .  git rebase --continue 
성공한후엔 git push -f  or git push --force origin <branch>
만약 포기하고 원래 상태로 되돌리려면: git rebase --abort  


---------------------

github cli 설치와 사용
brew install gh  (sudo apt install gh)
gh --version
gh auth login
gh auth status


gh issue create --title "버그: 로그인 오류" --body "로그인 시 토큰 갱신 문제 발생"
gh issue create --title "기능 요청" --body "기능 설명" --assignee @me --label enhancement
gh issue list
gh issue view 123 --comments
gh issue close 123

현재 브랜치 기준 PR 생성
gh pr create --title "새 기능 구현" --body "작업 설명"
(base/HEAD 지정 PR 생성) gh pr create --base main --head feature-branch --title "..." --body "..."
(Draft PR 생성) gh pr create --draft --title "작업 중인 기능"
gh pr list
PR 체크아웃 (로컬로 가져오기) gh pr checkout 456
PR 병합 gh pr merge 456  -default merge 전략으로 병합

.github/workflows/ci/build.yml

gh workflow list
gh run list 최근 build/CI 실행 내역 열람
gh run list --workflow test.yml
gh run cancel(or rerun) 123456789
gh workflow run "Deploy"
gh list --workflow <..yml>
gh run view <run.id>



gh release create v1.0.0 -n "note내용" --target <branch/commit>  (v1.0.0이라는 릴리즈 Tag를 자동 생성)
gh release list  ...view
(사용하기) https://github.com/<owner>/<repo>/releases/tag/v1.2.0
git clone https://github.com/<owner>/<repo>.git
cd <repo>
git checkout v1.2.0

git tag v1.2.0 현재 HEAD 커밋에 v1.2.0이라는 태그를 붙여
git tag v1.2.0 a1b2c3d4  커밋 해시로 지정
git tag
git tag -l "featureA*"
git push origin v1.2.0
git push origin --tags


로컬 머신에 github self-hosted runner 설치하기 
actions-runner/_work/<repo-name>/<repo-name>: 기본적으로 매번 git checkout을 수행
./config.sh --url https://github.com/<OWNER>/<REPO> --token <TOKEN>  --name my-runner --labels mylabel
run: | cp -r $GITHUB_WORKSPACE /home/runner/webProjects/myrepo
cp /home/runner/secrets/.env $GITHUB_WORKSPACE/.env
ls -la $GITHUB_WORKSPACE/.env
GitHub Secrets에 .env 설정값들을 저장하고 workflow에서 환경변수로 주입:env:DATABASE_URL: ${{ secrets.DATABASE_URL }}

gh workflow run test.yml --ref dev -f suite=regression -f otherParam=foobar  #branch명 dev, parameter -f
  (param은 yml에서 이렇게 사용됨: (1)선언: on: workflow_dispatch: inputs: suite:  
    (2)사용 echo "Suite is: ${{ github.event.inputs.suite }}")

github action yml

- uses: actions/checkout@v4, - uses: actions/cache@v3

