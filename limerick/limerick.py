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

    def apostrophe_tokenize(self, line):
        word_tokens = word_tokenize(line)
        apostrophe_tokens = []
        i = 0
        while i < len(word_tokens):
            if i + 1 < len(word_tokens) and word_tokens[i + 1] == "n't" or word_tokens[i + 1] == "'ve":
                apostrophe_tokens.append(word_tokens[i] + word_tokens[i + 1])
                i += 1
            else:
                apostrophe_tokens.append(word_tokens[i])
            i += 1
        return apostrophe_tokens

    def guess_syllables(self, word):
        """
        Guesses the number of syllables by counting the number of non-contiguous vowels
        """
        # the most common letters that denote a vowel sound are aeiouy
        # however, if the last letter is 'e' it is usually omitted. Like 'spite', 'hike', 'placate'
        vowels = "aeiouyAEIOUY"
        last_character_vowel = False
        n_vowels = 0
        for i in range(len(word)):
            current_character_vowel = word[i] in vowels
            if (not last_character_vowel and current_character_vowel) \
                    and (not (i == len(word) - 1 and word[i] == "e")):
                n_vowels += 1
            last_character_vowel = current_character_vowel
        return n_vowels

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        # if either word does not exist in the dictionary, return False
        if a not in self._pronunciations or b not in self._pronunciations:
            return False

        n_a = self.num_syllables(a)
        n_b = self.num_syllables(b)

        # in principle we can have more than one pronunciation for each word
        # get all the shortest pronunciations
        min_phonemes_a = min(map(len, self._pronunciations[a]))
        phonemes_a = list(filter(lambda x: len(x) == min_phonemes_a, self._pronunciations[a]))

        min_phonemes_b = min(map(len, self._pronunciations[b]))
        phonemes_b = list(filter(lambda x: len(x) == min_phonemes_b, self._pronunciations[b]))

        for p_a in phonemes_a:
            for p_b in phonemes_b:

                vowel_positions_a = [x for x in range(len(p_a)) if p_a[x][-1].isdigit()]
                vowel_positions_b = [x for x in range(len(p_b)) if p_b[x][-1].isdigit()]

                # no vowels in the phonemes
                if len(vowel_positions_b) == 0 or len(vowel_positions_a) == 0:
                    continue

                first_vowel_a = vowel_positions_a[0]
                first_vowel_b = vowel_positions_b[0]

                if n_a == n_b:
                    # if they are the same length
                    if p_a[first_vowel_a:] == p_b[first_vowel_b:]:
                        return True
                else:
                    # if they are not the same length, one word must have another as suffix
                    if n_b < n_a:
                        # SWAP A and B
                        p_a, p_b, first_vowel_a, first_vowel_b = p_b, p_a, first_vowel_b, first_vowel_a

                    if p_a[first_vowel_a:] == p_b[len(p_b) - len(p_a) + first_vowel_a:]:
                        return True

        return False

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
        lines = text.split("\n")

        # if more than 5 lines in the text
        rhyme_scheme = "AABBA"
        rhyme_dict = {}
        line_counter = 0
        for line in lines:
            tokens = nltk.tokenize.word_tokenize(line)

            if len(tokens) == 0:
                continue

            words = [x for x in tokens if x not in punctuation]
            last_word = words[-1]

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
            for i in range(len(v) - 1):
                rhyme_flag = rhyme_flag and self.rhymes(v[i], v[i + 1])

        return rhyme_flag





if __name__ == "__main__":
    buffer = ""
    inline = " "
    while inline != "":
        buffer += "%s\n" % inline
        inline = input()

    ld = LimerickDetector()
    print("%s\n-----------\n%s" % (buffer.strip(), ld.is_limerick(buffer)))
