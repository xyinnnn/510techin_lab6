import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


def generate_lyrics(theme, count):
    prompt_template = f"""
    You are Noel Gallagher, a songwriter and guitarist known for his work with the band Oasis. Here's some of the styles of lyrics you've written in the past:
    
"Today is gonna be the day
That they're gonna throw it back to you
By now, you should've somehow
Realized what you gotta do
I don't believe that anybody
Feels the way I do, about you now"

"And all the roads we have to walk are winding
And all the lights that lead us there are blinding
There are many things that I would like to say to you
But I don't know how"

    Please create lyrics and provide a list of rhymes based on the following details:
    - Theme: {theme}
    - Number of rhymes requested: {count}
    - Follow your own lyrics writing style
    - Please separate the rhymes from the lyrics and list them first. Use the rhymes in the lyrics you write
    """
    response = model.generate_content(prompt_template)
    lyrics = response.text
    # Assuming rhymes are always prefixed with "Rhymes:" and followed by "Lyrics:"
    rhymes_index = lyrics.find("Rhymes:")
    lyrics_index = lyrics.find("Lyrics:")

    if rhymes_index != -1 and lyrics_index != -1:
        rhymes = lyrics[rhymes_index + len("Rhymes:"):lyrics_index].strip()
        lyrics = lyrics[lyrics_index + len("Lyrics:"):].strip()
    else:
        rhymes = "No rhymes provided."
        lyrics = lyrics.strip()  # Assume the whole text is lyrics if no clear separation

    return lyrics, rhymes


st.title("🎤 AI Oasis Lyric Generator")
image_url = "https://example.com/oasis-band.jpg"
st.image(image_url)

theme = st.text_input("Enter the theme of your song:")
rhyme_count = st.number_input("Enter the number of rhymes you want:", min_value=1, value=5)

if st.button("Generate Lyrics"):
    lyrics, rhymes = generate_lyrics(theme, rhyme_count)
    
    # Display lyrics with improved layout
    st.subheader("Lyrics")
    st.text_area("Here are your lyrics:", lyrics, height=300)

    # Optionally display rhymes if needed
    st.subheader("Rhymes")
    st.text(rhymes)


