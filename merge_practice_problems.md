# Git Merge 충돌 해결 연습 문제

## 문제 상황 재현

터미널에서 본 오류:
```
$ git merge origin/main
Updating f291627..b048e06
error: Your local changes to the following files would be overwritten by merge:
        README.md
Please commit your changes or stash them before you merge.
```

---

## 연습 문제

### 문제 1: 기본 상황 이해

**Q1-1.** 위 오류가 발생한 이유는 무엇인가요?

**답:**
```
로컬에 커밋되지 않은 변경사항(README.md)이 있고, 
원격 저장소의 main 브랜치에서도 같은 파일이 수정되어 
Git이 자동으로 병합할 수 없기 때문입니다.
```

**Q1-2.** 이 오류를 해결하기 위한 3가지 방법을 말씀해주세요.

**답:**
```
1. 로컬 변경사항을 커밋한 후 merge
2. 로컬 변경사항을 stash에 저장한 후 merge하고 다시 적용
3. 로컬 변경사항을 버리고 원격 변경사항만 사용
```

---

### 문제 2: 커밋 후 Merge

**Q2-1.** 로컬 변경사항을 보존하면서 원격 변경사항을 가져오려면 어떤 순서로 명령어를 실행해야 하나요?

**답:**
```bash
# 1. 변경사항 스테이징
git add README.md

# 2. 커밋
git commit -m "로컬 README.md 수정사항"

# 3. 원격 저장소 최신 정보 가져오기
git fetch origin

# 4. Merge 실행
git merge origin/main
```

**Q2-2.** Merge 후 충돌이 발생했다면 어떻게 해결하나요?

**답:**
```bash
# 1. 충돌 파일 열기 (README.md)
# 2. 충돌 마커 확인:
#    <<<<<<< HEAD
#    로컬 변경사항
#    =======
#    원격 변경사항
#    >>>>>>> origin/main
# 3. 필요한 부분 선택하거나 병합
# 4. 충돌 마커 삭제
# 5. 스테이징 및 커밋
git add README.md
git commit -m "Merge origin/main and resolve conflicts"
```

---

### 문제 3: Stash 사용

**Q3-1.** 아직 완성되지 않은 작업을 임시 저장하고 merge하려면?

**답:**
```bash
# 1. 변경사항을 stash에 저장
git stash save "작업 중인 README.md"

# 2. 원격 저장소 최신 정보 가져오기
git fetch origin

# 3. Merge 실행
git merge origin/main

# 4. Stash한 변경사항 다시 적용
git stash pop
```

**Q3-2.** Stash 목록을 확인하고, 특정 stash를 삭제하는 방법은?

**답:**
```bash
# Stash 목록 확인
git stash list

# 출력 예시:
# stash@{0}: WIP on main: abc1234 작업 중인 README.md
# stash@{1}: WIP on main: def5678 이전 작업

# 특정 stash 삭제
git stash drop stash@{1}

# 모든 stash 삭제
git stash clear
```

---

### 문제 4: 변경사항 버리기

**Q4-1.** 로컬 변경사항이 불필요해서 원격 버전만 사용하고 싶다면?

**답:**
```bash
# 1. 특정 파일의 변경사항 버리기
git checkout -- README.md

# 2. 모든 변경사항 버리기
git checkout -- .

# 3. 원격 저장소 최신 정보 가져오기
git fetch origin

# 4. Merge 실행
git merge origin/main
```

**Q4-2.** 실수로 변경사항을 버렸을 때 복구하는 방법은?

**답:**
```bash
# 1. Git reflog로 이전 상태 확인
git reflog

# 2. 복구하고 싶은 커밋 해시 찾기
# 3. 해당 파일 복구
git checkout <commit-hash> -- README.md

# 예시:
git checkout abc1234 -- README.md
```

---

### 문제 5: 실제 시나리오

**Q5-1.** 다음 상황에서 어떻게 해결할까요?

**상황:**
- README.md에 "로컬에서 작업 중" 추가
- 원격에는 "원격에서 작업 완료" 추가
- 두 변경사항 모두 보존하고 싶음

**답:**
```bash
# 방법 1: 커밋 후 Merge (권장)
git add README.md
git commit -m "로컬 작업 추가"
git fetch origin
git merge origin/main

# 충돌 발생 시:
# README.md 파일을 열어서:
# <<<<<<< HEAD
# 로컬에서 작업 중
# =======
# 원격에서 작업 완료
# >>>>>>> origin/main
# 
# 다음과 같이 수정:
# 로컬에서 작업 중
# 원격에서 작업 완료

git add README.md
git commit -m "로컬과 원격 변경사항 병합"
```

**Q5-2.** 다음 상황에서 어떻게 해결할까요?

**상황:**
- README.md 작업 중인데 아직 완성 안 됨
- 원격 변경사항을 먼저 가져와야 함
- 나중에 작업 계속하고 싶음

**답:**
```bash
# Stash 사용
git stash save "README.md 작업 중"
git fetch origin
git merge origin/main
git stash pop

# 충돌 발생 시 해결 후
git add README.md
git commit -m "Stash 적용 및 충돌 해결"
```

---

### 문제 6: 고급 상황

**Q6-1.** 여러 파일에 변경사항이 있고, 일부만 보존하고 싶다면?

**답:**
```bash
# 1. 보존할 파일만 커밋
git add README.md
git commit -m "README.md 변경사항"

# 2. 나머지 파일은 stash
git stash save "기타 변경사항"

# 3. Merge 실행
git fetch origin
git merge origin/main

# 4. 필요하면 stash 적용
git stash pop
```

**Q6-2.** Merge 전에 원격 변경사항을 미리 확인하고 싶다면?

**답:**
```bash
# 1. 원격 저장소 정보 가져오기 (merge 없이)
git fetch origin

# 2. 원격 브랜치와 로컬 브랜치 비교
git diff main origin/main

# 3. 특정 파일만 비교
git diff main origin/main -- README.md

# 4. 원격 브랜치의 파일 내용 확인
git show origin/main:README.md

# 5. 확인 후 merge 결정
git merge origin/main
```

---

### 문제 7: 실전 문제

**Q7-1.** 다음 명령어 순서가 올바른지 확인하고, 틀렸다면 수정하세요.

```bash
git merge origin/main
git add README.md
git commit -m "변경사항"
```

**답:**
```
틀렸습니다. 올바른 순서:

1. git add README.md        # 먼저 변경사항 스테이징
2. git commit -m "변경사항"  # 커밋
3. git fetch origin         # 원격 정보 가져오기
4. git merge origin/main    # 그 다음 merge
```

**Q7-2.** Merge 후 충돌을 해결했는데, 어떻게 확인하나요?

**답:**
```bash
# 1. 충돌 파일이 모두 해결되었는지 확인
git status

# 2. 충돌이 해결되지 않은 파일이 있으면:
#    "both modified: README.md" 같은 메시지가 나타남

# 3. 모든 충돌 해결 후:
git add .
git commit -m "충돌 해결 완료"

# 4. Merge 완료 확인
git log --oneline --graph -5
```

---

## 종합 문제

### 종합 문제 1: 완전한 워크플로우

**상황:**
1. 로컬에서 README.md 수정 중
2. 다른 개발자가 원격에 push함
3. 두 변경사항 모두 보존하고 싶음
4. 충돌 발생 예상

**전체 해결 과정을 단계별로 작성하세요.**

**답:**
```bash
# 1단계: 현재 상태 확인
git status
git log --oneline -3

# 2단계: 로컬 변경사항 커밋
git add README.md
git commit -m "로컬 README.md 수정사항"

# 3단계: 원격 저장소 최신 정보 가져오기
git fetch origin

# 4단계: 원격 변경사항 미리 확인 (선택사항)
git diff main origin/main -- README.md

# 5단계: Merge 실행
git merge origin/main

# 6단계: 충돌 발생 시 해결
# - README.md 파일 열기
# - 충돌 마커 확인 및 해결
# - 필요한 부분 모두 보존

# 7단계: 충돌 해결 후 커밋
git add README.md
git commit -m "Merge origin/main and resolve conflicts in README.md"

# 8단계: 결과 확인
git log --oneline --graph -5
git status
```

---

### 종합 문제 2: 여러 해결 방법 비교

**상황:** README.md에 "로컬 작업" 추가했는데, 원격에 "원격 작업" 추가됨

**각 해결 방법의 결과를 비교하세요:**

**답:**

| 방법 | README.md 최종 내용 | 커밋 히스토리 |
|------|-------------------|--------------|
| **커밋 후 Merge** | "로컬 작업" + "원격 작업" (충돌 해결 필요) | 2개 커밋 + 1개 merge 커밋 |
| **Stash 사용** | "로컬 작업" + "원격 작업" (충돌 해결 필요) | 1개 merge 커밋 + 1개 적용 커밋 |
| **변경사항 버리기** | "원격 작업"만 | 1개 merge 커밋 (로컬 작업 손실) |

**권장:** 커밋 후 Merge (히스토리 추적 용이)

---

## 자가 진단 체크리스트

다음 질문에 답할 수 있나요?

- [ ] Git merge 충돌 오류의 원인을 설명할 수 있나요?
- [ ] 커밋 후 merge 방법을 실행할 수 있나요?
- [ ] Stash를 사용하여 임시 저장할 수 있나요?
- [ ] 충돌 마커를 해석하고 해결할 수 있나요?
- [ ] Merge 전에 원격 변경사항을 미리 확인할 수 있나요?
- [ ] 실수로 버린 변경사항을 복구할 수 있나요?
- [ ] 여러 해결 방법의 장단점을 비교할 수 있나요?

---

## 추가 학습 자료

- `merge_solution_guide.md` - 상세한 해결 가이드
- `git_merge_test_scenario.md` - 테스트 시나리오
- `test_merge_scenario.bat` (Windows) 또는 `test_merge_scenario.sh` (Linux/Mac) - 실행 스크립트
