from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import yaml 
import pandas as pd

def generation(retriever, prompt_path, resume_path):
    # llm load
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # user prompt(resume) load
    with open (resume_path, "r") as file:
        resume = file.read()
        
    # prompt load
    with open(prompt_path, 'r') as file:
        prompt_data = yaml.safe_load(file)

    # prompt load
    task = "resume alignment evaluation"
    prompt_template = prompt_data['prompts'][task]['prompt_template']
    prompt = PromptTemplate.from_template(prompt_template)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(resume)
    return answer

def format_docs(docs):
    """doc의 metadata에 저장되어있는 원본 description을 가져오기"""

    df = pd.read_csv('./data/preprocessed/USA_jobs_total.csv')
    retrival_origin_jd = []
    doc_list = set([doc.metadata['index'] for doc in docs])

    for doc_idx in doc_list:
        jd = df.loc[df["index"] == doc_idx, 'description'].iloc[0]
        retrival_origin_jd.append(jd)

    return retrival_origin_jd[0] # top 1


    