import ccxt
import pandas as pd
import os
import requests
import time
from src.config import EXCHANGE_ID, RAW_DATA_DIR, DEFAULT_TIMEFRAME, DEFAULT_LIMIT

# 1. 제외할 스테이블코인 및 래핑 코인 리스트 (분석 노이즈 제거)
STABLECOINS = [
    'USDT', 'USDC', 'DAI', 'FDUSD', 'TUSD', 'USDD', 'PYUSD', 'USDP', 
    'LUSD', 'BUSD', 'USTC', 'WBTC', 'WETH', 'WSTETH', 'STETH', 'WSTETH'
]

def get_top_symbols_filtered(limit=150):
    """
    CoinGecko에서 넉넉하게 상위 150개를 가져와서 스테이블코인을 필터링합니다.
    """
    print(f"📡 CoinGecko에서 시가총액 순위를 분석 중 (대상: 상위 {limit}개)...")
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # 스테이블코인이 아닌 것들만 필터링하여 심볼 리스트 생성
        filtered_symbols = [
            coin['symbol'].upper() for coin in data 
            if coin['symbol'].upper() not in STABLECOINS
        ]
        return filtered_symbols
    except Exception as e:
        print(f" 코인 리스트 확보 실패: {e}")
        return ['BTC', 'ETH', 'SOL', 'ADA', 'XRP'] # 실패 시 비상용 리스트

def fetch_top_50_valid_coins():
    """
    Binance.US에서 지원하는 코인 중 유효한 50개를 채울 때까지 수집합니다.
    """
    candidate_symbols = get_top_symbols_filtered(limit=150)
    
    # 거래소 객체 생성
    exchange_class = getattr(ccxt, EXCHANGE_ID)
    exchange = exchange_class({'enableRateLimit': True})
    markets = exchange.load_markets()
    tradeable_pairs = [s for s in markets if '/USDT' in s]
    
    success_count = 0
    target_count = 50 
    
    print(f"\n {EXCHANGE_ID} 에서 시가총액 상위에 있는 코인 {target_count}개를 수집합니다.")

    for symbol in candidate_symbols:
        if success_count >= target_count:
            break # 50개 달성 시 중단
            
        pair = f"{symbol}/USDT"
        if pair not in tradeable_pairs:
            continue # 상장되지 않은 코인은 조용히 스킵
            
        try:
            # OHLCV 데이터 수집
            ohlcv = exchange.fetch_ohlcv(pair, DEFAULT_TIMEFRAME, limit=DEFAULT_LIMIT)
            
            if not ohlcv:
                continue

            # 데이터 가공
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # 파일 저장
            file_name = f"{EXCHANGE_ID}_{symbol}_{DEFAULT_TIMEFRAME}.csv"
            file_path = os.path.join(RAW_DATA_DIR, file_name)
            
            os.makedirs(RAW_DATA_DIR, exist_ok=True)
            df.to_csv(file_path, index=False)
            
            success_count += 1
            print(f" [{success_count}/{target_count}] {symbol} 수집 및 저장 완료")
            
            # API 호출 간격 유지
            time.sleep(exchange.rateLimit / 1000)

        except Exception as e:
            # 에러 발생 시 로그만 남기고 다음 코인으로 진행
            print(f"⚠️ {symbol} 수집 중 오류 발생: {e}")

    print(f"\n 수집 종료! 총 {success_count}개의 유효한 코인 데이터를 확보했습니다.")

if __name__ == "__main__":
    fetch_top_50_valid_coins()