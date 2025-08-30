#### 🧬 BLAST Pipeline

This project provides a pipeline to run BLASTN searches from Nucleotide sequences and explore results in a Streamlit web app. It lets you manually paste or upload FASTA files, run BLAST, and filter results by alignment length, % identity, and e-value.



###### ***Requirements:***

1\. Gitbash for Windows (We’ll use Gitbash as the terminal) (https://git-scm.com/downloads/win)

2\. Micromamba (https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)

3\. NCBI BLAST+ executables (https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)


###### ***Setup for Windows in Gitbash:***

1\. Clone this repository

* git clone https://github.com/pushparajrane-byte/blast-pipeline.git



* cd blast-pipeline

>All further steps are to be done in blast-pipeline folder


2\. Create the environment in blast-pipeline in Gitbash

micromamba create -f environment-win.yml -y


3\. Activate it the environment in Gitbash

micromamba activate blast



###### ***Run the App in Gitbash:*** (Whenever one wants to run the app, they should open Gitbash in the blast_pipeline folder)

* streamlit run app.py
* Choose Paste FASTA or Upload FASTA
* Click Run BLAST


###### ***Stop the App in Gitbash:***
* Ctrl + c in Gitbash

###### ***FASTA File Requirements***
1\. When pasting or uploading FASTA files, please ensure:
Each sequence must begin with a header line starting with >.

Example:>sequence1

ATGCCGTAGCTAGCTAGCTA

2\. Do not leave empty lines before the first header.



3\. No spaces before >, the first character of the file should be > and the sequence should be on the second line.



4\. Sequences can be wrapped across multiple lines, but should only contain valid nucleotide letters (A, T, G, C, N). N = any nucleotide (A, T, G, or C), completely unknown base.



5\. Save the file in plain text format (.fasta, .fa, .txt) without formatting (avoid MS Word etc.).




















