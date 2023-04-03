import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

candidates = ["Alice", "Bob", "Charlie", "David", "Emily"]
votes = {candidate: 0 for candidate in candidates}
voters = set()

voter_pins = {"Adam": "1234", "Beth": "5678", "Cindy": "9012", "Dave": "3456", "Eve": "7890",
              "Frank": "1235", "Grace": "5679", "Henry": "9013", "Ivy": "3457", "Jack": "7891"}

# Define the file name for storing the vote data
VOTE_FILE = "C:/Users/Danom/Documents/ICT Opleiding/Vakken/Script/Voting System/voters.txt"

# Load the vote data from the file if it exists
try:
    with open(VOTE_FILE, "r") as file:
        votes = {line.split(":")[0]: int(line.split(":")[1]) for line in file}
    print("Vote data loaded successfully.")
except FileNotFoundError:
    print("Vote file not found, starting with empty vote data.")
    pass

# Initialize the vote count for all candidates to zero
for candidate in candidates:
    if candidate not in votes:
        votes[candidate] = 0

# Create the main window and title
window = tk.Tk()
window.title("Voting System")

# Use the ttk "vista" theme for a modern and professional look
style = ttk.Style(window)
style.theme_use("vista")

# Define custom styles for the UI elements
style.configure("Header.TLabel", font=("Arial", 20, "bold"))
style.configure("Subheader.TLabel", font=("Arial", 14, "bold"))
style.configure("PrimaryButton.TButton", font=("Arial", 12, "bold"), background="#4CAF50", foreground="black", padding=10)
style.map("PrimaryButton.TButton", background=[("active", "#43A047")])
style.configure("SecondaryButton.TButton", font=("Arial", 12, "bold"), background="#E0E0E0", foreground="black", padding=10)
style.map("SecondaryButton.TButton", background=[("active", "#BDBDBD")])
style.configure("Error.TLabel", font=("Arial", 12), foreground="red")

# Create the UI elements
header_label = ttk.Label(window, text="Welcome to the Voting System", style="Header.TLabel")
name_label = ttk.Label(window, text="Your name:", style="Subheader.TLabel")
name_entry = ttk.Entry(window)
pin_label = ttk.Label(window, text="Your PIN:", style="Subheader.TLabel")
pin_entry = ttk.Entry(window, show="*")
candidate_label = ttk.Label(window, text="Choose a candidate:", style="Subheader.TLabel")
candidate_combobox = ttk.Combobox(window, values=candidates)
vote_button = ttk.Button(window, text="Vote", style="PrimaryButton.TButton")
results_button = ttk.Button(window, text="Results", style="SecondaryButton.TButton")

# Define the layout of the UI elements using the grid layout manager
header_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
name_label.grid(row=1, column=0, padx=20, pady=10, sticky="W")
name_entry.grid(row=1, column=1, padx=20, pady=10)
pin_label.grid(row=2, column=0, padx=20, pady=10, sticky="W")
pin_entry.grid(row=2, column=1, padx=20, pady=10)
candidate_label.grid(row=3, column=0, padx=20, pady=10, sticky="W")
candidate_combobox.grid(row=3, column=1, padx=20, pady=10)
vote_button.grid(row=4, column=0, padx=20, pady=10)
results_button.grid(row=4, column=1, padx=20, pady=10)

# Define a function to validate the voter's PIN
def validate_pin():
    pin = pin_entry.get()

    # Check if the pin is valid
    if len(pin) == 4 and pin.isdigit():
        return True
    else:
        messagebox.showerror("Error", "Invalid PIN")
        return False

    # Here is where you can add additional code to execute
    # after the if-else block, indented properly
    name = name_entry.get()
    print(name)

# Define a function to handle the vote button click event
def vote():
    name = name_entry.get()
    pin = pin_entry.get()
    candidate = candidate_combobox.get()

    # Check if the name and PIN are valid
    if name not in voter_pins or voter_pins[name] != pin:
        messagebox.showerror("Error", "Invalid name or PIN.")
        return

    # Check if the voter has already voted
    if name in voters:
        messagebox.showerror("Error", "You have already voted.")
        return

    # Record the vote and update the UI
    votes[candidate] += 1
    voters.add(name)
    messagebox.showinfo("Success", "Your vote for {} has been recorded.".format(candidate))

    # Save the vote data to the file
    with open(VOTE_FILE, "w") as file:
        for candidate, count in votes.items():
            file.write("{}:{}\n".format(candidate, count))


# Define a function to add a password to the Results button
def check_password():
    password = "mypassword"

    # Create a new toplevel window for the password input
    password_window = tk.Toplevel(window)
    password_window.title("Enter Password")

    # Create the UI elements for the password window
    password_label = ttk.Label(password_window, text="Please enter the password to view the results:",
                               font=("Arial", 12))
    password_entry = ttk.Entry(password_window, show="*")
    submit_button = ttk.Button(password_window, text="Submit", command=lambda: verify_password(password_entry.get()))

    # Define the layout of the UI elements using the grid layout manager
    password_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
    password_entry.grid(row=1, column=0, padx=10, pady=10)
    submit_button.grid(row=2, column=0, padx=10, pady=10)

    # Define a function to verify the password
    def verify_password(input_password):
        nonlocal password_window
        if input_password == password:
            password_window.destroy()
            show_results()
        else:
            messagebox.showerror("Error", "Invalid password.")
            password_entry.delete(0, tk.END) # clear the password entry field


# Define a function to show the results
def show_results():
    # Create a new toplevel window for the results
    results_window = tk.Toplevel(window)
    results_window.title("Results")

    # Create the UI elements for the results window
    results_label = ttk.Label(results_window, text="Results:", font=("Arial", 12))
    results_text = tk.Text(results_window, width=30, height=10)
    results_text.insert(tk.END, "Candidate\tVotes\n")
    results_text.insert(tk.END, "-" * 20 + "\n")
    for candidate, count in votes.items():
        results_text.insert(tk.END, "{}\t{}\n".format(candidate, count))
    results_text.config(state=tk.DISABLED)

    # Define the layout of the UI elements using the grid layout manager
    results_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
    results_text.grid(row=1, column=0, padx=10, pady=10)

# Define a function to handle the results button click event
def results():
    result_text = ""
    for candidate, count in votes.items():
        result_text += f"{candidate}: {count} vote(s)\n"
    messagebox.showinfo("Results", result_text)

# Attach the functions to the button click events
vote_button.configure(command=vote)
results_button.configure(command=results)

# Start the main event loop
window.mainloop()