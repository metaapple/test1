# Git Merge 충돌 해결 가이드

## 문제 상황

```
$ git merge origin/main
Updating f291627..b048e06
error: Your local changes to the following files would be overwritten by merge:
        README.md
Please commit your changes or stash them before you merge.
```

## 문제 원인

- 로컬에 **커밋되지 않은 변경사항**이 있음
- 원격 저장소의 같은 파일이 수정됨
- Git이 자동으로 병합할 수 없어서 오류 발생

---

## 해결 방법 비교표

| 방법 | 장점 | 단점 | 언제 사용? |
|------|------|------|-----------|
| **커밋 후 Merge** | 히스토리 보존, 안전 | 작은 변경도 커밋 필요 | 변경사항이 의미있는 경우 |
| **Stash 사용** | 히스토리 깔끔, 임시 보관 | Stash 잊을 수 있음 | 임시 변경사항인 경우 |
| **변경사항 버리기** | 빠름 | 데이터 손실 위험 | 변경사항이 불필요한 경우 |
| **백업 후 병합** | 안전, 수동 제어 | 시간 소요 | 복잡한 변경사항인 경우 |

---

## 상세 해결 방법

### ✅ 방법 1: 커밋 후 Merge (가장 권장)

**언제 사용:**
- 변경사항이 의미있고 보존하고 싶을 때
- 나중에 추적이 필요할 때

**단계별 실행:**

```bash
# 1. 현재 상태 확인
git status

# 2. 변경사항 스테이징
git add README.md

# 3. 커밋
git commit -m "README.md 로컬 수정사항"

# 4. 원격 저장소 최신 정보 가져오기
git fetch origin

# 5. Merge 실행
git merge origin/main

# 6. 충돌 발생 시 (같은 부분을 수정한 경우)
#    - 충돌 마커 확인: <<<<<<< HEAD, =======, >>>>>>> origin/main
#    - 수동으로 병합
#    - git add README.md
#    - git commit -m "Merge origin/main and resolve conflicts"
```

**예상 결과:**
- 로컬 변경사항과 원격 변경사항이 모두 보존됨
- 충돌이 없으면 자동으로 merge commit 생성
- 충돌이 있으면 수동 해결 후 커밋

---

### ✅ 방법 2: Stash 사용 (임시 변경사항)

**언제 사용:**
- 변경사항이 아직 완성되지 않았을 때
- 커밋하기 전에 테스트하고 싶을 때

**단계별 실행:**

```bash
# 1. 현재 변경사항을 stash에 저장
git stash save "README.md 작업 중"

# 2. Stash 목록 확인
git stash list

# 3. 원격 저장소 최신 정보 가져오기
git fetch origin

# 4. Merge 실행
git merge origin/main

# 5. Stash한 변경사항 다시 적용
git stash pop

# 6. 충돌 발생 시
#    - 충돌 해결
#    - git add README.md
#    - git commit -m "Apply stashed changes after merge"
```

**Stash 관련 명령어:**
```bash
git stash list          # Stash 목록 보기
git stash show          # 최근 stash 내용 보기
git stash pop           # 적용하고 삭제
git stash apply         # 적용만 하고 삭제 안 함
git stash drop          # 삭제
git stash clear         # 모든 stash 삭제
```

---

### ⚠️ 방법 3: 변경사항 버리기 (주의!)

**언제 사용:**
- 변경사항이 실수로 만든 것이거나 불필요할 때
- 원격 버전만 필요할 때

**단계별 실행:**

```bash
# 1. 변경사항 버리기 (주의: 복구 불가능!)
git checkout -- README.md

# 또는 모든 변경사항 버리기
git checkout -- .

# 2. 원격 저장소 최신 정보 가져오기
git fetch origin

# 3. Merge 실행
git merge origin/main
```

**복구 방법 (만약 실수로 버렸다면):**
```bash
# Git reflog로 복구 시도
git reflog
git checkout <commit-hash> -- README.md
```

---

### ✅ 방법 4: 백업 후 수동 병합

**언제 사용:**
- 변경사항이 복잡하고 신중하게 병합하고 싶을 때
- 두 변경사항을 모두 보존해야 할 때

**단계별 실행:**

```bash
# 1. 변경사항 백업
cp README.md README.md.backup

# 2. 로컬 변경사항 되돌리기
git checkout -- README.md

# 3. 원격 저장소 최신 정보 가져오기
git fetch origin

# 4. Merge 실행
git merge origin/main

# 5. 백업 파일과 현재 파일 비교
#    (에디터나 diff 도구 사용)
diff README.md.backup README.md

# 6. 수동으로 필요한 부분 병합
#    - 에디터로 두 파일 열기
#    - 필요한 부분 복사하여 병합
#    - git add README.md
#    - git commit -m "Merge local and remote changes manually"
```

---

## 충돌 해결 방법

Merge 후 충돌이 발생하면 파일에 다음과 같은 마커가 나타납니다:

```
<<<<<<< HEAD
로컬 변경사항
=======
원격 변경사항
>>>>>>> origin/main
```

**해결 방법:**
1. 충돌 마커를 찾습니다 (`<<<<<<<`, `=======`, `>>>>>>>`)
2. 필요한 부분을 선택하거나 둘 다 병합합니다
3. 충돌 마커를 삭제합니다
4. `git add`로 스테이징합니다
5. `git commit`으로 커밋합니다

**예시:**
```markdown
# 원본 (충돌 상태)
<<<<<<< HEAD
이것은 내 변경사항입니다.
=======
이것은 다른 개발자의 변경사항입니다.
>>>>>>> origin/main

# 해결 후 (둘 다 보존)
이것은 내 변경사항입니다.
이것은 다른 개발자의 변경사항입니다.
```

---

## 실전 연습 문제

### 문제 1: 기본 Merge 충돌

**상황:**
- README.md에 "로컬 작업 중" 추가
- 원격에는 "원격 작업 완료" 추가
- 두 변경사항 모두 보존하고 싶음

**답:**
```bash
git add README.md
git commit -m "로컬 작업 추가"
git fetch origin
git merge origin/main
# 충돌 발생 시 수동 병합
git add README.md
git commit -m "로컬과 원격 변경사항 병합"
```

---

### 문제 2: 임시 작업 중 Merge 필요

**상황:**
- README.md 작업 중인데 아직 완성 안 됨
- 원격 변경사항을 먼저 가져와야 함
- 나중에 작업 계속하고 싶음

**답:**
```bash
git stash save "작업 중인 README.md"
git fetch origin
git merge origin/main
git stash pop
# 충돌 발생 시 해결
```

---

### 문제 3: 실수로 만든 변경사항

**상황:**
- README.md를 실수로 수정함
- 원격 버전만 필요함
- 로컬 변경사항은 버려도 됨

**답:**
```bash
git checkout -- README.md
git fetch origin
git merge origin/main
```

---

## 체크리스트

Merge 전에 확인할 사항:

- [ ] 현재 변경사항이 무엇인지 확인 (`git status`)
- [ ] 변경사항을 보존할지 결정
- [ ] 원격 저장소 최신 정보 가져오기 (`git fetch`)
- [ ] 적절한 해결 방법 선택
- [ ] Merge 후 충돌 확인 및 해결
- [ ] 테스트 실행하여 정상 동작 확인

---

## 주의사항

1. **변경사항 버리기 전에 항상 확인**
   - `git checkout --` 명령은 되돌릴 수 없습니다
   - 중요한 변경사항은 백업하세요

2. **Stash는 임시 저장소**
   - Stash 목록을 정기적으로 확인하세요
   - 오래된 stash는 삭제하세요

3. **충돌 해결 후 테스트 필수**
   - Merge 후 코드가 정상 동작하는지 확인하세요
   - 특히 같은 부분을 수정한 경우 주의하세요

4. **커밋 메시지 작성**
   - 의미있는 커밋 메시지를 작성하세요
   - 나중에 히스토리를 추적할 때 도움이 됩니다
