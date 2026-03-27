import ccxt
import pandas as pd
import os
# 우리가 만든 config 불러오기
from src.config import EXCHANGE_ID, RAW_DATA_DIR, DEFAULT_TIMEFRAME, DEFAULT_LIMIT

def fetch_and_save_ohlcv(symbol, timeframe=DEFAULT_TIMEFRAME, limit=DEFAULT_LIMIT):
    print(f"[{EXCHANGE_ID}]에서 [{symbol}] 데이터 가져오는 중...")
    
    # 1. 설정된 거래소 객체 생성
    exchange_class = getattr(ccxt, EXCHANGE_ID)
    exchange = exchange_class()
    
    # 2. OHLCV 데이터 가져오기
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    # 3. 데이터 가공
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # 4. 저장
    safe_symbol = symbol.replace('/', '_')
    file_name = f"{EXCHANGE_ID}_{safe_symbol}_{timeframe}.csv"
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f" 저장 완료: {file_path}")

if __name__ == "__main__":
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    for symbol in symbols:
        try:
            fetch_and_save_ohlcv(symbol)
        except Exception as e:
            print(f" {symbol} 실패: {e}")