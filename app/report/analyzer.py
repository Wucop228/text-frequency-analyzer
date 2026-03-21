from collections import defaultdict

import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def analyze_file(filepath: str) -> dict[str, dict]:
    word_stats = {}
    line_cnt = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line_cnt += 1
            words_in_line = defaultdict(int)

            for token in get_words(line):
                words_in_line[token] += 1

            for word, count in words_in_line.items():
                if word not in word_stats:
                    lemma = morph.parse(word)[0].normal_form
                    word_stats[word] = {
                        "lemma": lemma,
                        "total": 0,
                        "per_line": [],
                    }

                stat = word_stats[word]
                stat["per_line"].extend([0] * (line_cnt - len(stat["per_line"]) - 1))
                stat["per_line"].append(count)
                stat["total"] += count

    for stat in word_stats.values():
        stat["per_line"].extend([0] * (line_cnt - len(stat["per_line"])))

    return word_stats

def get_words(line: str) -> list[str]:
    res = []
    curr = []

    for char in line:
        if char.isalpha() or char == "-":
            curr.append(char.lower())
        else:
            if curr:
                word = "".join(curr).strip("-")
                if word:
                    res.append(word)
                curr = []

    if curr:
        word = "".join(curr).strip("-")
        if word:
            res.append(word)

    return res