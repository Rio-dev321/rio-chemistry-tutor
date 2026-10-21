
import os
import streamlit as st
from groq import Groq

# -----------------------------
# RIO - AI CHEMISTRY TUTOR
# -----------------------------

st.set_page_config(
    page_title="RIO Chemistry Tutor",
    page_icon="🧪",
    layout="centered"
)

st.title("🧪 RIO - AI Chemistry Tutor")
st.caption("Your personal AI Chemistry teacher | Class 10")

# Read API key securely from Streamlit secrets or environment
try:
    api_key = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    api_key = ""

api_key = api_key or os.getenv("GROQ_API_KEY", "")

MODEL_NAME = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are RIO, a friendly Chemistry tutor for Class 10 students.

Teach topics in simple English and Roman Urdu.

For each topic, include:
1. Topic name
2. Definition in English
3. Definition in Roman Urdu
4. Detailed explanation
5. Daily-life examples
6. Relevant chemical formulas and balanced equations
7. A simple labelled text diagram or flowchart
8. Important points to remember
9. Five practice questions with short answers

Use headings and simple language.
Make scientific explanations accurate.
Use text-based diagrams inside code blocks.
If a diagram is not relevant, explain why.
"""

# Language options
language = st.selectbox(
    "Choose your answer language",
    ["English + Roman Urdu", "English", "Roman Urdu"]
)

# Topic input
topic = st.text_input(
    "Enter your Chemistry topic",
    placeholder="e.g. Atomic Structure, Acids and Bases"
)

# Generate answer
if st.button("Generate Explanation", type="primary"):

    if not topic.strip():
        st.warning("Please enter a Chemistry topic.")

    elif not api_key:
        st.error(
            "Groq API key not found. Add GROQ_API_KEY "
            "to Streamlit Secrets or your environment variables."
        )

    else:
        language_instructions = {
            "English + Roman Urdu":
                "Explain in both English and Roman Urdu.",
            "English":
                "Explain in English only.",
            "Roman Urdu":
                "Explain in Roman Urdu only."
        }

        try:
            with st.spinner("RIO is preparing your lesson..."):

                client = Groq(api_key=api_key)

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Chemistry topic: {topic.strip()}\n"
                                f"Student level: Class 10\n"
                                f"Language: "
                                f"{language_instructions[language]}"
                            )
                        }
                    ],
                    temperature=0.4,
                    max_completion_tokens=3500
                )

                answer = response.choices[0].message.content

            if answer:
                st.markdown("---")
                st.subheader(f"📘 Topic: {topic}")
                st.markdown(answer)
            else:
                st.warning("RIO could not generate an answer. Try again.")

        except Exception as error:
            st.error(
                "Something went wrong. Check your API key, "
                "model access, internet connection, and usage limits."
            )
            st.caption(f"Technical details: {error}")

st.markdown("---")
st.caption("RIO Chemistry Tutor | Powered by Generative AI")
