import os
import fitz  # PyMuPDF
from google import genai
import streamlit as st

# Set up page branding
st.set_page_config(
    page_title="Raneemiee_studies <3",
    page_icon="📖",
    layout="centered",
)

st.title("✨ Raneemiee_studies <3 ✨")
st.caption("Your personalized AI study partner for PDFs & topics!")

# Sidebar for API Key
with st.sidebar:
    st.header("🔑 Settings")
    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        help="Get your key at aistudio.google.com",
    )

    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

    st.markdown("---")
    st.markdown("Built with Streamlit & Google Gemini")

# Initialize Gemini Client
client = None

if os.environ.get("GEMINI_API_KEY"):
    try:
        client = genai.Client()
    except Exception:
        st.sidebar.error("Invalid API Key.")

# Input Mode Choice
input_mode = st.radio(
    "Choose your study source:",
    ["Enter a Topic", "Upload PDF Document"],
)

input_text_content = ""

if input_mode == "Enter a Topic":
    topic = st.text_input("What topic would you like to study?")

    if topic:
        input_text_content = (
            f"Comprehensive study guide and flashcards for the topic: {topic}"
        )

else:
    uploaded_file = st.file_uploader(
        "Upload your lecture notes or PDF textbook",
        type=["pdf"],
    )

    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
            try:
                doc = fitz.open(
                    stream=uploaded_file.read(),
                    filetype="pdf",
                )

                extracted_text = ""

                for page in doc:
                    extracted_text += page.get_text()

                if extracted_text.strip():
                    st.success(f"Successfully loaded {len(doc)} pages!")
                    input_text_content = extracted_text
                else:
                    st.error(
                        "Could not read text. The PDF might be scanned/image-only."
                    )

            except Exception as e:
                st.error(f"Error reading PDF: {e}")

# Generate Button
if input_text_content and st.button("✨ Generate Study Materials"):
    if not os.environ.get("GEMINI_API_KEY"):
        st.error(
            "Please enter your Gemini API key in the left sidebar first!"
        )

    elif client is None:
        st.error("Please check your Gemini API key and try again.")

    else:
        with st.spinner(
            "Raneemiee_studies <3 is generating your flashcards..."
        ):
            try:
                prompt = f"""
You are an expert AI tutor for the app "Raneemiee_studies <3".

Analyze the following content and create:
1. A summary of core concepts (3-5 bullet points).
2. 5 high-yield flashcards in a clear "Question | Answer" format.

Content:
{input_text_content[:15000]}
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

                st.markdown("---")
                st.markdown("### 🧠 Your Study Guide")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error generating study guide: {e}")
