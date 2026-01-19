# Alpha Extraction Ideas - Moon Dev API

**Trading Bot Ideas for the Hyperliquid Data Layer**

These are alpha extraction concepts based on the API endpoints. Each example file exposes data that Wall Street has used for decades - now available to anyone with an API key. Below are trading bot ideas for each endpoint.

Built with love by Moon Dev

---

## 01_liquidations.py - Hyperliquid Liquidations

**Endpoint:** `/api/liquidations/{timeframe}.json`

1. **Liquidation Cascade Trader** - When liquidations spike 3x above the 1-hour rolling average, enter positions in the cascade direction (short if long liqs dominate). Liquidations beget more liquidations - ride the cascade.

2. **Liquidation Exhaustion Bot** - After a massive liquidation event ($10M+ in 10 minutes), fade the move. Extreme liquidations often mark local bottoms/tops. Enter counter-trend with tight stops.

3. **Liquidation Imbalance Scanner** - Track long vs short liquidation ratios. When 80%+ of liquidations are one-sided for 4+ hours, the market is overextended. Position for mean reversion.

---

## 02_positions.py - Whale Positions Near Liquidation

**Endpoint:** `/api/positions/all.json` (148 symbols)

1. **Liquidation Hunting Bot** - Monitor positions within 2% of liquidation price. When BTC moves toward these levels, front-run the liquidation cascade. Target the clusters.

2. **Whale Shadow Trader** - When top 10 whales are 70%+ aligned (all long or all short), follow them. Large players often have better information. Exit when whale consensus breaks.

3. **Risk Concentration Alert** - When total position value in a single symbol exceeds $500M with >60% one-sided, expect volatility. Trade the direction of crowded positioning getting stopped out.

---

## 03_whales.py - Whale Activity Tracker

**Endpoint:** `/api/whales.json` ($25k+ trades)

1. **Whale Order Flow Bot** - When whale buy volume exceeds sell volume by 3:1 over 15 minutes, enter long. Whales move markets. Ride their wake.

2. **Whale Reversal Detector** - Track when a whale who was accumulating starts distributing. If a whale does 5 buys then 3 sells of similar size, they're exiting. Front-run the distribution.

3. **Multi-Whale Consensus Trader** - When 3+ different whale addresses buy the same asset within 1 hour, it's coordinated. Follow the smart money with a position sized to the total whale volume.

---

## 04_events.py - Blockchain Events

**Endpoint:** `/api/events.json`

1. **Large Deposit Anticipation Bot** - When a whale bridges $500k+ to Hyperliquid, they're about to trade. Monitor for the deposit event, then watch their first position. Mirror it.

2. **Withdrawal Spike Alert** - Mass withdrawals often precede volatility (people moving funds to safety). When withdrawal events spike 5x, reduce exposure and wait for clarity.

3. **Swap Pattern Analyzer** - Track swap events for arbitrage opportunities. If swaps consistently go USDC→asset, accumulation is happening. Position before the crowd notices.

---

## 05_contracts.py - Contract Registry

**Endpoint:** `/api/contracts.json`

1. **New Contract Alpha** - When a new high-value contract appears, it's often a new trading strategy or protocol. Monitor early interactions for alpha on what they're trading.

2. **Contract Activity Divergence** - If a contract that's been dormant suddenly shows activity, something changed. Track the delta and investigate what they're doing differently.

3. **Protocol Flow Tracker** - Aggregate flows across all known contracts to understand net protocol sentiment. Are smart contracts net accumulating or distributing?

---

## 06_ticks.py - Live Price Data

**Endpoint:** `/api/ticks/{symbol}_{timeframe}.json`

1. **Tick Velocity Bot** - When tick frequency (trades per second) spikes 5x above normal while price is flat, a big move is brewing. Enter on the direction of the first significant price move.

2. **Volatility Breakout System** - Calculate tick-by-tick volatility. When volatility compresses below the 20-period low then expands, trade the breakout direction with a 2:1 reward-to-risk.

3. **Micro-Structure Alpha** - Analyze tick patterns for recurring signatures. Certain tick sequences (3 up ticks, pause, 5 up ticks) may precede continuation moves. Pattern match and trade.

---

## 07_orderflow.py - Order Flow Analysis

**Endpoint:** `/api/orderflow.json`, `/api/imbalance/{timeframe}.json`

1. **Delta Divergence Bot** - When price makes a new high but cumulative delta doesn't confirm (negative delta on up move), the move is weak. Fade it with a stop above the high.

2. **Absorption Detector** - When buy pressure is high but price isn't moving, large sellers are absorbing. The next direction is likely down. Position short when absorption is confirmed.

3. **Imbalance Mean Reversion** - When buy/sell imbalance exceeds 2 standard deviations, expect mean reversion. Enter counter to the extreme imbalance with a tight timeframe.

---

## 08_trades.py - Recent Trades

**Endpoint:** `/api/trades.json`, `/api/large_trades.json`

1. **Large Trade Momentum** - When 3+ trades over $100k hit in the same direction within 5 minutes, momentum is real. Enter with the flow, trail stop.

2. **Trade Size Analysis** - Average trade size increasing while price rises = strong trend. Average size decreasing = weak hands buying. Trade with conviction when size confirms.

3. **Time-Weighted Trade Bot** - Weight trades by recency and size. Recent large trades matter more than old small ones. Create a proprietary signal and trade when it crosses thresholds.

---

## 09_smart_money.py - Smart Money Rankings

**Endpoint:** `/api/smart_money/rankings.json`, `/api/smart_money/signals_{timeframe}.json`

1. **Copy Top 10 Traders** - Mirror the positions of the top 10 ranked traders. When the majority are long, be long. Position size proportional to their conviction level.

2. **Fade Bottom 100** - When the worst performers (bottom 100) are heavily positioned one way, fade them. "Dumb money" is the best counter-indicator.

3. **Smart Money Divergence** - When smart money and dumb money disagree, follow smart money. The divergence signal has edge. Size up when divergence is extreme.

---

## 10_user_positions.py - Any Wallet's Positions

**Endpoint:** `/api/user/{address}/positions`

1. **Specific Whale Tracker** - Identify 10 consistently profitable addresses. Build a bot that monitors their positions in real-time and mirrors entries with slight delay.

2. **Position Change Alerts** - When a tracked wallet increases position by 50%+, they're adding to winners. Follow the addition. When they reduce, respect their exit.

3. **Portfolio Correlation Bot** - Track how a whale's portfolio changes over time. If they rotate from BTC to alts, something's changing. Front-run the rotation.

---

## 11_user_fills.py - Trade History

**Endpoint:** `/api/user/{address}/fills`

1. **Win Rate Analyzer** - Calculate win rate for top traders by analyzing their fills. Copy traders with >60% win rate AND positive expectancy. Both matter.

2. **Entry Pattern Learner** - Study how top traders enter positions (DCA, all-in, scaled). Adopt the patterns that correlate with higher PnL.

3. **Exit Timing Bot** - Analyze when profitable traders exit. If they consistently exit at 15% profit, use that as your target. Inherit their discipline.

---

## 12_hlp_positions.py - HLP Protocol Positions

**Endpoint:** `/api/hlp/positions`, `/api/hlp/trades`

1. **HLP Counter-Trade Bot** - HLP is the house. When HLP is heavily short, retail is long. Fade retail by going short with HLP. The house usually wins.

2. **Strategy Divergence Alpha** - When different HLP strategies disagree (one long, one short same asset), volatility is coming. Trade a straddle or wait for resolution.

3. **HLP Trade Follower** - When HLP makes a large trade (top 1% by size), follow within 60 seconds. They have information edge from seeing all order flow.

---

## 13_binance_liquidations.py - Binance Liquidations

**Endpoint:** `/api/binance_liquidations/{timeframe}.json`

1. **Cross-Exchange Liquidation Arbitrage** - When Binance liquidations spike but Hyperliquid doesn't, expect spillover. Position on Hyperliquid for the incoming cascade.

2. **Exchange Divergence Bot** - If Binance longs are getting liquidated but Hyperliquid longs aren't, price will converge. Trade the convergence on the lagging exchange.

3. **Binance Lead Indicator** - Binance often leads smaller exchanges. Use Binance liquidation direction to predict Hyperliquid liquidations. Be positioned before the cascade hits.

---

## 14_multi_liquidations.py - All Exchange Liquidations

**Endpoint:** `/api/all_liquidations/{timeframe}.json`

1. **Global Liquidation Tsunami Bot** - When combined liquidations across all 4 exchanges exceed $100M in 1 hour, it's a market-wide event. Position for continuation until volume dies.

2. **Exchange Liquidation Sequencing** - Track which exchange liquidates first. If Hyperliquid leads, it's organic. If Binance leads, it's cascading. Trade the follow-through.

3. **Liquidation Correlation Breakdown** - When one exchange has massive liquidations but others don't, something exchange-specific happened. Arbitrage the dislocation.

---

## 15_buyers.py - Buyer Tracker

**Endpoint:** `/api/buyers.json` ($5k+ buyers, HYPE/SOL/XRP/ETH only)

1. **Accumulation Detection Bot** - When unique buyer count increases 50%+ over 24 hours while price is flat, accumulation is happening. Enter before the markup phase.

2. **Buyer Concentration Alert** - If 70%+ of buying is from 5 addresses, it's coordinated. Follow if they're known smart money, fade if they're historically wrong.

3. **Buy Pressure Divergence** - When buyer count is increasing but price is dropping, large sellers are distributing to new buyers. The sellers know something. Stay out or short.

---

## 16_depositors.py - All Hyperliquid Depositors

**Endpoint:** `/api/depositors.json`

1. **New Depositor Surge Bot** - When new depositor count spikes 2x above 7-day average, fresh capital is entering. Bull signal. Position long on high-beta assets.

2. **Depositor Quality Analysis** - Track if new depositors are small (<$1k) or large (>$100k). Large depositors = institutions arriving. More bullish signal.

3. **Depositor Retention Tracker** - If depositors are leaving (withdrawals > deposits), risk-off is coming. Reduce exposure proportionally to net outflows.

---

## 17_hlp_sentiment.py - HLP Z-Score Signals

**Endpoint:** `/api/hlp/sentiment`

1. **Z-Score Extremes Bot** - When HLP z-score exceeds +2.0 (HLP very long), retail is very short. Enter long for squeeze. Vice versa for z < -2.0. This is THE signal.

2. **Z-Score Mean Reversion** - When z-score hits +3.0, it WILL revert. Don't chase. Wait for reversion to begin, then enter with the trend back to 0.

3. **Multi-Timeframe Z-Score** - Compare 1-hour z-score to 24-hour z-score. When both are extreme in same direction, the signal is stronger. Size up on alignment.

---

## 18_hlp_analytics.py - HLP Deep Analytics

**Endpoint:** `/api/hlp/liquidators/status`, `/api/hlp/market-maker`, `/api/hlp/timing`

1. **Liquidator Activation Bot** - When HLP liquidators activate, forced selling is imminent. Position for the liquidation direction. Exit when liquidator goes idle.

2. **Timing-Based Entry** - HLP analytics show which hours are most profitable. Only trade during historically profitable hours for the asset. Avoid bad timing.

3. **Market Maker Position Tracker** - Strategy B is the market maker. When it's heavily positioned, it's confident in the direction. Follow with smaller size.

---

## 19_market_data.py - Rate-Limit-Free Market Data

**Endpoint:** `/api/prices`, `/api/orderbook/{coin}`, `/api/account/{address}`

1. **Orderbook Imbalance Scanner** - Scan all 224 coins for bid/ask imbalances. When bids are 3x asks, upward pressure exists. Enter before the move.

2. **Multi-Coin Correlation Bot** - Monitor all 224 prices simultaneously. When correlations break (BTC up, ETH flat), trade the spread for convergence.

3. **Account Concentration Tracker** - Monitor top accounts' positions in real-time without rate limits. When multiple top accounts shift, follow immediately.

---

## 20_hip3_liquidations.py - TradFi Liquidations

**Endpoint:** `/api/hip3_liquidations/{timeframe}.json`

1. **Stock Liquidation Cascade** - When TSLA or NVDA liquidations spike during market hours, volatility is real. Position for continuation in the liquidation direction.

2. **TradFi-Crypto Correlation Bot** - When stock liquidations are high but crypto is calm, expect spillover. Position crypto for the incoming volatility.

3. **Category Rotation Alert** - When liquidations shift from stocks to commodities, macro conditions are changing. Adjust portfolio to match the rotation.

---

## 21_hip3_market_data.py - Multi-Dex TradFi Data

**Endpoint:** `/api/hip3_ticks/stats.json`, `/api/hip3_ticks/{dex}_{ticker}.json`

1. **Cross-Dex Arbitrage** - If GOLD trades at different prices on xyz vs flx, arbitrage exists. Trade the spread until convergence.

2. **Pre-IPO Sentiment Bot** - Monitor OPENAI, ANTHROPIC, SPACEX tick data on vntl. Volume spikes may precede news. Position before announcements.

3. **TradFi Hours Trader** - Trade stocks (xyz, flx) only during traditional market hours when liquidity is highest. Avoid overnight gaps.

---

## 22_hip3_dashboard.py - HIP3 Combined Dashboard

**Endpoint:** Multiple HIP3 endpoints combined

1. **Sector Rotation Scanner** - Monitor all 58 HIP3 symbols for momentum. Rotate into the strongest sector (stocks vs commodities vs crypto vs FX).

2. **Liquidation-Price Divergence** - When a sector has high liquidations but prices haven't moved much, big moves are coming. Position for the breakout.

3. **Full Market Sentiment Bot** - Combine all HIP3 data into a single sentiment score. When the score is extreme, trade the mean reversion across all correlated assets.

---

## Implementation Notes

These ideas are starting points. Each requires:
- Backtesting against historical data
- Risk management rules (position sizing, stop losses)
- Execution optimization (latency, slippage)
- Continuous monitoring and adjustment

**Remember:** Past performance doesn't guarantee future results. Paper trade first. Size appropriately. The API gives you the data - your edge comes from how you use it.

---

Built with love by Moon Dev | api.moondev.com
