import streamlit as st

def main():
    st.title("Fight Goblin")

    st.write("Welcome to Fight Goblin! This is a UFC fight companion that allows friends to make predictions on the outcomes of matches.")

    st.write("To get started, please enter your name and device ID.")

    st.session_state.name = st.text_input("Name")
    st.session_state.create_user_button = st.button("Join the Goblin")

if __name__ == "__main__":
    main()
