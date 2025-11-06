


import sacrebleu
# from codebleu import calc_codebleu

def bleu_score(reference: str, hypothesis: str) -> float:
    bleu = sacrebleu.corpus_bleu([hypothesis], [[reference]])
    return bleu.score

# def codebleu_score(reference: str, hypothesis: str, lang: str = "python") -> float:
#     result = calc_codebleu(
#         [reference],
#         [hypothesis],
#         lang=lang,
#         weights=(0.25, 0.25, 0.25, 0.25)
#     )
#     return result["codebleu"]
