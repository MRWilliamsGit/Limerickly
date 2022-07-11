from scripts.lim import limerickly
import streamlit as st


def writelim():
    for l in st.session_state.ourlim.limerick:
        st.write(l)


def get_guest_line(text):
    nextline = st.text_input(text, " ")
    if nextline != " ":
        st.session_state.ourlim.add_line(nextline)
        st.experimental_rerun()


def get_robo_line(text):
    rhymes = st.session_state.ourlim.get_sentences2(5)
    nextline = st.selectbox(text, rhymes)
    if nextline != " ":
        st.session_state.ourlim.add_line(nextline)
        st.experimental_rerun()


def main():

    st.title("Limerickly")
    st.write("🤖 Let's write a limerick together!")
    st.markdown("""---""")

    if "ourlim" not in st.session_state:
        with st.spinner("assembling the robot..."):
            st.session_state.ourlim = limerickly()

    writelim()

    # get which line we are on and proceed accordingly
    place = len(st.session_state.ourlim.limerick)

    if place == 0:
        get_guest_line("Start your limerick:")
    elif place == 1:
        get_robo_line("Choose a second line:")
    elif place == 2:
        get_guest_line("Write a third line:")
    elif place == 3:
        get_robo_line("Choose a fourth line:")
    elif place == 4:
        get_robo_line("Choose a final line:")
        get_guest_line("(Or write your own):")
    elif place == 5:
        if st.button("Lets do it again!"):
            del st.session_state.ourlim
            st.experimental_rerun()


if __name__ == "__main__":
    main()
