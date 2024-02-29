import streamlit as st
from functions import convert_pdf_to_txt_file, confirm_list, limit_to_4096_characters, save_image_from_url
from prompts import system_prompt, delimiter, summarizer_prompt, system_prompt_for_describing_image
from completion import get_completion, generate_audio_from_text, get_image_url, get_image_description
from multimodal_search import MultiModalSearch
from moviepy.editor import ImageSequenceClip, AudioFileClip
from moviepy.editor import *
from PIL import Image
import numpy as np
import os
import shutil

st.markdown("""
    ## Media Content
""")

with st.sidebar:
    st.title("🧾 Social-Auto-Delve")
    # textOutput = st.selctbox(
    #     "How do you want your output text?",
    #     ('One text file (.txt)', 'Text file per page (ZIP)'))
    st.markdown("""
    # How does it work?
    1. Simply upload your PDF.
    2. Text Extraction.
    3. Keywords Extraction (from original text)
    4. Summarize Text (from original text)
    5. Relevant Image Generation.
    6. Audio of summarised text.
    7. Keyword - Images
    8. Video output
    """)

pdf_file = st.file_uploader("Upload your PDF", type=['pdf'])

if pdf_file:
    path = pdf_file.read()
    # pdf to text
    text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
    st.info(f'Total Pages in PDF : {nbPages}')
    if text_data_f:
        st.info(f'Text is extracted.')
        user_message_for_summary = f"""{delimiter}{text_data_f}{delimiter}"""
        summary_messages = [
            {
                    "role": "system", "content": summarizer_prompt
                },
                {
                    "role": "user", "content": user_message_for_summary
                }
        ]
        with st.spinner("Summarizing the Text Extracted."):
            summarised_text = get_completion(messages=summary_messages)
        st.info(f"Summarised text")
        
        with st.spinner("Generating Image for Post."):
            img_url = get_image_url(summarised_text)
        save_image_from_url(img_url, "PostImages/postimage1.jpg")
        st.image(img_url)
        st.info(img_url)
        st.info(f"Generated Image Post")
        
        
        
        messages_for_image_description =  [
                {"role": "system",
                 "content":system_prompt_for_describing_image,
                },
                {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": "Give Description for this image."
                 },
                {
                 "type": "image_url",
                    "image_url": {
                    "url": img_url
                 }
                },
                {
                    "type": "text",
                    "text": f"{delimiter}{summarised_text}{delimiter}"
                 }
                ]
      }
    ]
        
        with st.spinner("Generating Description for Post generated."):
            image_description = get_image_description(messages=messages_for_image_description)
        st.info(f"Generated Description for Image Post.")
        
        with st.spinner("Generating Audio for Video Post."):
            limited_text = limit_to_4096_characters(summarised_text)
            limited_text_audio = generate_audio_from_text(limited_text)
        audio_file = open('output.mp3', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes)
        st.info(f"Audio generated.")
        
        
        user_message = f"""{delimiter}{text_data_f}{delimiter}"""
        messages = [
                {
                    "role": "system", "content": system_prompt
                },
                {
                    "role": "user", "content": user_message
                }
            ]
        
        with st.spinner("Getting Keywords from Document."):
            response_keywords = get_completion(messages=messages)
            ast_response_keywords = confirm_list(response_keywords)
        st.info(f"Keywords generated.")
        st.info(ast_response_keywords)
    
    
    multimodal_search = MultiModalSearch()
    
    images_directory = 'qurated_images'
    os.makedirs(images_directory, exist_ok=True)
    
    
    # KEY-WORD ===> IMAGES BAESED on them.
    image_paths = [] # Initialize an empty list to hold image file paths for video generation
    if len(ast_response_keywords) > 0:
        for one_keyword in ast_response_keywords:
            st.warning(f"one keyword : {one_keyword}")
            if len(one_keyword) > 0:
                results = multimodal_search.search(query=one_keyword)
                st.info(f'Query or Keyword  was : {one_keyword}')
                col1, col2, col3 = st.columns([1,1,1])
                with col1:
                    st.image(results[0].content, use_column_width=True)
                    image_file_location = results[0].content
                    image_filename = f"image_{one_keyword}_0.jpg"
                    image_path = os.path.join(images_directory, image_filename)
                    # save_image_from_url(results[0].content, image_path)
                    shutil.copyfile(image_file_location, image_path)
                    # with open(image_path, 'wb') as file:
                    #     file.write(results[0].content)
                    image_paths.append(image_path)
                with col2:
                    st.image(results[1].content, use_column_width=True)
                    image_file_location = results[0].content
                    image_filename = f"image_{one_keyword}_1.jpg"
                    image_path = os.path.join(images_directory, image_filename)
                    shutil.copyfile(image_file_location, image_path)
                    # with open(image_path, 'wb') as file:
                    #     file.write(results[1].content)
                    image_paths.append(image_path)
                with col3:
                    st.image(results[2].content, use_column_width=True)
                    image_file_location = results[0].content
                    image_filename = f"image_{one_keyword}_2.jpg"
                    image_path = os.path.join(images_directory, image_filename)
                    shutil.copyfile(image_file_location, image_path)
                    # with open(image_path, 'wb') as file:
                    #     file.write(results[2].content)
                    image_paths.append(image_path) 
            else:
                st.warning("Keyword or Query length short")
        st.warning(len(image_paths))
        # VIDEO GENERATION PART...

        audio_clip = AudioFileClip('output.mp3')   
        audio_duration = audio_clip.duration
        # Cut the audio to the first 60 seconds (for example)
        audio_clip = audio_clip.subclip(0, audio_duration)
        
        # Compute the duration of each image so that total duration matches the audio length
        total_duration = audio_duration
        image_duration = total_duration / len(image_paths)
        
        # Resize images to a common size
        width, height = 1280, 720  # Adjust dimensions as needed
        resized_image_paths = []
        for path in image_paths:
            img = Image.open(path)
            img = img.resize((width, height))
            img_array = np.array(img)  # Convert PIL.Image to numpy array
        resized_image_paths.append(img_array)

        with st.spinner("Generating Video."):
             # Create a video clip from images
            video_clip = ImageSequenceClip(resized_image_paths, durations=[image_duration] * len(resized_image_paths))
            final_clip = video_clip.set_audio(audio_clip)
            # Output the final video with audio
            final_clip.write_videofile('final_output.mp4', fps=24, codec='libx264', audio_codec='aac')
        st.info(f"Generated Video Clip")
        
        st.video(final_clip, format="video/mp4", start_time=0)
    else:
        st.warning("Something wrong in Keywords generation")    