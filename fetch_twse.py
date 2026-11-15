import json
import requests

def main():
    quotes = {}
    
    # 1. 抓取 TWSE 上市股票每日收盤行情
    try:
        res = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL", timeout=15)
        if res.status_code == 200:
            for item in res.json():
                code = str(item.get("Code", "")).strip()
                price_str = str(item.get("ClosingPrice", "")).replace(",", "")
                if code and price_str:
                    try:
                        price = float(price_str)
                        if price > 0:
                            quotes[code] = {
                                "market": "TWSE",
                                "code": code,
                                "name": str(item.get("Name", code)).strip(),
                                "price": price
                            }
                    except ValueError:
                        pass
    except Exception as e:
        print(f"TWSE fetch error: {e}")

    # 2. 抓取 TPEx 上櫃股票每日收盤行情
    try:
        res = requests.get("https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes", timeout=15)
        if res.status_code == 200:
            for item in res.json():
                code = str(item.get("SecuritiesCompanyCode", "")).strip()
                price_str = str(item.get("Close", "")).replace(",", "")
                if code and price_str:
                    try:
                        price = float(price_str)
                        if price > 0:
                            quotes[code] = {
                                "market": "TPEX",
                                "code": code,
                                "name": str(item.get("CompanyName", code)).strip(),
                                "price": price
                            }
                    except ValueError:
                        pass
    except Exception as e:
        print(f"TPEx fetch error: {e}")

    output = {
        "count": len(quotes),
        "quotes": quotes
    }
    
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved {len(quotes)} quotes to market_data.json")

if __name__ == "__main__":
    main()