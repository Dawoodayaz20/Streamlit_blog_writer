from litellm import completion
import asyncio
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

if not GOOGLE_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in your .env file")

def generate_topic():
    response = completion(
        model="gemini/gemini-2.0-flash",
        messages=[{
            "role": "user",
            "content": "Generate a creative blog topic for 2025."
        }],
        api_key=GOOGLE_API_KEY
    )
    return response["choices"][0]["message"]["content"].strip()

def generate_outline(topic):
    response = completion(
        model="gemini/gemini-2.0-flash",
        messages=[{
            "role": "user",
            "content": f"Based on the topic '{topic}', create a detailed outline for a blog post."
        }],
        api_key=GOOGLE_API_KEY
    )
    return response["choices"][0]["message"]["content"].strip()

async def generate_content():
    topic = await asyncio.to_thread(generate_topic)
    outline = await asyncio.to_thread(generate_outline, topic)
    return (topic, outline)

def main():
    st.set_page_config(page_title="UV Topic Generator", page_icon="✍️")
    
    st.title("✨ Blog Topic and Outline Generator")
    st.write("Generate creative blog topics and detailed outlines using AI.")

    if 'topic' not in st.session_state:
        st.session_state.topic = None
    if 'outline' not in st.session_state:
        st.session_state.outline = None

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Generate New Topic & Outline", type="primary"):
            with st.spinner("Generating content..."):
                try:
                    topic, outline = asyncio.run(generate_content())
                    st.session_state.topic = topic
                    st.session_state.outline = outline
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    if st.session_state.topic:
        st.subheader("Generated Topic:")
        st.info(st.session_state.topic)

    if st.session_state.outline:
        st.subheader("Blog Outline:")
        st.markdown(st.session_state.outline)

    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Gemini")

if __name__ == "__main__":
    main()
