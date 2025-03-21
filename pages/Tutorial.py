import streamlit as st
import base64


@st.cache_data
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def main():

    st.set_page_config(
        page_title="Tutorial",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    img_path = "Ship.png"  
    img_base64 = get_img_as_base64(img_path)


    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        background-blend-mode: multiply; /* Blend mode for better contrast */
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: rgba(255, 255, 255, 0.3); /* Semi-transparent white overlay */
        z-index: 0;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    body {{
        background-color: #e0f7fa; /* Set a background color for the body */
    }}
    </style>
    """


    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .title {
            color: #00796b;
            font-size: 2.5em;
            text-align: center;
            margin-top: 20px;
        }
        .subtitle {
            color: #004d40;
            font-size: 1.5em;
            text-align: center;
            margin-bottom: 20px;
        }
        .video-frame {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .content {
            color: #004d40;
            font-size: 1.2em;
            text-align: center;
            margin: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.subheader("About the Model")
    st.sidebar.write("This website uses a Random Forest model (`model_RF.pkl`) for predictions.")

    st.markdown('<h1 class="title">Coral Bleaching Prediction Tutorial 🎥</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">Learn how to use this app to predict coral bleaching levels</h2>', unsafe_allow_html=True)
    st.write('<div class="content">Watch the tutorial below to understand how to use the app and make predictions:</div>', unsafe_allow_html=True)


    youtube_url = "https://www.youtube.com/watch?v=qjlVAsvQLM8"  # Replace with your actual YouTube video URL
    video_id = youtube_url.split("=")[-1]  # Extract the video ID
    st.markdown(
        f'<div class="video-frame"><iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe></div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()