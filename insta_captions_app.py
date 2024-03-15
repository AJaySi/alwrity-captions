import time #Iwish
import os
import json
import openai
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
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

    # Sidebar input for OpenAI API Key
    openai_api_key = st.sidebar.text_input("**Enter OpenAI API Key(Optional)**", type="password")
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown(f"🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")
    
    # Title and description
    st.title("✍️ Alwrity - AI Instagram Caption Generator")

    with st.expander("How to Write **Great Instagram Captions** ? 📝❗"):
        st.markdown('''## Instagram Caption Best Practices 📝  
        - **Drafting:✍️ ** Before posting, refine your caption by writing multiple drafts. This process allows you to experiment with different ideas and find the perfect fit for your content.

        - ** Front-Loading:🚀 ** Grab your audience's attention by placing the most important information or message,
        at the beginning of your caption. This ensures that it's seen even if the caption gets cut off in users' feeds.

        - ** Call-to-Action (CTA):📣 ** Encourage engagement by including a clear call-to-action. 
        Whether it's asking for likes, comments, shares, or visits to your profile or website, CTAs prompt your audience to take action.

        - ** Hashtag Usage:#️⃣  ** While hashtags can increase discoverability, limit yourself to four relevant hashtags per post. 
        Too many hashtags can clutter your caption and distract from your message.

        - **Brand Voice and Tone:💬 ** Maintain consistency with your brand's voice while embracing Instagram's casual 
        and friendly tone. Find a balance that resonates with your audience and reflects your brand's personality.

        - **Emojis:😊** Inject personality and emotion into your captions by incorporating emojis. 
        These visual elements can add flair, convey tone, and increase engagement with your content.

        - **Cross-Promotion:🔄** Leverage Instagram to promote your other social channels. 
        Encourage followers to connect with you on platforms like Facebook, Twitter, or YouTube for a holistic brand experience.

        - **Brevity:🕒** In a fast-paced environment like Instagram, brevity is key. 
        Keep your captions concise and to the point, ensuring that they're easily digestible for your audience.

         ''')
        st.markdown("""## Instagram Algorithm Insights 📊

        The Instagram algorithm is a complex set of instructions that determines which content appears in users' feeds. 
        It considers factors such as user history, interests, and post relevancy to personalize the user experience.

                ### Key Factors Influencing the Instagram Algorithm:

                - **Relationship with users:** Users who engage frequently with your content are more likely to see your future posts.
                - **Interest conveyed by the user:** The algorithm prioritizes content that aligns with users' 
                past interactions and interests.
                - **Relevancy of the post:** Posts are ranked based on their relevance to the user, 
                determined by factors like engagement and timeliness.

        Additionally, Instagram's algorithm prioritizes recent and engaging content, 
        making it essential to focus on building relationships with your audience and creating high-quality, relevant posts.

        Understanding the Instagram algorithm can help inform your caption strategy and maximize your reach on the platform.
        """)

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
                        st.subheader('**👩‍🔬👩‍🔬Go Viral, with these Instagram captions!🎆🎇 🎇**')
                        st.code(insta_captions)
                        st.balloons()
                    else:
                        st.error("💥**Failed to generate instagram Captions. Please try again!**")

    # Display Animation.
    data_oracle = import_json(r"lottie_files/robo_analytics.json")
    st_lottie(data_oracle, key="InstaCaption")

    st.markdown('''
                Generates Instagram Captions - powered by AI (OpenAI GPT-3, Gemini Pro).  
                Implemented by [Alwrity](https://alwrity.netlify.app).  
                Captions are optimised for given keywords, demographic, tone & CTA.  
                ''')


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
        insta_captions = openai_chatgpt(prompt)
        return insta_captions


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", temperature=0.2, max_tokens=500, top_p=0.9, n=3):
    """
    Wrapper function for OpenAI's ChatGPT completion.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "gpt-4-1106-preview".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.2.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 8192.
        top_p (float, optional): Controls diversity. Defaults to 0.9.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    # Wait for 10 seconds to comply with rate limits
    for _ in range(10):
        time.sleep(1)

    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
            # Additional parameters can be included here
        )
        return response.choices[0].message.content

    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"OpenAI error: {err}")



# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url


if __name__ == "__main__":
    main()
