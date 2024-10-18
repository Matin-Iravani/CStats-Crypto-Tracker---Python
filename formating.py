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