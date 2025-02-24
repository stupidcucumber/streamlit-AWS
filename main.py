import boto3
from dotenv import load_dotenv
import streamlit as st
import os


st.set_page_config(
    page_title="Text -> Voice",
    page_icon="🔊",
)
st.title('🔊 Text -> Voice')
st.caption('Enter some text and turn it into a voice!') 



if st.session_state.get("AWS_POLLY_CLIENT") is None:
    load_dotenv()
    
    if os.getenv("AWS_ACCESS_KEY_ID") is None or os.getenv("AWS_SECRET_ACCESS_KEY") is None:
        st.error("⚠️ Problem with the AWS Credentials Keys!")

    else:
        st.session_state["AWS_POLLY_CLIENT"] = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        ).client(service_name="polly", region_name="eu-north-1")




with st.sidebar.expander("⚙️ Settings"):
    gender = st.selectbox(
        "Gender options ⚥",
        [
            "Male",
            "Female"
        ],
        help="Choose the gender of an actor."
    )
    
    voice = st.selectbox(
        "Voice Options 🗣️",
        [
            voice_description["Id"] 
            for voice_description in st.session_state["AWS_POLLY_CLIENT"].describe_voices(
                Engine='standard',
                LanguageCode="en-US"
            )["Voices"]
            if voice_description["Gender"] == gender
        ] if st.session_state.get("AWS_POLLY_CLIENT") else [],
        help="Choose the voice you want to use."
    )


with st.form(key='text_form'):
    text_input = st.text_area(
        "Enter Text", 
        "My name is Arya Stark. I want you to know that."
    )
    submit_button = st.form_submit_button(label='Generate Audio 🎵', type="primary")


if submit_button is not None:
    polly_client = st.session_state.get("AWS_POLLY_CLIENT")
    
    if polly_client:
        with st.spinner('Generating audio...'):
            response = polly_client.synthesize_speech(
                Text=text_input,
                OutputFormat='mp3',
                VoiceId=voice
            )
            
        st.audio(response["AudioStream"].read(), format='mp3')