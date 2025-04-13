from django.shortcuts import render
import yfinance as yf
from django.http import JsonResponse

# 顯示首頁
def home(request):
    return render(request, 'StockTrackerMain.html')

# 用來抓取股票資料並回傳 JSON
def get_stock_data(request):
    stock_symbol = request.GET.get('symbol', '').upper()  # 取得股票代碼，轉換為大寫
    if not stock_symbol:
        return JsonResponse({'error': '請輸入股票代碼'}, status=400)

    try:
        # 使用 yfinance 來抓取股票資料，這裡使用 download() 方法
        data = yf.download(stock_symbol, period='3mo', interval='1d')

        if data.empty:
            raise ValueError("無法取得資料，請確認股票代碼是否正確")

        # 轉換成 JSON 格式，處理資料列名
        response = {
            'dates': data.index.strftime('%Y-%m-%d').tolist() if not data.index.empty else [],
            'open': data[('Open', stock_symbol)].tolist() if ('Open', stock_symbol) in data.columns else [],
            'high': data[('High', stock_symbol)].tolist() if ('High', stock_symbol) in data.columns else [],
            'low': data[('Low', stock_symbol)].tolist() if ('Low', stock_symbol) in data.columns else [],
            'close': data[('Close', stock_symbol)].tolist() if ('Close', stock_symbol) in data.columns else [],
            'volume': data[('Volume', stock_symbol)].tolist() if ('Volume', stock_symbol) in data.columns else []
        }

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({'error': f"無法取得股票資料：{str(e)}"}, status=400)
