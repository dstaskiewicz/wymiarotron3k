from tkinter import *
import sqlite3
from tkinter import messagebox
import greedypacker

root = Tk()
root.title('Wymiarotron 3000')
root.geometry("900x600")

# database
database = sqlite3.connect('products.db')
# cursor
cursor = database.cursor()

'''
# create a table
cursor.execute("""CREATE TABLE products (
            name text,
            EAN text,
            height integer,
            length integer,
            width integer,
            weight integer
            )""")
'''
'''

print_label.pack()
'''

basket_list = []


def add_new_product(window, name, ean, height, length, width, weight):
    add_database = sqlite3.connect('products.db')
    add_cursor = add_database.cursor()
    if name != '' and ean != '' and height != '' and length != '' and width != '' and weight != '':
        add_cursor.execute("INSERT INTO products VALUES (:name, :EAN, :height, :length, :width, :weight)",
                           {
                               'name': name,
                               'EAN': ean,
                               'height': height,
                               'length': length,
                               'width': width,
                               'weight': weight
                           }
                           )
        messagebox.showinfo(title="Success", message="Successfully added a new product")
        window.destroy()
    else:
        messagebox.showerror(title="Error", message="One of the fields is empty")

    add_database.commit()
    add_database.close()


def open_add_new_product_window():
    add_new_product_window = Toplevel(root)
    add_new_product_window.title('Add new product')
    add_new_product_window.geometry("275x175")

    name_label = Label(add_new_product_window, text="Name", width=10)
    name_label.grid(row=0, column=0)
    ean_label = Label(add_new_product_window, text="EAN", width=10)
    ean_label.grid(row=1, column=0)
    height_label = Label(add_new_product_window, text="Height", width=10)
    height_label.grid(row=2, column=0)
    length_label = Label(add_new_product_window, text="Length", width=10)
    length_label.grid(row=3, column=0)
    width_label = Label(add_new_product_window, text="Width", width=10)
    width_label.grid(row=4, column=0)
    weight_label = Label(add_new_product_window, text="Weight", width=10)
    weight_label.grid(row=5, column=0)

    name_entry = Entry(add_new_product_window, width=30)
    name_entry.grid(row=0, column=1)
    ean_entry = Entry(add_new_product_window, width=30)
    ean_entry.grid(row=1, column=1)
    height_entry = Entry(add_new_product_window, width=30)
    height_entry.grid(row=2, column=1)
    length_entry = Entry(add_new_product_window, width=30)
    length_entry.grid(row=3, column=1)
    width_entry = Entry(add_new_product_window, width=30)
    width_entry.grid(row=4, column=1)
    weight_entry = Entry(add_new_product_window, width=30)
    weight_entry.grid(row=5, column=1)

    accept_button = Button(add_new_product_window, text="Apply", command=lambda: add_new_product(add_new_product_window,
                                                                                                 name_entry.get(),
                                                                                                 ean_entry.get(),
                                                                                                 height_entry.get(),
                                                                                                 length_entry.get(),
                                                                                                 width_entry.get(),
                                                                                                 weight_entry.get()))
    accept_button.grid(row=6, column=0, columnspan=2)


def open_display_products_window():
    display_products_window = Toplevel(root)
    display_products_window.title('Show all products')
    display_products_window.geometry("1500x600")

    display_database = sqlite3.connect('products.db')
    display_cursor = display_database.cursor()

    display_cursor.execute("SELECT *, oid FROM products")
    records = display_cursor.fetchall()

    table = [("Name", "EAN", "Height", "Length", "Width", "Weight", "ID")] + records

    # Create a main Frame
    main_frame = Frame(display_products_window)
    main_frame.pack(fill=BOTH, expand=1)

    # Create a Canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Add a Scrollbar to the Canvas
    my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    # Configure the Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Create another Frame inside the Canvas
    second_frame = Frame(my_canvas)

    # Add new Frame to a Window in the Canvas
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    for i in range(len(table)):
        for j in range(len(table[0])):
            temp_label = Label(second_frame, text=table[i][j], width=20, font=('Arial', 12))
            temp_label.grid(row=i, column=j)

    display_database.commit()
    display_database.close()


def open_delete_product_window():
    delete_product_window = Toplevel(root)
    delete_product_window.title('Remove product')
    delete_product_window.geometry("400x400")

    delete_database = sqlite3.connect('products.db')
    delete_cursor = delete_database.cursor()

    delete_cursor.execute("SELECT *, oid FROM products")
    results = delete_cursor.fetchall()

    delete_product_listbox = Listbox(delete_product_window, width=64, height=20)
    delete_product_listbox.grid(row=0, column=0, sticky='news', pady=5, padx=5)
    delete_product_scrollbar = Scrollbar(delete_product_window, orient=VERTICAL)
    delete_product_scrollbar.grid(row=0, column=0, sticky='nse', pady=5)
    delete_product_listbox.config(yscrollcommand=delete_product_scrollbar.set)
    delete_product_scrollbar.config(command=delete_product_listbox.yview)
    for product in results:
        delete_product_listbox.insert(END, product)

    remove_product_button = Button(delete_product_window, text="Remove selected product",
                                   command=lambda: delete_product_from_database(
                                       delete_product_listbox.get(delete_product_listbox.curselection()[0])))
    remove_product_button.grid(row=2, column=0, padx=5, pady=5)
    delete_database.commit()
    delete_database.close()


def delete_product_from_database(oid):
    delete_database = sqlite3.connect('products.db')
    delete_cursor = delete_database.cursor()

    delete_cursor.execute("DELETE from products WHERE oid = (:oid)", {'oid': oid[6]})
    messagebox.showinfo(title="Success", message="Successfully deleted product from the database.")
    delete_database.commit()
    delete_database.close()


def search_product_ean(ean):
    search_database = sqlite3.connect('products.db')
    search_cursor = search_database.cursor()

    search_cursor.execute("SELECT * FROM products WHERE EAN=(:EAN)", {'EAN': ean})
    result = search_cursor.fetchone()

    product_string = str(result[0]) + " " + str(result[1]) + " " + str(result[2]) + "cm x " + str(
        result[3]) + "cm x " + str(result[4]) + "cm " + str(result[5]) + "g"
    basket_listbox.insert(END, product_string)
    basket_list.append(result)

    search_database.commit()
    search_database.close()


def empty_basket():
    basket_listbox.delete(0, END)
    basket_list.clear()


def remove_one_from_basket():
    basket_list.pop(basket_listbox.curselection()[0])
    basket_listbox.delete(basket_listbox.curselection())


def show():
    bin_manager = greedypacker.BinManager(41, 38, pack_algo='shelf',
                                          heuristic='best_width_fit', wastemap=True, rotation=True)
    for item in basket_list:
        bin_manager.add_items(greedypacker.Item(item[2], item[4]))
    bin_manager.execute()

    ratio = 5

    screen_height = 38 * ratio
    screen_width = 41 * ratio * 9

    arrangement = Toplevel(root)
    arrangement.title('Arrangement')

    my_canvas = Canvas(arrangement, width=screen_width, height=screen_height, bg='white')
    my_canvas.pack(pady=5, padx=5)

    spaces = []

    for i in range(0, screen_width + 1, 41 * ratio):
        my_canvas.create_line(i, 0, i, screen_height, fill='black')
        spaces.append(i)

    def draw_rectangle(x, y, width, height, add):
        my_canvas.create_line(x + add, y, x + width + add, y)
        my_canvas.create_line(x + width + add, y, x + width + add, y + height)
        my_canvas.create_line(x + add, y + height, x + width + add, y + height)
        my_canvas.create_line(x + add, y, x + add, y + height)

    i = 0
    for BIN in bin_manager.bins:

        for shelf in BIN.shelves:

            for item in shelf.items:
                add_width = spaces[i]
                draw_rectangle(item.x * ratio, item.y * ratio, item.width * ratio, item.height * ratio, add_width)
        i += 1


################## MENU buttons ########################
# Add new product
add_new_product_button = Button(root, text="Add a new product", command=open_add_new_product_window, width=20)
add_new_product_button.grid(row=0, column=0, pady=5, padx=5)

# Show products button
show_products_button = Button(root, text="Show products", command=open_display_products_window, width=20)
show_products_button.grid(row=0, column=1, pady=5, padx=5)

# Remove from database button
remove_from_database_button = Button(root, text="Remove a product", command=open_delete_product_window, width=20)
remove_from_database_button.grid(row=0, column=2, pady=5, padx=5)

# Entry for searching the products by EAN, description label and the search button
ean_entry_label = Label(root, width=20, text="Enter products EAN:")
ean_entry_label.grid(row=1, column=0, columnspan=3, pady=5)
search_ean_entry = Entry(root, width=40)
search_ean_entry.grid(row=2, column=0, columnspan=3, pady=5)
ean_search_button = Button(root, width=10, text="Search",
                           command=lambda: search_product_ean(search_ean_entry.get()))
ean_search_button.grid(row=3, column=0, columnspan=3, pady=5)

# Basket ListBox
basket_listbox = Listbox(root)
basket_listbox.grid(row=4, column=0, sticky='news', columnspan=3, rowspan=2, pady=5, padx=5)
basket_scrollbar = Scrollbar(root, orient=VERTICAL)
basket_scrollbar.grid(row=4, column=0, columnspan=3, rowspan=2, sticky='nse', pady=5)
basket_listbox.config(yscrollcommand=basket_scrollbar.set)
basket_scrollbar.config(command=basket_listbox.yview)

# Delete an item from basket button
remove_from_basket_button = Button(root, text="Delete selected item", command=remove_one_from_basket, width=20)
remove_from_basket_button.grid(row=6, column=0, pady=5, padx=5)

# Empty basket button
empty_basket_button = Button(root, text="Empty basket", command=empty_basket, width=20)
empty_basket_button.grid(row=6, column=1, pady=5, padx=5)

# Show button
show_button = Button(root, text="Show", command=show, width=20)
show_button.grid(row=6, column=2, padx=5, pady=5)

# commit changes
database.commit()

# close connection
database.close()

root.mainloop()
