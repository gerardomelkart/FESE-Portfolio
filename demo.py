"""Run the complete synthetic scenario in a new workspace."""
import argparse
import json
import sqlite3
from pathlib import Path
from etl import generate, ingest, report

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--workdir', default='work/demo')
args = parser.parse_args()
root = Path(args.workdir)
if (root/'history.sqlite').exists():
    parser.error('Choose a new --workdir; existing history is never reset')
inputs = root/'inputs'
generate(inputs)
for month in range(1,4):
    period = f'2026-{month:02}'
    print(json.dumps(ingest(root,inputs/f'{period}.csv',period,True),indent=2))
print(json.dumps(ingest(root,inputs/'2026-03-corrected.csv','2026-03',True,True,'Synthetic revision: Aurora A01 +17'),indent=2))
with sqlite3.connect(root/'history.sqlite') as db:
    assert db.execute('SELECT count(*) FROM totals').fetchone()[0] == 36
    assert db.execute('SELECT count(*) FROM audit').fetchone()[0] == 4
print('Reports:', report(root,2026))
print('Correction audit ID: 4')
