#### 🧬 BLAST Pipeline

This project provides a pipeline to run BLASTN searches from FASTA sequences and explore results in a Streamlit web app. It lets you manually paste or upload FASTA files, run BLAST, and filter results by alignment length, % identity, and e-value.



###### ***Requirements:***

1\. Gitbash for Windows (We’ll use Gitbash as the terminal) (https://git-scm.com/downloads/win)

2\. Micromamba (https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)

3\. NCBI BLAST+ executables (https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)


In Gitbash:
###### ***Setup for Windows:***

1\. Clone this repository

* git clone https://github.com/pushparajrane-byte/blast-pipeline.git



* cd blast-pipeline



2\. Create the environment

micromamba create -f environment-win.yml -y



3\. Activate it

micromamba activate blast



###### ***Run the App:***

* streamlit run app.py
* Choose Paste FASTA or Upload FASTA
* Click Run BLAST

###### ***Close the App:***
* Ctrl + C in Gitbash





