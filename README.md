# 코스 개요 테스트 프로젝트

이 프로젝트는 특정 사이트의 의 개요를 테스트하는 도구입니다.

## 기능

- 웹 페이지 스크래핑
- 코스 개요 정보 추출
- 개요 데이터 검증 테스트
- 테스트 리포트 생성

## 설치

```bash
pip install -r requirements.txt
```

## 사용 방법

### 1. 스크래퍼 직접 실행

```bash
python scraper.py
```

### 2. 테스트 실행

```bash
# 기본 테스트 실행
pytest test_overview.py -v

# HTML 리포트 생성
pytest test_overview.py -v --html=report.html --self-contained-html

# 상세 출력
pytest test_overview.py -v -s
```

## 프로젝트 구조

```
.
├── config.py          # 설정 파일
├── scraper.py         # 웹 스크래퍼
├── test_overview.py   # 테스트 파일
├── requirements.txt   # 의존성 패키지
└── README.md         # 프로젝트 설명
```

## 테스트 항목

1. **페이지 접근성**: 페이지가 정상적으로 로드되는지 확인
2. **개요 존재 여부**: 개요 데이터가 추출되는지 확인
3. **제목 존재 여부**: 코스 제목이 있는지 확인
4. **콘텐츠 존재 여부**: 실제 콘텐츠가 있는지 확인
5. **개요 구조**: 개요 데이터 구조가 올바른지 확인
6. **콘텐츠 길이**: 추출된 콘텐츠가 비어있지 않은지 확인
7. **파싱 오류**: 파싱 중 오류가 발생하지 않는지 확인

## 설정

`config.py` 파일에서 다음을 수정할 수 있습니다:

- `COURSE_URL`: 테스트할 코스 URL
- `TIMEOUT`: 요청 타임아웃 시간
- `HEADERS`: HTTP 요청 헤더

## 주의사항

- 일부 페이지는 로그인이 필요할 수 있습니다
- 동적 콘텐츠의 경우 Selenium을 사용해야 할 수 있습니다
- 웹사이트 구조 변경 시 선택자를 업데이트해야 할 수 있습니다

