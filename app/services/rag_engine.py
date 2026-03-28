
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


#pre final version 

# import fitz
# import os
# import pytesseract
# from PIL import Image

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaLLM, OllamaEmbeddings
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# # ✅ Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# CHROMA_DIR = "data/chroma_db"


# # ✅ OCR + TEXT EXTRACTION
# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""

#     for page in doc:
#         page_text = page.get_text()

#         if not page_text.strip():  # OCR fallback
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)

#         text += page_text

#     doc.close()
#     print(f"Extracted {len(text)} characters from PDF")
#     return text


# # ✅ RULE-BASED POLICY TYPE (NO LLM)
# def detect_policy_type(text: str) -> str:
#     text_lower = text.lower()

#     if "package policy" in text_lower or "comprehensive" in text_lower or "section i" in text_lower:
#         return "Comprehensive"
#     elif "third party" in text_lower and "own damage" not in text_lower:
#         return "Third Party"
#     elif "own damage" in text_lower and "third party" not in text_lower:
#         return "Own Damage"
#     else:
#         return "Comprehensive"


# # ✅ BUILD VECTOR STORE
# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     if not text.strip():
#         raise ValueError("No text extracted from PDF")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_text(text)

#     if not chunks:
#         raise ValueError("No chunks created from PDF")

#     embeddings = OllamaEmbeddings(model="llama3.2:1b")

#     # ✅ FIX: Removed deletion of DB (no crash now)

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore, text  # ✅ FIX: no double extraction


# # ✅ ASK COVERAGE (STRICT CONTROL)
# def ask_coverage(question: str, vectorstore) -> str:
#     llm = OllamaLLM(
#         model="llama3.2:1b",
#         temperature=0  # ✅ removes randomness
#     )

#     retriever = vectorstore.as_retriever(
#         search_kwargs={"k": 3}
#     )

#     prompt = PromptTemplate.from_template(
#         "You are an insurance policy analyzer.\n"
#         "RULE 1: Answer ONLY using the policy context below.\n"
#         "RULE 2: If not clearly mentioned, say: NOT MENTIONED IN POLICY\n"
#         "RULE 3: Never guess. Never use outside knowledge.\n"
#         "RULE 4: Always start with YES or NO.\n\n"
#         "Policy Context:\n{context}\n\n"
#         "Question: {question}\n\n"
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


# # ✅ MAIN FUNCTION
# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore, full_text = build_vector_store(pdf_path)

#     policy_type = detect_policy_type(full_text)

#     coverage_results = []

#     # ✅ VALID CAUSES (IMPROVED)
#     valid_causes = ["accident", "fire", "flood", "riot", "theft"]

#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")
#         cause = damage.get("cause", "accident").lower()
#         severity = damage.get("severity", "unknown")

#         # ❌ Reject invalid causes
#         if cause not in valid_causes:
#             coverage_results.append({
#                 "part": part,
#                 "damage_type": damage_type,
#                 "cause": cause,
#                 "covered": False,
#                 "reason": f"Not covered — cause '{cause}' is excluded in policy."
#             })
#             continue

#         # ✅ Ask LLM
#         question = (
#             f"Under Section I (Own Damage), is {damage_type} damage "
#             f"to {part} caused by {cause} covered under this policy? "
#             f"Severity is {severity}."
#         )

#         answer = ask_coverage(question, vectorstore)

#         covered = answer.strip().upper().startswith("YES")

#         coverage_results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "cause": cause,
#             "covered": covered,
#             "reason": answer.strip()
#         })

#     covered_items = [r for r in coverage_results if r["covered"]]
#     excluded_items = [r for r in coverage_results if not r["covered"]]

#     return {
#         "policy_type": policy_type,
#         "total_damages": len(damages),
#         "covered_count": len(covered_items),
#         "excluded_count": len(excluded_items),
#         "coverage_details": coverage_results
#     }


# import fitz
# import os
# import pytesseract
# from PIL import Image

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaLLM, OllamaEmbeddings
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# CHROMA_DIR = "data/chroma_db"


# # -----------------------------
# # PDF TEXT EXTRACTION (OCR + TEXT)
# # -----------------------------
# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""

#     for page in doc:
#         page_text = page.get_text()

#         if not page_text.strip():
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)

#         text += page_text

#     doc.close()
#     return text


# # -----------------------------
# # POLICY TYPE DETECTION (RULE BASED)
# # -----------------------------
# def detect_policy_type(text: str) -> str:
#     text_lower = text.lower()

#     if "package policy" in text_lower or "comprehensive" in text_lower or "section i" in text_lower:
#         return "Comprehensive"
#     elif "third party" in text_lower and "own damage" not in text_lower:
#         return "Third Party"
#     elif "own damage" in text_lower and "third party" not in text_lower:
#         return "Own Damage"
#     else:
#         return "Comprehensive"


# # -----------------------------
# # VECTOR STORE
# # -----------------------------
# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     if not text.strip():
#         raise ValueError("No text extracted from PDF")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_text(text)

#     embeddings = OllamaEmbeddings(model="llama3.2:1b")

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore, text


# # -----------------------------
# # ASK COVERAGE (STRICT + STRUCTURED)
# # -----------------------------
# def ask_coverage(question: str, vectorstore) -> str:
#     llm = OllamaLLM(
#         model="llama3.2:1b",
#         temperature=0
#     )

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#     prompt = PromptTemplate.from_template(
#         "You are an insurance expert.\n"
#         "Answer ONLY using the policy.\n"
#         "Do NOT guess.\n\n"
#         "Context:\n{context}\n\n"
#         "Question: {question}\n\n"
#         "Return in this format:\n"
#         "Decision: YES or NO\n"
#         "Reason: explanation\n"
#         "Clause: section if available"
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


# # -----------------------------
# # MAIN FUNCTION
# # -----------------------------
# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore, full_text = build_vector_store(pdf_path)

#     policy_type = detect_policy_type(full_text)

#     coverage_results = []

#     valid_causes = ["accident", "fire", "flood", "riot", "theft"]

#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")
#         cause = damage.get("cause", "accident").lower()
#         severity = damage.get("severity", "unknown")
#         confidence = damage.get("confidence", 0)

#         if cause not in valid_causes:
#             coverage_results.append({
#                 "part": part,
#                 "covered": False,
#                 "reason": f"Invalid cause: {cause}"
#             })
#             continue

#         question = (
#             f"Is {damage_type} damage to {part} caused by {cause} covered "
#             f"under this policy?"
#         )

#         answer = ask_coverage(question, vectorstore)

#         covered = "YES" in answer.upper()

#         coverage_results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "cause": cause,
#             "severity": severity,
#             "confidence": confidence,
#             "covered": covered,
#             "explanation": answer
#         })

#     covered_items = [r for r in coverage_results if r["covered"]]
#     excluded_items = [r for r in coverage_results if not r["covered"]]

#     return {
#         "policy_type": policy_type,
#         "total_damages": len(damages),
#         "covered_count": len(covered_items),
#         "excluded_count": len(excluded_items),
#         "coverage_details": coverage_results
#     }



# import fitz
# import os
# import pytesseract
# from PIL import Image

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaLLM, OllamaEmbeddings
# from langchain_core.prompts import PromptTemplate

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# CHROMA_DIR = "data/chroma_db"


# # -----------------------------
# # PDF TEXT EXTRACTION (OCR + TEXT)
# # -----------------------------
# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""

#     for page in doc:
#         page_text = page.get_text()

#         # OCR fallback
#         if not page_text.strip():
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)

#         text += page_text

#     doc.close()
#     return text


# # -----------------------------
# # POLICY TYPE DETECTION
# # -----------------------------
# def detect_policy_type(text: str) -> str:
#     text_lower = text.lower()

#     if "package policy" in text_lower or "comprehensive" in text_lower or "section i" in text_lower:
#         return "Comprehensive"
#     elif "third party" in text_lower and "own damage" not in text_lower:
#         return "Third Party"
#     elif "own damage" in text_lower and "third party" not in text_lower:
#         return "Own Damage"
#     else:
#         return "Comprehensive"


# # -----------------------------
# # VECTOR STORE
# # -----------------------------
# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     if not text.strip():
#         raise ValueError("No text extracted from PDF")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_text(text)

#     embeddings = OllamaEmbeddings(model="llama3.2:1b")

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore, text


# # -----------------------------
# # ASK COVERAGE (STRICT + CONTROLLED)
# # -----------------------------
# def ask_coverage(question: str, vectorstore):
#     llm = OllamaLLM(model="llama3.2:1b", temperature=0)

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#     docs = retriever.invoke(question)

#     context = "\n\n".join([doc.page_content for doc in docs])
#     evidence = docs[0].page_content if docs else "No evidence found"

#     prompt = PromptTemplate.from_template(
#         "You are an insurance expert.\n"
#         "Use ONLY the context below.\n"
#         "Do NOT guess.\n"
#         "If not found, say: NOT MENTIONED\n\n"

#         "Context:\n{context}\n\n"
#         "Question: {question}\n\n"

#         "STRICT FORMAT:\n"
#         "Decision: YES or NO\n"
#         "Reason: exact explanation\n"
#         "Clause: mention section name"
#     )

#     formatted_prompt = prompt.format(context=context, question=question)

#     answer = llm.invoke(formatted_prompt)

#     return answer, evidence


# # -----------------------------
# # PARSE LLM OUTPUT
# # -----------------------------
# def parse_answer(answer: str):
#     answer_upper = answer.upper()

#     covered = "YES" in answer_upper and "NO" not in answer_upper

#     # Extract fields safely
#     reason = answer
#     clause = "Not specified"

#     lines = answer.split("\n")

#     for line in lines:
#         if "REASON" in line.upper():
#             reason = line.split(":", 1)[-1].strip()
#         if "CLAUSE" in line.upper():
#             clause = line.split(":", 1)[-1].strip()

#     return covered, reason, clause


# # -----------------------------
# # MAIN FUNCTION
# # -----------------------------
# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore, full_text = build_vector_store(pdf_path)

#     policy_type = detect_policy_type(full_text)

#     coverage_results = []

#     valid_causes = ["accident", "fire", "flood", "riot", "theft"]

#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")
#         cause = damage.get("cause", "accident").lower()
#         severity = damage.get("severity", "unknown")
#         confidence = damage.get("confidence", 0)

#         # Invalid cause handling
#         if cause not in valid_causes:
#             coverage_results.append({
#                 "part": part,
#                 "covered": False,
#                 "reason": f"Invalid cause: {cause}"
#             })
#             continue

#         question = (
#             f"Is {damage_type} damage to {part} caused by {cause} "
#             f"covered under this policy?"
#         )

#         answer, evidence = ask_coverage(question, vectorstore)

#         covered, reason, clause = parse_answer(answer)

#         coverage_results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "cause": cause,
#             "severity": severity,
#             "confidence": confidence,
#             "covered": covered,
#             "reason": reason,
#             "clause": clause,
#             "evidence": evidence[:300]  # trimmed
#         })

#     covered_items = [r for r in coverage_results if r["covered"]]
#     excluded_items = [r for r in coverage_results if not r["covered"]]

#     return {
#         "policy_type": policy_type,
#         "total_damages": len(damages),
#         "covered_count": len(covered_items),
#         "excluded_count": len(excluded_items),
#         "coverage_details": coverage_results
#     }

# import fitz
# import os
# import pytesseract
# from PIL import Image

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaLLM, OllamaEmbeddings
# from langchain_core.prompts import PromptTemplate

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# CHROMA_DIR = "data/chroma_db"


# # -----------------------------
# # PDF TEXT EXTRACTION (OCR + TEXT)
# # -----------------------------
# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""

#     for page in doc:
#         page_text = page.get_text()

#         if not page_text.strip():
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)

#         text += page_text

#     doc.close()
#     return text


# # -----------------------------
# # POLICY TYPE DETECTION
# # -----------------------------
# def detect_policy_type(text: str) -> str:
#     text_lower = text.lower()

#     if "package policy" in text_lower or "comprehensive" in text_lower or "section i" in text_lower:
#         return "Comprehensive"
#     elif "third party" in text_lower and "own damage" not in text_lower:
#         return "Third Party"
#     elif "own damage" in text_lower and "third party" not in text_lower:
#         return "Own Damage"
#     else:
#         return "Comprehensive"


# # -----------------------------
# # VECTOR STORE
# # -----------------------------
# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     if not text.strip():
#         raise ValueError("No text extracted from PDF")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_text(text)

#     embeddings = OllamaEmbeddings(model="llama3.2:1b")

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore, text


# # -----------------------------
# # ASK COVERAGE (BALANCED PROMPT)
# # -----------------------------
# def ask_coverage(question: str, vectorstore):
#     llm = OllamaLLM(model="llama3.2:1b", temperature=0)

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#     docs = retriever.invoke(question)

#     context = "\n\n".join([doc.page_content for doc in docs])
#     evidence = docs[0].page_content if docs else "No evidence found"

#     # ✅ FIXED PROMPT (IMPORTANT CHANGE)
#     prompt = PromptTemplate.from_template(
#         "You are an insurance expert.\n"
#         "Use the policy context to answer.\n"
#         "Apply general insurance rules.\n"
#         "Do NOT guess outside context.\n\n"

#         "IMPORTANT RULE:\n"
#         "If policy says 'accidental damage is covered',\n"
#         "then ALL accident-related damages are covered.\n\n"

#         "Context:\n{context}\n\n"
#         "Question: {question}\n\n"

#         "STRICT FORMAT:\n"
#         "Decision: YES or NO\n"
#         "Reason: explain based on policy meaning\n"
#         "Clause: mention section name"
#     )

#     formatted_prompt = prompt.format(context=context, question=question)

#     answer = llm.invoke(formatted_prompt)

#     return answer, evidence


# # -----------------------------
# # PARSE OUTPUT
# # -----------------------------
# def parse_answer(answer: str):
#     answer_upper = answer.upper()

#     covered = "YES" in answer_upper and "NO" not in answer_upper

#     reason = answer
#     clause = "Not specified"

#     lines = answer.split("\n")

#     for line in lines:
#         if "REASON" in line.upper():
#             reason = line.split(":", 1)[-1].strip()
#         if "CLAUSE" in line.upper():
#             clause = line.split(":", 1)[-1].strip()

#     return covered, reason, clause


# # -----------------------------
# # MAIN FUNCTION
# # -----------------------------
# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore, full_text = build_vector_store(pdf_path)

#     policy_type = detect_policy_type(full_text)

#     coverage_results = []

#     valid_causes = ["accident", "fire", "flood", "riot", "theft"]

#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")
#         cause = damage.get("cause", "accident").lower()
#         severity = damage.get("severity", "unknown")
#         confidence = damage.get("confidence", 0)

#         if cause not in valid_causes:
#             coverage_results.append({
#                 "part": part,
#                 "covered": False,
#                 "reason": f"Invalid cause: {cause}"
#             })
#             continue

#         question = (
#             f"Is {damage_type} damage to {part} caused by {cause} covered?"
#         )

#         answer, evidence = ask_coverage(question, vectorstore)

#         covered, reason, clause = parse_answer(answer)

#         coverage_results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "cause": cause,
#             "severity": severity,
#             "confidence": confidence,
#             "covered": covered,
#             "reason": reason,
#             "clause": clause,
#             "evidence": evidence[:300]
#         })

#     covered_items = [r for r in coverage_results if r["covered"]]
#     excluded_items = [r for r in coverage_results if not r["covered"]]

#     return {
#         "policy_type": policy_type,
#         "total_damages": len(damages),
#         "covered_count": len(covered_items),
#         "excluded_count": len(excluded_items),
#         "coverage_details": coverage_results
#     }

# import fitz
# import os
# import pytesseract
# from PIL import Image

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaLLM, OllamaEmbeddings

# # 🔥 SET YOUR TESSERACT PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# CHROMA_DIR = "data/chroma_db"


# # -----------------------------
# # 📄 EXTRACT TEXT (OCR + NORMAL)
# # -----------------------------
# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""

#     for page in doc:
#         page_text = page.get_text()

#         # If scanned → OCR
#         if not page_text.strip():
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)

#         text += page_text

#     doc.close()
#     return text


# # -----------------------------
# # 🧠 DETECT POLICY TYPE
# # -----------------------------
# def detect_policy_type(text: str) -> str:
#     t = text.lower()

#     if "package policy" in t or "comprehensive" in t:
#         return "Comprehensive"
#     elif "third party" in t and "own damage" not in t:
#         return "Third Party"
#     elif "own damage" in t:
#         return "Own Damage"
#     else:
#         return "Comprehensive"


# # -----------------------------
# # 📦 BUILD VECTOR STORE
# # -----------------------------
# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     if not text.strip():
#         raise ValueError("No text extracted from PDF")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_text(text)

#     embeddings = OllamaEmbeddings(model="llama3.2:1b")

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore, text


# # -----------------------------
# # 🔍 EXTRACT SECTION NAME FROM TEXT
# # -----------------------------
# def extract_section_name(text_chunk: str) -> str:
#     text_upper = text_chunk.upper()

#     if "SECTION I" in text_upper:
#         return "Section I - Own Damage"
#     elif "SECTION II" in text_upper:
#         return "Section II - Third Party Liability"
#     elif "SECTION III" in text_upper:
#         return "Section III - Personal Accident"
#     else:
#         return "Policy Section"


# # -----------------------------
# # 🤖 ASK COVERAGE (ANTI-HALLUCINATION PROMPT)
# # -----------------------------
# def ask_coverage(question: str, vectorstore):
#     llm = OllamaLLM(model="llama3.2:1b", temperature=0)

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
#     docs = retriever.invoke(question)

#     context = "\n\n".join([doc.page_content for doc in docs])
#     evidence = docs[0].page_content if docs else "No evidence found"

#     section = extract_section_name(evidence)

#     prompt = f"""
# You are an insurance policy analyst.

# STRICT RULES:
# - Answer ONLY using the given context
# - DO NOT invent clause numbers
# - DO NOT say "Clause 2.1" or similar
# - Use ONLY section names like "Section I", "Section II"
# - If not clearly mentioned → say "Not clearly specified"

# LOGIC RULE:
# If context contains "accidental external means"
# → treat it as accidental damage covered

# ---------------------

# Context:
# {context}

# Question:
# {question}

# ---------------------

# OUTPUT FORMAT:

# Decision: YES or NO
# Reason: Short explanation from context
# Section: {section}
# """

#     answer = llm.invoke(prompt)

#     return answer, evidence, section


# # -----------------------------
# # 🧾 PARSE OUTPUT SAFELY
# # -----------------------------
# def parse_answer(answer: str):
#     decision = "NO"
#     reason = "Not clear"
#     section = "Policy Section"

#     for line in answer.split("\n"):
#         line_upper = line.upper()

#         if "DECISION" in line_upper:
#             if "YES" in line_upper:
#                 decision = "YES"
#             elif "NO" in line_upper:
#                 decision = "NO"

#         elif "REASON" in line_upper:
#             reason = line.split(":", 1)[-1].strip()

#         elif "SECTION" in line_upper:
#             section = line.split(":", 1)[-1].strip()

#     covered = decision == "YES"

#     return covered, reason, section


# # -----------------------------
# # 🚀 MAIN FUNCTION
# # -----------------------------
# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore, full_text = build_vector_store(pdf_path)

#     policy_type = detect_policy_type(full_text)

#     results = []

#     valid_causes = ["accident", "fire", "flood", "theft", "riot"]

#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")
#         cause = damage.get("cause", "accident").lower()
#         severity = damage.get("severity", "unknown")
#         confidence = damage.get("confidence", 0)

#         # ❌ Invalid cause handling
#         if cause not in valid_causes:
#             results.append({
#                 "part": part,
#                 "covered": False,
#                 "reason": f"Invalid cause: {cause}"
#             })
#             continue

#         question = f"Is {damage_type} damage to {part} caused by {cause} covered?"

#         answer, evidence, section = ask_coverage(question, vectorstore)

#         covered, reason, section = parse_answer(answer)

#         clean_evidence = evidence.replace("\n", " ").strip()[:200]

#         results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "cause": cause,
#             "severity": severity,
#             "confidence": confidence,
#             "covered": covered,
#             "reason": reason,
#             "section": section,
#             "evidence": clean_evidence
#         })

#     covered_items = [r for r in results if r["covered"]]
#     excluded_items = [r for r in results if not r["covered"]]

#     return {
#         "policy_type": policy_type,
#         "total_damages": len(damages),
#         "covered_count": len(covered_items),
#         "excluded_count": len(excluded_items),
#         "coverage_details": results
#     }


# import fitz
# import os
# import re
# import pytesseract
# from PIL import Image

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaLLM, OllamaEmbeddings

# # ✅ SET TESSERACT PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# CHROMA_DIR = "data/chroma_db"


# # -----------------------------
# # 📄 TEXT EXTRACTION (OCR + NORMAL)
# # -----------------------------
# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""

#     for page in doc:
#         page_text = page.get_text()

#         if not page_text.strip():  # scanned PDF
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)

#         text += page_text

#     doc.close()
#     return text


# # -----------------------------
# # 🧠 POLICY TYPE DETECTION
# # -----------------------------
# def detect_policy_type(text: str) -> str:
#     t = text.lower()

#     if "package policy" in t or "comprehensive" in t:
#         return "Comprehensive"
#     elif "third party" in t and "own damage" not in t:
#         return "Third Party"
#     elif "own damage" in t:
#         return "Own Damage"
#     else:
#         return "Comprehensive"


# # -----------------------------
# # 📦 VECTOR STORE
# # -----------------------------
# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     if not text.strip():
#         raise ValueError("No text extracted from PDF")

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_text(text)

#     embeddings = OllamaEmbeddings(model="llama3.2:1b")

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore


# # -----------------------------
# # 🔍 REFERENCE DETECTION (CLAUSE / SECTION / HEADING)
# # -----------------------------
# def extract_reference(text_chunk: str) -> str:
#     text = text_chunk.strip()

#     # Try clause
#     clause_match = re.search(r"(Clause\s*\d+(\.\d+)*)", text, re.IGNORECASE)
#     if clause_match:
#         return clause_match.group(1)

#     # Try section
#     text_upper = text.upper()
#     if "SECTION I" in text_upper:
#         return "Section I - Own Damage"
#     elif "SECTION II" in text_upper:
#         return "Section II - Third Party Liability"
#     elif "SECTION III" in text_upper:
#         return "Section III - Personal Accident"

#     # fallback heading
#     return text.split("\n")[0][:80]


# # -----------------------------
# # 🔎 GET CLEAN EVIDENCE LINE
# # -----------------------------
# def extract_evidence(text_chunk: str) -> str:
#     lines = text_chunk.split("\n")

#     for line in lines:
#         if "accidental" in line.lower():
#             return line.strip()

#     return lines[0].strip()


# # -----------------------------
# # 🤖 ASK MODEL (STRICT + BALANCED)
# # -----------------------------
# def ask_llm(question: str, context: str) -> str:
#     llm = OllamaLLM(model="llama3.2:1b", temperature=0)

#     prompt = f"""
# You are an insurance expert.

# STRICT RULES:
# - Use ONLY the context
# - DO NOT invent anything
# - If clearly covered → YES
# - If clearly excluded → NO
# - If unclear → NOT CLEAR

# IMPORTANT LOGIC:
# "accidental external means" = covered

# Context:
# {context}

# Question:
# {question}

# Answer format:
# Decision: YES or NO or NOT CLEAR
# Reason: one line explanation
# """

#     return llm.invoke(prompt)


# # -----------------------------
# # 🧾 PARSE OUTPUT (SAFE)
# # -----------------------------
# def parse_answer(answer: str):
#     decision = "NOT CLEAR"
#     reason = "Not clear"

#     for line in answer.split("\n"):
#         line_upper = line.upper()

#         if "YES" in line_upper:
#             decision = "YES"
#         elif "NO" in line_upper:
#             decision = "NO"

#         if "REASON" in line_upper:
#             reason = line.split(":", 1)[-1].strip()

#     return decision, reason


# # -----------------------------
# # 🚀 MAIN FUNCTION
# # -----------------------------
# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore = build_vector_store(pdf_path)

#     results = []

#     valid_causes = ["accident", "fire", "flood", "theft", "riot"]

#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")
#         cause = damage.get("cause", "accident").lower()
#         severity = damage.get("severity", "unknown")
#         confidence = damage.get("confidence", 0)

#         if cause not in valid_causes:
#             results.append({
#                 "part": part,
#                 "covered": False,
#                 "reason": f"Invalid cause: {cause}"
#             })
#             continue

#         question = f"Is {damage_type} damage to {part} caused by {cause} covered?"

#         # retrieve
#         retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
#         docs = retriever.invoke(question)

#         context = "\n\n".join([doc.page_content for doc in docs])
#         top_chunk = docs[0].page_content if docs else ""

#         # LLM decision
#         answer = ask_llm(question, context)
#         decision, reason = parse_answer(answer)

#         # final fields
#         reference = extract_reference(top_chunk)
#         evidence = extract_evidence(top_chunk)

#         results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "cause": cause,
#             "severity": severity,
#             "confidence": confidence,
#             "covered": decision == "YES",
#             "reason": reason,
#             "reference": reference,
#             "evidence": evidence
#         })

#     covered_items = [r for r in results if r["covered"]]
#     excluded_items = [r for r in results if not r["covered"]]

#     return {
#         "total_damages": len(damages),
#         "covered_count": len(covered_items),
#         "excluded_count": len(excluded_items),
#         "coverage_details": results
#     }


# import fitz
# import os
# import re
# import pytesseract
# from PIL import Image

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaLLM, OllamaEmbeddings

# # ✅ SET TESSERACT PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# CHROMA_DIR = "data/chroma_db"


# # -----------------------------
# # 📄 TEXT EXTRACTION (OCR + CLEAN)
# # -----------------------------
# def extract_text_from_pdf(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)
#     text = ""

#     for page in doc:
#         page_text = page.get_text()

#         if not page_text.strip():
#             pix = page.get_pixmap()
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#             img = img.convert("L")
#             page_text = pytesseract.image_to_string(img)

#         text += page_text + "\n"

#     doc.close()

#     # 🔥 CLEAN OCR NOISE
#     text = re.sub(r'\s+', ' ', text)
#     return text


# # -----------------------------
# # 📦 VECTOR STORE
# # -----------------------------
# def build_vector_store(pdf_path: str):
#     text = extract_text_from_pdf(pdf_path)

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_text(text)

#     embeddings = OllamaEmbeddings(model="llama3.2:1b")

#     vectorstore = Chroma.from_texts(
#         texts=chunks,
#         embedding=embeddings,
#         persist_directory=CHROMA_DIR
#     )

#     return vectorstore


# # -----------------------------
# # 🔍 REFERENCE DETECTION (STRONG)
# # -----------------------------
# def extract_reference(text: str) -> str:
#     t = text.upper()

#     if "SECTION I" in t:
#         return "Section I - Own Damage"
#     elif "SECTION II" in t:
#         return "Section II - Third Party Liability"
#     elif "SECTION III" in t:
#         return "Section III - Personal Accident"

#     return "Policy Document"


# # -----------------------------
# # 🔎 CLEAN EVIDENCE EXTRACTION
# # -----------------------------
# def extract_evidence(text: str) -> str:
#     text_lower = text.lower()

#     # 🎯 PRIORITY MATCH
#     if "accidental external means" in text_lower:
#         return "by accidental external means"

#     if "fire" in text_lower:
#         return "damage caused by fire"

#     if "theft" in text_lower:
#         return "damage caused by theft"

#     # fallback → first meaningful line
#     lines = text.split(".")
#     for line in lines:
#         if len(line.strip()) > 20:
#             return line.strip()

#     return text[:100]


# # -----------------------------
# # 🤖 LLM (STRICT + CONTROLLED)
# # -----------------------------
# def ask_llm(question: str, context: str) -> str:
#     llm = OllamaLLM(model="llama3.2:1b", temperature=0)

#     prompt = f"""
# You are an insurance expert.

# STRICT RULES:
# - Use ONLY the context
# - DO NOT guess
# - If clearly covered → YES
# - If clearly excluded → NO
# - If unclear → NOT CLEAR

# IMPORTANT:
# "accidental external means" = covered

# Context:
# {context}

# Question:
# {question}

# Answer format:
# Decision: YES or NO or NOT CLEAR
# Reason: short explanation
# """

#     return llm.invoke(prompt)


# # -----------------------------
# # 🧾 PARSE OUTPUT
# # -----------------------------
# def parse_answer(answer: str):
#     decision = "NOT CLEAR"
#     reason = "Not clear"

#     for line in answer.split("\n"):
#         line_upper = line.upper()

#         if "YES" in line_upper:
#             decision = "YES"
#         elif "NO" in line_upper:
#             decision = "NO"

#         if "REASON" in line_upper:
#             reason = line.split(":", 1)[-1].strip()

#     return decision, reason


# # -----------------------------
# # 🚀 MAIN FUNCTION
# # -----------------------------
# def check_coverage(pdf_path: str, damages: list) -> dict:
#     vectorstore = build_vector_store(pdf_path)

#     results = []

#     for damage in damages:
#         part = damage.get("part", "")
#         damage_type = damage.get("damage_type", "")
#         cause = damage.get("cause", "accident").lower()
#         severity = damage.get("severity", "unknown")
#         confidence = damage.get("confidence", 0)

#         question = f"Is {damage_type} damage to {part} caused by {cause} covered?"

#         retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
#         docs = retriever.invoke(question)

#         context = "\n\n".join([doc.page_content for doc in docs])
#         top_chunk = docs[0].page_content if docs else ""

#         # 🤖 LLM decision
#         answer = ask_llm(question, context)
#         decision, reason = parse_answer(answer)

#         # 🔍 Clean reference + evidence
#         reference = extract_reference(top_chunk)
#         evidence = extract_evidence(top_chunk)

#         results.append({
#             "part": part,
#             "damage_type": damage_type,
#             "cause": cause,
#             "severity": severity,
#             "confidence": confidence,
#             "covered": decision == "YES",
#             "reason": reason,
#             "reference": reference,
#             "evidence": evidence
#         })

#     covered_items = [r for r in results if r["covered"]]
#     excluded_items = [r for r in results if not r["covered"]]

#     return {
#         "total_damages": len(damages),
#         "covered_count": len(covered_items),
#         "excluded_count": len(excluded_items),
#         "coverage_details": results
#     }



import fitz
import os
import re
import pytesseract
from PIL import Image

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM, OllamaEmbeddings

# ✅ Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

CHROMA_DIR = "data/chroma_db"


# -----------------------------
# 📄 TEXT EXTRACTION (OCR + CLEAN)
# -----------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        page_text = page.get_text()

        if not page_text.strip():
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.convert("L")
            page_text = pytesseract.image_to_string(img)

        text += page_text + "\n"

    doc.close()

    text = re.sub(r'\s+', ' ', text)
    return text


# -----------------------------
# 📦 VECTOR STORE
# -----------------------------
def build_vector_store(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    embeddings = OllamaEmbeddings(model="llama3.2:1b")

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    return vectorstore


# -----------------------------
# 🔍 REFERENCE EXTRACTION
# -----------------------------
def extract_reference(text: str) -> str:
    t = text.upper()

    if "SECTION I" in t:
        return "Section I - Own Damage"
    elif "SECTION II" in t:
        return "Section II - Third Party Liability"
    elif "SECTION III" in t:
        return "Section III - Personal Accident"

    return "Policy Document"


# -----------------------------
# 🔎 DEEP EVIDENCE EXTRACTION (FINAL FIX)
# -----------------------------
def extract_evidence(text: str, cause: str) -> str:
    text_lower = text.lower()

    sentences = re.split(r'[.!?]', text)

    relevant_sentences = []

    # 🎯 Match sentences based on cause
    for sent in sentences:
        s = sent.strip()

        if len(s) < 25:
            continue

        # Avoid OCR garbage
        if re.search(r'[^a-zA-Z0-9\s,.-]', s):
            continue

        if cause == "accident" and "accident" in s.lower():
            relevant_sentences.append(s)

        elif cause == "accident" and "accidental external means" in s.lower():
            relevant_sentences.append(s)

        elif cause == "fire" and "fire" in s.lower():
            relevant_sentences.append(s)

        elif cause == "theft" and "theft" in s.lower():
            relevant_sentences.append(s)

    # ✅ If good matches found → return top 2–3 sentences
    if relevant_sentences:
        return ". ".join(relevant_sentences[:3]).strip()

    # fallback → meaningful clean lines
    clean_lines = []
    for sent in sentences:
        s = sent.strip()

        if len(s) > 40 and not re.search(r'[^a-zA-Z0-9\s,.-]', s):
            clean_lines.append(s)

    if clean_lines:
        return ". ".join(clean_lines[:2]).strip()

    return "Not clearly specified in policy"


# -----------------------------
# 🤖 LLM (BALANCED)
# -----------------------------
def ask_llm(question: str, context: str) -> str:
    llm = OllamaLLM(model="llama3.2:1b", temperature=0)

    prompt = f"""
You are an expert in motor insurance.

Rules:
- Use ONLY the context
- Do NOT assume anything outside context
- YES = clearly covered
- NO = clearly excluded
- NOT CLEAR = insufficient info

Important:
Accidental external means → covered

Context:
{context}

Question:
{question}

Answer format:
Decision: YES or NO or NOT CLEAR
Reason: clear explanation
"""

    return llm.invoke(prompt)


# -----------------------------
# 🧾 PARSE
# -----------------------------
def parse_answer(answer: str):
    decision = "NOT CLEAR"
    reason = "Not clear"

    for line in answer.split("\n"):
        line_upper = line.upper()

        if "YES" in line_upper:
            decision = "YES"
        elif "NO" in line_upper:
            decision = "NO"

        if "REASON" in line_upper:
            reason = line.split(":", 1)[-1].strip()

    return decision, reason


# -----------------------------
# 🚀 MAIN
# -----------------------------
def check_coverage(pdf_path: str, damages: list) -> dict:
    vectorstore = build_vector_store(pdf_path)

    results = []

    for damage in damages:
        part = damage.get("part", "")
        damage_type = damage.get("damage_type", "")
        cause = damage.get("cause", "accident").lower()
        severity = damage.get("severity", "unknown")
        confidence = damage.get("confidence", 0)

        question = f"Is {damage_type} damage to {part} caused by {cause} covered?"

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(question)

        context = "\n\n".join([doc.page_content for doc in docs])
        top_chunk = docs[0].page_content if docs else ""

        answer = ask_llm(question, context)
        decision, reason = parse_answer(answer)

        reference = extract_reference(top_chunk)
        evidence = extract_evidence(top_chunk, cause)

        results.append({
            "part": part,
            "damage_type": damage_type,
            "cause": cause,
            "severity": severity,
            "confidence": confidence,
            "covered": decision == "YES",
            "reason": reason,
            "reference": reference,
            "evidence": evidence
        })

    covered_items = [r for r in results if r["covered"]]
    excluded_items = [r for r in results if not r["covered"]]

    return {
        "total_damages": len(damages),
        "covered_count": len(covered_items),
        "excluded_count": len(excluded_items),
        "coverage_details": results
    }git