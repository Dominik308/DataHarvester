import tkinter as tk
from tkinter import ttk
import requests
from elasticsearch import Elasticsearch

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Data Viewer")
        
        self.label = tk.Label(root, text="Enter stock symbol:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button = tk.Button(root, text="Get Data", command=self.get_stock_data)
        self.button.pack()

        self.text = tk.Text(root, height=20, width=80)
        self.text.pack()

        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def get_stock_data(self):
        symbol = self.entry.get()
        query = {
            'query': {
                'match': {
                    'symbol': symbol
                }
            }
        }
        res = self.es.search(index='stocks', body=query)
        self.display_stock_data(res['hits']['hits'])

    def display_stock_data(self, data):
        self.text.delete(1.0, tk.END)
        if data:
            for entry in data:
                self.text.insert(tk.END, f"Symbol: {entry['_source']['symbol']}\n")
                self.text.insert(tk.END, f"Time: {entry['_source']['time']}\n")
                for key, value in entry['_source']['data'].items():
                    self.text.insert(tk.END, f"  {key}: {value}\n")
                self.text.insert(tk.END, "\n")
        else:
            self.text.insert(tk.END, "No data available.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
