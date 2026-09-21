from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

CONFIG = json.loads(Path('config/capital_reduction_phase2.json').read_text())

def load_manifest() -> pd.DataFrame:
    path = Path(CONFIG['span_manifest'])
    if not path.exists():
        raise FileNotFoundError(f'Missing SPAN manifest: {path}')
    df = pd.read_csv(path)
    required = {'as_of_date','file_name','file_type','sha256','source_status'}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f'Missing manifest columns: {sorted(missing)}')
    df['as_of_date'] = pd.to_datetime(df['as_of_date']).dt.normalize()
    return df

def load_baseline() -> pd.DataFrame:
    path = Path(CONFIG['source_baseline_ledger'])
    df = pd.read_csv(path)
    df['expiry'] = pd.to_datetime(df['expiry'])
    df['d3'] = pd.to_datetime(df['d3'])
    df = df[df['gate'].fillna(False).astype(bool)].copy()
    return df

def position_list(row: pd.Series) -> list[dict]:
    expiry = row['expiry'].strftime('%Y%m%d')
    lot = int(row['lot_size'])
    return [
        {'symbol':'NIFTY','instrument':'PE','expiry':expiry,'strike':float(row['P35']),'transaction_type':'BUY','quantity':lot},
        {'symbol':'NIFTY','instrument':'PE','expiry':expiry,'strike':float(row['P20']),'transaction_type':'SELL','quantity':2*lot},
        {'symbol':'NIFTY','instrument':'CE','expiry':expiry,'strike':float(row['P65']),'transaction_type':'BUY','quantity':lot},
        {'symbol':'NIFTY','instrument':'CE','expiry':expiry,'strike':float(row['P80']),'transaction_type':'SELL','quantity':2*lot},
    ]

def calculate_file(path: Path, positions: list[dict], as_of: str):
    from marginism import RiskEngine
    engine = RiskEngine.from_file(str(path), symbols=['NIFTY'])
    result = engine.basket(positions, as_of_date=as_of)
    final = result['data']['final']
    return {
        'span': float(final.get('span', 0.0)),
        'exposure': float(final.get('exposure', 0.0)),
        'additional': float(final.get('additional', 0.0)),
        'total_margin': float(final.get('total', 0.0)),
        'option_premium': float(final.get('option_premium', 0.0)),
    }

def choose_entry_file(row: pd.Series, manifest: pd.DataFrame):
    d3 = row['d3']
    exact = manifest[(manifest['as_of_date'].eq(d3)) & manifest['file_type'].str.upper().eq('BOD')]
    if len(exact):
        return exact.iloc[0]
    prev = manifest[(manifest['as_of_date'].lt(d3)) & manifest['file_type'].str.upper().eq('EOD')].sort_values('as_of_date')
    if len(prev):
        return prev.iloc[-1]
    return None

def main() -> None:
    manifest = load_manifest()
    baseline = load_baseline()
    rows = []
    for _, row in baseline.iterrows():
        entry = choose_entry_file(row, manifest)
        if entry is None:
            rows.append({'expiry':row['expiry'].date().isoformat(),'d3':row['d3'].date().isoformat(),'status':'MISSING_SPAN_ENTRY_FILE'})
            continue
        path = Path(CONFIG['span_dir']) / str(entry['file_name'])
        if not path.exists():
            rows.append({'expiry':row['expiry'].date().isoformat(),'d3':row['d3'].date().isoformat(),'status':'MISSING_SPAN_CACHE','file_name':str(entry['file_name'])})
            continue
        try:
            pos = position_list(row)
            out = calculate_file(path, pos, row['d3'].strftime('%Y-%m-%d'))
            net_premium_credit_inr = float(row.get('premium_credit_points', 0.0)) * float(row['lot_size'])
            net_premium_payable_inr = max(-net_premium_credit_inr, 0.0)
            entry_capital = out['total_margin'] + net_premium_payable_inr
            rows.append({
                'expiry':row['expiry'].date().isoformat(),
                'd3':row['d3'].date().isoformat(),
                'span_file':str(entry['file_name']),
                'span':out['span'],
                'exposure':out['exposure'],
                'additional':out['additional'],
                'margin_total':out['total_margin'],
                'net_premium_credit_inr':net_premium_credit_inr,
                'net_premium_payable_inr':net_premium_payable_inr,
                'entry_capital':entry_capital,
                'status':'OK'
            })
        except Exception as exc:
            rows.append({'expiry':row['expiry'].date().isoformat(),'d3':row['d3'].date().isoformat(),'status':'CALC_ERROR','error':str(exc)})
    out = pd.DataFrame(rows)
    out_dir = Path('data/derived/capital_reduction_phase2')
    out_dir.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_dir/'baseline_entry_capital_ledger.csv',index=False)
    print(out['status'].value_counts(dropna=False).to_string())

if __name__ == '__main__':
    main()