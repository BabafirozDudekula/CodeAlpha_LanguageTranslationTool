
import streamlit as st
from deep_translator import MyMemoryTranslator
from gtts import gTTS
import io


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CodeAlpha Language Translator",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Language Translation Tool")
st.write("Translate text between multiple languages easily.")
st.divider()


# --------------------------------------------------
# SUPPORTED LANGUAGES
# --------------------------------------------------

languages = {
    "English": "english",
    "Hindi": "hindi",
    "Telugu": "telugu",
    "Tamil": "tamil india",
    "Kannada": "kannada",
    "Malayalam": "malayalam",
    "French": "french",
    "German": "german",
    "Spanish": "spanish",
    "Japanese": "japanese",
    "Korean": "korean",
    "Arabic": "arabic",
    "Chinese (Simplified)": "chinese simplified"
}

# Language codes required by Google Text-to-Speech
speech_codes = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Chinese (Simplified)": "zh-CN"
}


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "translated_result" not in st.session_state:
    st.session_state.translated_result = ""

if "source_text" not in st.session_state:
    st.session_state.source_text = ""

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "English"

if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Hindi"


# --------------------------------------------------
# CALLBACK FUNCTIONS
# --------------------------------------------------

def swap_languages():
    source = st.session_state.source_lang
    target = st.session_state.target_lang
    result = st.session_state.translated_result

    st.session_state.source_lang = target
    st.session_state.target_lang = source

    if result:
        st.session_state.source_text = result
        st.session_state.translated_result = ""


def clear_all():
    st.session_state.source_text = ""
    st.session_state.translated_result = ""


# --------------------------------------------------
# LANGUAGE SELECTION
# --------------------------------------------------

col1, col2 = st.columns([5, 1])

with col1:
    st.selectbox(
        "Translate From",
        options=list(languages.keys()),
        key="source_lang"
    )

with col2:
    st.write("")
    st.write("")
    st.button(
        "⇄",
        on_click=swap_languages,
        help="Swap languages",
        use_container_width=True
    )

st.selectbox(
    "Translate To",
    options=list(languages.keys()),
    key="target_lang"
)


# --------------------------------------------------
# INPUT TEXT
# --------------------------------------------------

st.text_area(
    "Enter Your Text",
    key="source_text",
    height=150,
    placeholder="Type or paste your text here..."
)


# --------------------------------------------------
# TRANSLATION
# --------------------------------------------------

if st.button(
    "🌐 Translate",
    type="primary",
    use_container_width=True
):

    text = st.session_state.source_text.strip()
    source = st.session_state.source_lang
    target = st.session_state.target_lang

    if not text:
        st.warning("Please enter some text.")

    elif source == target:
        st.session_state.translated_result = text
        st.success("Source and target languages are the same.")

    else:
        try:
            with st.spinner("Translating..."):

                translator = MyMemoryTranslator(
                    source=languages[source],
                    target=languages[target]
                )

                result = translator.translate(text)

            if result:
                st.session_state.translated_result = result
                st.success("Translation completed successfully!")

            else:
                st.session_state.translated_result = ""
                st.warning("No translation was returned.")

        except Exception as error:
            st.session_state.translated_result = ""
            st.error(f"Translation failed: {error}")
            st.info("Check your internet connection or try again later.")


# --------------------------------------------------
# TRANSLATED OUTPUT
# --------------------------------------------------

if st.session_state.translated_result:

    st.divider()
    st.subheader("📝 Translated Output")

    st.text_area(
        "Translation",
        value=st.session_state.translated_result,
        height=150,
        disabled=True
    )

    # Copy-friendly output
    st.caption("You can select and copy the translated text above.")

    # --------------------------------------------------
    # TEXT TO SPEECH
    # --------------------------------------------------

    st.subheader("🔊 Pronunciation Reader")

    if st.button("▶️ Listen to Translation", use_container_width=True):

        try:
            with st.spinner("Generating speech..."):

                audio = gTTS(
                    text=st.session_state.translated_result,
                    lang=speech_codes[st.session_state.target_lang],
                    slow=False
                )

                audio_file = io.BytesIO()
                audio.write_to_fp(audio_file)
                audio_file.seek(0)

            st.audio(audio_file, format="audio/mp3")
            st.success("Audio generated successfully!")

        except Exception as error:
            st.error(f"Speech generation failed: {error}")


# --------------------------------------------------
# CLEAR BUTTON
# --------------------------------------------------

st.divider()

st.button(
    "🗑️ Clear All",
    on_click=clear_all,
    use_container_width=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CodeAlpha AI Internship | Language Translation Tool"
)
