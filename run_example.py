"""
실행 예제 스크립트
"""
from scraper import CourseScraper
import json

def main():
    print("=" * 60)
    print("멀티캠퍼스 코스 개요 테스트")
    print("=" * 60)
    
    scraper = CourseScraper()
    
    try:
        print("\n[1단계] 페이지 가져오는 중...")
        overview = scraper.get_course_overview()
        
        print("\n[2단계] 개요 데이터 추출 완료!")
        print("\n" + "=" * 60)
        print("추출된 개요 정보:")
        print("=" * 60)
        
        for key, value in overview.items():
            print(f"\n[{key}]")
            if isinstance(value, list):
                for idx, item in enumerate(value, 1):
                    text = str(item)[:200]  # 처음 200자만 표시
                    print(f"  {idx}. {text}{'...' if len(str(item)) > 200 else ''}")
            elif value:
                text = str(value)[:200]
                print(f"  {text}{'...' if len(str(value)) > 200 else ''}")
            else:
                print("  (없음)")
        
        # JSON으로 저장
        output_file = "overview_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(overview, f, ensure_ascii=False, indent=2)
        
        print(f"\n\n결과가 '{output_file}' 파일에 저장되었습니다.")
        print("\n테스트를 실행하려면: pytest test_overview.py -v")
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        print("\n가능한 원인:")
        print("1. 인터넷 연결 확인")
        print("2. 페이지 접근 권한 확인 (로그인 필요할 수 있음)")
        print("3. 웹사이트 구조 변경 확인")

if __name__ == "__main__":
    main()

