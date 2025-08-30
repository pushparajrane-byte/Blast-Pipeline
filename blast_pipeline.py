import subprocess
from pathlib import Path

DATA_DIR = Path("data")
DB_DIR = Path("db")
RESULTS_DIR = Path("results")

query_file = DATA_DIR / "query.fasta"
subject_file = DATA_DIR / "subject.fasta"
db_name = DB_DIR / "subject_db"
output_file = RESULTS_DIR / "blast_results.txt"

DB_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

subprocess.run([
    "makeblastdb",
    "-in", str(subject_file),
    "-dbtype", "nucl",
    "-out", str(db_name)
], check=True)

subprocess.run([
    "blastn",
    "-query", str(query_file),
    "-db", str(db_name),
    "-out", str(output_file),
    "-outfmt", "6"
], check=True)

subprocess.run([
    "blastn",
    "-query", str(query_file),
    "-db", str(db_name),
    "-out", str(output_file),
    "-outfmt", "7",
    "-task", "blastn-short"
])

print(f"BLAST search completed! Results saved to {output_file}")

import pandas as pd

columns = [
    "query_id", "subject_id", "percent_identity", "alignment_length",
    "mismatches", "gap_opens", "q_start", "q_end",
    "s_start", "s_end", "evalue", "bit_score"
]

results_df = pd.read_csv(output_file, sep="\t", comment="#", names=columns)

print("\nParsed BLAST results:")
print(results_df)

results_df.to_csv("results/blast_results.csv", index=False)
print("\nResults also saved as results/blast_results.csv")

