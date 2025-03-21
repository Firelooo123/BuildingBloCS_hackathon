import streamlit as st
import pandas as pd
import base64


@st.cache_data
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    st.set_page_config(
        page_title="Past Predictions",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'past_predictions' not in st.session_state:
        st.session_state.past_predictions = []

    img_path = "Ship.png"  
    img_base64 = get_img_as_base64(img_path)


    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
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
        background-color: rgba(255, 255, 255, 0.45); /* Semi-transparent white overlay */
        z-index: 0; /* Ensure this is behind the input container */
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.sidebar.subheader("About the Model")
    st.sidebar.write("This website uses a Random Forest model (`model_RF.pkl`) for predictions.")

    st.title("Past Predictions")
    st.write("View all previous predictions here.")

    if st.session_state.past_predictions:
        past_predictions_df = pd.DataFrame(st.session_state.past_predictions)
        st.table(past_predictions_df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#f0f0f0'), ('font-weight', 'bold')]},
            {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f9f9f9')]},
            {'selector': 'tr:hover', 'props': [('background-color', '#e0e0e0')]},
        ]))
    else:
        st.info("No past predictions available. Make a prediction on the main page.")

if __name__ == "__main__":
    main()