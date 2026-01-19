"""
Moon Dev's HIP3 Market Data Dashboard - Multi-Dex TradFi & Crypto Assets
Built with love by Moon Dev | Run with: python examples/21_hip3_market_data.py

HIP3 Dexes (58 symbols total):
- xyz (27): Stocks, commodities, FX (TSLA, NVDA, GOLD, EUR)
- flx (7): Stocks, XMR, commodities
- vntl (7): Pre-IPO (OPENAI, ANTHROPIC, SPACEX, indices)
- hyna (12): Crypto (BTC, ETH, HYPE, SOL, FARTCOIN, PUMP)
- km (5): US indices (US500, USTECH, SMALL2000)

Categories: Stocks (25) | Indices (8) | Commodities (7) | FX (2) | Crypto (13) | Pre-IPO (3)

Symbol Format: {dex}:{ticker} (e.g., xyz:TSLA, hyna:BTC, km:US500, vntl:OPENAI)

Usage:
    python examples/21_hip3_market_data.py              # Show all dexes and symbols
    python examples/21_hip3_market_data.py xyz tsla     # Show xyz:TSLA tick data
    python examples/21_hip3_market_data.py hyna btc     # Show hyna:BTC tick data
    python examples/21_hip3_market_data.py vntl openai  # Show vntl:OPENAI tick data
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import MoonDevAPI
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich import box

console = Console()

DEX_INFO = {
    'xyz': {'color': 'cyan', 'name': 'XYZ', 'focus': 'Stocks/Commodities/FX'},
    'flx': {'color': 'yellow', 'name': 'FLX', 'focus': 'Stocks/XMR/Commodities'},
    'vntl': {'color': 'blue', 'name': 'VNTL', 'focus': 'Pre-IPO/Indices'},
    'hyna': {'color': 'magenta', 'name': 'HYNA', 'focus': 'Crypto/Memes'},
    'km': {'color': 'green', 'name': 'KM', 'focus': 'US Indices'}
}

def format_price(value, compact=False):
    if value is None:
        return "N/A"
    try:
        value = float(value)
    except:
        return str(value)
    if compact:
        if value >= 10000:
            return f"{value/1000:.0f}k"
        elif value >= 1000:
            return f"{value:.0f}"
        elif value >= 1:
            return f"{value:.2f}"
        elif value >= 0.01:
            return f"{value:.3f}"
        else:
            return f"{value:.4f}"
    else:
        if value >= 10000:
            return f"${value:,.0f}"
        elif value >= 1000:
            return f"${value:,.2f}"
        elif value >= 1:
            return f"${value:.2f}"
        elif value >= 0.01:
            return f"${value:.4f}"
        else:
            return f"${value:.6f}"

def get_dex_style(dex):
    return DEX_INFO.get(dex.lower(), {'color': 'white', 'name': dex.upper(), 'focus': 'Unknown'})

def display_compact_dashboard(api):
    """Display compact HIP3 dashboard"""

    # Fetch data from stats endpoint (meta endpoint may 404)
    stats = api.get_hip3_tick_stats()

    # Get symbols and prices
    symbol_list = stats.get('symbols', [])
    symbol_count = stats.get('symbol_count', len(symbol_list))
    latest_prices = stats.get('latest_prices', {})

    # Stats
    collector = stats.get('collector_stats', {})
    ticks_recv = collector.get('ticks_received', 0)
    ticks_saved = collector.get('ticks_saved', 0)
    dex_counts = stats.get('dex_counts', {})
    categories_raw = stats.get('categories', {})
    # Count symbols per category
    categories = {cat: len(syms) for cat, syms in categories_raw.items() if syms}

    # Group symbols by dex with prices
    dex_symbols = {'xyz': [], 'flx': [], 'vntl': [], 'hyna': [], 'km': []}

    for sym in symbol_list:
        if isinstance(sym, str) and ':' in sym:
            dex, ticker = sym.split(':', 1)
            # Get price from latest_prices dict
            price_data = latest_prices.get(sym, {})
            price = price_data.get('price') if isinstance(price_data, dict) else None
            if dex in dex_symbols:
                dex_symbols[dex].append({'ticker': ticker, 'price': price})

    # Build the dashboard
    console.clear()

    # Header
    header = Table(box=None, show_header=False, padding=0, expand=True)
    header.add_column(ratio=1)
    header.add_row(Text("HIP3 API", style="bold yellow", justify="center"))
    header.add_row(Text("Real-Time TradFi & Crypto Market Data", style="dim", justify="center"))

    console.print(Panel(header, border_style="yellow", padding=(0, 2)))

    # Stats row
    stats_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2), expand=True)
    stats_table.add_column(justify="center")
    stats_table.add_column(justify="center")
    stats_table.add_column(justify="center")
    stats_table.add_column(justify="center")
    stats_table.add_column(justify="center")

    stats_table.add_row(
        f"[bold white]{symbol_count}[/] Symbols",
        f"[bold cyan]{len(dex_counts)}[/] Dexes",
        f"[bold yellow]{ticks_recv:,}[/] Ticks Recv",
        f"[bold green]{ticks_saved:,}[/] Ticks Saved",
        f"[dim]WebSocket Live[/dim]"
    )
    console.print(stats_table)

    # Categories row
    cat_parts = []
    for cat, count in categories.items():
        if count and count > 0:
            cat_parts.append(f"[dim]{cat.replace('_', '-').title()}:[/dim] [white]{count}[/white]")
    if cat_parts:
        console.print(" | ".join(cat_parts), justify="center")
    console.print()

    # Create 5 dex tables side by side
    dex_tables = []

    for dex_name in ['xyz', 'flx', 'vntl', 'hyna', 'km']:
        style = get_dex_style(dex_name)
        syms = dex_symbols.get(dex_name, [])
        count = dex_counts.get(dex_name, len(syms))

        t = Table(
            box=box.SIMPLE,
            border_style=style['color'],
            padding=(0, 0),
            collapse_padding=True,
        )
        t.add_column(f"[{style['color']}]{style['name']}[/] {count}", style="white", width=7, no_wrap=True, overflow="crop")
        t.add_column("", style="yellow", width=5, no_wrap=True, overflow="crop")

        for s in syms[:15]:  # Show up to 15 per dex
            ticker = s.get('ticker', '?')
            price = s.get('price')
            t.add_row(ticker, format_price(price, compact=True) if price else "")

        # Pad if needed
        for _ in range(15 - len(syms[:15])):
            t.add_row("", "")

        dex_tables.append(t)

    console.print(Columns(dex_tables, equal=True, expand=True))

    # All symbols summary at bottom
    console.print()
    all_syms_table = Table(box=box.ROUNDED, border_style="dim", padding=(0, 1), expand=True, show_header=False)
    all_syms_table.add_column()

    for dex_name in ['xyz', 'flx', 'vntl', 'hyna', 'km']:
        style = get_dex_style(dex_name)
        syms = dex_symbols.get(dex_name, [])
        tickers = sorted([s['ticker'] for s in syms])
        if tickers:
            all_syms_table.add_row(
                f"[{style['color']}]{style['name']}:[/{style['color']}] " +
                ", ".join([f"[white]{t}[/white]" for t in tickers])
            )

    console.print(all_syms_table)

    # Footer
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim]api.moondev.com | {now} | Built by Moon Dev[/dim]", justify="center")

def display_symbol_ticks(api, dex, ticker):
    """Display tick data for a specific symbol"""
    style = get_dex_style(dex)

    console.clear()
    console.print(Panel(
        f"[bold {style['color']}]{dex.upper()}:{ticker.upper()}[/bold {style['color']}] Tick Data",
        border_style=style['color'],
        padding=(0, 2)
    ))

    try:
        data = api.get_hip3_ticks(dex, ticker)

        if isinstance(data, list):
            ticks = data
            tick_count = len(ticks)
            latest_price = ticks[-1].get('p', ticks[-1].get('price', 'N/A')) if ticks else 'N/A'
        elif isinstance(data, dict):
            ticks = data.get('ticks', data.get('data', []))
            tick_count = data.get('tick_count', data.get('count', len(ticks)))
            latest_price = data.get('latest_price', data.get('price', 'N/A'))
        else:
            ticks = []
            tick_count = 0
            latest_price = 'N/A'

        # Stats
        stats_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2), expand=True)
        stats_table.add_column(justify="center")
        stats_table.add_column(justify="center")
        stats_table.add_column(justify="center")
        stats_table.add_row(
            f"[bold yellow]{format_price(latest_price)}[/] Latest",
            f"[bold white]{tick_count:,}[/] Ticks",
            f"[dim]{style['focus']}[/dim]"
        )
        console.print(stats_table)

        if ticks:
            table = Table(box=box.ROUNDED, border_style=style['color'], padding=(0, 1))
            table.add_column("#", style="dim", width=4)
            table.add_column("Time", style="dim", width=20)
            table.add_column("Price", style="yellow", justify="right", width=14)

            for i, tick in enumerate(ticks[-20:], 1):
                timestamp = tick.get('t', tick.get('timestamp', tick.get('time', 0)))
                price = tick.get('p', tick.get('price', 0))
                dt_str = tick.get('dt', '')

                if dt_str:
                    time_str = dt_str[:19] if len(dt_str) > 19 else dt_str
                elif timestamp:
                    try:
                        ts = timestamp / 1000 if timestamp > 1e10 else timestamp
                        dt = datetime.fromtimestamp(ts)
                        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        time_str = str(timestamp)
                else:
                    time_str = "N/A"

                table.add_row(str(i), time_str, format_price(price))

            console.print(table)
            console.print(f"[dim]Showing last 20 of {len(ticks)} ticks[/dim]", justify="center")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim]api.moondev.com | {now} | Built by Moon Dev[/dim]", justify="center")

def main():
    api = MoonDevAPI()

    if not api.api_key:
        console.print("[red]No API key found. Set MOONDEV_API_KEY in .env[/red]")
        return

    args = sys.argv[1:]

    if len(args) == 0:
        display_compact_dashboard(api)
    elif len(args) >= 2:
        dex = args[0].lower()
        ticker = args[1].lower()
        if dex not in ['xyz', 'flx', 'vntl', 'hyna', 'km']:
            console.print(f"[red]Unknown dex: {dex}. Use: xyz, flx, vntl, hyna, km[/red]")
            return
        display_symbol_ticks(api, dex, ticker)
    else:
        console.print("[yellow]Usage: python 21_hip3_market_data.py [dex] [ticker][/yellow]")
        console.print("[dim]Example: python 21_hip3_market_data.py xyz tsla[/dim]")

if __name__ == "__main__":
    main()
