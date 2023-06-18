#!/usr/bin/env python
import os
os.environ['OPENAI_API_KEY'] = "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"

import logging
import sys
import requests
from pathlib import Path

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from llama_index import GPTVectorStoreIndex, download_loader


PDFReader = download_loader("PDFReader")
loader = PDFReader()
documents = loader.load_data(file=Path('./reference.pdf')) # this needs to be saved to a common name and
# into a directory we can access

index = GPTVectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# here we need to change the string based on the queries entered
# site should error if no queries
query = "What is the"

for i in range(len(queries)):
    if (i == len(queries) - 1) :
        query = query + " and"
    query = query + " " + item
query = query + " in the text" 
response = query_engine.query(query)




