import tkinter as tk
from ui.components import ProductListView

def main():
    root = tk.Tk()
    root.title("Optimización de Precios")
    root.geometry("600x400")
    app = ProductListView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
