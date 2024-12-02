import tkinter as tk
from backend.controllers import get_all_products

class ProductListView:
    def __init__(self, master):
        self.master = master
        self.products = []
        self.create_widgets()
        self.product_listbox.bind('<<ListboxSelect>>', self.show_product_details)

    def create_widgets(self):
        self.product_listbox = tk.Listbox(self.master)
        self.product_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.details_frame = tk.Frame(self.master)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.load_products()
        self.product_listbox.bind('<<ListboxSelect>>', self.show_product_details)

    def load_products(self):
        self.products = get_all_products()
        for product in self.products:
            self.product_listbox.insert(tk.END, product.name)

    def show_product_details(self, event):
        selected_index = self.product_listbox.curselection()
        if selected_index:
            product = self.products[selected_index[0]]
            for widget in self.details_frame.winfo_children():
                widget.destroy()
            tk.Label(self.details_frame, text=f"Nombre: {product.name}").pack()
            tk.Label(self.details_frame, text=f"Costo: {product.cost}").pack()
