# PIA_ONPREM
A personal intelligent Assistant (Full On premise)

This is the very basic of a personal intelligent assistant. you can make this agent more intelligent providing more web or document (txt/pdf) source 


create a virtual environment named .venv within the project folder PIA_ONPREM

UPDATE BASE DIR PATH IN 
	* main.py
	* ingest.py
	* scraper.py
	and the two modefile in model folder

activate the env calling .\.venv\Scripts\Activate.ps1 

install all required package from requirements.txt file.

download and place these files in the model folder:

llama-3.2-3b-instruct-q4_k_m.gguf
nomic-embed-text-v1.5.Q5_K_M.gguf


run srs/tools/scraper.py to collect raw data for the vector db

place all .txt or pdf file in the PIA_ONPREM\data\raw_docs folder 

run srs/tools/ingest.py to populate the vector db


finally run src/app.py

enjoy
