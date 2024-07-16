import streamlit as st
from openai import OpenAI

# Set up OpenAI API credentials
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Function to generate story based on user prompt
def make_story(prompt):
    story_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": 'system',
                "content": "you're a best seller story writer. you will take user's prompt and generate a 100 words story."
            },
            {
                "role": "user",
                "content": f'{prompt}'
            }
        ],
        max_tokens=1000,
        temperature=0.8
    )
    story = story_response.choices[0].message.content
    return story

# Function to generate cover image prompt based on generated story
def cover_image_prompt(story):
    designed_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": 'system',
                "content": "based on the story given, you will design a detailed image prompt for the cover of this story."
            },
            {
                "role": "user",
                "content": f'{story}'
            }
        ],
        max_tokens=1000,
        temperature=0.8
    )
    designed = designed_response.choices[0].message.content
    return designed

# Function to generate image based on the designed prompt and style
def make_image(desc, style="realistic"):
    if style == "realistic":
        prompt = f'{desc}, in realistic style'
    elif style == "cartoon":
        prompt = f'{desc}, in cartoon style'
    elif style == "abstract":
        prompt = f'{desc}, in abstract style'

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1,
    )
    image_url = response.data[0].url
    return image_url

# Main Streamlit app code
def main():
    st.title("Story and Image Generator")

    # Initialize session state variables
    if 'generated_story' not in st.session_state:
        st.session_state.generated_story = ""
    if 'cover_prompt' not in st.session_state:
        st.session_state.cover_prompt = ""
    if 'prompt_entered' not in st.session_state:
        st.session_state.prompt_entered = False

    # User input for prompt
    prompt = st.text_input("Enter your prompt to generate a story and image:")

    if st.button("Generate Story and Image"):
        if prompt:
            # Generate story
            story = make_story(prompt)
            st.session_state.generated_story = story

            # Generate cover image prompt
            cover_prompt = cover_image_prompt(story)
            st.session_state.cover_prompt = cover_prompt

            st.session_state.prompt_entered = True

    # Display the generated story and image if prompt was entered
    if st.session_state.prompt_entered:
        st.subheader("Generated Story:")
        st.write(st.session_state.generated_story)

        # Choose image style
        style = st.radio("Choose image style:", ["Realistic", "Cartoon", "Abstract"])
        style_mapping = {
            "Realistic": "realistic",
            "Cartoon": "cartoon",
            "Abstract": "abstract"
        }

        if style in style_mapping:
            image = make_image(st.session_state.cover_prompt, style=style_mapping[style])
            st.subheader(f"Generated {style} Image:")
            st.image(image, caption=f"{style} style image based on the story")

if __name__ == "__main__":
    main()
