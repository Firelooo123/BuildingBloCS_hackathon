import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

@st.cache_data
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data
def load_data():
    return pd.read_csv("coral_bleaching_data.csv")


def plot_bleaching_exposure(cleaned_df):
    sns.catplot(
        data=cleaned_df.sort_values(by='Exposure'),
        x='Exposure',
        y='Percent_Bleaching',
        kind='violin',
        aspect=2
    )
    plt.title("Percent Bleaching against Exposure")
    st.pyplot(plt.gcf())
    plt.clf() 


def plot_percent_bleaching_vs_bleaching_level(cleaned_df):
    sns.catplot(
        data=cleaned_df.sort_values(by='Bleaching_Level'),
        x='Bleaching_Level',
        y='Percent_Bleaching',
        kind='violin',
        aspect=2
    )
    plt.title("Percent Bleaching against Bleaching Level")
    st.pyplot(plt.gcf())
    plt.clf()


def plot_Percent_Bleaching_vs_Bleaching_Level_vs_Exposure(cleaned_df):
    sns.catplot(
        data=cleaned_df,
        x="Percent_Bleaching",
        y='Bleaching_Level',
        col='Exposure',
        alpha=0.5
    )
    plt.suptitle("Percent Bleaching vs Bleaching Level vs Exposure", y=1.05)
    st.pyplot(plt.gcf())
    plt.clf()


def plot_percent_cover_vs_country_name(cleaned_df):
    plt.figure(figsize=(15, 5))
    sns.boxplot(data=cleaned_df, x="Country_Name", y="Percent_Cover")
    plt.title("Percent Cover vs Country Name")
    st.pyplot(plt.gcf())
    plt.clf()


def main():
    st.set_page_config(
        page_title="Graphs Page",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


    img_path = "Ship.png"  # Callum Replace here
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
        background-color: rgba(255, 255, 255, 0.3); /* Semi-transparent white overlay */
        z-index: 0;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}

    p {{
        color: #000000;  /* Custom color */
        text-bold: True;
    }}

    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.sidebar.subheader("About the Model")
    st.sidebar.write("This website uses a Random Forest model (`model_RF.pkl`) for predictions.")

    st.markdown("<h1 style='text-align: center;'>Past Coral Bleaching Data</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Explore visualizations of the past years coral bleaching dataset.</p>" , unsafe_allow_html=True)


    cleaned_df = load_data()

    st.markdown("<hr style='border: 5px solid black;'>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: center;'>Graph 1: Percent Cover vs Country Name</h4>", unsafe_allow_html=True)
    plot_percent_cover_vs_country_name(cleaned_df)
    st.markdown("<p style='text-align: center;'>This box plot shows coral cover across Southeast Asian countries, with Thailand, Philippines, "
    "Malaysia, and Myanmar having higher and more variable cover, while Singapore has the lowest. Indonesia, Vietnam, and "
    "Brunei have many outliers, indicating diverse conditions.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 5px solid black;'>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: center;'>Graph 2: Percent Bleaching against Exposure</h4>", unsafe_allow_html=True)
    plot_bleaching_exposure(cleaned_df)
    st.markdown("<p style='text-align: center;'>Based on historical coral bleaching events, "
    "all three exposure categories exhibit a wide distribution of data, with bleaching levels remaining below <b>20%</b> This shows that for the "
    "past decade, most of the Southeast countries coral bleaching is not severe, but we need to take precautions of the coral reefs in the future.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 5px solid black;'>", unsafe_allow_html=True)


    st.markdown("<h4 style='text-align: center;'>Graph 3: Percent Bleaching against Bleaching Level</h4>", unsafe_allow_html=True)
    plot_percent_bleaching_vs_bleaching_level(cleaned_df)
    st.markdown(
    "<p style='text-align: center;'>Based on historical coral bleaching events, most coral reefs in Southeast Asia "
    "exhibit a wide distribution with bleaching levels below <b>5%</b>. In contrast, at the colony level, the data distribution "
    "is evenly spread across all bleaching percentage categories.</p>",
    unsafe_allow_html=True)
    st.markdown("<hr style='border: 5px solid black;'>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: center;'>Graph 4: Percent Bleaching vs Bleaching Level vs Exposure</h4>", unsafe_allow_html=True)
    plot_Percent_Bleaching_vs_Bleaching_Level_vs_Exposure(cleaned_df)
    st.markdown("<p style='text-align: center;'>Based on historical coral bleaching events, the data shows "
    "that population-level bleaching is concentrated at lower percentages, while colony-level bleaching is more "
    "widely distributed. Sheltered corals have a more even bleaching distribution. whereas exposed corals show greater"
    "variability, suggesting exposure influences bleaching serverity.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 5px solid black;'>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()