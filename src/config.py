import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 거래소 설정 (기본값은 binanceus)
EXCHANGE_ID = os.getenv('EXCHANGE_ID', 'binanceus')

# 데이터 저장 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')

# 분석 설정
DEFAULT_TIMEFRAME = '1d'
DEFAULT_LIMIT = 365