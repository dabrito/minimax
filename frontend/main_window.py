import math
import tkinter as tk
from tkinter import ttk, messagebox
from backend.models import Product
from backend.minimax import minimax, alpha_beta
from backend.controllers import (
    add_product_to_db,
    update_product_in_db,
    delete_product_from_db,
    get_all_products
)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Pricing System")
        self.products = []
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        # Create main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=1)

        # Products list frame (right side)
        products_frame = ttk.LabelFrame(main_container, text="Productos", padding="5")
        products_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Product list
        self.products_list = tk.Listbox(products_frame, height=15)
        self.products_list.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.products_list.bind('<<ListboxSelect>>', self.on_product_select)

        # Make the listbox expand
        products_frame.columnconfigure(0, weight=1)
        products_frame.rowconfigure(0, weight=1)

        # Load products into the list
        self.load_products()

        # Control panel (left side)
        control_frame = ttk.LabelFrame(main_container, text="Panel de Control", padding="5")
        control_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Configure control_frame grid
        for i in range(8):
            control_frame.rowconfigure(i, weight=1)
        control_frame.columnconfigure(1, weight=1)

        # Product details entries
        ttk.Label(control_frame, text="Nombre Producto:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(control_frame)
        self.name_entry.grid(row=0, column=1, sticky=(tk.E, tk.W))

        ttk.Label(control_frame, text="Costo Producto:").grid(row=1, column=0, sticky=tk.W)
        self.cost_entry = ttk.Entry(control_frame)
        self.cost_entry.grid(row=1, column=1, sticky=(tk.E, tk.W))

        ttk.Label(control_frame, text="Precio Producto Rival:").grid(row=2, column=0, sticky=tk.W)
        self.rival_price_entry = ttk.Entry(control_frame)
        self.rival_price_entry.grid(row=2, column=1, sticky=(tk.E, tk.W))

        ttk.Label(control_frame, text="Precio Inicial Propio:").grid(row=3, column=0, sticky=tk.W)
        self.initial_price_entry = ttk.Entry(control_frame)
        self.initial_price_entry.grid(row=3, column=1, sticky=(tk.E, tk.W))

        ttk.Label(control_frame, text="Precio Minimo Propio:").grid(row=4, column=0, sticky=tk.W)
        self.min_price_entry = ttk.Entry(control_frame)
        self.min_price_entry.grid(row=4, column=1, sticky=(tk.E, tk.W))

        ttk.Label(control_frame, text="Precio Maximo Propio:").grid(row=5, column=0, sticky=tk.W)
        self.max_price_entry = ttk.Entry(control_frame)
        self.max_price_entry.grid(row=5, column=1, sticky=(tk.E, tk.W))

        # Selector de estrategias propias
        ttk.Label(control_frame, text="Estrategia Propia:").grid(row=6, column=0, sticky=tk.W)
        self.own_strategy_var = tk.StringVar()
        self.own_strategy_combo = ttk.Combobox(control_frame, textvariable=self.own_strategy_var)
        self.own_strategy_combo['values'] = ('Agresivo', 'Moderado', 'Conservador')
        self.own_strategy_combo.grid(row=6, column=1, sticky=(tk.E, tk.W))

        # Previous Rival Strategies selector
        ttk.Label(control_frame, text="Estrategia Rival Previa:").grid(row=7, column=0, sticky=tk.W)
        self.rival_strategy_var = tk.StringVar()
        self.rival_strategy_combo = ttk.Combobox(control_frame, textvariable=self.rival_strategy_var)
        self.rival_strategy_combo['values'] = ('Agresivo', 'Moderado', 'Conservador')
        self.rival_strategy_combo.grid(row=7, column=1, sticky=(tk.E, tk.W))

        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Calcular MiniMax", command=self.calculate_price_minimax).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calcular AlphaBetha", command=self.calculate_price_alphabetha).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.update_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Agregar", command=self.add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.delete_product).pack(side=tk.LEFT, padx=5)

        # Aquí agregamos el botón Clean
        ttk.Button(button_frame, text="Limpiar", command=self.clean_fields).pack(side=tk.LEFT, padx=5)

        # Details frame for product details display
        self.details_frame = ttk.LabelFrame(main_container, text="Detalles de Producto", padding="5")
        self.details_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Configure details_frame grid
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.rowconfigure(0, weight=1)

    def clean_fields(self):
        self.name_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        self.rival_price_entry.delete(0, tk.END)
        self.initial_price_entry.delete(0, tk.END)
        self.min_price_entry.delete(0, tk.END)
        self.max_price_entry.delete(0, tk.END)

        self.own_strategy_var.set('')
        self.rival_strategy_var.set('')
        
        for widget in self.details_frame.winfo_children():
          widget.destroy()

    def load_products(self):
        self.products = get_all_products()
        self.products_list.delete(0, tk.END)
        for product in self.products:
            self.products_list.insert(tk.END, product.name)

    def on_product_select(self, event):
        selected_index = self.products_list.curselection()
        if selected_index:
            product = self.products[selected_index[0]]
            # Clear previous details
            for widget in self.details_frame.winfo_children():
                widget.destroy()
            # Display product details
            ttk.Label(self.details_frame, text=f"Nombre: {product.name}").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(self.details_frame, text=f"Costo: {product.cost}").grid(row=1, column=0, sticky=tk.W)
            ttk.Label(self.details_frame, text=f"Precio Rival: {product.rival_price}").grid(row=2, column=0, sticky=tk.W)
            ttk.Label(self.details_frame, text=f"Precio Inicial: {product.initial_price}").grid(row=3, column=0, sticky=tk.W)
            ttk.Label(self.details_frame, text=f"Precio Minimo: {product.min_price}").grid(row=4, column=0, sticky=tk.W)
            ttk.Label(self.details_frame, text=f"Pricio Maximo: {product.max_price}").grid(row=5, column=0, sticky=tk.W)
            # Populate entries in control panel
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, product.name)
            self.cost_entry.delete(0, tk.END)
            self.cost_entry.insert(0, str(product.cost))
            self.rival_price_entry.delete(0, tk.END)
            self.rival_price_entry.insert(0, str(product.rival_price))
            self.initial_price_entry.delete(0, tk.END)
            self.initial_price_entry.insert(0, str(product.initial_price))
            self.min_price_entry.delete(0, tk.END)
            self.min_price_entry.insert(0, str(product.min_price))
            self.max_price_entry.delete(0, tk.END)
            self.max_price_entry.insert(0, str(product.max_price))

    def calculate_price_alphabetha(self):
      try:
        costo = float(self.cost_entry.get())
        precio_rival = float(self.rival_price_entry.get())
        precio_min = float(self.min_price_entry.get())
        precio_max = float(self.max_price_entry.get())
        estrategia_propia = self.own_strategy_var.get()
        estrategia_rival = self.rival_strategy_var.get()

        print(f"Inputs -> costo: {costo}, precio_rival: {precio_rival}, precio_min: {precio_min}, precio_max: {precio_max}")
        print(f"Estrategias -> propia: {estrategia_propia}, rival: {estrategia_rival}")

        valor, precio_optimo = alpha_beta(
            nodo=precio_rival,
            profundidad=5,
            alfa=-math.inf,
            beta=math.inf,
            maximizador=True,
            costo=costo,
            precio_min=precio_min,
            precio_max=precio_max,
            precio_rival=precio_rival,
            estrategia_propia=estrategia_propia,
            estrategia_rival=estrategia_rival
        )
        messagebox.showinfo("Precio Optimo", f"El precio optimo es: {precio_optimo:.2f}\nValor: {valor:.2f}")
      except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

    def calculate_price_minimax(self):
      try:
            costo = float(self.cost_entry.get())
            precio_rival = float(self.rival_price_entry.get())
            precio_min = float(self.min_price_entry.get())
            precio_max = float(self.max_price_entry.get())
            estrategia_propia = self.own_strategy_var.get()
            estrategia_rival = self.rival_strategy_var.get()

            print(f"Inputs -> costo: {costo}, precio_rival: {precio_rival}, precio_min: {precio_min}, precio_max: {precio_max}")
            print(f"Estrategias -> propia: {estrategia_propia}, rival: {estrategia_rival}")

            valor, precio_optimo = minimax(
                nodo=precio_rival,
                profundidad=5,
                maximizador=True,
                costo=costo,
                precio_min=precio_min,
                precio_max=precio_max,
                precio_rival=precio_rival,
                estrategia_propia=estrategia_propia,
                estrategia_rival=estrategia_rival
            )
            messagebox.showinfo("Precio Optimo", f"El precio optimo es: {precio_optimo:.2f}\nValor: {valor:.2f}")
      except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")


    def update_product(self):
        selected_index = self.products_list.curselection()
        if selected_index:
            product = self.products[selected_index[0]]
            # Actualiza los atributos del producto con los datos ingresados
            product.name = self.name_entry.get()
            product.cost = float(self.cost_entry.get())
            product.rival_price = float(self.rival_price_entry.get())
            product.initial_price = float(self.initial_price_entry.get())
            product.min_price = float(self.min_price_entry.get())
            product.max_price = float(self.max_price_entry.get())
            # Actualiza en la base de datos
            update_product_in_db(product)
            # Refresca la lista de productos
            self.load_products()
            tk.messagebox.showinfo("Actualizado", "El producto ha sido actualizado exitosamente.")
        else:
            tk.messagebox.showwarning("Advertencia", "No se ha seleccionado ningún producto para actualizar.")

    def add_product(self):
      try:
        # Crea una nueva instancia del producto con los datos ingresados
        product = Product(
            name=self.name_entry.get(),
            cost=float(self.cost_entry.get()),
            rival_price=float(self.rival_price_entry.get()),
            initial_price=float(self.initial_price_entry.get()),
            min_price=float(self.min_price_entry.get()),
            max_price=float(self.max_price_entry.get())
        )
        # Agrega a la base de datos
        add_product_to_db(product)
        # Refresca la lista de productos
        self.load_products()
        tk.messagebox.showinfo("Agregado", "El producto ha sido agregado exitosamente.")
      except ValueError:
        tk.messagebox.showerror("Error de entrada", "Por favor, ingrese valores numéricos válidos.")

    def delete_product(self):
      try:
        # Delete selected product from the database
        selected_index = self.products_list.curselection()
        if selected_index:
            product = self.products[selected_index[0]]
            print(f"Deleting product '{product.name}' from the database...")
            delete_product_from_db(product.id)
            self.load_products()
            tk.messagebox.showinfo("Eliminado", f"El producto '{product.name}' ha sido eliminado.")
        else:
            tk.messagebox.showwarning("Advertencia", "No se ha seleccionado ningún producto para eliminar.")
      except ValueError:
        tk.messagebox.showerror("Error", "No se ha seleccionado ningún producto para eliminar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
