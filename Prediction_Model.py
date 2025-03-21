import streamlit as st
import numpy as np
import joblib
import base64
import pandas as pd


def load_model():
    model = joblib.load('model_RF.pkl')
    return model


def predict(model, input_data):
    prediction = model.predict(input_data)
    return prediction


@st.cache_data
def get_img_as_base64(file):
    with open(file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


if 'past_predictions' not in st.session_state:
    st.session_state.past_predictions = []

def main():

    st.set_page_config(
        page_title="Coral Bleaching Prediction",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


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
    .stTextInput label {{
        color: #333; /* Darker text color for labels */
    }}
    .stTextInput > div > div {{
        background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent input fields */
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add shadow for depth */
    }}
    .stButton > button {{
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


    model = load_model()

    st.sidebar.subheader("About the Model")
    st.sidebar.write("This website uses a Random Forest model (`model_RF.pkl`) for predictions.")


    st.title("Coral Bleaching Prediction")
    st.write("Welcome to the Coral Bleaching Prediction website! Our website is designed to help you predict the likelihood of coral bleaching "
    "based on two various scenarios: Manual and Automated!")

    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    prediction_mode = st.radio(
        "Prediction Mode",
        options=["Manual", "IoT sensors"]
    )


    if prediction_mode == "Manual":

        st.header("Manual Prediction")

        st.write("This feature allows you to manually input data to make predictions on coral bleaching acrosss Southeast Asia. Happy predicting!")

        col1, col2 = st.columns(2)
        with col1:
            depth_m = st.number_input("Depth (m)", value=0.0, step=1.0, format="%.1f", min_value=0.0)
            turbidity = st.number_input("Turbidity", value=0.0, step=0.05, format="%.4f", min_value=0.0)
            percent_cover = st.number_input("Percent Cover", value=0.0, step=0.5, format="%.2f", min_value=0.0)
        with col2:
            distance_to_shore = st.number_input("Distance to Shore", value=0.0, step=5.0, format="%.1f", min_value=0.0)
            ssta = st.number_input("SSTA", value=0.0, step=0.5, format="%.2f")
            tsa = st.number_input("TSA", value=0.0, step=0.5, format="%.2f")


        country_name = st.selectbox(
            "Country Name",
            options=["Malaysia", "Others", "Philippines", "Indonesia"],
            index=0
        )
        exposure = st.selectbox(
            "Exposure",
            options=["Sheltered", "Sometimes", "Exposed"],
            index=0
        )
        bleaching_level_population = st.selectbox(
            "Bleaching Level",
            options=["Population", "Colony"],
            index=0
        )


        if country_name == "Malaysia":
            country_name_malaysia = 1
            country_name_others = 0
            country_name_philippines = 0
        elif country_name == "Others":
            country_name_malaysia = 0
            country_name_others = 1
            country_name_philippines = 0
        elif country_name == "Indonesia":
            country_name_malaysia = 0
            country_name_others = 0
            country_name_philippines = 0
        else:  # Philippines
            country_name_malaysia = 0
            country_name_others = 0
            country_name_philippines = 1

        if exposure == "Sheltered":
            exposure_sheltered = 1
            exposure_sometimes = 0
        elif exposure == "Exposed":
            exposure_sheltered = 0
            exposure_sometimes = 0
        else:
            exposure_sheltered = 0
            exposure_sometimes = 1

        if bleaching_level_population == "Population":
            bleaching_level_population = 0
        else:
            bleaching_level_population = 1



        input_data = np.array([
            [
                depth_m,
                distance_to_shore,
                turbidity,
                ssta,
                tsa,
                percent_cover,
                country_name_malaysia,
                country_name_others,
                country_name_philippines,
                exposure_sheltered,
                exposure_sometimes,
                bleaching_level_population
            ]
        ])

        rounded_prediction = None


        if st.button("Predict"):
            with st.spinner("Making prediction..."):
                prediction = predict(model, input_data)
                rounded_prediction = round(prediction[0], 2)
                st.success(f"Predicted Bleaching Percentage: {rounded_prediction}%")

        if rounded_prediction is not None:
            input_dict = {
                "Depth (m)": depth_m,
                "Distance to Shore": distance_to_shore,
                "Turbidity": turbidity,
                "SSTA": ssta,
                "TSA": tsa,
                "Percent Cover": percent_cover,
                "Country Name": country_name,
                "Exposure": exposure,
                "Bleaching Level": bleaching_level_population,
                "Prediction": rounded_prediction
            }

            st.session_state.past_predictions.append(input_dict)

        st.markdown('</div>', unsafe_allow_html=True)

    elif prediction_mode == "IoT sensors":

        st.header("IoT sensors Prediction")
        st.write("Welcome to the IoT sensors prediction feature.")
        st.write("Please select a Southeast Asia country! (If your country is not listed, select 'Others')")

        country_name = st.selectbox(
            "Country Name",
            options=["Malaysia", "Philippines", "Indonesia", "Others"],
            index=0
        )

        

        data = {
            'Depth (m)': [5.0],
            'Distance to Shore': [40.0],
            'Turbidity': [3.0],
            'SSTA': [24.5],
            'TSA': [15.4],
            'Percent Cover': [24.0],
            'Country Name': [country_name],
            'Exposure': ['Sheltered'],
            'Bleaching Level': ['Population']
        }

        df = pd.DataFrame(data)

        # Display the table in Streamlit
        st.title("IoT Sensors Data")
        st.dataframe(df)

        if country_name == "Malaysia":
            country_name_malaysia = 1
            country_name_others = 0
            country_name_philippines = 0
        elif country_name == "Others":
            country_name_malaysia = 0
            country_name_others = 1
            country_name_philippines = 0
        elif country_name == "Indonesia":
            country_name_malaysia = 0
            country_name_others = 0
            country_name_philippines = 0
        else:  # Philippines
            country_name_malaysia = 0
            country_name_others = 0
            country_name_philippines = 1

        input_data = np.array([
            [
                5.0,
                40.0,
                3.0,
                24.5,
                15.4,
                24.0,
                country_name_malaysia,
                country_name_others,
                country_name_philippines,
                1,
                0,
                1
            ]
        ])

        if st.button("Predict"):
            with st.spinner("Making prediction..."):
                prediction = predict(model, input_data)
                rounded_prediction = round(prediction[0], 2)
                st.success(f"Predicted Bleaching Percentage: {rounded_prediction}%")

if __name__ == "__main__":
    main()