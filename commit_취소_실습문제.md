# Git Commit 취소 실습 문제

## 🎯 목표
다양한 상황에서 commit을 취소하는 방법을 실습합니다.

---

## 📝 문제 1: 기본 이해

### 문제 1-1
**질문:** `git reset --soft HEAD~1`과 `git reset HEAD~1`의 차이는 무엇인가요?

**답:**
```
git reset --soft HEAD~1:
- 커밋만 취소됨
- 변경사항은 staged 상태로 유지됨 (git add 된 상태)
- 바로 다시 커밋 가능

git reset HEAD~1 (또는 --mixed):
- 커밋 취소됨
- 변경사항은 unstaged 상태로 유지됨 (git add 안 된 상태)
- 파일은 수정된 상태로 남아있음
- git add 후 다시 커밋 필요
```

### 문제 1-2
**질문:** `git reset`과 `git revert`의 차이를 설명하세요.

**답:**
```
git reset:
- 커밋을 히스토리에서 삭제함
- 로컬에서만 사용 (아직 push 안 한 경우)
- 히스토리가 변경됨

git revert:
- 새로운 커밋을 생성하여 이전 커밋을 되돌림
- 이미 push한 커밋에 사용
- 히스토리는 유지됨 (안전함)
```

---

## 📝 문제 2: 커밋 메시지 수정

### 문제 2-1
**상황:** 방금 "test"라는 메시지로 커밋했는데, "테스트 시나리오 추가"로 수정하고 싶습니다.

**해결 방법을 작성하세요.**

**답:**
```bash
# 방법 1: amend 사용 (가장 간단)
git commit --amend -m "테스트 시나리오 추가"

# 방법 2: reset --soft 사용
git reset --soft HEAD~1
git commit -m "테스트 시나리오 추가"
```

### 문제 2-2
**상황:** 커밋 메시지를 수정하면서 마지막 커밋에 파일도 추가하고 싶습니다.

**해결 방법을 작성하세요.**

**답:**
```bash
# 1. 추가할 파일 스테이징
git add new-file.txt

# 2. 이전 커밋에 포함시키기
git commit --amend -m "수정된 메시지와 새 파일 추가"

# 또는 메시지는 그대로 두고 파일만 추가
git commit --amend --no-edit
```

---

## 📝 문제 3: 커밋 취소 (변경사항 유지)

### 문제 3-1
**상황:** 방금 커밋했는데, 변경사항을 다시 검토한 후 일부만 커밋하고 싶습니다.

**해결 과정을 단계별로 작성하세요.**

**답:**
```bash
# 1. 커밋 취소 (변경사항 unstaged 상태로)
git reset HEAD~1

# 2. 변경사항 확인
git status

# 3. 원하는 파일만 스테이징
git add README.md
# 다른 파일은 add 안 함

# 4. 다시 커밋
git commit -m "README.md만 커밋"
```

### 문제 3-2
**상황:** 커밋을 취소했지만 변경사항은 그대로 두고, 나중에 다시 커밋하고 싶습니다.

**답:**
```bash
# 방법 1: reset (기본) - unstaged 상태
git reset HEAD~1
# 변경사항이 unstaged 상태로 남아있음

# 방법 2: reset --soft - staged 상태
git reset --soft HEAD~1
# 변경사항이 staged 상태로 남아있음 (바로 커밋 가능)
```

---

## 📝 문제 4: 커밋 완전히 삭제

### 문제 4-1
**상황:** 실수로 커밋한 것을 완전히 지우고 싶습니다. 변경사항도 필요 없습니다.

**⚠️ 주의사항과 함께 해결 방법을 작성하세요.**

**답:**
```bash
# ⚠️ 주의: 복구 불가능할 수 있으므로 백업 권장!

# 방법 1: 백업 후 삭제 (안전)
git branch backup-branch  # 백업 브랜치 생성
git reset --hard HEAD~1   # 커밋과 변경사항 삭제

# 방법 2: 바로 삭제 (위험)
git reset --hard HEAD~1

# 복구 방법 (실수로 삭제했을 때)
git reflog
git reset --hard <commit-hash>  # 이전 커밋 해시로 복구
```

---

## 📝 문제 5: 이미 Push한 커밋 취소

### 문제 5-1
**상황:** 이미 `git push`로 원격 저장소에 올린 커밋을 취소하고 싶습니다.

**안전한 해결 방법을 작성하세요.**

**답:**
```bash
# ✅ 안전한 방법: revert 사용
git revert HEAD

# 커밋 메시지 편집기 열림
# "Revert '커밋 메시지'" 자동 생성

# 원격에 push
git push origin main

# 결과: 새로운 커밋이 생성되어 이전 커밋을 되돌림
# 히스토리는 유지됨 (안전함)
```

### 문제 5-2
**질문:** 이미 push한 커밋에 `git reset --hard`를 사용하면 어떻게 되나요?

**답:**
```
❌ 문제 발생:
1. 로컬에서 커밋이 삭제됨
2. git push --force 필요
3. 다른 개발자들의 로컬 저장소와 충돌 발생
4. 팀 작업에 문제 생김

✅ 올바른 방법:
git revert HEAD  # 새로운 커밋으로 되돌림
git push origin main  # 안전하게 push
```

---

## 📝 문제 6: 여러 커밋 취소

### 문제 6-1
**상황:** 최근 3개 커밋을 취소하고 싶습니다. 변경사항은 유지하고 싶습니다.

**답:**
```bash
# 방법 1: 변경사항 staged 상태로 유지
git reset --soft HEAD~3

# 방법 2: 변경사항 unstaged 상태로 유지
git reset HEAD~3

# 방법 3: 변경사항 완전히 삭제 (주의!)
git reset --hard HEAD~3
```

### 문제 6-2
**상황:** 특정 커밋 해시 `abc1234`로 되돌리고 싶습니다.

**답:**
```bash
# 1. 커밋 해시 확인
git log --oneline

# 2. 특정 커밋으로 되돌리기
git reset --soft abc1234  # 변경사항 유지 (staged)
# 또는
git reset abc1234         # 변경사항 유지 (unstaged)
# 또는
git reset --hard abc1234  # 변경사항 삭제
```

---

## 📝 문제 7: 실전 시나리오

### 문제 7-1
**상황:**
1. README.md 수정 후 커밋
2. 커밋 메시지가 "test"로 실수로 잘못 입력됨
3. 변경사항은 그대로 두고 메시지만 "README.md 업데이트"로 수정하고 싶음

**전체 해결 과정을 작성하세요.**

**답:**
```bash
# 방법 1: amend 사용 (가장 간단)
git commit --amend -m "README.md 업데이트"

# 방법 2: reset --soft 사용
git reset --soft HEAD~1
git commit -m "README.md 업데이트"

# 결과 확인
git log --oneline -1
# "README.md 업데이트"로 변경됨
```

### 문제 7-2
**상황:**
1. 파일 A, B, C를 수정하고 한 번에 커밋
2. 나중에 파일 B는 커밋에서 제외하고 싶음
3. 파일 A, C만 커밋하고 싶음

**해결 과정을 작성하세요.**

**답:**
```bash
# 1. 커밋 취소 (변경사항 유지)
git reset HEAD~1

# 2. 상태 확인
git status
# 파일 A, B, C가 모두 modified로 표시됨

# 3. 파일 A, C만 스테이징
git add fileA.txt fileC.txt
# 파일 B는 add 안 함

# 4. 다시 커밋
git commit -m "파일 A, C 수정"

# 5. 파일 B는 여전히 수정된 상태로 남아있음
git status
# fileB.txt가 modified로 표시됨
```

---

## 📝 문제 8: 복구 문제

### 문제 8-1
**상황:** 실수로 `git reset --hard HEAD~1`을 실행했습니다. 복구 방법은?

**답:**
```bash
# 1. Git reflog로 이전 상태 찾기
git reflog

# 출력 예시:
# abc1234 HEAD@{0}: reset: moving to HEAD~1
# def5678 HEAD@{1}: commit: 삭제된 커밋  <- 이전 커밋

# 2. 이전 커밋으로 복구
git reset --hard def5678

# 또는 reflog 인덱스 사용
git reset --hard HEAD@{1}

# 3. 확인
git log --oneline -3
# 삭제된 커밋이 다시 나타남
```

### 문제 8-2
**질문:** 커밋을 완전히 잃어버렸을 때 찾는 방법은?

**답:**
```bash
# 1. 모든 참조 확인
git fsck --lost-found

# 2. dangling commit 찾기
git log --all --full-history -- README.md

# 3. 복구할 커밋 해시 찾기
git reflog --all

# 4. 복구
git checkout <commit-hash>
git branch recovery-branch
```

---

## 📝 종합 문제

### 종합 문제 1: 완전한 워크플로우

**상황:**
1. README.md와 config.py 수정
2. "업데이트"라는 메시지로 커밋
3. 원격에 push 완료
4. 나중에 README.md 변경사항만 취소하고 싶음
5. config.py 변경사항은 유지하고 싶음

**전체 해결 과정을 작성하세요.**

**답:**
```bash
# 방법 1: Revert 사용 (이미 push 했으므로)
# 1. README.md만 되돌리는 새 커밋 생성
git checkout HEAD~1 -- README.md  # 이전 버전으로 되돌림
git add README.md
git commit -m "Revert README.md changes"
git push origin main

# 방법 2: Reset 후 선택적 커밋 (로컬에서만)
# ⚠️ 이미 push 했으므로 주의 필요
git reset HEAD~1  # 커밋 취소, 변경사항 유지
git checkout -- README.md  # README.md만 이전 상태로
git add config.py  # config.py만 스테이징
git commit -m "config.py만 업데이트"
git push --force origin main  # ⚠️ 팀 작업 시 주의!
```

---

### 종합 문제 2: 여러 상황 비교

**다음 상황에서 어떤 방법을 사용할까요?**

| 상황 | 추천 방법 | 명령어 |
|------|----------|--------|
| 커밋 메시지만 수정 | `commit --amend` | `git commit --amend -m "새 메시지"` |
| 커밋 취소, 변경사항 staged로 유지 | `reset --soft` | `git reset --soft HEAD~1` |
| 커밋 취소, 변경사항 unstaged로 유지 | `reset` | `git reset HEAD~1` |
| 커밋과 변경사항 완전 삭제 | `reset --hard` | `git reset --hard HEAD~1` |
| 이미 push한 커밋 취소 | `revert` | `git revert HEAD` |
| 마지막 커밋에 파일 추가 | `commit --amend` | `git add file; git commit --amend` |

---

## ✅ 자가 진단 체크리스트

다음 질문에 답할 수 있나요?

- [ ] `reset --soft`, `reset`, `reset --hard`의 차이를 설명할 수 있나요?
- [ ] `reset`과 `revert`의 차이를 설명할 수 있나요?
- [ ] 커밋 메시지를 수정할 수 있나요?
- [ ] 커밋을 취소하고 변경사항을 유지할 수 있나요?
- [ ] 이미 push한 커밋을 안전하게 취소할 수 있나요?
- [ ] 실수로 삭제한 커밋을 복구할 수 있나요?
- [ ] 여러 커밋을 취소할 수 있나요?
- [ ] 특정 파일만 커밋에서 제외할 수 있나요?

---

## 🎯 빠른 참조

```bash
# 커밋 메시지 수정
git commit --amend -m "새 메시지"

# 커밋 취소 (변경사항 staged)
git reset --soft HEAD~1

# 커밋 취소 (변경사항 unstaged)
git reset HEAD~1

# 커밋 취소 (변경사항 삭제)
git reset --hard HEAD~1

# 이미 push한 커밋 취소
git revert HEAD

# N개 커밋 취소
git reset --soft HEAD~N

# 복구
git reflog
git reset --hard <commit-hash>
```
