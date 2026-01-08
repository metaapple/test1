#!/bin/bash

# Git Merge 충돌 테스트 시나리오 실행 스크립트
# 이 스크립트는 문제 상황을 재현하고 해결 방법을 테스트합니다.

echo "=========================================="
echo "Git Merge 충돌 테스트 시나리오"
echo "=========================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 현재 상태 확인
echo -e "${YELLOW}[1단계] 현재 Git 상태 확인${NC}"
git status
echo ""

# 원격 저장소 확인
echo -e "${YELLOW}[2단계] 원격 저장소 확인${NC}"
git remote -v
echo ""

# 브랜치 확인
echo -e "${YELLOW}[3단계] 브랜치 확인${NC}"
git branch -a
echo ""

# 최근 커밋 확인
echo -e "${YELLOW}[4단계] 최근 커밋 히스토리${NC}"
git log --oneline -5
echo ""

echo -e "${GREEN}=========================================="
echo "테스트 시나리오 준비 완료"
echo "==========================================${NC}"
echo ""
echo "이제 다음 중 하나를 선택하여 테스트하세요:"
echo ""
echo "1. 문제 상황 재현:"
echo "   - README.md 파일을 수정하세요"
echo "   - git merge origin/main 실행"
echo "   - 오류 메시지 확인"
echo ""
echo "2. 해결 방법 1 (커밋 후 Merge):"
echo "   git add README.md"
echo "   git commit -m '로컬 변경사항'"
echo "   git fetch origin"
echo "   git merge origin/main"
echo ""
echo "3. 해결 방법 2 (Stash 사용):"
echo "   git stash save '임시 변경사항'"
echo "   git fetch origin"
echo "   git merge origin/main"
echo "   git stash pop"
echo ""
echo "4. 해결 방법 3 (변경사항 버리기 - 주의!):"
echo "   git checkout -- README.md"
echo "   git fetch origin"
echo "   git merge origin/main"
echo ""
