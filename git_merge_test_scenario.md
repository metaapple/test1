# Git Merge 충돌 테스트 시나리오

## 문제 상황

다른 개발자들이 master(main) 브랜치에 코드를 merge한 후, 당신의 로컬에 커밋되지 않은 변경사항이 있을 때 merge를 시도하면 다음과 같은 오류가 발생합니다:

```
$ git merge origin/main
Updating f291627..b048e06
error: Your local changes to the following files would be overwritten by merge:
        README.md
Please commit your changes or stash them before you merge.
```

## 테스트 시나리오

### 시나리오 설정

1. **로컬에 커밋되지 않은 변경사항이 있는 상태**
2. **원격 저장소의 main 브랜치에 다른 개발자들이 새로운 커밋을 push한 상태**
3. **로컬 변경사항과 원격 변경사항이 같은 파일(README.md)을 수정한 상태**

---

## 문제: 어떻게 해결할까요?

다른 개발자들의 수정사항을 유지하면서 현재 프로젝트에 적용하려면 어떻게 해야 할까요?

### 선택지

**A.** 로컬 변경사항을 커밋한 후 merge
**B.** 로컬 변경사항을 stash한 후 merge하고 다시 적용
**C.** 로컬 변경사항을 버리고 원격 변경사항만 사용
**D.** 로컬 변경사항을 강제로 덮어쓰기

---

## 해결 방법

### 방법 1: 커밋 후 Merge (권장)

**장점:**
- 모든 변경사항의 히스토리가 보존됨
- 나중에 추적하기 쉬움
- 안전함

**단점:**
- 작은 변경사항도 커밋해야 함

**실행 순서:**
```bash
# 1. 현재 변경사항 확인
git status

# 2. 변경사항 스테이징
git add README.md

# 3. 커밋
git commit -m "로컬 README.md 수정사항"

# 4. 원격 저장소의 최신 변경사항 가져오기
git fetch origin

# 5. Merge 실행
git merge origin/main

# 6. 충돌이 발생하면 해결 후
git add .
git commit -m "Merge origin/main and resolve conflicts"
```

---

### 방법 2: Stash 사용

**장점:**
- 임시 변경사항을 깔끔하게 보관
- 커밋 히스토리를 깔끔하게 유지 가능
- 나중에 다시 적용 가능

**단점:**
- stash를 잊어버릴 수 있음

**실행 순서:**
```bash
# 1. 현재 변경사항을 stash에 저장
git stash save "README.md 임시 변경사항"

# 2. 원격 저장소의 최신 변경사항 가져오기
git fetch origin

# 3. Merge 실행
git merge origin/main

# 4. Stash한 변경사항 다시 적용
git stash pop

# 5. 충돌이 발생하면 해결
# 충돌 해결 후
git add .
git commit -m "Merge origin/main and apply local changes"
```

---

### 방법 3: 변경사항 버리기 (주의!)

**장점:**
- 빠르게 원격 상태로 맞출 수 있음

**단점:**
- 로컬 변경사항이 영구적으로 손실됨

**실행 순서:**
```bash
# 1. 로컬 변경사항 버리기 (주의!)
git checkout -- README.md

# 2. 원격 저장소의 최신 변경사항 가져오기
git fetch origin

# 3. Merge 실행
git merge origin/main
```

---

### 방법 4: Merge 전에 변경사항 백업

**장점:**
- 안전하게 변경사항 보존
- 나중에 수동으로 병합 가능

**실행 순서:**
```bash
# 1. 변경사항을 별도 파일로 백업
cp README.md README.md.backup

# 2. 로컬 변경사항 버리기
git checkout -- README.md

# 3. Merge 실행
git merge origin/main

# 4. 백업 파일에서 필요한 부분 수동으로 병합
# (에디터로 README.md.backup과 README.md를 비교하여 수동 병합)
```

---

## 실제 테스트 시나리오 실행

아래 스크립트를 실행하여 문제 상황을 재현하고 해결할 수 있습니다.
