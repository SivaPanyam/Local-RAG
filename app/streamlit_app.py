import sys
from pathlib import Path

import streamlit as st


# --------------------------------------------------
# Project path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.indexing import process_documents
from app.rag_pipeline import ask_question


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Local RAG",
    page_icon="🧠",
    layout="wide",
)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "indexing_complete" not in st.session_state:
    st.session_state.indexing_complete = False

if "indexing_result" not in st.session_state:
    st.session_state.indexing_result = None


# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stage-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        margin: 25px 0;
    }

    .stage {
        flex: 1;
        padding: 18px 10px;
        border-radius: 14px;
        border: 1px solid #333842;
        text-align: center;
        background: #15171d;
        transition: all 0.3s ease;
    }

    .stage.active {
        border-color: #4c9aff;
        box-shadow: 0 0 18px rgba(76, 154, 255, 0.35);
        animation: pulse 1.5s infinite;
    }

    .stage.complete {
        border-color: #31c48d;
        box-shadow: 0 0 10px rgba(49, 196, 141, 0.15);
    }

    .stage-icon {
        font-size: 30px;
        margin-bottom: 8px;
    }

    .stage-title {
        font-weight: 600;
        font-size: 15px;
    }

    .stage-status {
        font-size: 12px;
        opacity: 0.7;
        margin-top: 5px;
    }

    .arrow {
        font-size: 24px;
        opacity: 0.5;
    }

    .processing-status {
        padding: 12px 16px;
        border-radius: 10px;
        background: #15171d;
        border: 1px solid #30343d;
        margin-top: 15px;
    }

    .complete-status {
        padding: 12px 16px;
        border-radius: 10px;
        background: #101c17;
        border: 1px solid #31c48d;
        margin-top: 15px;
    }

    @keyframes pulse {

        0% {
            box-shadow: 0 0 8px rgba(76, 154, 255, 0.2);
        }

        50% {
            box-shadow: 0 0 25px rgba(76, 154, 255, 0.55);
        }

        100% {
            box-shadow: 0 0 8px rgba(76, 154, 255, 0.2);
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("Local RAG")

st.write(
    "Ask questions about your local documents."
)


# --------------------------------------------------
# Document Processing
# --------------------------------------------------

st.subheader("Document Processing")

st.write(
    "Documents should be placed in `watch_folder/`."
)


# --------------------------------------------------
# Persistent UI placeholders
# --------------------------------------------------

pipeline_placeholder = st.empty()

progress_placeholder = st.empty()

status_placeholder = st.empty()


# --------------------------------------------------
# Pipeline stages
# --------------------------------------------------

stages = [
    ("loading", "📄", "Loading PDFs"),
    ("chunking", "✂️", "Creating Chunks"),
    ("embedding", "🧠", "Generating Embeddings"),
    ("storing", "🗄️", "Storing in Vector DB"),
]


def render_pipeline(
    active_stage=None,
    completed_stages=None,
):
    """
    Render the document-processing pipeline.
    """

    if completed_stages is None:
        completed_stages = []

    html = '<div class="stage-container">'

    for index, (stage_id, icon, title) in enumerate(stages):

        if stage_id in completed_stages:

            state = "complete"
            status = "✓ Complete"

        elif stage_id == active_stage:

            state = "active"
            status = "Processing..."

        else:

            state = ""
            status = "Waiting"

        html += f"""
        <div class="stage {state}">
            <div class="stage-icon">{icon}</div>
            <div class="stage-title">{title}</div>
            <div class="stage-status">{status}</div>
        </div>
        """

        if index < len(stages) - 1:
            html += '<div class="arrow">→</div>'

    html += "</div>"

    pipeline_placeholder.markdown(
        html,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Process button
# --------------------------------------------------

process_button = st.button(
    "▶ Process Documents",
    type="primary",
)


if process_button:

    # ----------------------------------------------
    # Progress callback
    # ----------------------------------------------

    def progress_callback(
        stage,
        current,
        total,
        message,
    ):

        stage_order = [
            "loading",
            "chunking",
            "embedding",
            "storing",
        ]

        current_index = stage_order.index(stage)

        completed_stages = stage_order[:current_index]

        render_pipeline(
            active_stage=stage,
            completed_stages=completed_stages,
        )

        if total > 0:
            progress_value = current / total
        else:
            progress_value = 0

        progress_placeholder.progress(
            progress_value,
            text=message,
        )

        status_placeholder.markdown(
            f"""
            <div class="processing-status">
                {message}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------------------------
    # Run indexing
    # ----------------------------------------------

    with st.spinner("Processing documents..."):

        result = process_documents(
            progress_callback=progress_callback
        )

    # ----------------------------------------------
    # Save indexing state
    # ----------------------------------------------

    st.session_state.indexing_complete = True

    st.session_state.indexing_result = result

    # ----------------------------------------------
    # Show completed pipeline
    # ----------------------------------------------

    render_pipeline(
        completed_stages=[
            "loading",
            "chunking",
            "embedding",
            "storing",
        ]
    )

    progress_placeholder.progress(
        1.0,
        text="Indexing complete",
    )

    status_placeholder.markdown(
        """
        <div class="complete-status">
            ✓ Indexing complete — documents are ready for questions.
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Restore completed pipeline after Streamlit reruns
# --------------------------------------------------

if st.session_state.indexing_complete:

    render_pipeline(
        completed_stages=[
            "loading",
            "chunking",
            "embedding",
            "storing",
        ]
    )

    progress_placeholder.progress(
        1.0,
        text="Indexing complete",
    )

    status_placeholder.markdown(
        """
        <div class="complete-status">
            ✓ Indexing complete — documents are ready for questions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = st.session_state.indexing_result

    if result:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Documents",
                result["documents"],
            )

        with col2:
            st.metric(
                "Chunks",
                result["chunks"],
            )

        with col3:
            st.metric(
                "Vectors",
                result["vectors"],
            )


# --------------------------------------------------
# Question answering
# --------------------------------------------------

st.divider()

st.subheader("Ask a question")

question = st.text_input(
    "Question",
    placeholder="Ask something about your documents...",
)


# --------------------------------------------------
# Ask button
# --------------------------------------------------

if st.button(
    "Ask",
    type="primary",
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        # ------------------------------------------
        # Route question + generate answer
        # ------------------------------------------

        with st.spinner(
            "Thinking..."
        ):

            result = ask_question(
                question,
                top_k=3,
            )

        # ------------------------------------------
        # Casual conversation
        # ------------------------------------------

        if result["route"] == "CHAT":

            st.subheader("Answer")

            st.write(
                result["answer"]
            )

        # ------------------------------------------
        # Document question / RAG
        # ------------------------------------------

        else:

            st.subheader("Answer")

            st.write(
                result["answer"]
            )

            # --------------------------------------
            # Show sources only when an answer
            # was actually found
            # --------------------------------------

            no_answer = (
                result["answer"].strip()
                == "I don't have enough information in the provided documents."
            )

            if not no_answer:

                st.subheader("Sources")

                for source in result["sources"]:

                    metadata = source["metadata"]

                    source_text = metadata.get(
                        "source",
                        "unknown",
                    )

                    page = metadata.get("page")

                    if page is not None:

                        st.write(
                            f"**{source_text}** "
                            f"(page {page}, "
                            f"distance: "
                            f"{source['distance']:.4f})"
                        )

                    else:

                        st.write(
                            f"**{source_text}** "
                            f"(distance: "
                            f"{source['distance']:.4f})"
                        )