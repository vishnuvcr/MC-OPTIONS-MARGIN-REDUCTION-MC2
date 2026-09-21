# Contract and Cost Timeline

## Expiry

NIFTY weekly expiry moved from Thursday to Tuesday, and NIFTY monthly, quarterly and half-yearly expiry moved from the last Thursday to the last Tuesday during the 2025 transition.

The transition was staged by contract generation dates. Therefore D3 is computed from each contract's actual expiry date.

## Lot size

NIFTY was 25 before the 2024 contract-size change. New contracts were moved to 75 with explicit transition dates. A later 2025 revision changed NIFTY from 75 to 65.

The backtest must use contract-specific metadata rather than one calendar-year constant.

## Execution cost assumptions

The baseline uses the user-specified 2 option points of adverse slippage for each of the four entry legs. It holds the position to expiry.

Brokerage, statutory transaction taxes and other exchange charges are date-sensitive parameters in the research engine and are not hard-coded into the strike-selection logic.
