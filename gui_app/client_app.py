import requests

API_URL = 'http://localhost:5000/stock/'

def get_stock_data(symbol):
    response = requests.get(API_URL + symbol)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def display_stock_data(data):
    if data:
        print(f"Stock data for {data[0]['_source']['symbol']}:")
        for entry in data:
            print(f"Time: {entry['_source']['time']}")
            for key, value in entry['_source']['data'].items():
                print(f"  {key}: {value}")
            print()
    else:
        print("Failed to retrieve data or no data available.")

def main():
    symbol = input("Enter stock symbol: ")
    data = get_stock_data(symbol)
    display_stock_data(data)

if __name__ == '__main__':
    main()
