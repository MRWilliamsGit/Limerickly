from scripts.helpers import get_rhyme
from scripts.lim import limerickly
#sources: https://devpost.com/software/rhyme-with-ai
#sources: https://ramsrigoutham.medium.com/sized-fill-in-the-blank-or-multi-mask-filling-with-roberta-and-huggingface-transformers-58eb9e7fb0c

def main():
    lim = limerickly()
    lim.add_line("There once was a frog in my soup")
    rhymes = lim.get_sentences2(5)
    #rhymes = get_rhyme("boast", 10)
    print(rhymes)

if __name__ == "__main__":
    main()