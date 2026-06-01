# MyAPI_WebSite
# 📌 Naver Search API 기반 웹 문서 검색 & 즐겨찾기

## 🚀 프로젝트 개요
네이버 웹문서 검색 API를 활용하여 특정 키워드와 관련된 웹사이트 정보를 가져오는 모듈입니다.  
검색 결과에는 **제목(title), 요약(description), 링크(URL)** 이 포함되며, 사용자는 원하는 사이트를 클릭하거나 즐겨찾기로 저장할 수 있습니다.  
음악, 가사, 뉴스 등 다양한 키워드 검색에 활용 가능하며, 앱/웹 서비스에서 외부 콘텐츠 탐색 기능을 손쉽게 구현할 수 있도록 지원합니다.

## 🛠️ 주요 기능
- **검색 기능**
  - `aiohttp` + `asyncio` 기반 비동기 API 호출
  - `NaverSiteScraper` 클래스: `fetch()` → API 요청, `search()` → 병렬 데이터 수집
  - `BeautifulSoup`으로 HTML 태그 제거 및 텍스트 정리
- **데이터 관리**
  - `SiteModel` (ODMantic) 구조 정의: keyword, title, link, description, is_favorite
  - MongoDB 저장 및 조회, JSON 형태로 프론트엔드 활용 가능
- **UI & 즐겨찾기**
  - `index.html` + `style.css` 카드형 UI
  - ♥ 버튼으로 즐겨찾기 추가/해제
  - `/favorites` 페이지에서 즐겨찾기 목록 확인 가능

## ✅ 테스트 및 실행
- `/search` → 검색 결과 정상 표시
- 즐겨찾기 추가/해제 기능 정상 동작
- `/favorites` → 즐겨찾기 목록 정상 표시
- 서버 시작/종료 시 MongoDB 연결 로그 확인

## ▶️ 실행 방법
- `server.py` → `uvicorn`으로 FastAPI 실행
- `secrets.json` → API 키 및 DB 접속 정보 관리
- `requirements.txt` → 모든 의존 패키지 버전 명시
