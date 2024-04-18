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
        page_title="Alwrity",
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
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"""
      <style>
      [class="st-emotion-cache-7ym5gk ef3psqc12"]{{
            display: inline-block;
            padding: 5px 20px;
            background-color: #4681f4;
            color: #FBFFFF;
            width: 300px;
            height: 35px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 8px;’
      }}
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
    st.title("✍️ Alwrity - AI Instagram Caption Generator")

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        input_insta_keywords = st.text_input('**Enter main keywords of Your instagram caption!**')
        col1, col2, space, col3, col4 = st.columns([5, 5, 0.5, 5, 5])
        with col1:
            input_insta_type = st.selectbox('Voice Tone', ('Neutral', 'Formal', 'Casual', 'Funny', 
                'Optimistic', 'Assertive', 'Friendly', 'Encouraging', 'Sarcastic'), index=0)
        with col2:
            input_insta_cta = st.selectbox('CTA (Call To Action)', ('Shop Now', 
                'Learn More', 'Swipe Up', 'Sign Up', 'Link in Bio', 'Sense of urgency'), index=0)
        with col3:
            input_insta_audience = st.selectbox('Choose Target Audience', ('For All', 
                'Age:18-24 (Gen Z)', 'Age:25-34 (Millennials)'), index=0)
        with col4:
            input_insta_language = st.selectbox('Choose Language', ('English', 'Hindustani',
                'Chinese', 'Hindi', 'Spanish'), index=0)

    
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
                        st.code(insta_captions)
                    else:
                        st.error("💥**Failed to generate instagram Captions. Please try again!**")


# Function to generate blog metadesc
def generate_insta_captions(input_insta_keywords, input_insta_type, input_insta_cta, input_insta_audience, input_insta_language):
    """ Function to call upon LLM to get the work done. """

    # If keywords and content both are given.
    if input_insta_keywords:
        prompt = f"""As an instagram expert and experienced content writer, 
        I will provide you with my 'instagram caption keywords', along with CTA, Target Audience & voice tone.
        Your task is to write 3 instagram captions.

        Follow below guidelines to generate instagram captions:
        1). Front-Loading: Capture attention by placing key info at the beginning of your captions.
        2). Optimise your captions for {input_insta_cta} Call-to-Action (CTA). 
        3). Hashtag Usage: Limit yourself to four relevant hashtags per caption.
        4). Brand Voice and Tone: Use and convey {input_insta_type} voice tone in your captions.
        5). Optimise your captions for {input_insta_audience} target audience.
        6). Emojis: Inject personality and emotion into your captions with emojis.
        7). Brevity: Keep your captions concise and to the point.
        8). Important: Your response should be in {input_insta_language} language.

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
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
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

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
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
