#### 🧬 BLAST Pipeline

This project provides a pipeline to run BLASTN searches from Nucleotide sequences and explore results in a Streamlit web app. It lets you manually paste or upload FASTA files, run BLAST, and filter results by alignment length, % identity, and e-value.



###### ***Requirements:***

1\. Gitbash for Windows (We’ll use Gitbash as the terminal) (https://git-scm.com/downloads/win)

2\. Micromamba (https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)

3\. NCBI BLAST+ executables (https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)


###### ***Setup for Windows in Gitbash:***

1\. Clone this repository

git clone https://github.com/pushparajrane-byte/blast-pipeline.git


cd blast-pipeline

>All further steps are to be done in blast-pipeline folder


2\. Create the environment in blast-pipeline in Gitbash

micromamba create -f environment-win.yml -y


3\. Activate it the environment in Gitbash

micromamba activate blast



###### ***Run the App in Gitbash:*** (Whenever one wants to run the app, they should open Gitbash in the blast_pipeline folder)

streamlit run app.py

 
* Choose Paste FASTA or Upload FASTA
* Click Run BLAST


###### ***Stop the App in Gitbash:***
Ctrl + c in Gitbash

###### ***FASTA File Requirements***
1\. When pasting or uploading FASTA files, please ensure:
Each sequence must begin with a header line starting with >.

Example:>sequence1

ATGCCGTAGCTAGCTAGCTA

2\. Do not leave empty lines before the first header.



3\. No spaces before >, the first character of the file should be > and the sequence should be on the second line.



4\. Sequences can be wrapped across multiple lines, but should only contain valid nucleotide letters (A, T, G, C, N). N = any nucleotide (A, T, G, or C), completely unknown base.



5\. Save the file in plain text format (.fasta, .fa, .txt) without formatting (avoid MS Word etc.).

⚠️Important: Please do not place the blast-pipeline folder in a path with spaces (e.g. C:\Users\Name\Desktop\New folder\). BLAST tools can fail with paths containing spaces. Instead, use a path without spaces, such as C:\Users\Name\blast-pipeline\.


###### ***Screenshots and video demo:***
Video demo: https://youtu.be/rZDzWSxP8LQ


Screenshots: 
1\. Main page: <img width="2468" height="1208" alt="blastpipeline_main" src="https://github.com/user-attachments/assets/95070c87-fa3f-4b12-b6cf-6b7a2007b762" />



2\. Paste FASTA results: <img width="2465" height="1189" alt="paste_FASTA_results" src="https://github.com/user-attachments/assets/f5d886ea-636b-4cc6-a5a8-5e8536fc4fa6" />



3\. Upload FASTA results: <img width="2478" height="1225" alt="upload_FASTA_results" src="https://github.com/user-attachments/assets/bbea2538-6e70-4f64-9e20-93d6c4568a5a" />


























