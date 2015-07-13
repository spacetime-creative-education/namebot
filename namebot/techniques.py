from __future__ import absolute_import
from __future__ import division

from random import choice
import re
import nltk

from . import settings as namebot_settings
from . import normalization


___prefixes___ = namebot_settings.PREFIXES
___suffixes___ = namebot_settings.SUFFIXES
___alphabet___ = namebot_settings.ALPHABET
___vowels___ = namebot_settings.VOWELS
___regexes___ = namebot_settings.regexes

"""
Unless otherwise noted, all techniques operate
on a list of words and return a list of modified words.
"""


class InsufficientWordsError(Exception):
    def __init__(self, msg):
        self.msg = msg


def spoonerism(words):
    "First: [f]oo [b]ar => boo far"
    new_words = []
    if len(words) < 2:
        raise InsufficientWordsError('Need more than one word to combine')
    for k, word in enumerate(words):
        try:
            new_words.append('{}{} {}{}'.format(
                words[k + 1][0],  # 2nd word, 1st letter
                word[1:],  # 1st word, 2nd letter to end
                word[0],  # 1st word, 1st letter
                words[k + 1][1:]))  # 2nd word, 2nd letter to end
        except IndexError:
            continue
    return new_words


def kniferism(words):
    "Mid: f[o]o b[a]r => fao bor"
    if len(words) < 2:
        raise InsufficientWordsError('Need more than one word to combine')
    new_words = []
    for k, word in enumerate(words):
        try:
            middle_second = int(len(words[k + 1]) / 2)
            middle_first = int(len(word) / 2)
            new_words.append('{}{}{} {}{}{}'.format(
                word[:middle_first],
                words[k + 1][middle_second],
                word[middle_first + 1:],
                words[k + 1][:middle_second],
                word[middle_first],
                words[k + 1][middle_second + 1:]))
        except IndexError:
            continue
    return new_words


def forkerism(words):
    "Last: fo[o] ba[r] => for bao"
    if len(words) < 2:
        raise InsufficientWordsError('Need more than one word to combine')
    new_words = []
    for k, word in enumerate(words):
        try:
            s_word = words[k + 1]
            s_word_len = len(s_word)
            f_word_len = len(word)
            f_w_last_letter = word[f_word_len - 1]
            s_w_last_letter = words[k + 1][s_word_len - 1]
            new_words.append('{}{} {}{}'.format(
                word[:f_word_len - 1],  # 1st word, 1st letter to last - 1
                s_w_last_letter,  # 2nd word, last letter
                s_word[:s_word_len - 1],  # 2nd word, 1st letter to last - 1
                f_w_last_letter))  # 1st word, last letter
        except IndexError:
            continue
    return new_words


def reduplication_ablaut(words, count=1, random=True, vowel='e'):
    """
    http://phrases.org.uk/meanings/reduplication.html
    A technique to combine words and altering the vowels
    e.g ch[i]t-ch[a]t, d[i]lly, d[a]lly
    """
    if len(words) < 2:
        raise InsufficientWordsError('Need more than one word to combine')
    new_words = []
    substitution = choice(___vowels___) if random else vowel
    for word in words:
        second = re.sub(r'a|e|i|o|u', substitution, word, count=count)
        # Only append if the first and second are different.
        if word != second:
            new_words.append('{} {}'.format(word, second))
    return new_words


def affix_words(words, affix_type):
    """
    Do some type of affixing technique,
    such as prefixing or suffixing.
    TODO FINISH *-fixes from article
    """
    new_arr = []
    if len(words):
        if affix_type is 'prefix':
            for word in words:
                if not word:
                    continue
                for prefix in ___prefixes___:
                    first_prefix_no_vowel = re.search(
                        ___regexes___['no_vowels'], word[0])
                    second_prefix_no_vowel = re.search(
                        ___regexes___['no_vowels'], prefix[0])
                    if first_prefix_no_vowel or second_prefix_no_vowel:
                                # if there's a vowel at the end of
                                # prefix but not at the beginning
                                # of the word (or vice versa)
                                vowel_beginning = re.search(
                                    r'a|e|i|o|u', prefix[-1:])
                                vowel_end = re.search(
                                    r'^a|e|i|o|u', word[:1])
                                if vowel_beginning or vowel_end:
                                    new_arr.append('{}{}'.format(prefix, word))

        elif affix_type is 'suffix':
            for word in words:
                if not word:
                    continue
                for suffix in ___suffixes___:
                    prefix_start_vowel = re.search(
                        ___regexes___['all_vowels'], word[0])
                    suffix_start_vowel = re.search(
                        ___regexes___['all_vowels'], suffix[0])
                    if prefix_start_vowel or suffix_start_vowel:
                            if suffix is "ify":
                                if word[-1] is "e":
                                    if word[-2] is not "i":
                                        new_arr.append('{}{}'.format(
                                            word[:-2], suffix))
                                    else:
                                        new_arr.append(
                                            '{}{}'.format(
                                                word[:-1], suffix))
                                new_arr.append(word + suffix)
                            else:
                                new_arr.append(word + suffix)

        elif affix_type is 'duplifix':
            """
            makes duplification
            (e.g: teeny weeny, etc...)
            """
            for word in words:
                if not word:
                    continue
                for letter in ___alphabet___:
                    vowel_first = re.match(
                        ___regexes___['all_vowels'], word[1])
                    no_vowel_letter = re.match(
                        ___regexes___['no_vowels'], letter)
                    no_vowel_first = re.match(
                        ___regexes___['no_vowels'], word[1])
                    vowel_letter = re.match(
                        ___regexes___['all_vowels'], letter)
                    # check if the first letter is
                    # NOT the same as the second letter in reduplication
                    if word[0] is not letter:
                        # check if the first word is
                        # NOT the same as the second word. (or letter)
                        if word is not letter + word[1:]:
                            if vowel_first:
                                if no_vowel_letter:
                                    new_arr.append('{} {}{}'.format(
                                        word, letter, word[1:]))
                            elif no_vowel_first:
                                if vowel_letter:
                                    new_arr.append('{} {}{}'.format(
                                        word, letter, word[1:]))
        elif affix_type is "infix":
            pass

        elif affix_type is "disfix":
            pass

    return new_arr


def make_founder_product_name(founder1, founder2, product):
    """
    get the name of two people
    forming a company and combine it
    TODO: 1, 0, infinite
    """
    return '{} & {} {}'.format(
        founder1[0].upper(),
        founder2[0].upper(),
        product)


def make_name_obscured(words):
    """
    Takes a name and makes it obscure,
    ala Bebo, Ning, Bix, Jajah, Kiko.

    TODO ADDME
    """
    return


def make_cc_to_vc_swap(arr):
    """
    make name based on original word,
    but swap a CC with a V+C combo.
    if no double CC is found, skip it.

    origination: zappos -> zapatos

    examples:
        christopher -> christofaher
        christopher -> christokoer
        marshmallow -> margimallow

    TODO ADDME
    """
    return


def make_name_alliteration(word_array, divider=' '):
    new_arr = []
    """
    java jacket
    singing sally
    earth engines
    ...etc

    1. Loop through a given array of words
    2. group by words with the same first letter
    3. combine them and return to new array

    """
    word_array = sorted(word_array)

    for word1 in word_array:
        for word2 in word_array:
            if word1[:1] is word2[:1] and word1 is not word2:
                new_arr.append(word1 + divider + word2)
    return new_arr


def make_name_abbreviation(words):
    """
    this function will make some kind of
    interesting company acronym
    eg: BASF, AT&T, A&W
    Returns a single string of the new word combined.
    """
    return ''.join([word[:1].upper() for word in words])


def make_vowel(words, vowel_type, vowel_index):
    """Primary for all Portmanteau generators, that creates
    the portmanteau based on :vowel_index, and :vowel_type.

    The algorithm works as following:

    It looks for the first occurrence of a specified vowel in the first word,
    then gets the matching occurrence (if any) of the second word,
    then determines which should be first or second position, based on
    the ratio of letters (for each word) divided by the position of the vowel
    in question (e.g. c[a]t (2/3) vs. cr[a]te (3/5)).

    The higher number is ordered first, and the two words are then fused
    together by the single matching vowel.
    """
    new_arr = []
    for i in words:
        for j in words:
            is_match_i = re.search(vowel_type, i)
            is_match_j = re.search(vowel_type, j)
            if i is not j and is_match_i and is_match_j:
                # get the indices and lengths to use in finding the ratio
                pos_i = i.index(vowel_index)
                len_i = len(i)
                pos_j = j.index(vowel_index)
                len_j = len(j)

                # If starting index is 0,
                # add 1 to it so we're not dividing by zero
                if pos_i is 0:
                    pos_i = 1
                elif pos_j is 0:
                    pos_j = 1

                # Decide which word should be the
                # prefix and which should be suffix
                if round(pos_i / len_i) > round(pos_j / len_j):
                    p = i[0: pos_i + 1]
                    p2 = j[pos_j: len(j)]
                    if len(p) + len(p2) > 2:
                        if re.search(
                            ___regexes___['all_vowels'], p) or re.search(
                                ___regexes___['all_vowels'], p2):
                                    if p[-1] is p2[0]:
                                        new_arr.append(p[:-1] + p2)
                                    else:
                                        new_arr.append(p + p2)
    return new_arr


def make_portmanteau_default_vowel(words):
    """
    Make a portmanteau based on vowel
    matches (ala Brad+Angelina = Brangelina)
    Only matches for second to last letter
    in first word and matching vowel in second word.

    This defers to the make_vowel function for all the internal
    magic, but is a helper in that it provides all types of vowel
    combinations in one function.
    """
    new_arr = []
    vowel_a_re = re.compile(r'a{1}')
    vowel_e_re = re.compile(r'e{1}')
    vowel_i_re = re.compile(r'i{1}')
    vowel_o_re = re.compile(r'o{1}')
    vowel_u_re = re.compile(r'u{1}')

    new_arr += make_vowel(words, vowel_a_re, "a")
    new_arr += make_vowel(words, vowel_e_re, "e")
    new_arr += make_vowel(words, vowel_i_re, "i")
    new_arr += make_vowel(words, vowel_o_re, "o")
    new_arr += make_vowel(words, vowel_u_re, "u")
    return new_arr


def make_portmanteau_split(words):
    """
    nikon = [ni]pp[on] go[k]aku
    make words similar to nikon,
    which is comprised of Nippon + Gokaku.

    We get the first C+V in the first word,
    then last V+C in the first word,
    then all C in the second word.
    """
    new_arr = []
    for i in words:
        for j in words:
                if i is not j:
                    l1 = re.search(r'[^a|e|i|o|u{1}]+[a|e|i|o|u{1}]', i)
                    l2 = re.search(r'[a|e|i|o|u{1}]+[^a|e|i|o|u{1}]$', j)
                    if i and l1 and l2:
                        # Third letter used for
                        # consonant middle splits only
                        l3 = re.split(r'[a|e|i|o|u{1}]', i)
                        l1 = l1.group(0)
                        l2 = l2.group(0)
                        if l3 and len(l3) > 0:
                            for v in l3:
                                new_arr.append(l1 + v + l2)
                            else:
                                new_arr.append('{}{}{}'.format(l1, 't', l2))
                                new_arr.append('{}{}{}'.format(l1, 's', l2))
                                new_arr.append('{}{}{}'.format(l1, 'z', l2))
                                new_arr.append('{}{}{}'.format(l1, 'x', l2))
    return new_arr


def make_punctuator(words, replace):
    """Put some hyphens or dots, or a given punctutation via :replace
    in the word, but only around vowels ala "del.ic.ious"
    """
    def _replace(words, replace, replace_type='.'):
        return [word.replace(
            replace, replace + replace_type) for word in words]

    hyphens = _replace(words, replace, replace_type='-')
    periods = _replace(words, replace)
    return hyphens + periods


def make_punctuator_vowels(words):
    """Helper function that combines all
    possible combinations for vowels"""
    new_words = []
    new_words += make_punctuator(words, 'a')
    new_words += make_punctuator(words, 'e')
    new_words += make_punctuator(words, 'i')
    new_words += make_punctuator(words, 'o')
    new_words += make_punctuator(words, 'u')
    return new_words


def make_vowelify(words):
    """Chop off consonant ala nautica
    if second to last letter is a vowel.
    """
    new_arr = []
    for word in words:
        if re.search(___regexes___['all_vowels'], word[:-2]):
            new_arr.append(word[:-1])
    return new_arr


def make_misspelling(words):
    """
    This is used as the primary "misspelling"
    technique, through a few different techniques
    that are all categorized as misspelling.

    Brute force all combinations,
    then use double metaphone to remove odd ones.
    ...find a better way to do this
    TODO

    """
    token_groups = (
        ('ics', 'ix'),
        ('ph', 'f'),
        ('kew', 'cue'),
        ('f', 'ph'),
        ('o', 'ough'),
        # these seem to have
        # sucked in practice
        ('o', 'off'),
        ('ow', 'o'),
        ('x', 'ecks'),
        ('za', 'xa'),
        ('xa', 'za'),
        ('ze', 'xe'),
        ('xe', 'ze'),
        ('zi', 'xi'),
        ('xi', 'zi'),
        ('zo', 'xo'),
        ('xo', 'zo'),
        ('zu', 'xu'),
        ('xu', 'zu'),
        # number based
        ('one', '1'),
        ('1', 'one'),
        ('two', '2'),
        ('2', 'two'),
        ('three', '3'),
        ('3', 'three'),
        ('four', '4'),
        ('4', 'four'),
        ('five', '5'),
        ('5', 'five'),
        ('six', '6'),
        ('6', 'six'),
        ('seven', '7'),
        ('7', 'seven'),
        ('eight', '8'),
        ('8', 'eight'),
        ('nine', '9'),
        ('9', 'nine'),
        ('ten', '10'),
        ('10', 'ten'),
        ('ecks', 'x'),
        ('spir', 'speer'),
        ('speer', 'spir'),
        ('x', 'ex'),
        ('on', 'awn'),
        ('ow', 'owoo'),
        ('awn', 'on'),
        ('awf', 'off'),
        ('s', 'z'),
        ('ce', 'ze'),
        ('ss', 'zz'),
        ('ku', 'koo'),
        ('trate', 'trait'),
        ('trait', 'trate'),
        ('ance', 'anz'),
        ('il', 'yll'),
        ('ice', 'ize'),
        ('chr', 'kr'),
        # These should only be at end of word!
        ('er', 'r'),
        ('lee', 'ly'),
    )
    new_arr = []
    for word in words:
        for tokens in token_groups:
            new_arr.append(word.replace(*tokens))
    return normalization.uniquify(new_arr)


def make_name_from_latin_root(name_list):
    # TODO ADDME
    """
    This will take a latin word that is returned
    from a seperate lookup function and tweak it
    for misspelling specific to latin roots.
    """
    return


def pig_latinize(word, postfix='ay'):
    """Generates standard pig latin style,
    with customizeable postfix argument"""
    # Common postfixes: ['ay', 'yay', 'way']
    if not type(postfix) is str:
        raise TypeError('Must use a string for postfix.')

    piggified = None

    vowel_re = re.compile(r'(a|e|i|o|u)')
    first_letter = word[0:1]

    # clean up non letters
    word = word.replace(r'[^a-zA-Z]', '')

    if vowel_re.match(first_letter):
        piggified = word + 'way'
    else:
        piggified = ''.join([word[1: len(word)], first_letter, postfix])
    return piggified


def make_word_metaphor(words):
    # TODO ADDME
    """
    Make a metaphor based
    on some words...?
    """
    return


def acronym_lastname(description, lastname):
    """Inspiration: ALFA Romeo"""
    desc = ''.join([word[0].upper() for word in normalization.remove_stop_words(
        description.split(' '))])
    return '{} {}'.format(desc, lastname)


print(acronym_lastname('We make cool products.', 'Tabor'))


def make_phrase(words):
    # TODO ADDME
    """
    WIP (e.g.
        simplyhired, second life,
        stumbleupon)
    """
    return


def get_descriptors(words):
    """
    Use NLTK to first grab tokens by looping through words,
    then tag part-of-speech (in isolation)
    and provide a dictionary with a list of each type
    for later retrieval and usage
    """

    descriptors = {}
    tokens = nltk.word_tokenize(' '.join(words))
    parts = nltk.pos_tag(tokens)

    # TODO ADD freq. measurement to metrics

    """
    populate with an empty array for each type
    so no KeyErrors will be thrown,
    and no knowledge of NLTK classification
    is required
    """
    for part in parts:
        descriptors[part[1]] = []

    # Then, push the word into the matching type
    for part in parts:
        descriptors[part[1]].append(part[0])

    return descriptors


def make_descriptors(words):
    """
    Make descriptor names based off of a
    verb or adjective and noun combination.
    Examples:
        -Pop Cap,
        -Big Fish,
        -Red Fin,
        -Cold Water (grill), etc...

    Combines VBP/VB, with NN/NNS

    ...could be optimized
    """
    new_words = []

    def _helper(nouns, verbs):
        words = []
        try:
            for noun in nouns:
                for verb in verbs:
                    words.append('{} {}'.format(noun, verb))
                    words.append('{} {}'.format(verb, noun))
        except KeyError:
            pass
        return words

    new_words += _helper(words['NN'], words['VBP'])
    new_words += _helper(words['NNS'], words['VBP'])
    new_words += _helper(words['NN'], words['VB'])
    return new_words


def super_scrub(data):
    """
    Runs words through a comprehensive
    list of filtering functions
    Expects a dictionary with key "words"
    """
    for technique in data['words']:
        data['words'][technique] = normalization.uniquify(
            normalization.remove_odd_sounding_words(
                normalization.clean_sort(
                    data['words'][technique])))
    return data


def generate_all_techniques(words):
    """
    Generates all techniques across the
    library in one place, and cleans them for use
    """
    data = {
        'words': {
            'alliterations': make_name_alliteration(words),
            'alliterations': make_name_alliteration(words),
            'portmanteau': make_portmanteau_default_vowel(words),
            'vowels': make_vowelify(words),
            'suffix': affix_words(words, 'suffix'),
            'prefix': affix_words(words, 'prefix'),
            'duplifix': affix_words(words, 'duplifix'),
            'disfix': affix_words(words, 'disfix'),
            'infix': affix_words(words, 'infix'),
            'founder_product_name': make_founder_product_name(
                'Lindsey', 'Chris', 'Widgets'),
            'cc_to_vc_swap': make_cc_to_vc_swap(words),
            'name_obscured': make_name_obscured(words),
            'punctuator': make_punctuator_vowels(words),
            'name_abbreviation': make_name_abbreviation(words),
            'make_portmanteau_split': make_portmanteau_split(words),
            'latin_root': make_name_from_latin_root(words),
            'make_word_metaphor': make_word_metaphor(words),
            'make_phrase': make_phrase(words),
            'forkerism': forkerism(words),
            'kniferism': kniferism(words),
            'spoonerism': spoonerism(words),
            'reduplication_ablaut': reduplication_ablaut(words),
            'misspelling': make_misspelling(words),
            'descriptors': make_descriptors(
                get_descriptors(words))
        }
    }
    return super_scrub(data)