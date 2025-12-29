import unittest
import re

CYR_RE = re.compile(r"[\u0400-\u04FF]")
SET_CYR_RE = {chr(code) for code in range (0x0400, 0x0500) if CYR_RE.match(chr(code))}
print('SET_CYR_RE =>', SET_CYR_RE)
LAT_RE = re.compile(r"[A-Za-z]")
CYR_TO_LAT_VISUAL = {
    # Великі
    "А": "A",
    "В": "B",
    "Е": "E",
    "К": "K",
    "М": "M",
    "Н": "H",
    "О": "O",
    "Р": "P",
    "С": "C",
    "Т": "T",
    "Х": "X",
    "У": "Y",
    "І": "I",
    "З": "3",

    # Малі
    "а": "a",
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "c",
    "х": "x",
    "у": "y",
    "і": "i",
    "к": "k",
    "з": "3",

}
CYR_VISUAL_KEYS = set(CYR_TO_LAT_VISUAL.keys())
CYR_SPECIFIC_KEYS = SET_CYR_RE - CYR_VISUAL_KEYS

SMILES_NOTLETTERS_SYMB = set("0123456789()[]-=#:.\/+@%*")

def clean_chem_formula(word: str):
    print()
    print('Рядок на вході =>', word)
    word_by_letters = list(word)
    all_cyr_specific_literas_in_word = [ch for ch in word if ch in CYR_SPECIFIC_KEYS ]
    len_cyr_specific = len(all_cyr_specific_literas_in_word)
    print('len_cyr_specific= ', len_cyr_specific )

    if len_cyr_specific > 0:
        print('all_cyr_specific_literas_in_word =>', all_cyr_specific_literas_in_word)
        print(f'У слові [{word}] наявні специфічні для кириличні маркери')
        print('Схоже, що поняття записане  українською і є складним.')
        return word

    else:

        if CYR_RE.search(word) and LAT_RE.search(word):
            print(f'У слові [{word}] змішані алфавіти кирилиці і латиниці')

            for pos, litera in enumerate(word_by_letters):
                if litera in CYR_TO_LAT_VISUAL:
                    print(f'pos={pos} cyr_litera={litera}')
                    word_by_letters[pos] = CYR_TO_LAT_VISUAL[litera]

            return ''.join(word_by_letters)

        else:
            print(f'Перевірка на наявність у слові [{word}] кириличних літер,\n що можуть мати латинські двійники:')
            gomoglif = 0
            for pos, litera in enumerate(word_by_letters):

                if litera in CYR_TO_LAT_VISUAL:
                    gomoglif+=1
                    print(f'pos={pos} cyr_litera={litera}')
                    word_by_letters[pos] = CYR_TO_LAT_VISUAL[litera]

            if gomoglif == 0:
                print(f'У слові [{word}] усі первинні літери латинські')
                if not (SMILES_NOTLETTERS_SYMB & set(word_by_letters)):
                    print('''Рекомендується ручна перевірка хімічної формули (типу КВ),\nоскільки в ній відсутні нелітерні специфічні хімічні символи''')
                    return ''.join(word_by_letters)
                else:
                    return ''.join(word_by_letters)

            else : #gomoglif > 0
                print(f'У слові [{word}] усі первинні літери кириличні були перетворено на  латинські')
                if not (SMILES_NOTLETTERS_SYMB & set(word_by_letters)):
                    print('''Рекомендується ручна перевірка хімічної формули (типу КВ),\nоскільки в ній відсутні нелітерні специфічні хімічні символи''')
                    return ''.join(word_by_letters)
                else:
                    return ''.join(word_by_letters)





##########
print(clean_chem_formula('СН3СООН'))
print(clean_chem_formula('буфери, детергенти(SDS)'))
print(clean_chem_formula('УФ випромінювання'))
print(clean_chem_formula('українське слово'))
print(clean_chem_formula('AgNO3'))
print(clean_chem_formula('Со(СН2=СН2-СOO)3'))
print(clean_chem_formula('Не'))
print(clean_chem_formula('КNО3'))
print(clean_chem_formula('НgNО3'))
print(clean_chem_formula('КВ'))
print(clean_chem_formula('F3N'))
print(clean_chem_formula('F'))
print(clean_chem_formula('КSСN'))
'''
class TestCleanChemFormula(unittest.TestCase):

    def test_valid_smiles(self):
        self.assertEqual(clean_chem_formula("AgNO3"), "AgNO3")

    def test_cyrillic_formula(self):
        self.assertEqual(clean_chem_formula("СН3СООН"), "CH3COOH")

    def test_mixed_alphabet(self):
        self.assertEqual(clean_chem_formula("КNО3"), "KNO3")

    def test_needs_review(self):
        self.assertEqual(clean_chem_formula("КВ"), "?KB")
        self.assertEqual(clean_chem_formula("Не"), "?He")

if __name__ == "__main__":
    unittest.main()'''