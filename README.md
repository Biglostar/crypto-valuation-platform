cat <<EOF > README.md
# Crypto Valuation Platform (CVP)

데이터 기반의 암호화폐 가치 평가 및 퀀트 분석 플랫폼입니다. 시가총액 상위 코인들의 데이터를 자동으로 수집하고, 수학적 모델을 통해 저평가된 자산을 발굴하는 것을 목표로 합니다.

## 🎯 Project Goals
- **Data Automation:** 전 세계 주요 거래소(Binance.US 등)의 데이터를 실시간/과거 데이터로 자동 수집.
- **Quant Modeling:** Applied Mathematics 지식을 활용하여 단순 가격 이상의 독자적인 가치 평가 지표 개발.
- **Risk Management:** 코인 간 상관관계(Correlation) 분석을 통한 포트폴리오 최적화 및 리스크 관리.

## 📂 Project Structure
\`\`\`text
crypto-valuation-platform/
├── data/raw/           # 수집된 원본 CSV 데이터 (BTC, ETH 등 주요 50종)
├── notebooks/          # 데이터 시각화 및 수학적 모델 검증용 연습장
├── src/
│   ├── collector/      # 데이터 수집 엔진 (CoinGecko + CCXT 활용)
│   ├── engine/         # 퀀트 및 수학적 계산 로직 (수식 구현)
│   └── config.py       # 프로젝트 중앙 설정 관리 (Environment-aware)
├── .env                # 환경 변수 (거래소 설정: binanceus / binance)
└── requirements.txt    # 설치가 필요한 라이브러리 목록
\`\`\`

## 🛠 Tech Stack
- **Language:** Python 3.9+
- **Libraries:** Pandas, CCXT (Exchange API), Requests, python-dotenv
- **Data Source:** CoinGecko (Market Cap Ranking), Binance.US (Price Data)

## ⚙️ Setup & Installation

1. **가상환경 생성 및 활성화**
   \`\`\`bash
   python3 -m venv .venv
   source .venv/bin/activate
   \`\`\`

2. **필수 라이브러리 설치**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **환경 변수 설정 (\`.env\`)**
   현재 개발 위치(미국/한국)에 맞는 거래소 ID를 설정합니다.
   \`\`\`env
   EXCHANGE_ID=binanceus
   \`\`\`

## 🚀 Usage

### 시가총액 상위 50개 코인 데이터 수집
Coingeko에서 스테이블코인을 제외한 변동성이 있는 유효 코인 50개의 일봉 데이터를 자동으로 가져옵니다.
\`\`\`bash
python3 -m src.collector.fetch_top_history
\`\`\`

## 🧪 Current Progress
- [x] 표준 프로젝트 폴더 구조 및 가상환경 구축
- [x] 중앙 집중식 설정 관리 시스템 (\`.env\`, \`config.py\`) 구현
- [x] 스테이블코인 필터링 로직이 포함된 시가총액 상위 50개 코인 자동 수집기 완성
- [ ] Jupyter Notebook을 통한 데이터 시각화 및 기초 통계 분석 (Next Step)
- [ ] 퀀트 모델링: 수익률 기반 상관관계 분석 및 변동성 지표 산출
EOF