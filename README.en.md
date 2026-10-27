# Monthly Operations ETL · FESE-Portfolio

**Python · SQLite · Excel · PDF · Data quality · Audit trails**

[Español](README.md) · [Architecture](docs/ARCHITECTURE.md)

An executable portfolio project that transforms monthly CSV/XLSX submissions into validated historical data, an annual Excel report and individual PDF receipts. Demonstrates repeated-period detection, review mode, reproducible data and reversible corrections.

**All centers, codes and counts are fictional.** Independently implemented demonstration, not official software. No institutional source code, repository history, inputs, templates, branding, contact lists or deployment configuration is included.

![Synthetic receipt](docs/comprobante-demo-es-v2.png)

## Quick start

Python 3.11+ on Windows, Linux or macOS. No Excel installation, Outlook or external database required.

```powershell
git clone https://github.com/gerardomelkart/FESE-Portfolio.git
cd FESE-Portfolio
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe demo.py
.\.venv\Scripts\python.exe -m pytest -q
```

Linux/macOS: substitute `.venv/bin/python`. With an activated environment use `python demo.py`.

The demo loads January–March 2026 for Aurora, Boreal and Coral, intentionally repeats Aurora's January distribution in March, records a warning, then applies a synthetic +17 correction. Choose a fresh `--workdir` to rerun; existing history is never reset.

| Output under `work/demo/` | Purpose |
| --- | --- |
| `history.sqlite` | 36 unique monthly records and four audited operations |
| `backups/*.sqlite` | Complete database snapshots before applied loads/corrections |
| `reports/annual-2026.xlsx` | Monthly summary, chart, records and audit sheet |
| `reports/*.pdf` | Nine fictional center/month receipts |
| `reports/audit.json` | Operation metadata, input hashes and warnings |

[Sample Excel](docs/annual-2026.xlsx) · [Sample PDF](docs/comprobante-demo-es-v2.pdf)

## Input and commands

CSV or the active XLSX sheet must have exactly `period,center,code,total` in that order. Every file contains all 12 pairs: centers `Aurora`, `Boreal`, `Coral` × codes `A01`, `A02`, `B01`, `B02`. Totals must be integers from 0 to 1,000,000,000. Monthly sums are calculated from validated rows.

```powershell
python etl.py generate --output examples
python etl.py load examples/2026-01.csv --period 2026-01
python etl.py load examples/2026-01.csv --period 2026-01 --apply
python etl.py report --year 2026
```

Without `--apply`, load/undo only preview business data changes; workspace initialization may create an empty database/schema. Identical loads are no-ops without extra audit entries. Changed months require `--correction` and a non-empty `--reason`.

## Corrections and recovery

After loading the original March file into the default workspace:

```powershell
python etl.py load examples/2026-03-corrected.csv --period 2026-03 --correction --reason "Synthetic revision" --apply
```

After `demo.py`, correction ID 4 can be previewed and reversed:

```powershell
python etl.py --workdir work/demo undo 4
python etl.py --workdir work/demo undo 4 --apply
python etl.py --workdir work/demo report --year 2026
```

Only the selected month changes in a SQLite transaction. Audit retains before/after records and the SHA-256 input hash. Undo refuses to overwrite a period changed since the selected audit entry; undo is itself audited. Regenerate reports after changes. Full snapshots support offline database recovery; undo provides selective guarded reversal.

## Quality and design

- Rejects invalid periods, unknown centers/codes, duplicate pairs, incomplete coverage and invalid counts.
- Compares each center's full distribution against **all earlier stored months**, including nonadjacent ones. Exact matches warn but do not automatically reject legitimate data.
- Nine behavioral tests cover CSV/XLSX validation, idempotency, nonadjacent repetitions, correction isolation, guarded undo, reproducibility and report reconciliation.
- GitHub Actions is configured for Python 3.11, 3.12 and 3.13.

## Scope

Small local CLI with fixed fictional catalogs. No email sending, web UI, authentication service or institutional integration. Reports are derived products generated separately from transactions. SQLite audit is operational history, not a tamper-proof compliance ledger. Data is monthly aggregates, not individual events.

No reuse license is granted; public visibility alone does not grant reuse rights. Dependencies retain their own licenses.
