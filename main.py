"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                CStats Main File                                  ║
║                                                                                  ║
║ This is the main file for the CStats application, a cryptocurrency tracking app. ║
║ It pulls cryptocurrency data from an API, processes it, and displays it in a     ║
║ user-friendly GUI using the customtkinter library. Key features include:         ║
║                                                                                  ║
║ - API data pull with a rate limit (max once every 2 hours).                      ║
║ - A table that lists cryptocurrencies with their name, price, percent changes,   ║
║   and market capitalization.                                                     ║
║ - An interactive UI that allows users to view more details about any listed coin.║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""


import os                                    # imports os
import json                                  # imports json
from PIL import Image                        # imports PIL (image) to be able to open images
from formating import *                      # imports the formating functions
from customtkinter import *                  # imports customtkinter to display data more visually
from CTkTable import CTkTable                # imports CTKTable to display table more visually
from functools import partial                # imports functools (partial)
from time_stamp import read_timestamp        # imports the read_timestamp function to read a last pulled time
from api_request import pull_from_api        # imports the pull_from_api
from datetime import datetime, timedelta     # imports datetime to save the time last pulled from api (due to limits of pulls)


# Global variables
global name_and_price_metric, total_spuply_metric, _24_hour_change_metric, metrics_frame
global table_frame, table


def update_data(file_path: str) -> None:
    """
    Reads cryptocurrency data from a JSON file, processes it, and updates the UI 
    table with the latest information.
    
    file_path (str): The file path to the JSON file containing cryptocurrency data.
    """
    # Initialize the table with the header row
    table_data = [["#", "Name", "Price(USD)", "1h %", "24h %", "MKT. Cap"]]

    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            info_dict = json.load(file)

            # Process the data if the 'data' key is found in the JSON file
            if "data" in info_dict.keys():
                table_data = process_crypto_data(info_dict["data"], table_data)

    # Update the UI with the new data
    update_table_ui(table_data)


def update_table_ui(table_data: list) -> None:
    """
    Updates the table UI by destroying the old table and creating a new one 
    with the updated data.

    Parameters:
    table_data (list): The updated table data.
    """
    global table

    # Destroy the old table UI element
    table.destroy()

    # Create a new table with the updated data
    table = CTkTable(
        master=table_frame,
        border_width=7,
        command=lambda row: print_row(row, table_data),
        border_color="#2c2c91",
        values=table_data,
        colors=["#484ab8", "#5a5de6"],
        header_color="#2c2c91",
        hover_color="#B4B4B4",
        corner_radius=10
    )

    # Style the header row
    table.edit_row(0, text_color="#fff", font=("Arial Bold", 15), hover_color="#2c2c91")

    # Apply styles to all rows except the first (header) row
    for row_index in range(1, len(table_data)):
        table.edit_row(
            row_index,
            text_color="#fff",
            font=("Arial Bold", 12),
            hover_color="#d37fcc"
        )

    # Pack the table into the window
    table.pack(expand=True)


def print_row(row: dict, table_data: list) -> None:
    """
    Retrieves the data of the selected row from the table and updates the 
    displayed cryptocurrency information at the top boxes of tkinter window.

    row (dict): A dictionary containing the selected row's information, with 
    the key "row" representing the row number.
    
    table_data (list): A list of all row data, where each row is a list of 
    cryptocurrency information.
    """
    # Get the row number from the 'row' dictionary, ensuring it's at least 1
    row_num = row["row"]
    row_num = max(1, row_num)  # Ensure row number is not less than 1

    # Retrieve the data for the specified row from the table_data
    row_data = table_data[row_num]

    # Update the displayed information using the row data
    update_crypto_info(row_data)
    

def update_crypto_info(row_data: list[str]) -> None:
    """
    Updates the displayed cryptocurrency information based on the selected row 
    data at the top boxes of the tkinter screen.

    row_data (list): A list containing cryptocurrency data such as rank, name, price, 
    hourly and daily changes, market cap, short name, and total supply.
    """
    # Clear old content from the metric frames
    clear_frame(name_and_price_metric)
    clear_frame(total_spuply_metric)
    clear_frame(_24_hour_change_metric)

    # Unpack the row data
    rank, name, price, hour_change, day_change, market_cap, short_name, total_supply = row_data

    # Update the 'name_and_price_metric' frame with cryptocurrency name, symbol, and price
    CTkLabel(master=name_and_price_metric, text=f"{name}", text_color="#fff", font=("Arial Bold", 17))\
        .grid(row=0, column=0, rowspan=2, padx=(5, 10), pady=10)
    CTkLabel(master=name_and_price_metric, text=f"{short_name}", text_color="gray", font=("Arial Bold", 12))\
        .grid(row=0, column=1, pady=2, sticky="sw")
    CTkLabel(master=name_and_price_metric, text=f"{price}", text_color="pink", font=("Arial Bold", 19), justify="left")\
        .grid(row=2, column=0, padx=(5, 5), sticky="nw", pady=(0, 10))

    # Update the 'total_spuply_metric' frame with the total supply of the cryptocurrency
    CTkLabel(master=total_spuply_metric, text="Total Supply:", text_color="#fff", font=("Arial Bold", 17))\
        .grid(row=0, column=0, rowspan=2, padx=(5, 200), pady=10)
    CTkLabel(master=total_spuply_metric, text=f"{total_supply}", text_color="pink", font=("Arial Bold", 16), justify="left")\
        .grid(row=2, column=0, padx=(5, 5), sticky="nw", pady=(0, 10))

    # Update the '_24_hour_change_metric' frame with the 24-hour percentage change title
    CTkLabel(master=_24_hour_change_metric, text="24H % Change", text_color="#fff", font=("Arial Bold", 17))\
        .grid(row=0, column=0, rowspan=2, padx=(5, 200), pady=10)

    # Determine color based on whether the change is positive (green) or negative (red)
    color = "#01ff85" if day_change[0] == "▲" else "#ff7a7a"
    
    # Display the 24-hour change with the appropriate color
    CTkLabel(master=_24_hour_change_metric, text=f"{day_change}", text_color=color, font=("Arial Bold", 16), justify="left")\
        .grid(row=2, column=0, padx=(5, 5), sticky="nw", pady=(0, 10))

    # Further updates (e.g., for hour_change and market_cap) can be added here if needed.


def check_last_pulled_and_pull(file_path: str, active_message: list[str]) -> None:
    """
    Checks the timestamp of the last API pull and determines whether to pull new data or not.
    
    file_path (str): The file path where the data will be saved.
    active_message (list[str]): A list where the first element indicates the status 
    (0 for success, 1 for error), and the second element holds the status message.
    """

    last_pull_time = read_timestamp()       # Retrieve the last time data was pulled
    time_now = datetime.now()               # Get the current time

    # If no last pull time exists, pull new data and then update_data gets called in main
    if last_pull_time == None:
        pull_from_api(file_path, active_message)        # Pull data from the API
        print(active_message)                           # Output the result message
        return
    
    # Convert the last pull time to a datetime object
    last_pull_time = datetime.fromisoformat(last_pull_time)

    # Check if enough time has passed since the last pull (2 hours NOTE you can change but be 
    # careful if you are a free user of the coinMarketCap API)
    if (time_now - last_pull_time) >= timedelta(hours=2):
        pull_from_api(file_path, active_message)     # Pull new data from the API
        
        # If pull is successful, update the data
        if active_message[0] == 0:
            update_data(file_path)                  # Update the table or UI with the new data
    else:
        # Not enough time has passed since the last pull
        active_message[0] = 4
        active_message[1] = "API Hourly Pull Exceeded - Try Again Later"
    
    # Print the final message (a list [errorCode, Message])
    print(active_message)


def create_sidebar(app: CTk) -> None:
    """
    Creates a visually appealing sidebar for the given app, including buttons for Dashboard, 
    Settings, and Account, along with the app logo at the top.
    
    Each button includes an icon, has a hover effect, and is aligned in the sidebar 
    for a clean UI.

    app (object): The main app window where the sidebar will be attached.
    """
    # Create the sidebar frame with specified color, dimensions, and corner radius
    sidebar_frame = CTkFrame(master=app, fg_color="#2c2c91",  width=176, height=650, corner_radius=0)
    # Prevent the frame from automatically resizing based on its contents
    sidebar_frame.pack_propagate(0)
    # Pack the frame to the left side of the window, filling vertically
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    # Load the app logo from assets and set it in the sidebar
    logo_img_data = Image.open(os.path.join("assets", "cStats.png"))
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(95, 95.42))
    # Display the logo image in the sidebar with padding from the top
    CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    analytics_img_data = Image.open(os.path.join("assets", "analytics_icon.png"))
    # Load the dashboard (analytics) icon from assets
    package_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)
    # Create a button for the Dashboard with the icon and styling
    CTkButton(master=sidebar_frame,image=package_img, text="Dashboard", corner_radius=10, 
        fg_color="#5a5de6", font=("Arial Bold", 15), text_color="#fff", 
        hover_color="#d37fcc", anchor="w"
    ).pack(anchor="center", ipady=5, pady=(60, 0))

    # Load the settings icon from assets
    settings_img_data = Image.open(os.path.join("assets", "settings_icon.png"))
    settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
    # Create a button for Settings with the icon and transparent background
    CTkButton(master=sidebar_frame, image=settings_img, corner_radius=10, text="Settings", 
        fg_color="transparent", font=("Arial Bold", 15), hover_color="#d37fcc", 
        anchor="w"
    ).pack(anchor="center", ipady=5, pady=(16, 0))

    # Load the person_icon from assets
    person_img_data = Image.open(os.path.join("assets", "person_icon.png"))
    person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
    # Create a button with Acount icon and transparent background
    CTkButton(master=sidebar_frame, image=person_img, text="Account", corner_radius=10, 
        fg_color="transparent", font=("Arial Bold", 15), hover_color="#d37fcc", 
        anchor="w"
    ).pack(anchor="center", ipady=5, pady=(16, 0))


def create_main_view(app: CTk) -> CTkFrame:
    """
    Creates the main view of the application, including a title frame with a label
    and a button to reload data.

    app (object): The main application window where the main view will be attached.
    
    Returns:
    main_view (CTkFrame): The main view frame for the application.
    """
    # Create the main view frame with specified color, dimensions, and corner radius
    main_view = CTkFrame(master=app, fg_color="#242a40",  width=680, height=650, corner_radius=0)
    # Prevent the frame from resizing based on its content
    main_view.pack_propagate(0)
    # Pack the main view to the left side of the window
    main_view.pack(side="left")

    # Create the title frame inside the main view
    title_frame = CTkFrame(master=main_view, fg_color="transparent")
    # Pack the title frame at the top (north) with padding and full width
    title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))
    # Add a label to the title frame displaying "Analytics Table"
    CTkLabel(master=title_frame, text="Analytics Table", font=("Arial Black", 25), 
        text_color="#fff"
    ).pack(anchor="nw", side="left")

    # Load the reload (update) button image from the assets folder
    reload_img_data = Image.open(os.path.join("assets", "returns_icon.png"))
    reload_img = CTkImage(dark_image=reload_img_data, light_image=reload_img_data)
    # Create the "Update Data" button with the image, styling, and a command to update data
    CTkButton(master=title_frame, image=reload_img, text="Update Data", corner_radius=10, 
        font=("Arial Bold", 15), text_color="#fff", fg_color="#2c2c91", 
        hover_color="#d37fcc", 
        command=partial(check_last_pulled_and_pull, 'crypto_data.json', [0, ''])
    ).pack(anchor="ne", side="right", ipady=5)

    return main_view


def create_metrics_view(main_view: CTkFrame) -> None:
    """
    Creates the metrics view section, consisting of three frames for displaying
    metrics: name and price, total supply, and 24-hour change.
    
    main_view (CTkFrame): The main view frame where the metrics view will be placed.
    """
    # Declare global variables for the metric frames
    global name_and_price_metric, total_spuply_metric, _24_hour_change_metric
    
    # Create the main metrics frame inside the main view
    metrics_frame = CTkFrame(master=main_view, fg_color="transparent")
    metrics_frame.pack(anchor="n", fill="x",  padx=27, pady=(36, 0))

    # Name and Price Metric Frame
    name_and_price_metric = CTkFrame(master=metrics_frame, corner_radius=10, border_width=0, 
        fg_color="#2c2c91", border_color="#7a7ded", 
    width=200, height=80)
    # Prevent the frame from resizing based on its contents
    name_and_price_metric.grid_propagate(0)
    name_and_price_metric.pack(side="left")
    # Label for Name and Price metric
    CTkLabel(master=name_and_price_metric, text="Click on a coin to start", text_color="pink", 
        font=("Arial Bold", 13), justify="center"
    ).grid(padx= (20, 25), pady=25, sticky="sw")
    
    # Total Supply Metric Frame
    total_spuply_metric = CTkFrame(master=metrics_frame, corner_radius=10, border_width=0, 
        fg_color="#2c2c91", border_color="#7a7ded", width=200, 
    height=80)
    # Prevent the frame from resizing based on its contents
    total_spuply_metric.grid_propagate(0)
    total_spuply_metric.pack(side="left", expand=True, anchor="center")
    # Label for Total Supply metric
    CTkLabel(master=total_spuply_metric, text="______________________", text_color="pink", 
        font=("Arial Bold", 13), justify="center").grid(padx= (20, 25), 
    pady=25, sticky="sw")

    # 24-Hour Change Metric Frame
    _24_hour_change_metric = CTkFrame(master=metrics_frame, corner_radius=10, border_width=0, 
        fg_color="#2c2c91", border_color="#7a7ded", 
    width=200, height=80)
    # Prevent the frame from resizing based on its contents
    _24_hour_change_metric.grid_propagate(0)
    _24_hour_change_metric.pack(side="right")
    # Label for 24-Hour Change metric
    CTkLabel(master=_24_hour_change_metric, text="______________________", text_color="pink", 
        font=("Arial Bold", 13), justify="center"
    ).grid(padx= (20, 25), pady=25, sticky="sw")


def create_table_view(main_view: CTkFrame, table_data: list) -> None:
    """
    Creates a table view inside the main view using the provided table data.
    
    main_view (CTkFrame): The main view frame where the table view will be placed.
    table_data (list): The data to be displayed in the table.
    """
    # Declare global variables for the table frame and the table widget
    global table_frame, table
    
    # Create a scrollable frame to hold the table
    table_frame = CTkScrollableFrame(master=main_view, corner_radius=10, border_width=0, 
        fg_color="transparent", scrollbar_fg_color="transparent", 
        scrollbar_button_color='#2c2c91', scrollbar_button_hover_color='#5d68a8', 
    border_color="#7a7ded")
    # Pack the scrollable frame with padding and set it to expand and fill the space
    table_frame.pack(expand=True, fill="both", padx=15, pady=21)
    
    # Create the table widget with data and custom colors
    table = CTkTable(master=table_frame, border_width=7, border_color="#2c2c91", 
        values=table_data, colors=["#484ab8", "#5a5de6"], header_color="#2c2c91", 
    hover_color="#B4B4B4", corner_radius=10)
    # Customize the appearance of the first row (header row)
    table.edit_row(0, text_color="#fff", font=("Arial Bold", 15), hover_color="#2c2c91")
    # Customize the remaining rows with different font sizes and hover effects
    for row_index in range(1, len(table_data)):
        table.edit_row(row_index, text_color="#fff", font=("Arial Bold", 12), hover_color="#d37fcc")
    
    # Pack the table to expand and fill the available space
    table.pack(expand=True)


def main():
    """
    Main function to initialize and run the crypto dashboard application.
    It sets up the app window, creates the sidebar, main view, metrics view,
    and table view, then pulls and updates crypto data.
    """

    # File paths and initial variables
    data_file_path = 'crypto_data.json'
    active_message = [0, '']
    table_data = [["Rank", "Crypto", "Price(USD)"]]

    # Initialize the main app window using tkinter library functions
    app = CTk()
    app.geometry("856x645")
    app.resizable(0, 0)

    # Set initial appearance mode (light mode)
    set_appearance_mode("light")
    
    # Create the UI components
    create_sidebar(app)
    main_view = create_main_view(app)
    create_metrics_view(main_view)
    create_table_view(main_view, table_data)

    # Initial data pull and update
    check_last_pulled_and_pull(data_file_path, active_message)
    update_data(data_file_path) #MIGHT NOT NEED???

    # Start the app loop for tkinter window
    app.mainloop()

if __name__ == '__main__':
    main()