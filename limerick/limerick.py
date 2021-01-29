# Author: YOUR NAME HERE
# Date: DATE SUBMITTED

# Use word_tokenize to split raw text into words
from string import punctuation
import itertools
import nltk
from nltk.tokenize import word_tokenize


class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        # if no entry, return 1
        if word not in self._pronunciations:
            return 1
        else:
            # get the shorter pronunciation
            phonemes = min(self._pronunciations[word], key=len)
            # count the number of stresses
            num_stress = len([x for x in phonemes if x[-1].isdigit()])
            return num_stress

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        # if either word does not exist in the dictionary, return False
        if a not in self._pronunciations or b not in self._pronunciations:
            return False

        rhyme = False
        # if words start with consonants

        for pronounce_a in self._pronunciations[a]:
            for pronounce_b in self._pronunciations[b]:
                _rhyme = True
                n_syllables_a = len(pronounce_a)
                n_syllables_b = len(pronounce_b)
                for p_a, p_b in zip(pronounce_a[n_syllables_a - min(n_syllables_a, n_syllables_b) + 1:],
                                    pronounce_b[n_syllables_b - min(n_syllables_a, n_syllables_b) + 1:]):
                    if p_a != p_b:
                        _rhyme = False
                        break
                rhyme = rhyme or _rhyme

        return rhyme

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other (and not the A
        lines).

        (English professors may disagree with this definition, but that's what
        we're using here.)
        """
        print(text)
        lines = text.split("\n")

        # if more than 5 lines in the text
        rhyme_scheme = "AABBA"
        rhyme_dict = {}
        line_counter = 0
        for line in lines:
            words = [x for x in nltk.tokenize.word_tokenize(line) if x not in punctuation]
            last_word = words[-1]

            # if only space or only one character
            if len(words)==0:
                continue

            # if any of the word is not in the dictionary, return False
            if last_word not in self._pronunciations:
                return False

            if rhyme_scheme[line_counter] not in rhyme_dict:
                rhyme_dict[rhyme_scheme[line_counter]] = [last_word]
            else:
                rhyme_dict[rhyme_scheme[line_counter]].append(last_word)
                # if the word already exists in the limerick
            line_counter += 1

        # more than five sentences
        if line_counter != 5:
            return False

        rhyme_flag = True
        for k, v in rhyme_dict.items():
            # check for pairwise rhyme
            for i in range(len(v)-1):
                print(v[i], v[i+1], self.rhymes(v[i], v[i+1]))
                rhyme_flag = rhyme_flag and self.rhymes(v[i], v[i+1])
        print(rhyme_flag)
        return rhyme_flag


if __name__ == "__main__":
    buffer = ""
    inline = " "
    while inline != "":
        buffer += "%s\n" % inline
        inline = input()

    ld = LimerickDetector()
    print("%s\n-----------\n%s" % (buffer.strip(), ld.is_limerick(buffer)))
