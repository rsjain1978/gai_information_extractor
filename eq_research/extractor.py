import openai
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import itertools

from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader, UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.callbacks import get_openai_callback

from kor import extract_from_documents, from_pydantic, create_extraction_chain

from schema import eq_schema

# Replace with your OpenAI API key
load_dotenv(find_dotenv())

# Replace with your OpenAI API key
api_key = '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'

def load_pdf_document(document_name):
    loader = PyPDFLoader(document_name)
    splitter = CharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=0,
        length_function=len
    )
    docs = loader.load_and_split(text_splitter=splitter)
    # print (docs)
    return docs

def load_text_document(document_name):
    loader = UnstructuredFileLoader(document_name)
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0,
        length_function=len
    )
    docs = loader.load_and_split(text_splitter=splitter)
    return docs

async def extract_information(docs):

    # Using gpt-3.5-turbo which is pretty cheap, but has worse quality
    llm = ChatOpenAI(temperature=0,
                     model='gpt-3.5-turbo',
                     openai_api_key=api_key)

    chain = create_extraction_chain(
        llm,
        eq_schema.schema,
        encoder_or_encoder_class="json",
        validator=eq_schema.extraction_validator,
        input_formatter=None,
    )

    with get_openai_callback() as cb:
        document_extraction_results = await extract_from_documents(
            chain, 
            docs, 
            max_concurrency=5, 
            use_uid=False, 
            return_exceptions=True
        )
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")    

        print (document_extraction_results)
        # validated_data = list(
        #     itertools.chain.from_iterable(
        #         extraction["validated_data"] for extraction in document_extraction_results
        #     )
        # )
        # validated_data = [d for d in document_extraction_results if d['validated_data'] and not d['errors']]
        validated_data = list(
            itertools.chain.from_iterable(
                extraction["validated_data"]
                for extraction in document_extraction_results
                if not isinstance(extraction, BaseException) and "validated_data" in extraction
            )
        )

        df = df = pd.DataFrame([record.dict() for record in validated_data])
        return df
    
print ('Reading document')
chunks = load_pdf_document("./data/input/morning_star_equity_research_report.pdf")

import asyncio
esg_info = None
try:
    print ('Extracting information')
    esg_info = asyncio.run(extract_information(chunks))
    esg_info.to_csv("./data/output/raw/eq_research_information-tmp.csv",index=False)
except RuntimeError:    
    print ('Exception occured!')
    esg_info.to_csv("./data/output/raw/eq_research_information-tmp.csv",index=False)