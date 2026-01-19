"""
Moon Dev's HIP3 Dashboard - TradFi & Crypto on Hyperliquid
Built with love by Moon Dev | python examples/22_hip3_dashboard.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import MoonDevAPI
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def fmt_price(val):
    if val is None: return "-"
    try: val = float(val)
    except: return str(val)
    if val >= 10000: return f"{val/1000:.1f}k"
    if val >= 1000: return f"{val:,.0f}"
    if val >= 1: return f"{val:.2f}"
    if val >= 0.01: return f"{val:.3f}"
    return f"{val:.4f}"

def fmt_usd(val):
    if val is None: return "-"
    try: val = float(val)
    except: return str(val)
    if val >= 1_000_000: return f"${val/1_000_000:.1f}M"
    if val >= 1_000: return f"${val/1_000:.1f}k"
    return f"${val:.0f}"

def main():
    api = MoonDevAPI()

    tick_stats = api.get_hip3_tick_stats()
    liq_stats = api.get_hip3_liquidation_stats()

    symbols = tick_stats.get('symbols', [])
    prices = tick_stats.get('latest_prices', {})
    dex_counts = tick_stats.get('dex_counts', {})
    ticks = tick_stats.get('collector_stats', {}).get('ticks_received', 0)

    windows = liq_stats.get('windows', {})
    liq_1h = windows.get('1h', {})

    # Group by dex
    dex_data = {d: [] for d in ['xyz', 'flx', 'vntl', 'hyna', 'km']}
    for sym in symbols:
        if ':' in sym:
            dex, ticker = sym.split(':', 1)
            price = prices.get(sym, {}).get('price')
            if dex in dex_data:
                dex_data[dex].append((ticker, price))

    console.clear()

    # === HEADER ===
    console.print(Panel(
        f"[bold yellow]HIP3 DATA LAYER[/]  |  [white]{len(symbols)}[/] Symbols  |  [cyan]{len(dex_counts)}[/] Dexes  |  [green]{ticks:,}[/] Ticks",
        border_style="yellow"
    ))

    # === LIQUIDATIONS ===
    liq_total = fmt_usd(liq_1h.get('total_value_usd', 0))
    liq_long = fmt_usd(liq_1h.get('long_value_usd', 0))
    liq_short = fmt_usd(liq_1h.get('short_value_usd', 0))
    liq_count = liq_1h.get('total_count', 0)
    console.print(Panel(
        f"[bold red]1H LIQUIDATIONS[/] {liq_total} ({liq_count:,})  |  Longs: [green]{liq_long}[/]  |  Shorts: [red]{liq_short}[/]",
        border_style="red"
    ))

    # === TRADFI PRICES (XYZ, FLX, KM) ===
    tradfi = Table(box=box.ROUNDED, border_style="cyan", title="[bold cyan]TradFi - Stocks, Commodities, FX, Indices[/]", expand=True)
    tradfi.add_column(f"XYZ ({dex_counts.get('xyz', 0)})", style="white")
    tradfi.add_column("$", style="yellow", justify="right")
    tradfi.add_column(f"FLX ({dex_counts.get('flx', 0)})", style="white")
    tradfi.add_column("$", style="yellow", justify="right")
    tradfi.add_column(f"KM ({dex_counts.get('km', 0)})", style="white")
    tradfi.add_column("$", style="yellow", justify="right")

    max_tf = max(len(dex_data['xyz']), len(dex_data['flx']), len(dex_data['km']))
    for i in range(min(max_tf, 15)):
        row = []
        for dex in ['xyz', 'flx', 'km']:
            items = dex_data[dex]
            if i < len(items):
                row.extend([items[i][0], fmt_price(items[i][1])])
            else:
                row.extend(["", ""])
        tradfi.add_row(*row)

    console.print(tradfi)

    # === CRYPTO & PRE-IPO (HYNA, VNTL) ===
    crypto = Table(box=box.ROUNDED, border_style="magenta", title="[bold magenta]Crypto & Pre-IPO[/]", expand=True)
    crypto.add_column(f"HYNA ({dex_counts.get('hyna', 0)})", style="white")
    crypto.add_column("$", style="yellow", justify="right")
    crypto.add_column(f"VNTL ({dex_counts.get('vntl', 0)})", style="white")
    crypto.add_column("$", style="yellow", justify="right")

    max_cr = max(len(dex_data['hyna']), len(dex_data['vntl']))
    for i in range(max_cr):
        row = []
        for dex in ['hyna', 'vntl']:
            items = dex_data[dex]
            if i < len(items):
                row.extend([items[i][0], fmt_price(items[i][1])])
            else:
                row.extend(["", ""])
        crypto.add_row(*row)

    console.print(crypto)

    # === TOP LIQUIDATED ===
    by_asset = liq_1h.get('by_asset', {})
    if by_asset:
        sorted_assets = sorted(by_asset.items(), key=lambda x: x[1].get('total_value', 0), reverse=True)[:6]
        liq_table = Table(box=box.ROUNDED, border_style="red", title="[bold red]Most Liquidated (1H)[/]", expand=True)
        liq_table.add_column("Asset", style="white")
        liq_table.add_column("Total", justify="right", style="yellow")
        liq_table.add_column("Longs", justify="right", style="green")
        liq_table.add_column("Shorts", justify="right", style="red")

        for asset, data in sorted_assets:
            liq_table.add_row(
                asset,
                fmt_usd(data.get('total_value', 0)),
                fmt_usd(data.get('long_value', 0)),
                fmt_usd(data.get('short_value', 0))
            )
        console.print(liq_table)

    # === FOOTER ===
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"\n[dim]api.moondev.com | {now} | Built by Moon Dev[/]", justify="center")

if __name__ == "__main__":
    main()
