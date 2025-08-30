# app.py
import subprocess
from pathlib import Path

import pandas as pd
import streamlit as st

# Constants
OUTFMT6_FIELDS = [
    "qseqid", "sseqid", "pident", "length", "mismatch", "gapopen",
    "qstart", "qend", "sstart", "send", "evalue", "bitscore",
]
NUMERIC_COLS = [
    "pident", "length", "mismatch", "gapopen",
    "qstart", "qend", "sstart", "send", "evalue", "bitscore",
]

# Helpers
def run_cmd(args, cwd=None) -> None:
    """Run a command and raise with stdout/stderr on failure."""
    res = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(args)}\n"
            f"STDOUT:\n{res.stdout}\n\nSTDERR:\n{res.stderr}"
        )

def write_fasta(text: str, path: Path) -> None:
    """Write FASTA text to file, ensuring there's at least one header."""
    txt = (text or "").strip().replace("\r\n", "\n")
    if not txt:
        raise ValueError("Empty FASTA text.")
    if not txt.lstrip().startswith(">"):
        txt = ">seq1\n" + txt
    path.write_text(txt, encoding="utf-8")

def parse_fasta_len(text: str) -> int:
    """Return total nucleotide count of the first sequence in a FASTA string."""
    if not text:
        return 0
    seq, started = [], False
    for line in text.splitlines():
        if line.startswith(">"):
            if started:
                break
            started = True
            continue
        if started:
            seq.append(line.strip())
    return len("".join(seq))

def build_db(subject_fa: Path, db_prefix: Path) -> None:
    db_prefix.parent.mkdir(parents=True, exist_ok=True)
    run_cmd([
        "makeblastdb",
        "-in", str(subject_fa),
        "-dbtype", "nucl",
        "-out", str(db_prefix),
    ])

def run_blast(query_fa: Path, db_prefix: Path, out_path: Path, short: bool) -> pd.DataFrame:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "blastn",
        "-query", str(query_fa),
        "-db", str(db_prefix),
        "-outfmt", "6 " + " ".join(OUTFMT6_FIELDS),
        "-out", str(out_path),
    ]
    if short:
        cmd += ["-task", "blastn-short", "-word_size", "4", "-dust", "no"]
    run_cmd(cmd)

    if not out_path.exists() or out_path.stat().st_size == 0:
        return pd.DataFrame(columns=OUTFMT6_FIELDS)

    df = pd.read_csv(out_path, sep="\t", names=OUTFMT6_FIELDS, header=None)
    for c in NUMERIC_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def peek_fasta(fp: Path, n=40):
    """Return (header, length, first_n_bases) for a FASTA file."""
    txt = fp.read_text(encoding="utf-8", errors="ignore")
    header = next((ln.strip() for ln in txt.splitlines() if ln.startswith(">")), ">?")
    seq = "".join(ln.strip() for ln in txt.splitlines() if not ln.startswith(">"))
    return header, len(seq), seq[:n]

def parse_evalue(s: str, default: float = 1e6) -> float:
    s = (s or "").strip()
    try:
        return float(s) if s else default
    except Exception:
        return default

# UI Setup
st.set_page_config(page_title="BLAST (blastn) Pipeline", layout="wide")
st.title("🧬 BLAST (blastn) Pipeline")
st.caption(
    "Upload or paste your **Query FASTA** and **Subject FASTA**. "
    "The app builds a DB from the subject, runs `blastn`, and shows a filterable table + downloadable CSV."
)

tab_paste, tab_upload = st.tabs(["Paste FASTA", "Upload FASTA files"])

# Working dirs
APP_DIR = Path.cwd()
WORK_DIR = APP_DIR / ".work"
DB_DIR   = WORK_DIR / "db"
RES_DIR  = WORK_DIR / "results"
DB_DIR.mkdir(parents=True, exist_ok=True)
RES_DIR.mkdir(parents=True, exist_ok=True)

# Session state
st.session_state.setdefault("df_results", None)
st.session_state.setdefault("raw_results_path", None)
st.session_state.setdefault("mode", None)

#  Paste Tab
with tab_paste:
    st.subheader("Paste FASTA")

    q_text = st.text_area("Query FASTA", height=160, placeholder=">query1\nATG...")
    s_text = st.text_area("Subject FASTA (DB)", height=160, placeholder=">subject1\nAAG...")

    if st.button("Run BLAST (pasted FASTA)", type="primary"):
        try:
            if not q_text.strip() or not s_text.strip():
                st.error("Please paste both Query and Subject FASTA.")
                st.stop()

            query_fa   = WORK_DIR / "query_pasted.fasta"
            subject_fa = WORK_DIR / "subject_pasted.fasta"
            write_fasta(q_text, query_fa)
            write_fasta(s_text, subject_fa)

            db_prefix = DB_DIR / "subject_db_pasted"
            build_db(subject_fa, db_prefix)

            q_len = parse_fasta_len(q_text)
            use_short = q_len <= 30

            out_path = RES_DIR / "blast_results_pasted.txt"
            df = run_blast(query_fa, db_prefix, out_path, short=use_short)

            st.session_state["df_results"] = df
            st.session_state["raw_results_path"] = str(out_path.resolve())
            st.session_state["mode"] = "PASTED"

            qh, ql, qs = peek_fasta(query_fa)
            sh, sl, ss = peek_fasta(subject_fa)
            st.success("BLAST complete (PASTED)!")
            st.caption(f"Query used:   {qh}  (len {ql}) → {qs}…")
            st.caption(f"Subject used: {sh}  (len {sl}) → {ss}…")
        except Exception as e:
            st.error(f"Error: {e}")

# Upload Tab
with tab_upload:
    st.subheader("Upload FASTA files")

    uq = st.file_uploader("Upload Query FASTA", type=["fa", "fasta", "txt"], key="up_q")
    us = st.file_uploader("Upload Subject FASTA (DB)", type=["fa", "fasta", "txt"], key="up_s")

    if st.button("Run BLAST (uploaded FASTA)"):
        try:
            if not uq or not us:
                st.error("Please upload both Query and Subject FASTA.")
                st.stop()

            query_fa   = WORK_DIR / "query_uploaded.fasta"
            subject_fa = WORK_DIR / "subject_uploaded.fasta"
            query_fa.write_bytes(uq.read())
            subject_fa.write_bytes(us.read())

            db_prefix = DB_DIR / "subject_db_uploaded"
            build_db(subject_fa, db_prefix)

            q_txt = query_fa.read_text(encoding="utf-8", errors="ignore")
            q_len = parse_fasta_len(q_txt)
            use_short = q_len <= 30

            out_path = RES_DIR / "blast_results_uploaded.txt"
            df = run_blast(query_fa, db_prefix, out_path, short=use_short)

            st.session_state["df_results"] = df
            st.session_state["raw_results_path"] = str(out_path.resolve())
            st.session_state["mode"] = "UPLOADED"

            qh, ql, qs = peek_fasta(query_fa)
            sh, sl, ss = peek_fasta(subject_fa)
            st.success("BLAST complete (UPLOADED)!")
            st.caption(f"Query used:   {qh}  (len {ql}) → {qs}…")
            st.caption(f"Subject used: {sh}  (len {sl}) → {ss}…")
        except Exception as e:
            st.error(f"Error: {e}")

# Clear Button
with st.container():
    if st.button("Clear previous results"):
        st.session_state["df_results"] = None
        st.session_state["raw_results_path"] = None
        st.session_state["mode"] = None
        st.rerun()

# Filters & Results
st.subheader("Filters")

colA, colB, colC = st.columns(3)
with colA:
    min_len = st.number_input("Min alignment length", min_value=0, value=0, step=1, key="min_len")
with colB:
    min_ident = st.number_input("Min % identity", min_value=0.0, value=0.0, step=0.1, format="%.2f", key="min_ident")
with colC:
    max_e_str = st.text_input("Max e-value (scientific or decimal)", value="1e6", key="max_e")

max_e = parse_evalue(max_e_str, 1e6)

st.subheader("Results")
mode = st.session_state.get("mode", "?")
raw_path = st.session_state.get("raw_results_path")
if raw_path:
    st.caption(f"Mode: **{mode}** — Raw results saved at: `{raw_path}`")

df = st.session_state.get("df_results")
if df is None:
    st.info("Run BLAST to see results here.")
else:
    df = df.copy()
    for c in NUMERIC_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    mask = (
        (df["length"] >= min_len) &
        (df["pident"] >= min_ident) &
        (df["evalue"] <= max_e)
    )
    df_filtered = df[mask].reset_index(drop=True)

    # User-friendly column names for display
    COLUMN_RENAME = {
        "qseqid":  "Query ID",
        "sseqid":  "Subject ID",
        "pident":  "% Identity",
        "length":  "Alignment Length",
        "mismatch": "Mismatches",
        "gapopen": "Gap Openings",
        "qstart":  "Query Start",
        "qend":    "Query End",
        "sstart":  "Subject Start",
        "send":    "Subject End",
        "evalue":  "E-value",
        "bitscore":"Bit Score",
    }
    df_display = df_filtered.rename(columns=lambda c: COLUMN_RENAME.get(c, c))

    if df_display.empty:
        st.info("No hits match the current filters.")
    else:
        st.dataframe(df_display, use_container_width=True)
        st.download_button(
            "Download filtered results (CSV)",
            data=df_display.to_csv(index=False),
            file_name="blast_filtered.csv",
            mime="text/csv",
        )
