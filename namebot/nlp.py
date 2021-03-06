"""Functions that use Natural Language Processing.

Word relationships found (via NLTK and other libraries)
to find and generate related words.
"""


from __future__ import absolute_import

import itertools

from nltk.corpus import (
    verbnet,
    wordnet,
)

from . import normalization


def _get_synset_words(word):
    """Simple helper wrapping the more involved get_synsets function.

    :param word (str): The seed word.
    :rtype words (list): The list of NLTK words.
    """
    res = get_synsets([word])[word]
    if not res:
        return []
    res = res.values()
    words = list(normalization.flatten([l for l in res if l]))
    return words


def print_all_synset_categories():
    """Print all domains and categories for research purposes.

    :rtype categories (list): A list of all wordnet synsets.
    """
    categories = []
    for synset in list(wordnet.all_synsets('n')):
        categories.append(synset)
    return categories


def _get_lemma_names(sub_synset, use_definitions=False):
    """Get lemma names."""
    results = []
    if sub_synset():
        for v in sub_synset():
            if hasattr(v.lemma_names, '__call__'):
                results += v.lemma_names()
            else:
                results += v.lemma_names
            if use_definitions:
                results.append(v.definition.split())
    return results


def get_hyponyms(synset, use_definitions=False):
    """Extract hyponyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(synset.hyponyms, use_definitions=use_definitions)


def get_inst_hyponyms(synset, use_definitions=False):
    """Extract instance hyponyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.instance_hyponyms, use_definitions=use_definitions)


def get_member_meronyms(synset, use_definitions=False):
    """Extract meronyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.member_meronyms, use_definitions=use_definitions)


def get_substance_meronyms(synset, use_definitions=False):
    """Extract substance meronyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.substance_meronyms, use_definitions=use_definitions)


def get_part_meronyms(synset, use_definitions=False):
    """Extract part meronyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.part_meronyms, use_definitions=use_definitions)


def get_substance_holoynms(synset, use_definitions=False):
    """Extract substance holoynms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.substance_holonyms, use_definitions=use_definitions)


def get_topic_domains(synset, use_definitions=False):
    """Extract topic domains from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.topic_domains, use_definitions=use_definitions)


def get_region_domains(synset, use_definitions=False):
    """Extract region domains from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.region_domains, use_definitions=use_definitions)


def get_usage_domains(synset, use_definitions=False):
    """Extract usage domains from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.usage_domains, use_definitions=use_definitions)


def get_attributes(synset, use_definitions=False):
    """Extract attributes from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.attributes, use_definitions=use_definitions)


def get_entailments(synset, use_definitions=False):
    """Extract entailments from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.entailments, use_definitions=use_definitions)


def get_causes(synset, use_definitions=False):
    """Extract causes from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    if synset.causes():
        return _get_lemma_names(
            synset.causes, use_definitions=use_definitions)


def get_also_sees(synset, use_definitions=False):
    """Extract also-sees from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.also_sees, use_definitions=use_definitions)


def get_verb_groups(synset, use_definitions=False):
    """Extract verb groups from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.verb_groups, use_definitions=use_definitions)


def get_similartos(synset, use_definitions=False):
    """Extract similar-tos from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.similar_tos, use_definitions=use_definitions)


def get_member_holoynms(synset, use_definitions=False):
    """Extract member holonyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.member_holonyms, use_definitions=use_definitions)


def get_part_holoynms(synset, use_definitions=False):
    """Extract part holonyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.part_holonyms, use_definitions=use_definitions)


def get_instance_hypernyms(synset, use_definitions=False):
    """Extract instance hypernyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.instance_hypernyms, use_definitions=use_definitions)


def get_hypernyms(synset, use_definitions=False):
    """Extract hypernyms from a synset.

    :param (object): The synset instance.
    :param use_definitions (bool, optional):
        Extract definitions from the synset.
    :rtype list: The results list.
    """
    return _get_lemma_names(
        synset.hypernyms, use_definitions=use_definitions)


def get_verb_lemmas(verbs):
    """Return verbnet lemmas for the given verbs.

    These verbs are stemmed before lookup to prevent empty results.

    :param verbs (list) - The list of verbs (verbs) to reference.
    :rtype lemmas (list) - A list of lemmas for all verbs
                        - these are not separated by verb.
    """
    lemmas = []
    for verb in normalization.stem_words(verbs):
        _lemmas = verbnet.classids(lemma=verb)
        lemmas += [l.split('-')[0] for l in _lemmas]
    return lemmas


def get_word_synsets(word):
    """Get all synsets for a word.

    :param word (str): The word to lookup.
    :rtype object: The synset ring instance.
    """
    return wordnet.synsets(word.encode('utf-8'), pos=None)


def get_synset_definitions(word):
    """Return all possible definitions for synsets in a word synset ring.

    :param word (str): The word to lookup.
    :rtype definitions (list): The synset definitions list.
    """
    definitions = []
    synsets = get_word_synsets(word)
    for _synset in synsets:
        definitions.append(_synset.definition().split())
    return definitions


def get_synsets_definitions(words):
    """Return all possible definitions for all synsets in the synset ring.

    :param words (list): The list of words.
    :rtype sets (list): The synsets.
    """
    return [get_synset_definitions(w) for w in words if w]


def get_synsets(words, use_definitions=False, clean=False):
    """Brute force loop on a synset ring to get all related words.

    You are expected to filter or remove any that are not relevant separately,
    if the resultant set is too long.
    The scoring module provides tools to filter based on pronunciation,
    but you can write your own and extend the functionality.

    :param words (list): The list of words.
    :param use_definitions (bool, optional): Determine if definition words
            should also be extracted.
    :param clean (bool, optional): Determine if set should be de-duped,
            cleaned, etc...
    :rtype results (dict): The results dictionary.
    """
    results = {}

    for word in words:
        synsets = get_word_synsets(word)

        key = {'synset_original': []}

        for synset in synsets:
            if hasattr(synset.lemma_names, '__call__'):
                key['synset_original'].append(synset.lemma_names())
            else:
                key['synset_original'].append(synset.lemma_names)

            # More Specific *nyms (deep)
            key['hyponyms'] = get_hyponyms(
                synset, use_definitions=use_definitions)
            key['instance_hyponyms'] = get_inst_hyponyms(
                synset, use_definitions=use_definitions)
            key['member_meronyms'] = get_member_meronyms(
                synset, use_definitions=use_definitions)
            key['substance_meronyms'] = get_substance_meronyms(
                synset, use_definitions=use_definitions)
            key['part_meronyms'] = get_part_meronyms(
                synset, use_definitions=use_definitions)
            key['substance_holonyms'] = get_substance_holoynms(
                synset, use_definitions=use_definitions)

            # More Generic *nyms (shallow)
            key['member_holonyms'] = get_member_holoynms(
                synset, use_definitions=use_definitions)
            key['part_holonyms'] = get_part_holoynms(
                synset, use_definitions=use_definitions)
            key['instance_hypernyms'] = get_instance_hypernyms(
                synset, use_definitions=use_definitions)
            key['hypernyms'] = get_hypernyms(
                synset, use_definitions=use_definitions)

            # Other types
            key['topic_domains'] = get_topic_domains(
                synset, use_definitions=use_definitions)
            key['region_domains'] = get_region_domains(
                synset, use_definitions=use_definitions)
            key['usage_domains'] = get_usage_domains(
                synset, use_definitions=use_definitions)
            key['attributes'] = get_attributes(
                synset, use_definitions=use_definitions)
            key['entailments'] = get_entailments(
                synset, use_definitions=use_definitions)
            key['causes'] = get_causes(
                synset, use_definitions=use_definitions)
            key['also_sees'] = get_also_sees(
                synset, use_definitions=use_definitions)
            key['verb_groups'] = get_verb_groups(
                synset, use_definitions=use_definitions)
            key['similar_tos'] = get_similartos(
                synset, use_definitions=use_definitions)

        results[word] = key

    # 1. get words back
    # 2. flatten nested array
    # 3. split up words
    # 4. filter, clean, stem, uniquify

    for nlp_type in results:
        if clean:
            results[nlp_type] = sorted(
                normalization.uniquify(
                    normalization.clean_sort(
                        normalization.remove_stop_words(
                            normalization.stem_words(
                                normalization.remove_bad_words(
                                    list(itertools.chain(
                                        *results[nlp_type]))))))))

    return results
