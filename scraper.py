"""
멀티캠퍼스 코스 상세 페이지 스크래퍼
"""
import requests
from bs4 import BeautifulSoup
from config import COURSE_URL, TIMEOUT, HEADERS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CourseScraper:
    """코스 상세 페이지를 스크래핑하는 클래스"""
    
    def __init__(self, url=None):
        self.url = url or COURSE_URL
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def fetch_page(self):
        """페이지를 가져옵니다"""
        try:
            logger.info(f"페이지 가져오는 중: {self.url}")
            response = self.session.get(self.url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"페이지 가져오기 실패: {e}")
            raise
    
    def parse_overview(self, html_content):
        """HTML에서 개요 섹션을 파싱합니다"""
        soup = BeautifulSoup(html_content, 'lxml')
        overview_data = {}
        
        # 다양한 가능한 선택자로 개요 섹션 찾기
        selectors = [
            {'name': 'title', 'selectors': ['h1', '.course-title', '.crs-title', '[class*="title"]']},
            {'name': 'overview', 'selectors': ['.overview', '.course-overview', '.crs-overview', '[class*="overview"]', '[id*="overview"]']},
            {'name': 'description', 'selectors': ['.description', '.course-description', '.crs-description', '[class*="description"]']},
            {'name': 'objectives', 'selectors': ['.objectives', '.course-objectives', '[class*="objective"]']},
            {'name': 'curriculum', 'selectors': ['.curriculum', '.course-curriculum', '[class*="curriculum"]']},
        ]
        
        for item in selectors:
            for selector in item['selectors']:
                elements = soup.select(selector)
                if elements:
                    overview_data[item['name']] = [elem.get_text(strip=True) for elem in elements]
                    logger.info(f"{item['name']} 발견: {len(elements)}개")
                    break
        
        # 메타 정보 추출
        overview_data['meta_title'] = soup.title.string if soup.title else None
        overview_data['meta_description'] = soup.find('meta', attrs={'name': 'description'})
        if overview_data['meta_description']:
            overview_data['meta_description'] = overview_data['meta_description'].get('content')
        
        # 모든 텍스트 내용 추출 (백업)
        if not overview_data.get('overview'):
            main_content = soup.find('main') or soup.find('div', class_='content') or soup.find('body')
            if main_content:
                overview_data['full_text'] = main_content.get_text(separator='\n', strip=True)[:2000]  # 처음 2000자만
        
        return overview_data
    
    def get_course_overview(self):
        """코스 개요를 가져옵니다"""
        html_content = self.fetch_page()
        return self.parse_overview(html_content)


if __name__ == "__main__":
    scraper = CourseScraper()
    overview = scraper.get_course_overview()
    print("\n=== 코스 개요 ===")
    for key, value in overview.items():
        print(f"\n{key}:")
        if isinstance(value, list):
            for item in value:
                print(f"  - {item[:100]}...")
        else:
            print(f"  {value}")

