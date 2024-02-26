import streamlit as st
from functions import convert_pdf_to_txt_file, confirm_list, limit_to_4096_characters
from prompts import system_prompt, delimiter
from completion import get_completion, generate_audio_from_text
from multimodal_search import MultiModalSearch
from moviepy.editor import ImageSequenceClip, AudioFileClip
import os

# languages = {
#     'English': 'eng',
#     'French': 'fra',
#     'Arabic': 'ara',
#     'Spanish': 'spa',
# }

st.markdown("""
    ## Media Content
""")

pdf_file = st.file_uploader("Upload your PDF", type=['pdf'])

if pdf_file:
    path = pdf_file.read()
    # pdf to text
    text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
    st.info(f'Total Pages in PDF : {nbPages}')
    if text_data_f:
        st.info(f'Text is extracted.')
        limited_text = limit_to_4096_characters(text_data_f)
        limited_text_audio = generate_audio_from_text(limited_text)
        audio_file = open('output.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes)
        # st.info(text_data_f)
        user_message = f"""{delimiter}{text_data_f}{delimiter}"""

    messages = [
                {
                    "role": "system", "content": system_prompt
                },
                {
                    "role": "user", "content": user_message
                }
            ]
    
    response_keywords = get_completion(messages=messages)
    ast_response_keywords = confirm_list(response_keywords)
    st.info(response_keywords)
    st.info(ast_response_keywords)
    st.info(len(ast_response_keywords))
    st.warning(f'type : {type(ast_response_keywords)}')
    
    multimodal_search = MultiModalSearch()
    
    images_directory = 'qurated_images'
    os.makedirs(images_directory, exist_ok=True)
    
    if len(ast_response_keywords) > 0:
        for one_keyword in ast_response_keywords:
            st.warning(f"one keyword : {one_keyword}")
            if len(one_keyword) > 0:
                results = multimodal_search.search(query=one_keyword)
                st.info(f'Query or Keyword  was : {one_keyword}')
                col1, col2, col3 = st.columns([1,1,1])
                image_paths = [] # Initialize an empty list to hold image file paths for video generation
                with col1:
                    st.image(results[0].content, use_column_width=True)
                    image_filename = f"image_{one_keyword}_0.jpg"
                    image_path = os.path.join(images_directory, image_filename)
                    with open(image_path, 'wb') as file:
                        file.write(results[0].content)
                    image_paths.append(image_path)
                with col2:
                    st.image(results[1].content, use_column_width=True)
                    image_filename = f"image_{one_keyword}_1.jpg"
                    image_path = os.path.join(images_directory, image_filename)
                    with open(image_path, 'wb') as file:
                        file.write(results[1].content)
                    image_paths.append(image_path)
                with col3:
                    st.image(results[2].content, use_column_width=True)
                    image_filename = f"image_{one_keyword}_2.jpg"
                    image_path = os.path.join(images_directory, image_filename)
                    with open(image_path, 'wb') as file:
                        file.write(results[2].content)
                    image_paths.append(image_path) 
            else:
                st.warning("Keyword or Query length short")
        
        # VIDEO GENERATION PART...
        audio_clip = AudioFileClip('output.mp3')    
        # Compute the duration of each image so that total duration matches the audio length
        total_duration = audio_clip.duration
        image_duration = total_duration / len(image_paths)
        # Create a video clip from images
        video_clip = ImageSequenceClip(image_paths, durations=[image_duration] * len(image_paths))
        # Set the audio of the video clip as the audio clip
        # If the audio is shorter than the video duration, it will be looped
        audio_clip = audio_clip.loop(duration=video_clip.duration)
        final_clip = video_clip.set_audio(audio_clip)
        # Output the final video with audio
        final_clip.write_videofile('final_output.mp4', fps=24, codec='libx264', audio_codec='aac')
    else:
        st.warning("Something wrong in Keywords generation")

    
    


with st.sidebar:
    st.title("🧾 PDF to Text")
    # textOutput = st.selctbox(
    #     "How do you want your output text?",
    #     ('One text file (.txt)', 'Text file per page (ZIP)'))
    st.markdown("""
    # How does it work?
    1. Simply upload your PDF.
    2. Text Extraction.
    """)
    