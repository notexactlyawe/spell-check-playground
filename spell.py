import whatthepatch
import enchant

def parse_patch_lines_changed(patch):
    """
    Parse a patch in order to return a list of lines that have been added
    or changed. ie. everywhere where new spelling errors have occured
    """
    lines_changed = []
    for diff in whatthepatch.parse_patch(patch):
        for line in diff.changes:
            if line[1] is not None:
                lines_changed.append(line)

    return lines_changed

def split_words(line):
    """
    Take a line from the patch and return a list of words split at " "
    and striped of any puntuation characters
    """
    words = []
    for word in line[2].split(" "):
        words.append(word.strip('.,!?:;'))

    return words

def correct_word(word, d):
    """
    Return a list of all possible corrections of a given word using dictionary d
    """
    if word:
        is_word = d.check(word)
    else:
        return []

    if not is_word:
        return d.suggest(word)
    else:
        return []

def spellcheck_patch(patch):
    d = enchant.Dict("en_US")

    lines_changed = parse_patch_lines_changed(patch)
    for line in lines_changed:
        words = split_words(line)
        for idx, word in enumerate(words):
            correction = correct_word(word, d)
            if correction:
                print("Line number: {}, word number: {}, word: {}, correction: {}".format(line[1], idx, word, correction[0]))

