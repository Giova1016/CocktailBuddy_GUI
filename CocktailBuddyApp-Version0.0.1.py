import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import bcrypt
from PIL import Image, ImageTk

# Saving the Users database to the same file as this Python code.
dir = os.path.dirname(os.path.abspath(__file__))
users_db = os.path.join(dir, 'data\CocktailBuddyUsers.db') 

# Connect to SQLite database
conn = sqlite3.connect(users_db)
cursor = conn.cursor()

# Connect to the CocktailBuddyBeverages.db database
beverages_db = os.path.join(dir, 'data\CocktailBuddyBeverages.db')
conn_beverages = sqlite3.connect(beverages_db)
cursor_beverages = conn_beverages.cursor()

# Create users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    frozen BOOLEAN, 
                    iced BOOLEAN,
                    hot BOOLEAN,
                    mocktail BOOLEAN,
                    sparkling BOOLEAN,
                    tea_based BOOLEAN,
                    herbal BOOLEAN,
                    creamy BOOLEAN,
                    sweetness INTEGER,
                    bitterness INTEGER
                  )''')
conn.commit()

# Function to create a dropdown menu for the user settings in the preferences window
def create_settings_dropdown_preferences(menu):
    menu.add_command(label="Sign Out", command=sign_out_preferences)

# Function to create a dropdown menu for the user settings in the change preferences window
def create_settings_dropdown_change_preferences(menu):
    menu.add_command(label="View Settings", command=view_settings)
    menu.add_separator()
    menu.add_command(label="Sign Out", command=sign_out_change_preferences)

# Function to create a dropdown menu for the user settings in the suggestions window
def create_settings_dropdown_suggestions(menu):
    menu.add_command(label="View Settings", command=view_settings)
    menu.add_command(label="Change Preferences", command=change_preferences_window)
    menu.add_separator()
    menu.add_command(label="Sign Out", command=sign_out_suggestions)

# Function to view user settings
def view_settings():
    cursor.execute("SELECT * FROM users WHERE username=?", (current_user,))
    row = cursor.fetchone()
    if row:
        # Display user settings in a message box
        message = f"Username: {row[1]}\n"
        message += "Preferences:\n"
        message += f"Frozen: {'Yes' if row[3] else 'No'}\n"
        message += f"Iced: {'Yes' if row[4] else 'No'}\n"
        message += f"Hot: {'Yes' if row[5] else 'No'}\n"
        message += f"Mocktail: {'Yes' if row[6] else 'No'}\n"
        message += f"Sparkling: {'Yes' if row[7] else 'No'}\n"
        message += f"Tea-based: {'Yes' if row[8] else 'No'}\n"
        message += f"Herbal: {'Yes' if row[9] else 'No'}\n"
        message += f"Creamy: {'Yes' if row[10] else 'No'}\n"
        message += f"Sweetness: {row[11]}\n"
        message += f"Bitterness: {row[12]}\n"
        messagebox.showinfo("User Settings", message)
    else:
        messagebox.showerror("Error", "Failed to fetch user settings.")

# Back to login button in preferences window
def sign_out_preferences():
    preferences_window.destroy()
    reset_login_screen()
    root.deiconify()

# Back to login button in the changing preferences window
def sign_out_change_preferences():
    change_preference_window.destroy()
    reset_login_screen()
    root.deiconify()

# Back to login button in suggestions window
def sign_out_suggestions():
    suggestions_window.destroy()
    reset_login_screen()
    root.deiconify()

# Function to reset the login screen
def reset_login_screen():
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")

# Function to register a new user
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    messagebox.showinfo("Registration Successful", "User registered successfully!")

# Function to authenticate a user
def authenticate_user():
    username = username_entry.get()
    password = password_entry.get()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if row:
        hashed_password = row[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            global current_user 
            current_user = username
            open_preferences_window(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to open preferences window
def open_preferences_window(username):
    root.withdraw()
    global preferences_window
    preferences_window = tk.Toplevel()
    preferences_window.title("Beverage Flavor Preferences")
    preferences_window.protocol("WM_DELETE_WINDOW", sign_out_preferences)

    # Create top-right dropdown menu
    settings_menu = tk.Menu(preferences_window, tearoff=0)
    create_settings_dropdown_preferences(settings_menu)
    settings_dropdown = tk.Menu(preferences_window, tearoff=0)

    # Display the menu at the top-right corner
    settings_dropdown.post(preferences_window.winfo_width(), 0)
    username_with_arrow = username + " ▼"
    settings_dropdown.add_cascade(label=username_with_arrow, menu=settings_menu)
    preferences_window.config(menu=settings_dropdown)

    # Apply styling
    preferences_window.configure(bg="#EFE8D6")
    preferences_window.option_add("Font", "Kanit")

    # Checkboxes for drink preferences
    preferences_frame = tk.LabelFrame(preferences_window, bg="#EFE8D6", text="Beverage Preferences")
    preferences_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    frozen_var = tk.BooleanVar()
    iced_var = tk.BooleanVar()
    hot_var = tk.BooleanVar()
    mocktail_var = tk.BooleanVar()
    sparkling_var = tk.BooleanVar()
    tea_based_var = tk.BooleanVar()
    herbal_var = tk.BooleanVar()
    creamy_var = tk.BooleanVar()

    tk.Checkbutton(preferences_frame, text="Frozen", variable=frozen_var, bg="#EFE8D6").grid(row=0, column=0, sticky="w")
    tk.Checkbutton(preferences_frame, text="Iced", variable=iced_var, bg="#EFE8D6").grid(row=1, column=0, sticky="w")
    tk.Checkbutton(preferences_frame, text="Hot", variable=hot_var, bg="#EFE8D6").grid(row=2, column=0, sticky="w")
    tk.Checkbutton(preferences_frame, text="Mocktail", variable=mocktail_var, bg="#EFE8D6").grid(row=3, column=0, sticky="w")
    tk.Checkbutton(preferences_frame, text="Sparkling", variable=sparkling_var, bg="#EFE8D6").grid(row=4, column=0, sticky="w")
    tk.Checkbutton(preferences_frame, text="Tea-based", variable=tea_based_var, bg="#EFE8D6").grid(row=5, column=0, sticky="w")
    tk.Checkbutton(preferences_frame, text="Herbal", variable=herbal_var, bg="#EFE8D6").grid(row=6, column=0, sticky="w")
    tk.Checkbutton(preferences_frame, text="Creamy", variable=creamy_var, bg="#EFE8D6").grid(row=7, column=0, sticky="w")

    # Slders for sweetness and bitterness
    sliders_frame = tk.LabelFrame(preferences_window, bg="#EFE8D6", text="Sweetness and Bitterness")
    sliders_frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
    sweetness_label = tk.Label(sliders_frame, text="Sweetness:", bg="#EFE8D6")
    sweetness_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
    sweetness_slider = tk.Scale(sliders_frame, from_=1, to=10, orient="horizontal", bg="#EFE8D6")
    sweetness_slider.grid(row=0, column=1, padx=5, pady=2)
    
    bitterness_label = tk.Label(sliders_frame, text="Bitterness:", bg="#EFE8D6")
    bitterness_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
    bitterness_slider = tk.Scale(sliders_frame, from_=1, to=10, orient="horizontal", bg="#EFE8D6")
    bitterness_slider.grid(row=1, column=1, padx=5, pady=2)

    # Save preferences button
    def save_preferences():
        cursor.execute('''UPDATE users SET frozen=?, iced=?, hot=?, mocktail=?, sparkling=?, 
                          tea_based=?, herbal=?, creamy=?, sweetness=?, bitterness=? WHERE username=?''',
                       (frozen_var.get(), iced_var.get(), hot_var.get(), mocktail_var.get(),
                        sparkling_var.get(), tea_based_var.get(), herbal_var.get(), creamy_var.get(),
                        sweetness_slider.get(), bitterness_slider.get(), username))
        conn.commit()
        messagebox.showinfo("Preferences Saved", "Drink preferences saved successfully!")
        
        # Query beverage suggestions based on user preferences
        query = "SELECT * FROM beverages WHERE "
        query += "frozen = ? AND iced = ? AND hot = ? AND mocktail = ? AND sparkling = ? AND "
        query += "tea_based = ? AND herbal = ? AND creamy = ? AND sweetness = ? AND bitterness = ?"
        cursor_beverages.execute(query, (frozen_var.get(), iced_var.get(), hot_var.get(), mocktail_var.get(),
                                        sparkling_var.get(), tea_based_var.get(), herbal_var.get(), creamy_var.get(),
                                        sweetness_slider.get(), bitterness_slider.get()))
        suggestions = cursor_beverages.fetchall()

        if not suggestions:
            # If no exact match found, retrieve beverages matching 3 to 5 preferences
            query = "SELECT * FROM beverages WHERE "
            query += "(frozen + iced + hot + mocktail + sparkling + tea_based + herbal + creamy >= 3) AND "
            query += "sweetness >= ? AND bitterness <= ?"
            cursor_beverages.execute(query, (sweetness_slider.get(), bitterness_slider.get()))
            suggestions = cursor_beverages.fetchall()

        unique_suggestions = []
        seen_names = set()
        for suggestion in suggestions:
            name = suggestion[1]
            if name not in seen_names:
                unique_suggestions.append(suggestion)
                seen_names.add(name)

        preferences_window.withdraw()
        open_suggestions_window(unique_suggestions, username)
        preferences_window.destroy()    
        
    save_button = tk.Button(preferences_window, text="Save Preferences", bg="#F49090", fg="#53290A", command=save_preferences)
    save_button.grid(row=1, column=0, columnspan=2, pady=10)

    #Loading Image using PIL
    image_path = "CocktailLogo.png"
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize((128,128))
    
    tk_image = ImageTk.PhotoImage(pil_image)
    image_label = tk.Label(preferences_window, bg="#EFE8D6", image=tk_image)
    image_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    image_label.image = tk_image

    # Function to open the change preferences window
def change_preferences_window():
    suggestions_window.destroy()
    global change_preference_window
    change_preference_window = tk.Toplevel()
    change_preference_window.title("Beverage Flavor Preferences")
    change_preference_window.protocol("WM_DELETE_WINDOW", sign_out_change_preferences)

    # Create top-right dropdown menu
    settings_menu = tk.Menu(change_preference_window, tearoff=0)
    create_settings_dropdown_change_preferences(settings_menu)
    settings_dropdown = tk.Menu(change_preference_window, tearoff=0)
    username_with_arrow = current_user + " ▼"
    settings_dropdown.add_cascade(label=username_with_arrow, menu=settings_menu)
    change_preference_window.config(menu=settings_dropdown)

    # Apply styling
    change_preference_window.configure(bg="#EFE8D6")
    change_preference_window.option_add("Font", "Kanit")

    # Checkboxes for drink preferences
    change_preferences_frame = tk.LabelFrame(change_preference_window, bg="#EFE8D6", text="Beverage Preferences")
    change_preferences_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    frozen_var = tk.BooleanVar()
    iced_var = tk.BooleanVar()
    hot_var = tk.BooleanVar()
    mocktail_var = tk.BooleanVar()
    sparkling_var = tk.BooleanVar()
    tea_based_var = tk.BooleanVar()
    herbal_var = tk.BooleanVar()
    creamy_var = tk.BooleanVar()

    tk.Checkbutton(change_preferences_frame, text="Frozen", variable=frozen_var, bg="#EFE8D6").grid(row=0, column=0, sticky="w")
    tk.Checkbutton(change_preferences_frame, text="Iced", variable=iced_var, bg="#EFE8D6").grid(row=1, column=0, sticky="w")
    tk.Checkbutton(change_preferences_frame, text="Hot", variable=hot_var, bg="#EFE8D6").grid(row=2, column=0, sticky="w")
    tk.Checkbutton(change_preferences_frame, text="Mocktail", variable=mocktail_var, bg="#EFE8D6").grid(row=3, column=0, sticky="w")
    tk.Checkbutton(change_preferences_frame, text="Sparkling", variable=sparkling_var, bg="#EFE8D6").grid(row=4, column=0, sticky="w")
    tk.Checkbutton(change_preferences_frame, text="Tea-based", variable=tea_based_var, bg="#EFE8D6").grid(row=5, column=0, sticky="w")
    tk.Checkbutton(change_preferences_frame, text="Herbal", variable=herbal_var, bg="#EFE8D6").grid(row=6, column=0, sticky="w")
    tk.Checkbutton(change_preferences_frame, text="Creamy", variable=creamy_var, bg="#EFE8D6").grid(row=7, column=0, sticky="w")

    # Slders for sweetness and bitterness
    sliders_frame = tk.LabelFrame(change_preference_window, bg="#EFE8D6", text="Sweetness and Bitterness")
    sliders_frame.grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
    sweetness_label = tk.Label(sliders_frame, text="Sweetness:", bg="#EFE8D6")
    sweetness_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
    sweetness_slider = tk.Scale(sliders_frame, from_=1, to=10, orient="horizontal", bg="#EFE8D6")
    sweetness_slider.grid(row=0, column=1, padx=5, pady=2)
    
    bitterness_label = tk.Label(sliders_frame, text="Bitterness:", bg="#EFE8D6")
    bitterness_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
    bitterness_slider = tk.Scale(sliders_frame, from_=1, to=10, orient="horizontal", bg="#EFE8D6")
    bitterness_slider.grid(row=1, column=1, padx=5, pady=2)

    # Change preferences button
    def change_preferences():
        cursor.execute('''UPDATE users SET frozen=?, iced=?, hot=?, mocktail=?, sparkling=?, 
                          tea_based=?, herbal=?, creamy=?, sweetness=?, bitterness=? WHERE username=?''',
                       (frozen_var.get(), iced_var.get(), hot_var.get(), mocktail_var.get(),
                        sparkling_var.get(), tea_based_var.get(), herbal_var.get(), creamy_var.get(),
                        sweetness_slider.get(), bitterness_slider.get(), current_user))
        conn.commit()
        messagebox.showinfo("Preferences Changed", "Drink preferences saved successfully!")
        
        # Query beverage suggestions based on user preferences
        query = "SELECT * FROM beverages WHERE "
        query += "frozen = ? AND iced = ? AND hot = ? AND mocktail = ? AND sparkling = ? AND "
        query += "tea_based = ? AND herbal = ? AND creamy = ? AND sweetness = ? AND bitterness = ?"
        cursor_beverages.execute(query, (frozen_var.get(), iced_var.get(), hot_var.get(), mocktail_var.get(),
                                        sparkling_var.get(), tea_based_var.get(), herbal_var.get(), creamy_var.get(),
                                        sweetness_slider.get(), bitterness_slider.get()))
        suggestions = cursor_beverages.fetchall()

        if not suggestions:
            # If no exact match found, retrieve beverages matching 3 to 5 preferences
            query = "SELECT * FROM beverages WHERE "
            query += "(frozen + iced + hot + mocktail + sparkling + tea_based + herbal + creamy >= 3) AND "
            query += "sweetness >= ? AND bitterness <= ?"
            cursor_beverages.execute(query, (sweetness_slider.get(), bitterness_slider.get()))
            suggestions = cursor_beverages.fetchall()

        unique_suggestions = []
        seen_names = set()
        for suggestion in suggestions:
            name = suggestion[1]
            if name not in seen_names:
                unique_suggestions.append(suggestion)
                seen_names.add(name)

        change_preference_window.withdraw()
        open_suggestions_window(unique_suggestions, current_user)
        change_preference_window.destroy()      
        
    save_button = tk.Button(change_preference_window, text="Change Preferences", bg="#F49090", fg="#53290A", command=change_preferences)
    save_button.grid(row=1, column=0, columnspan=2, pady=10)

    #Loading Image using PIL
    image_path = "CocktailLogo.png"
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize((128,128))
    
    tk_image = ImageTk.PhotoImage(pil_image)
    image_label = tk.Label(change_preference_window, bg="#EFE8D6", image=tk_image)
    image_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    image_label.image = tk_image

# Function to open the suggestions window
def open_suggestions_window(suggestions, username):
    # Create a new window for beverage Suggestions
    global suggestions_window
    suggestions_window  = tk.Toplevel()
    suggestions_window .title("Beverage Suggestions")
    suggestions_window.protocol("WM_DELETE_WINDOW", sign_out_suggestions)

    # Create top-right dropdown menu for settings
    settings_menu = tk.Menu(suggestions_window, tearoff=0)
    create_settings_dropdown_suggestions(settings_menu)
    settings_dropdown = tk.Menu(suggestions_window, tearoff=0)

    # Display the menu at the top-right corner
    username_with_arrow = username + " ▼"
    settings_dropdown.add_cascade(label=username_with_arrow, menu=settings_menu)
    suggestions_window.config(menu=settings_dropdown)

    # Apply Styling
    suggestions_window.configure(bg="#EFE8D6") # Set the background color to cream
    suggestions_window.option_add("Font", "Kanit") # Set the font of the text to Kanit

    # Load and display the logo
    logo_path = "CocktailLogo.png"
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((128, 128))
    tk_logo_image = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(suggestions_window , bg="#EFE8D6", image=tk_logo_image)
    logo_label.grid(row=0, column=0, padx=10, pady=10)
    logo_label.image = tk_logo_image

    # Add labels for displaying saved preferences
    preferences_label = tk.Label(suggestions_window , text="Beverages of your preference:", bg="#EFE8D6", fg="#53290A")
    preferences_label.grid(row=0, column=1, padx=10, pady=10)

    # Create a frame for displaying suggestions with scrollbar
    suggestions_frame = tk.Frame(suggestions_window, background="#EFE8D6")
    suggestions_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Create a canvas inside the frame
    canvas = tk.Canvas(suggestions_frame, bg="#EFE8D6")
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(suggestions_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create another frame inside the canvas
    inner_frame = tk.Frame(canvas, bg="#EFE8D6")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Display beverage suggestions
    for idx, suggestion in enumerate(suggestions):
        label = tk.Label(inner_frame, text=f"{idx + 1}. {suggestion[1]}", bg="#EFE8D6", fg="#53290A")  # Assuming the name of the beverage is in the second column
        label.grid(row= idx, column=0, pady=5)
        
# Create main window
root = tk.Tk()
root.title("User Authentication")

# Apply Styling
root.configure(bg="#EFE8D6") # Set the background color to cream
root.option_add("Font", "Kanit") # Set the font of the text to Kanit

#Loading Image using PIL
image_path = "CocktailLogo.png"
pil_image = Image.open(image_path)
pil_image = pil_image.resize((128,128))

tk_image = ImageTk.PhotoImage(pil_image)
image_label = tk.Label(root, bg="#EFE8D6", image=tk_image)
image_label.grid(row=0, column=0, columnspan=7, padx=5, pady=5)
image_label.image = tk_image

# Version text below the logo n the login page
version_label = tk.Label(root, text="Version 0.0.1", bg="#EFE8D6", fg="#53290A", font=("Kanit", 8))
version_label.grid(row=0, column=1, columnspan=7, padx=5, pady=(0, 20))

# Create username label and entry
username_label = tk.Label(root, text="Username:", bg="#EFE8D6")
username_label.grid(row=0, column=0, padx=(80, 10), pady=(200, 5), sticky=tk.W)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=(0, 10), pady=(200, 5))

# Create password label and entry
password_label = tk.Label(root, text="Password:", bg="#EFE8D6")
password_label.grid(row=1, column=0, padx=(80, 10), pady=5, sticky=tk.W)
password_entry = tk.Entry(root, show="*") # Masking the password
password_entry.grid(row=1, column=1, padx=(0, 10), pady=5)

# Create register button
register_button = tk.Button(root, text="Register", bg="#BDE09E", fg="#53290A", command=register_user)
register_button.grid(row=2, column=0, padx=(80, 10), pady=5)

# Create login button
login_button = tk.Button(root, text="Login", bg="#F49090", fg="#53290A", command=authenticate_user)
login_button.grid(row=2, column=1, padx=(0, 10), pady=5)

# Set the dimensions to be similar to mobile devices
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width // 2) - (320 // 2)  # Half screen width - half window width
y_coordinate = (screen_height // 2) - (480 // 2)  # Half screen height - half window height
root.geometry("320x480+{}+{}".format(x_coordinate, y_coordinate))

# Run the application
root.mainloop()

# Close database connection
conn.close()
