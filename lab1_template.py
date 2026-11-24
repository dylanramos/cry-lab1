# IMPORTANT
# IL EST PRIMORDIAL DE NE PAS CHANGER LA SIGNATURE DES FONCTIONS
# SINON LES CORRECTIONS RISQUENT DE NE PAS FONCTIONNER CORRECTEMENT
from itertools import count

from unidecode import unidecode


def sanitize_text(text):
    """
    Parameters
    ----------
    text: the text to sanitize

    Returns
    -------
    the sanitized text
    """
    text = ''.join(char for char in text if char.isalpha()).upper()
    text = unidecode(text)  # Convert letters with accents to their equivalent without accents
    text = ''.join(char for char in text if 65 <= ord(char) <= 90)

    return text


def caesar_encrypt(text, key):
    """
    Parameters
    ----------
    text: the plaintext to encrypt
    key: the shift which is a number

    Returns
    -------
    the ciphertext of <text> encrypted with Caesar under key <key>
    """
    ciphertext = []

    for char in text:
        shifted_char = chr((ord(char) - 65 + key) % 26 + 65)
        ciphertext.append(shifted_char)

    return ''.join(ciphertext)


def caesar_decrypt(text, key):
    """
    Parameters
    ----------
    text: the ciphertext to decrypt
    key: the shift which is a number

    Returns
    -------
    the plaintext of <text> decrypted with Caesar under key <key>
    """
    plain_text = []

    for char in text:
        shifted_char = chr((ord(char) - 65 - key) % 26 + 65)
        plain_text.append(shifted_char)

    return ''.join(plain_text)


def freq_analysis(text):
    """
    Parameters
    ----------
    text: the text to analyse

    Returns
    -------
    list
        the frequencies of every letter (a-z) in the text.

    """
    # Each value in the vector should be in the range [0, 1]
    freq_vector = [0] * 26
    text_length = len(text)

    if text_length == 0:
        print("The text is empty")
        return freq_vector

    for char in text:
        freq_vector[ord(char) - 65] += 1

    freq_vector = [freq / text_length for freq in freq_vector]

    return freq_vector


def caesar_break(text, ref_freq):
    """
    Parameters
    ----------
    text: the ciphertext to break
    ref_freq: the output of the freq_analysis function on a reference text

    Returns
    -------
    a number corresponding to the caesar key
    """
    chi2_sums = [0] * 26

    for i in range(26):
        freq = freq_analysis(caesar_decrypt(text, i))
        chi2_sums[i] = sum((f - r) ** 2 / r if r != 0 else 1 for f, r in zip(freq, ref_freq))

    return chi2_sums.index(min(chi2_sums))


def vigenere_encrypt(text, key):
    """
    Parameters
    ----------
    text: the plaintext to encrypt
    key: the keyword used in Vigenere (e.g. "pass")

    Returns
    -------
    the ciphertext of <text> encrypted with Vigenere under key <key>
    """
    ciphertext = []
    key_length = len(key)

    if key_length == 0:
        print("The key is empty")
        return ''

    for i, char in enumerate(text):
        ciphertext.append(chr((ord(char) - 65 + ord(key[i % key_length]) - 65) % 26 + 65))

    return ''.join(ciphertext)


def vigenere_decrypt(text, key):
    """
    Parameters
    ----------
    text: the ciphertext to decrypt
    key: the keyword used in Vigenere (e.g. "pass")

    Returns
    -------
    the plaintext of <text> decrypted with Vigenere under key <key>
    """
    plain_text = []
    key_length = len(key)

    if key_length == 0:
        print("The key is empty")
        return ''

    for i, char in enumerate(text):
        plain_text.append(chr((ord(char) - 65 - (ord(key[i % key_length]) - 65)) % 26 + 65))

    return ''.join(plain_text)


def coincidence_index(text):
    """
    Parameters
    ----------
    text: the text to analyse

    Returns
    -------
    the index of coincidence of the text
    """
    text_length = len(text)

    if text_length == 0:
        print("The text is empty")
        return 0

    letter_count_vector = [0] * 26

    for char in text:
        letter_count_vector[ord(char) - 65] += 1

    ci = 26 * sum(letter_count * (letter_count - 1) for letter_count in letter_count_vector) / (
            text_length * (text_length - 1)) if text_length > 1 else 1

    return ci


def vigenere_break(text, ref_freq, ref_ci):
    """
    Parameters
    ----------
    text: the ciphertext to break
    ref_freq: the output of the freq_analysis function on a reference text
    ref_ci: the output of the coincidence_index function on a reference text

    Returns
    -------
    the keyword corresponding to the encryption key used to obtain the ciphertext
    """
    text_length = len(text)

    if text_length == 0:
        print("The text is empty")
        return ''

    max_key_length = text_length + 1 if text_length < 21 else 21
    ci_vector = [0] * max_key_length

    for key_length in range(1, max_key_length):
        sub_text = []

        for i in range(text_length):
            if i % key_length == 0:
                sub_text.append(text[i])

        ci_vector[key_length] = coincidence_index(''.join(sub_text))
        key_length += 1

    key_length = min(range(max_key_length), key=lambda index: abs(ci_vector[index] - ref_ci))
    key = []

    for i in range(key_length):
        sub_text = []

        for j in range(i, text_length, key_length):
            sub_text.append(text[j])

        key.append(chr((caesar_break(''.join(sub_text), ref_freq)) + 65))

    return ''.join(key)


def vigenere_improved_encrypt(text, key):
    """
    Parameters
    ----------
    text: the plaintext to encrypt
    key: the keyword used in Vigenere (e.g. "pass")
    
    Returns
    -------
    the ciphertext of <text> encrypted with improved Vigenere under key <key> 
    """
    key_length = len(key)

    if key_length == 0:
        print("The key is empty")
        return ''

    ciphertext = []

    for i in range(0, len(text), key_length):
        block = text[i:i + key_length]
        encrypted_block = vigenere_encrypt(block, key)
        ciphertext.append(encrypted_block)
        key = vigenere_encrypt(encrypted_block, key)

    return ''.join(ciphertext)


def vigenere_improved_decrypt(text, key):
    """
    Parameters
    ----------
    text: the plaintext to decrypt
    key: the keyword used in Vigenere (e.g. "pass")
    
    Returns
    -------
    the plaintext of <text> decrypted with improved Vigenere under key <key>
    """
    key_length = len(key)

    if key_length == 0:
        print("The key is empty")
        return ''

    plain_text = []

    for i in range(0, len(text), key_length):
        block = text[i:i + key_length]
        decrypted_block = vigenere_decrypt(block, key)
        key = vigenere_encrypt(block, key)
        plain_text.append(decrypted_block)

    return ''.join(plain_text)


def vigenere_improved_break(text, ref_freq, ref_ci):
    """
    Parameters
    ----------
    text: the ciphertext to break
    ref_freq: the output of the freq_analysis function on a reference text
    ref_ci: the output of the coincidence_index function on a reference text

    Returns
    -------
        the keyword corresponding to the key used to obtain the ciphertext
    """
    text_length = len(text)

    if text_length == 0:
        print("The text is empty")
        return ''

    max_key_length = text_length + 1 if text_length < 21 else 21
    # Vector containing the ciphertexts for each key length
    cipher_vector = [''] * max_key_length

    for key_length in range(1, max_key_length):
        block_count = 1
        cipher_blocks = [text[:key_length]]

        for i in range(key_length, text_length, key_length):
            current_block = text[i:i + key_length]
            new_block = cipher_blocks[0]

            # Encrypt the first block with each block preceding the current block
            for j in range(key_length, key_length * block_count, key_length):
                new_block = vigenere_encrypt(new_block, text[j:j + key_length])

            # Decrypt the current block using the new block
            cipher_blocks.append(vigenere_decrypt(current_block, new_block))

            block_count += 1

        cipher_vector[key_length] = ''.join(cipher_blocks)

    ci_vector = [0] * max_key_length

    # Calculate the coincidence index mean for each cipher text
    for cipher_index in range(1, max_key_length):
        ci = 0

        # We have to try all the key lengths for each cipher text
        for key_length in range(1, max_key_length):
            sub_text = []

            for i in range(text_length):
                if i % key_length == 0:
                    sub_text.append(cipher_vector[cipher_index][i])

            ci += coincidence_index(''.join(sub_text))

        ci_vector[cipher_index] = ci / (max_key_length - 1)

    key_length = min(range(max_key_length), key=lambda index: abs(ci_vector[index] - ref_ci))
    key = []

    for i in range(key_length):
        sub_text = []

        for j in range(i, text_length, key_length):
            sub_text.append(cipher_vector[key_length][j])

        key.append(chr((caesar_break(''.join(sub_text), ref_freq)) + 65))

    return ''.join(key)


def guess_text_language(text, ref_freq_fr, ref_ci_fr, ref_freq_en, ref_ci_en):
    """
    Parameters
    ----------
    text: the text to analyse
    ref_freq_fr: the output of the freq_analysis function on a reference French text
    ref_ci_fr: the output of the coincidence_index function on a reference French text
    ref_freq_en: the output of the freq_analysis function on a reference English text
    ref_ci_en: the output of the coincidence_index function on a reference English text

    Returns
    -------
    the language of the text
    """
    if len(text) == 0:
        print("The text is empty")
        return ''

    text_freq = freq_analysis(text)
    text_ci = coincidence_index(text)

    chi2_fr = sum((f - r) ** 2 / r if r != 0 else 1 for f, r in zip(text_freq, ref_freq_fr))
    chi2_en = sum((f - r) ** 2 / r if r != 0 else 1 for f, r in zip(text_freq, ref_freq_en))

    if abs(text_ci - ref_ci_fr) < abs(text_ci - ref_ci_en) and chi2_fr < chi2_en:
        return "French"
    else:
        return "English"


def main():
    print("Welcome to the Vigenere breaking tool")
    ref_text = open("ref_text.txt", "r", encoding="utf-8").read()
    ref_text = sanitize_text(ref_text)
    ref_freq = freq_analysis(ref_text)
    ref_ci = coincidence_index(ref_text)

    vigenere_file = open("vigenere.txt", "r", encoding="utf-8").read()
    vigenere_file = sanitize_text(vigenere_file)
    vigenere_key = vigenere_break(vigenere_file, ref_freq, ref_ci)

    print("Vigenere key:", vigenere_key)
    print("Decrypted Vigenere:", vigenere_decrypt(vigenere_file, vigenere_key))

    vigenere_improved_file = open("vigenere_improved.txt", "r").read()
    vigenere_improved_file = sanitize_text(vigenere_improved_file)
    vigenere_improved_key = vigenere_improved_break(vigenere_improved_file, ref_freq, ref_ci)

    print("Improved Vigenere key:", vigenere_improved_key)
    print("Decrypted Improved Vigenere:", vigenere_improved_decrypt(vigenere_improved_file, vigenere_improved_key))

    ref_text_en = open("ref_text_en.txt", "r", encoding="utf-8").read()
    ref_text_en = sanitize_text(ref_text_en)
    ref_freq_en = freq_analysis(ref_text_en)
    ref_ci_en = coincidence_index(ref_text_en)

    text_en = """
        From the physiologist's or psychologist's point of view we may seem to
        be making an unwarrantable abstraction in desiring to handle the subject
        of speech without constant and explicit reference to that basis.
        However, such an abstraction is justifiable. We can profitably discuss
        the intention, the form, and the history of speech, precisely as we
        discuss the nature of any other phase of human culture--say art or
        religion--as an institutional or cultural entity, leaving the organic
        and psychological mechanisms back of it as something to be taken for
        granted. Accordingly, it must be clearly understood that this
        introduction to the study of speech is not concerned with those aspects
        of physiology and of physiological psychology that underlie speech. Our
        study of language is not to be one of the genesis and operation of a
        concrete mechanism; it is, rather, to be an inquiry into the function
        and form of the arbitrary systems of symbolism that we term languages.
    """
    text_en = sanitize_text(text_en)
    print("English text:", guess_text_language(text_en, ref_freq, ref_ci, ref_freq_en, ref_ci_en))

    text_fr = """
        Je le pris par la main, cet excellent jeune homme. Je le fis asseoir sur
        le meilleur banc du jardin, car nous en avons deux. Il m’apprit qu’il
        était botaniste et qu’il avait une mission du Jardin des Plantes de
        Hambourg. Tout en complétant son herbier, il avait observé de son mieux
        le pays, les bêtes et les gens. Ses descriptions naïves, ses vues,
        courtes mais justes, me rappelaient un peu la manière du bonhomme
        Hérodote. Il s’exprimait lourdement, mais avec une candeur qui imposait
        la confiance; il appuyait sur ses paroles du ton d’un homme profondément
        convaincu. Il put me donner des nouvelles, sinon de toute la ville
        d’Athènes, au moins des principaux personnages que j’ai nommés dans mon
        livre. Dans le cours de la conversation, il énonça quelques idées
        générales qui me parurent d’autant plus judicieuses que je les avais
        développées avant lui. Au bout d’une heure d’entretien, nous étions
        intimes.
    """
    text_fr = sanitize_text(text_fr)
    print("French text:", guess_text_language(text_fr, ref_freq, ref_ci, ref_freq_en, ref_ci_en))


if __name__ == "__main__":
    main()
