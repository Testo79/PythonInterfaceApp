import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox

# Create a SQLite database and table
conn = sqlite3.connect('result.db')
c = conn.cursor()
c.execute(
    'CREATE TABLE IF NOT EXISTS results (cargison TEXT, date TEXT, humidity REAL, ashes REAL, sulfur REAL, volatile_matter REAL, calorific_value REAL, granulometry TEXT, friability REAL, hydrogen REAL, nitrogen REAL, carbon REAL, oxygen REAL, fixed_carbon REAL, chlorine REAL, acceptance TEXT)')

conn.commit()

# Declare global variables for entry fields
entry_cargison =None
entry_humidity = None
entry_ashes = None
entry_sulfur = None
entry_volatile_matter = None
entry_calorific_value = None
entry_granulometry = None
entry_friability = None
entry_hydrogen = None
entry_nitrogen = None
entry_carbon = None
entry_oxygen = None
entry_fixed_carbon = None
entry_chlorine = None

# Function to check conditions and add to the database
def add_to_database():
    entry_values = [
        entry_cargison.get(), float(entry_humidity.get()), float(entry_ashes.get()), float(entry_sulfur.get()),
        float(entry_volatile_matter.get()), float(entry_calorific_value.get()), entry_granulometry.get(),
        float(entry_friability.get()), float(entry_hydrogen.get()), float(entry_nitrogen.get()),
        float(entry_carbon.get()), float(entry_oxygen.get()), float(entry_fixed_carbon.get()),
        float(entry_chlorine.get())
    ]


    # Perform your conditions checking
    condition_met = (
            4 <= entry_values[1] <= 13 and
            9 <= entry_values[2] <= 20 and
            0.5 <= entry_values[3] <= 1.5 and
            22 <= entry_values[4] <= 40 and
            5600 <= entry_values[5] <= 7000 and
            entry_values[6] == 0 and
            40 <= entry_values[7] <= 70 and
            3.2 <= entry_values[8] <= 6 and
            0 <= entry_values[9] <= 2 and
            50 <= entry_values[10] <= 80 and
            3 <= entry_values[11] <= 9.5 and
            entry_values[12] == 40 and
            0 <= entry_values[13] <= 0.2
    )

    if condition_met:
        entry_values.append("accepted")
    else:
        entry_values.append("not accepted")
    print(entry_values)
    c.execute('INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', entry_values)
    conn.commit()

    messagebox.showinfo('Success', 'Entry added to database.')
    update_database_display()


# Function to update the database display
def update_database_display():
    # Clear existing entries
    for row in database_tree.get_children():
        database_tree.delete(row)

    c.execute('SELECT rowid, * FROM results')
    results = c.fetchall()
    for result in results:
        database_tree.insert('', 'end', values=result)

# Function to delete a selected entry
def delete_entry():
    selected_item = database_tree.selection()
    if selected_item:
        selected_row_id = database_tree.item(selected_item, 'values')[0]
        c.execute('DELETE FROM results WHERE rowid=?', (selected_row_id,))
        conn.commit()
        update_database_display()


# Create the main window
root = tk.Tk()
root.title('Data Entry App')
root.geometry('1200x800')

# Create and place entry fields vertically on the left
entry_frame = tk.Frame(root, padx=20, pady=20)
entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create labels and entry fields


field_labels = ["cargison:", "Humidity:", "Ashes:", "Sulfur:", "Volatile Matter:", "Calorific Value:", "Granulometry:",
                "Friability:", "Hydrogen:", "Nitrogen:", "Carbon:", "Oxygen:", "Fixed Carbon:", "Chlorine:"]
entry_fields = []
for label_text in field_labels:
    label = tk.Label(entry_frame, text=label_text)
    label.pack(anchor='w', padx=10)
    entry = tk.Entry(entry_frame)
    entry.pack(fill=tk.X, padx=10)
    entry_fields.append(entry)

    # Assign entry fields to global variables
    if label_text == "cargison:":
        entry_cargison = entry
    if label_text == "Humidity:":
        entry_humidity = entry
    elif label_text == "Ashes:":
        entry_ashes = entry
    elif label_text == "Sulfur:":
        entry_sulfur = entry
    elif label_text == "Volatile Matter:":
        entry_volatile_matter = entry
    elif label_text == "Calorific Value:":
        entry_calorific_value = entry
    elif label_text == "Granulometry:":
        entry_granulometry = entry
    elif label_text == "Friability:":
        entry_friability = entry
    elif label_text == "Hydrogen:":
        entry_hydrogen = entry
    elif label_text == "Nitrogen:":
        entry_nitrogen = entry
    elif label_text == "Carbon:":
        entry_carbon = entry
    elif label_text == "Oxygen:":
        entry_oxygen = entry
    elif label_text == "Fixed Carbon:":
        entry_fixed_carbon = entry
    elif label_text == "Chlorine:":
        entry_chlorine = entry

# Create and place buttons to add and delete entries
add_button = tk.Button(root, text='Add to Database', command=add_to_database)
add_button.pack()

delete_button = tk.Button(root, text='Delete Selected', command=delete_entry)
delete_button.pack()
database_frame = tk.Frame(root)
database_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

database_label = tk.Label(database_frame, text='Database (Results):')
database_label.pack()

# Create and place a treeview widget for the database content
database_tree = ttk.Treeview(database_frame, columns=['rowid', 'cargison', 'humidity', 'ashes', 'sulfur', 'volatile_matter', 'calorific_value', 'granulometry', 'friability', 'hydrogen', 'nitrogen', 'carbon', 'oxygen', 'fixed_carbon', 'chlorine', 'acceptance'])
database_scrollbar = ttk.Scrollbar(database_frame, orient='vertical', command=database_tree.yview)
database_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
database_tree.configure(yscrollcommand=database_scrollbar.set)

database_scrollbar_x = ttk.Scrollbar(database_frame, orient='horizontal', command=database_tree.xview)
database_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
database_tree.configure(xscrollcommand=database_scrollbar_x.set)#wa zbi hhhh
database_tree.heading('#0', text='Row ID')
database_tree.heading('cargison', text='Cargison')
database_tree.heading('humidity', text='Humidity')
database_tree.heading('ashes', text='Ashes')
database_tree.heading('sulfur', text='Sulfur')
database_tree.heading('volatile_matter', text='Volatile Matter')
database_tree.heading('calorific_value', text='Calorific Value')
database_tree.heading('granulometry', text='Granulometry')
database_tree.heading('friability', text='Friability')
database_tree.heading('hydrogen', text='Hydrogen')
database_tree.heading('nitrogen', text='Nitrogen')
database_tree.heading('carbon', text='Carbon')
database_tree.heading('oxygen', text='Oxygen')
database_tree.heading('fixed_carbon', text='Fixed Carbon')
database_tree.heading('chlorine', text='Chlorine')
database_tree.heading('acceptance', text='Acceptance')
database_tree.pack(fill=tk.BOTH, expand=True)

# Bind selection event to a function
def on_item_select(event):
    selected_item = database_tree.selection()
    if selected_item:
        selected_row_id = database_tree.item(selected_item, 'values')[0]
        print("Selected Row ID:", selected_row_id)  # Replace with your logic for editing or deleting

database_tree.bind('<<TreeviewSelect>>', on_item_select)

# Create and place a button to refresh the database display
refresh_button = tk.Button(database_frame, text='Refresh Database', command=update_database_display)
refresh_button.pack()
# Create and place a label for the database section on the right
database_frame = tk.Frame(root)
database_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

database_label = tk.Label(database_frame, text='Database (Results):')
database_label.pack()

# Create and place a text widget to display the database content
database_text = tk.Text(database_frame)
database_text.pack(fill=tk.BOTH, expand=True)

# Create and place a button to refresh the database display
refresh_button = tk.Button(database_frame, text='Refresh Database', command=update_database_display)
refresh_button.pack()

update_database_display()



# Start the GUI event loop
root.mainloop()

# Close the database connection when the GUI is closed
conn.close()
