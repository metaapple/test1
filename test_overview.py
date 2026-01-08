"""
코스 개요 테스트
"""
import pytest
from scraper import CourseScraper
from config import COURSE_URL


class TestCourseOverview:
    """코스 개요 테스트 클래스"""
    
    @pytest.fixture(scope="class")
    def scraper(self):
        """스크래퍼 인스턴스 생성"""
        return CourseScraper()
    
    @pytest.fixture(scope="class")
    def overview_data(self, scraper):
        """개요 데이터 가져오기"""
        return scraper.get_course_overview()
    
    def test_page_accessibility(self, scraper):
        """페이지 접근 가능 여부 테스트"""
        html_content = scraper.fetch_page()
        assert html_content is not None
        assert len(html_content) > 0
        assert "html" in html_content.lower() or "<" in html_content
    
    def test_overview_exists(self, overview_data):
        """개요 데이터가 존재하는지 테스트"""
        assert overview_data is not None
        assert isinstance(overview_data, dict)
        assert len(overview_data) > 0
    
    def test_has_title(self, overview_data):
        """제목이 있는지 테스트"""
        has_title = (
            overview_data.get('title') or 
            overview_data.get('meta_title') or
            overview_data.get('full_text')
        )
        assert has_title, "제목 또는 메타 제목이 없습니다"
    
    def test_has_content(self, overview_data):
        """콘텐츠가 있는지 테스트"""
        has_content = False
        for key, value in overview_data.items():
            if value:
                if isinstance(value, list) and len(value) > 0:
                    has_content = True
                    break
                elif isinstance(value, str) and len(value) > 0:
                    has_content = True
                    break
        
        assert has_content, "콘텐츠가 없습니다"
    
    def test_overview_structure(self, overview_data):
        """개요 구조 검증"""
        # 최소한 하나의 유효한 필드가 있어야 함
        valid_fields = ['title', 'overview', 'description', 'objectives', 'curriculum', 'meta_title', 'meta_description', 'full_text']
        has_valid_field = any(
            overview_data.get(field) for field in valid_fields
        )
        assert has_valid_field, "유효한 개요 필드가 없습니다"
    
    def test_overview_content_length(self, overview_data):
        """개요 내용 길이 테스트"""
        total_length = 0
        for key, value in overview_data.items():
            if isinstance(value, list):
                total_length += sum(len(str(item)) for item in value)
            elif isinstance(value, str):
                total_length += len(value)
        
        assert total_length > 0, "개요 내용이 비어있습니다"
    
    def test_no_error_in_parsing(self, scraper):
        """파싱 중 오류가 없는지 테스트"""
        try:
            overview = scraper.get_course_overview()
            assert overview is not None
        except Exception as e:
            pytest.fail(f"파싱 중 오류 발생: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html", "--self-contained-html"])

