import sys
from pathlib import Path

import streamlit as st


# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.indexing import process_documents
from app.rag_pipeline import ask_question


st.set_page_config(
    page_title="Local RAG",
)

st.title("Local RAG")

st.write("Documents should be placed in `watch_folder/`.")


if st.button("Process Documents"):
    with st.spinner("Processing documents..."):
        result = process_documents()

    st.success("Documents processed successfully.")

    st.write(f"Documents: {result['documents']}")
    st.write(f"Chunks: {result['chunks']}")
    st.write(f"Vectors: {result['vectors']}")


st.divider()

st.subheader("Ask a question")

question = st.text_input(
    "Question",
    placeholder="Ask something about your documents...",
)


if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            result = ask_question(
                question,
                top_k=3,
            )

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")

        for source in result["sources"]:
            metadata = source["metadata"]

            st.write(
                f"**{metadata.get('source')}** "
                f"(distance: {source['distance']:.4f})"
            )