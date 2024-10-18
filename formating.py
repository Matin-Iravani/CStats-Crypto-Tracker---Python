"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                          CStats Formatting and Data Processing                   ║
║                                                                                  ║
║ This file contains utility functions for formatting cryptocurrency data and      ║
║ processing it for display in the CStats application. These functions help with   ║
║ formatting prices, percentage changes, market capitalization, and total supply.  ║
║ It also includes functions for clearing UI frames and processing cryptocurrency  ║
║ data for a table display.                                                        ║
║                                                                                  ║
║ Key features:                                                                    ║
║ - Format price, percentage change, market cap, and total supply for display.     ║
║ - Process cryptocurrency data and format it into a table-friendly format.        ║
║ - Clear tkinter frames by removing all widgets.                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""


def format_price(price: float) -> str:
    """
    Formats the price value for display.

    price (float): The cryptocurrency price.

    Returns:
    str: The formatted price string.
    """
    return f"${price: ,.5g}"


def format_percent_change(percent_change: float) -> str:
    """
    Formats the percentage change value with an arrow indicating the direction.

    percent_change (float): The percentage change value.

    Returns:
    str: The formatted percentage change string with an arrow.
    """
    if percent_change > 0:
        return f"▲{percent_change: .2f}%"
    else:
        return f"▼{-1 * percent_change: .2f}%"


def format_market_cap(market_cap: float) -> str:
    """
    Formats the market cap value for display.

    Parameters:
    market_cap (float): The cryptocurrency market cap.

    Returns:
    str: The formatted market cap string.
    """
    return f"${market_cap: ,.3g}"


def format_total_supply(total_supply: float, short_name: str) -> str:
    """
    Formats the total supply value for display.

    Parameters:
    total_supply (float): The total supply of the cryptocurrency.
    short_name (str): The symbol of the cryptocurrency.

    Returns:
    str: The formatted total supply string with the cryptocurrency symbol.
    """
    return f"{total_supply: .8g} {short_name}"


def clear_frame(frame):
    """
    Clears all widgets from the specified frame.
    """
    # Loop through all widgets within the frame and destroy them
    for widget in frame.winfo_children():
        widget.destroy()


def process_crypto_data(data: list, table_data: list) -> list:
    """
    Processes cryptocurrency data and formats it for display in the table.

    data (list): The list of cryptocurrency data entries.
    table_data (list): The table data to append to.

    Returns:
    list: The updated table data with processed cryptocurrency information.
    """
    number = 1  # Initialize row number for ranking

    for crypto in data:
        # Extract and format relevant data
        rank = f"{number}"
        name = f"{crypto['name']}"
        crypto_price = format_price(crypto["quote"]["USD"]["price"])
        day_change = format_percent_change(crypto["quote"]["USD"]["percent_change_24h"])
        hour_change = format_percent_change(crypto["quote"]["USD"]["percent_change_1h"])
        crypto_market_cap = format_market_cap(crypto["quote"]["USD"]["market_cap"])
        short_name = crypto["symbol"]
        total_supply = format_total_supply(crypto["total_supply"], short_name)

        # Create a row with the formatted data
        temp = [
            rank,
            name,
            crypto_price,
            hour_change,
            day_change,
            crypto_market_cap,
            short_name,
            total_supply
        ]
        table_data.append(temp)
        number += 1  # Increment row number

    return table_data