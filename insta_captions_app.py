import time #Iwish
import os
import json
import requests
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import google.generativeai as genai

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity - AI insta caption writer",
        layout="wide",
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        ::-webkit-scrollbar-track {
        background: #e1ebf9;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }

        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
      </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ ALwrity - AI Instagram Caption Generator")

    # Add API Key Input Section
    with st.expander("**🔑 API Key Configuration:**", expanded=False):
        user_api_key = st.text_input("**Enter your Google Generative AI API Key (Optional):**", type="password", placeholder="Enter API Key here")

    # Pass the user-provided API key to the generate_text_with_exception_handling function
    if user_api_key:
        pass  # Placeholder to fix the indentation error

    # Input section
    with st.expander("**💡  Instructions:**  Read the following before generating your Instagram captions.", expanded=True):
        st.markdown("**Let's create the perfect caption!** ✍️")
    
        # Main Keywords
        input_insta_keywords = st.text_input("**Enter your main keywords:**", placeholder="e.g., travel, adventure, sunset")
        # Input Columns
        col1, col2, col3, col4 = st.columns([3, 3, 3, 3])
    
        with col1:
            # Voice Tone
            input_insta_type = st.selectbox(
                "**Voice Tone:**",
                (
                    "Neutral 😐",
                    "Formal 👔",
                    "Casual 😎",
                    "Funny 😂",
                    "Optimistic 😊",
                    "Assertive 💪",
                    "Friendly 🤗",
                    "Encouraging 👍",
                    "Sarcastic 🙄"
                ),
                index=0
            )   
        with col2:
            # CTA (Call To Action)
            input_insta_cta = st.selectbox(
                "**Call To Action:**",
                (
                    "Shop Now 🛒",
                    "Learn More 📚",
                    "Swipe Up 👉",
                    "Sign Up ✍️",
                    "Link in Bio 🔗",
                    "Sense of Urgency ⏰"
                ),
                index=0
            )
        with col3:
            # Target Audience
            input_insta_audience = st.selectbox(
                "**Target Audience:**",
                (
                    "For All 🌎",
                    "Age: 18-24 (Gen Z) 🧑‍🤝‍🧑",
                    "Age: 25-34 (Millennials) 👨‍👩‍👧‍👦"
                ),
                index=0
            )
        with col4:
            # Language
            input_insta_language = st.selectbox(
                "**Language:**",
                (
                    "English",
                    "Hindustani",
                    "Chinese",
                    "Hindi",
                    "Spanish"
                ),
                index=0
            )
    
        # Generate Blog Title button
        if st.button('**Get Instagram Captions**'):
            with st.spinner():
                # Clicking without providing data, really ?
                if not input_insta_keywords:
                    st.error('** 🫣 P🫣   Provide Inputs to generate Blog Tescription.  Keywords, are required!**')
                elif input_insta_keywords:
                    insta_captions = generate_insta_captions(input_insta_keywords,
                            input_insta_type, 
                            input_insta_cta,
                            input_insta_audience,
                            input_insta_language
                            )
                    if insta_captions:
                        st.subheader('**👩👩🔬Go Viral, with these Instagram captions!🎆🎇 🎇**')
                        st.markdown(insta_captions)
                    else:
                        st.error("💥**Failed to generate instagram Captions. Please try again!**")


# Function to generate blog metadesc
def generate_insta_captions(input_insta_keywords, input_insta_type, input_insta_cta, input_insta_audience, input_insta_language):
    """ Function to call upon LLM to get the work done. """

    # If keywords and content both are given.
    if input_insta_keywords:
        prompt = f"""You are an experienced Instagram content creator and expert copywriter. Using the details provided below, generate 5 concise and engaging Instagram captions that adhere to the following guidelines:

        1). Start with a strong, attention-grabbing opening that front-loads key information.
        2). Keep the language concise, clear, and impactful (limit each caption to 2-3 sentences).
        3). Incorporate storytelling elements or emotional appeal where relevant, but keep it brief.
        4). Use a call-to-action optimized for {input_insta_cta}.
        5). Reflect a {input_insta_type} voice and tone consistently.
        6). Tailor the captions for the {input_insta_audience} target audience.
        7). Include up to four relevant hashtags per caption, ensuring diversity and relevance.
        8). Use emojis to add personality and break up the text.
        9). Ensure the captions are written in {input_insta_language}.
        10). Highlight unique aspects of Kalimpong, such as its serene landscapes, vibrant culture, or Himalayan charm.
        11). Include a question or prompt to encourage user interaction, such as 'What's your dream adventure spot?'
        12). Ensure captions are optimized for Instagram SEO by including keywords naturally and strategically.

        \nInstagram caption keywords: '{input_insta_keywords}'\n
        """
        insta_captions = generate_text_with_exception_handling(prompt)
        return insta_captions


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 0.6,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 1096,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    main()
