import streamlit as st
import pickle
from streamlit_extras.let_it_rain import rain

filename = "model.h5"
model = pickle.load(open(filename, "rb"))

sex_d = {0: "Kobieta", 1: "Mężczyzna"}
pclass_d = {0: "Pierwsza", 1: "Druga", 2: "Trzecia"}
embarked_d = {0: "Cherbourg", 1: "Queenstown", 2: "Southampton"}

def main():
    st.set_page_config(
        page_title="Czy przeżyłbyś katastrofę?",
        page_icon="🚢",
    ) 
    overview = st.container()
    left, right = st.columns(2)
    prediction = st.container()
    image = st.empty()
    
    original_image = "https://media1.popsugar-assets.com/files/thumbor/7CwCuGAKxTrQ4wPyOBpKjSsd1JI/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2017/04/19/743/n/41542884/5429b59c8e78fbc4_MCDTITA_FE014_H_1_.JPG"
    st.image(original_image)
    
    with overview:
        st.title("Czy przeżyłbyś katastrofę?")
        
    with left:
        sex_radio = st.radio("Płeć", list(sex_d.keys()), format_func=lambda x: sex_d[x])
        pclass_radio = st.radio("Klasa", list(pclass_d.keys()), format_func=lambda x: pclass_d[x])
        embarked_radio = st.radio("Port", list(embarked_d.keys()), index=2, format_func=lambda x: embarked_d[x])
        
    with right:
        age_slider = st.slider("Wiek", value=50, min_value=1, max_value=100)
        sibsp_slider = st.slider("# Liczba rodzeństwa i/lub partnera", min_value=0, max_value=8)
        parch_slider = st.slider("# Liczba rodziców i/lub dzieci", min_value=0, max_value=6)
        fare_slider = st.slider("Cena biletu", min_value=0.0, max_value=500.0, value=50.0)
    
    if st.button('Predict'):
        if embarked_radio == 0:
            embarked_Q = 0
            embarked_S = 0
        elif embarked_radio == 1:
            embarked_Q = 1
            embarked_S = 0
        else:
            embarked_Q = 0
            embarked_S = 1

        data = [
            [
                pclass_radio,
                age_slider,
                sibsp_slider,
                parch_slider,
                fare_slider,
                sex_radio,
                embarked_Q,
                embarked_S
            ]
        ]

        survival = model.predict(data)
        s_confidence = model.predict_proba(data)

        with prediction:
            st.header("Dana osoba {0} przeżyje!".format("" if survival[0] == 1 else "NIE"))
            st.subheader("Pewność predykcji: {:.2f} %".format(s_confidence[0][survival[0]] * 100))
        
        if survival[0] == 1:
            st.balloons()
            new_image = "https://www.shutterstock.com/shutterstock/photos/59466772/display_1500/stock-photo-happy-man-in-a-yacht-or-sailing-boat-enjoying-life-59466772.jpg"
        else:
            rain(
                emoji="❄️",
                font_size=54,
                falling_speed=5,
                animation_length="infinite",
            )
            new_image = "https://www.shutterstock.com/shutterstock/photos/101902864/display_1500/stock-photo-portrait-of-a-man-frozen-into-an-ice-cube-101902864.jpg"
            
        image.image(new_image)


if __name__ == '__main__':
    main()
