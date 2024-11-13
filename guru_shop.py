import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class GuruBookshopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guru Bookshop")
        self.root.geometry("700x500")
        
        # Book catalog
        self.books = [
            {"id": 1, "title": "Python Basics", "author": "John Doe", "price": 15.99, "genre": "Programming"},
            {"id": 2, "title": "AI with Python", "author": "Jane Smith", "price": 25.99, "genre": "AI"},
            {"id": 3, "title": "Tkinter Guide", "author": "Sam Brown", "price": 10.99, "genre": "Programming"},
            {"id": 4, "title": "ML for Beginners", "author": "Mike White", "price": 20.00, "genre": "Machine Learning"},
        ]
        self.cart = []

        # Main UI
        self.create_main_ui()

    def create_main_ui(self):
        # Book list
        tk.Label(self.root, text="Welcome to Guru Bookshop", font=("Arial", 16)).pack(pady=10)
        
        # Filter Frame
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Genre: ").grid(row=0, column=0)
        self.genre_var = tk.StringVar()
        genre_menu = ttk.Combobox(filter_frame, textvariable=self.genre_var, values=["All", "Programming", "AI", "Machine Learning"])
        genre_menu.current(0)
        genre_menu.grid(row=0, column=1)
        
        tk.Label(filter_frame, text="Max Price: ").grid(row=0, column=2)
        self.price_var = tk.DoubleVar()
        tk.Entry(filter_frame, textvariable=self.price_var, width=10).grid(row=0, column=3)
        
        tk.Button(filter_frame, text="Apply Filters", command=self.apply_filters).grid(row=0, column=4, padx=5)
        
        # Book listbox
        self.book_listbox = tk.Listbox(self.root, width=80, height=10)
        self.book_listbox.pack(pady=10)
        self.update_book_listbox(self.books)
        
        # Add to cart button
        tk.Button(self.root, text="Add to Cart", command=self.add_to_cart).pack(pady=5)
        
        # Cart summary
        tk.Button(self.root, text="View Cart", command=self.view_cart).pack(pady=5)
        
        # Admin section
        tk.Button(self.root, text="Admin Section", command=self.admin_section).pack(pady=5)

    def apply_filters(self):
        genre = self.genre_var.get()
        max_price = self.price_var.get()

        filtered_books = [
            book for book in self.books 
            if (genre == "All" or book["genre"] == genre) and 
               (max_price == 0 or book["price"] <= max_price)
        ]
        
        self.update_book_listbox(filtered_books)

    def update_book_listbox(self, books):
        self.book_listbox.delete(0, tk.END)
        for book in books:
            self.book_listbox.insert(tk.END, f"{book['title']} by {book['author']} - ${book['price']:.2f}")

    def add_to_cart(self):
        selected_idx = self.book_listbox.curselection()
        if not selected_idx:
            messagebox.showwarning("Select Book", "Please select a book to add to cart.")
            return
        
        selected_book = self.books[selected_idx[0]]
        self.cart.append(selected_book)
        messagebox.showinfo("Added to Cart", f"{selected_book['title']} added to cart.")

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Your Cart")
        
        cart_listbox = tk.Listbox(cart_window, width=50, height=10)
        cart_listbox.pack(pady=10)
        
        total = 0
        for item in self.cart:
            cart_listbox.insert(tk.END, f"{item['title']} - ${item['price']:.2f}")
            total += item["price"]
        
        tk.Label(cart_window, text=f"Total: ${total:.2f}").pack(pady=5)
        tk.Button(cart_window, text="Checkout", command=self.checkout).pack(pady=5)

    def checkout(self):
        checkout_window = tk.Toplevel(self.root)
        checkout_window.title("Checkout")
        
        tk.Label(checkout_window, text="Enter your details to place the order", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(checkout_window, text="Name").pack()
        name_entry = tk.Entry(checkout_window)
        name_entry.pack()
        
        tk.Label(checkout_window, text="Address").pack()
        address_entry = tk.Entry(checkout_window)
        address_entry.pack()
        
        tk.Button(checkout_window, text="Place Order", command=lambda: self.place_order(name_entry.get(), address_entry.get())).pack(pady=10)

    def place_order(self, name, address):
        if not name or not address:
            messagebox.showwarning("Missing Information", "Please enter both name and address.")
            return
        
        messagebox.showinfo("Order Placed", f"Thank you for your order, {name}!")
        self.cart.clear()  # Clear cart after checkout

    def admin_section(self):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Admin Section")
        
        tk.Label(admin_window, text="Add New Book", font=("Arial", 12)).pack(pady=10)
        
        tk.Label(admin_window, text="Title").pack()
        title_entry = tk.Entry(admin_window)
        title_entry.pack()
        
        tk.Label(admin_window, text="Author").pack()
        author_entry = tk.Entry(admin_window)
        author_entry.pack()
        
        tk.Label(admin_window, text="Price").pack()
        price_entry = tk.Entry(admin_window)
        price_entry.pack()
        
        tk.Label(admin_window, text="Genre").pack()
        genre_entry = tk.Entry(admin_window)
        genre_entry.pack()
        
        tk.Button(admin_window, text="Add Book", command=lambda: self.add_book(
            title_entry.get(), author_entry.get(), price_entry.get(), genre_entry.get()
        )).pack(pady=5)

    def add_book(self, title, author, price, genre):
        if not title or not author or not price or not genre:
            messagebox.showwarning("Missing Information", "All fields are required to add a new book.")
            return
        
        try:
            price = float(price)
            new_book = {"id": len(self.books) + 1, "title": title, "author": author, "price": price, "genre": genre}
            self.books.append(new_book)
            self.update_book_listbox(self.books)
            messagebox.showinfo("Book Added", f"'{title}' by {author} has been added to the catalog.")
        except ValueError:
            messagebox.showerror("Invalid Price", "Please enter a valid price.")

# Run the application
root = tk.Tk()
app = GuruBookshopApp(root)
root.mainloop()
