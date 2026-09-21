# Phase 1 Literature Matrix

| Source | Topic | Key finding relevant to MC2 | Design implication |
|---|---|---|---|
| NSE India — Equity Derivatives Margins | Exchange margining | NSE Clearing uses SPAN as a portfolio-based margining system; initial margin is collected upfront. | Optimize the whole four-leg portfolio, not isolated short legs. |
| NSE India — NSE Clearing SPAN | Portfolio risk / offsets | SPAN evaluates combined futures/options positions under standardized price and volatility scenarios and incorporates net option value. | Strike placement and leg ratios can alter margin through portfolio offsets and scenario losses. |
| NSE Clearing — SPAN Risk Parameters | Risk parameters | SPAN uses price/volatility scan ranges and publishes risk-parameter files; parameters vary over time. | Historical margin must be reconstructed with date-specific risk inputs. |
| NSE Clearing — Margins | Expiry effects | Additional extreme-loss margin applies to short index options on expiry day. | Entry and peak capital must be measured separately. |
| Paytm Money — Margin FAQ | Retail upfront requirement | Paytm Money states that overnight F&O positions require complete SPAN + exposure margin and that option-writing margin is exchange-defined. | Use broker/exchange capital as the primary target where attributable. |
| Paytm Money — Margin Calculator | Combined positions | Paytm Money states that multiple positions can be added together and that hedge positions can reduce overall margin; long options require premium rather than writing margin. | Model the complete BATMAN portfolio jointly. |
| Saretto & Santa-Clara (2006) | Option strategy implementation | Trading costs and margin requirements materially constrain practical option-strategy implementation. | Evaluate capital together with costs and P&L. |
| Coffman, Matsypura & Timkovsky (2010) | Strategy vs risk margining | Margin outcomes differ under alternative portfolio-margining approaches. | Do not infer broker margin from payoff shape alone. |
| Chen, Wu & Li (2023) | Option-portfolio margin netting | Option-portfolios can be decomposed into simple strategies to study netting efficiency and margin requirements. | Examine which parameter changes improve internal portfolio netting. |
| Guasoni, Mayerhofer & Zhao (2026) | Option portfolio selection under constraints | Position limits, trading costs and margin-like solvency constraints can materially change implementable option portfolios. | Capital-constrained optimization should be an explicit objective. |
| Sehgal & Narayanamurthy (2008) | NIFTY implied volatility | NIFTY option implied volatility varies with moneyness and shows structured smile/skew behavior. | Strike changes affect pricing and risk; preserve moneyness context. |
| Shaikh & Padhi (2014) | NIFTY volatility surface | NIFTY options show persistent smile/smirk behavior and liquidity is associated with volatility patterns. | Check liquidity of candidate strikes. |

## Sources
- NSE margins: https://www.nseindia.com/static/products-services/equity-derivatives-margins
- NSE Clearing SPAN: https://www.nseindia.com/static/products-services/equity-derivatives-nse-clearing-span
- NSE Clearing SPAN risk parameters: https://www.nseclearing.in/risk-management/equity-derivatives/span-risk-parameters
- NSE Clearing margins: https://www.nseclearing.in/risk-management/equity-derivatives/margins
- Paytm Money margin FAQ: https://www.paytmmoney.com/stocks/customer/fno-faq/margin-leverage/margin/what-is-margin-call-requirement-received-notification-email-from-paytm-money
- Paytm Money margin calculator: https://www.paytmmoney.com/blog/margin-calculator/
- Saretto & Santa-Clara: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=681643
- Coffman et al.: https://doi.org/10.1007/s10288-010-0129-5
- Chen et al.: https://doi.org/10.1016/j.jedc.2022.104572
- Guasoni et al.: https://doi.org/10.1016/j.jempfin.2026.101770
- Sehgal & Narayanamurthy: https://doi.org/10.1108/AJRAFM-12-2013-0103
- Shaikh & Padhi: https://doi.org/10.1108/JIBR-12-2013-0103