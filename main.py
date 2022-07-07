from scripts.helpers import get_rhyme
from scripts.lim import limerickly
import streamlit as st

def main():
    lim = limerickly()

    st.title("Limerickly")
    st.write("Let's write a limerick together!")
    line1 = st.text_input("Start your limerick:", ' ')

    if line1 != ' ':
        lim.add_line(line1)
        rhymes1 = lim.get_sentences2(5)     
        choose1 = st.selectbox("Choose your second line:", rhymes1)

        if choose1 != ' ':
            lim.add_line(choose1)
            line2 = st.text_input("Write a third line:", ' ')

            if line2 != ' ':
                lim.add_line(line2)
                rhymes2 = lim.get_sentences2(5) 
                choose2 = st.selectbox("Choose your fourth line:", rhymes2)

                if choose2 != ' ':
                    lim.add_line(choose2)
                    line3 = st.text_input("Write the final line...", ' ')
                    rhymes3 = lim.get_sentences2(5)
                    choose3 = st.selectbox("Or choose one from the AI:", rhymes3)



if __name__ == "__main__":
    main()