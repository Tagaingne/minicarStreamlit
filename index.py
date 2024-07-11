import streamlit as st
import streamlit.components.v1 as components

def main():
    st.title("MINICAR")

    # Charger le contenu HTML depuis le fichier controlcar.html
    with open('controlcar.html', 'r', encoding='utf-8') as f:
        controlcar_html = f.read()

    # Afficher le contenu HTML dans Streamlit
    components.html(controlcar_html, height=800)

if __name__ == '__main__':
    main()
