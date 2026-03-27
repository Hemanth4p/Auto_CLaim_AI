# import fitz
# import os
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_ollama import OllamaLLM
# from langchain.chains import RetrievalQA

# CHROMA_DIR = "data/chroma_db"


# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text


# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )
#     chunks = splitter.split_text(text)

#     embeddings = SentenceTransformerEmbeddings(
#         model_name="all-MiniLM-L6-v2"
#     )

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore


# def ask_policy(question: str, vectorstore) -> str:
#     llm = OllamaLLM(model="llama3.2:1b")

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=vectorstore.as_retriever(
#             search_kwargs={"k": 3}
#         )
#     )

#     result = qa_chain.invoke({"query": question})
#     return result["result"]


# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore = build_vector_store(pdf_path)

#     policy_type_answer = ask_policy(
#         "What type of insurance policy is this? "
#         "Is it first party, third party, or comprehensive?",
#         vectorstore
#     )

#     coverage_results = []
#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")

#         question = (
#             f"Is {part} {damage_type} damage covered "
#             f"under this insurance policy? "
#             f"Answer yes or no and give the reason."
#         )

#         answer = ask_policy(question, vectorstore)

#         coverage_results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "covered": "yes" in answer.lower(),
#             "reason": answer
#         })

#     covered = [r for r in coverage_results if r["covered"]]
#     excluded = [r for r in coverage_results if not r["covered"]]

#     return {
#         "policy_type": policy_type_answer,
#         "total_damages": len(damages),
#         "covered_count": len(covered),
#         "excluded_count": len(excluded),
#         "coverage_details": coverage_results
#     }

# import fitz
# import os
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# CHROMA_DIR = "data/chroma_db"


# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text


# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )
#     chunks = splitter.split_text(text)

#     embeddings = SentenceTransformerEmbeddings(
#         model_name="all-MiniLM-L6-v2"
#     )

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore


# def ask_policy(question: str, vectorstore) -> str:
#     llm = OllamaLLM(model="llama3.2:1b")

#     retriever = vectorstore.as_retriever(
#         search_kwargs={"k": 3}
#     )

#     prompt = PromptTemplate.from_template(
#         "Use the following policy context to answer the question.\n"
#         "Context: {context}\n"
#         "Question: {question}\n"
#         "Answer:"
#     )

#     def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)

#     chain = (
#         {
#             "context": retriever | format_docs,
#             "question": RunnablePassthrough()
#         }
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     return chain.invoke(question)


# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore = build_vector_store(pdf_path)

#     policy_type_answer = ask_policy(
#         "What type of insurance policy is this? "
#         "Is it first party, third party, or comprehensive?",
#         vectorstore
#     )

#     coverage_results = []
#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")

#         question = (
#             f"Is {part} {damage_type} damage covered "
#             f"under this insurance policy? "
#             f"Answer yes or no and give the reason."
#         )

#         answer = ask_policy(question, vectorstore)

#         coverage_results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "covered": "yes" in answer.lower(),
#             "reason": answer
#         })

#     covered = [r for r in coverage_results if r["covered"]]
#     excluded = [r for r in coverage_results if not r["covered"]]

#     return {
#         "policy_type": policy_type_answer,
#         "total_damages": len(damages),
#         "covered_count": len(covered),
#         "excluded_count": len(excluded),
#         "coverage_details": coverage_results
#     }


# import fitz
# import os
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaLLM, OllamaEmbeddings
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# CHROMA_DIR = "data/chroma_db"


# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     doc.close()
#     return text


# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     if not text.strip():
#         raise ValueError("PDF is empty or could not be read")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )
#     chunks = splitter.split_text(text)

#     if not chunks:
#         raise ValueError("No text chunks created from PDF")

#     embeddings = OllamaEmbeddings(model="llama3.2:1b")

#     if os.path.exists(CHROMA_DIR):
#         import shutil
#         shutil.rmtree(CHROMA_DIR)

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore


# def ask_policy(question: str, vectorstore) -> str:
#     llm = OllamaLLM(model="llama3.2:1b")

#     retriever = vectorstore.as_retriever(
#         search_kwargs={"k": 3}
#     )

#     prompt = PromptTemplate.from_template(
#         "Use the following insurance policy context to answer.\n"
#         "Context: {context}\n"
#         "Question: {question}\n"
#         "Give a clear yes or no answer with reason:"
#     )

#     def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)

#     chain = (
#         {
#             "context": retriever | format_docs,
#             "question": RunnablePassthrough()
#         }
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     return chain.invoke(question)


# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore = build_vector_store(pdf_path)

#     policy_type_answer = ask_policy(
#         "What type of insurance policy is this? "
#         "Is it first party, third party, or comprehensive?",
#         vectorstore
#     )

#     coverage_results = []
#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")

#         question = (
#             f"Is {part} {damage_type} damage covered "
#             f"under this insurance policy? "
#             f"Answer yes or no with reason."
#         )

#         answer = ask_policy(question, vectorstore)

#         coverage_results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "covered": "yes" in answer.lower(),
#             "reason": answer
#         })

#     covered = [r for r in coverage_results if r["covered"]]
#     excluded = [r for r in coverage_results if not r["covered"]]

#     return {
#         "policy_type": policy_type_answer,
#         "total_damages": len(damages),
#         "covered_count": len(covered),
#         "excluded_count": len(excluded),
#         "coverage_details": coverage_results
#     }


#final version 


import fitz
import os
import pytesseract
from PIL import Image

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ✅ Tesseract path (important)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

CHROMA_DIR = "data/chroma_db"


# ✅ HYBRID TEXT EXTRACTION (TEXT + OCR)
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        # Step 1: Try normal extraction
        page_text = page.get_text()

        # Step 2: If empty → OCR
        if not page_text.strip():
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Improve OCR accuracy
            img = img.convert("L")

            page_text = pytesseract.image_to_string(img)

        text += page_text

    doc.close()

    print("TEXT LENGTH:", len(text))  # Debug
    return text


# ✅ BUILD VECTOR STORE
def build_vector_store(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        raise ValueError("❌ No text extracted from PDF")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    if not chunks:
        raise ValueError("❌ No text chunks created from PDF")

    embeddings = OllamaEmbeddings(model="llama3.2:1b")

    # ❌ REMOVED shutil.rmtree (was causing crash)

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    return vectorstore


# ✅ ASK POLICY QUESTIONS
def ask_policy(question: str, vectorstore) -> str:
    llm = OllamaLLM(model="llama3.2:1b")

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    prompt = PromptTemplate.from_template(
        "Use the following insurance policy context to answer.\n"
        "Context: {context}\n"
        "Question: {question}\n"
        "Give a clear yes or no answer with reason:"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(question)


# ✅ MAIN FUNCTION
def check_coverage(pdf_path: str, damages: list) -> dict:
    vectorstore = build_vector_store(pdf_path)

    policy_type_answer = ask_policy(
        "What type of insurance policy is this? "
        "Is it first party, third party, or comprehensive?",
        vectorstore
    )

    coverage_results = []

    for damage in damages:
        part = damage.get("part", "")
        damage_type = damage.get("damage_type", "")

        question = (
            f"Is {part} {damage_type} damage covered "
            f"under this insurance policy? "
            f"Answer yes or no with reason."
        )

        answer = ask_policy(question, vectorstore)

        coverage_results.append({
            "part": part,
            "damage_type": damage_type,
            "covered": "yes" in answer.lower(),
            "reason": answer
        })

    covered = [r for r in coverage_results if r["covered"]]
    excluded = [r for r in coverage_results if not r["covered"]]

    return {
        "policy_type": policy_type_answer,
        "total_damages": len(damages),
        "covered_count": len(covered),
        "excluded_count": len(excluded),
        "coverage_details": coverage_results
    }