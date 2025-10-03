import sys
import re
import argparse
from typing import Dict, List

# Define the file name as specified in the request
WORD_LIST = "words_alpha.txt"
num_to_word: Dict[int, str] = {}
word_to_num: Dict[str, int] = {}
MODULO: int = -1


def create_word_maps(filepath: str) -> None:
    global num_to_word
    global word_to_num
    global MODULO
    words = []
    try:
        with open(filepath, "r") as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return {}, {}
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return {}, {}

    count = 0
    for word in words:
        cleaned_word = word.strip().lower()

        if cleaned_word:
            num_to_word[count] = cleaned_word
            word_to_num[cleaned_word] = count
            count += 1

    MODULO = count


def get_text_from_file(filepath: str) -> List[str]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

    text = text.lower()
    words = re.sub(r"[^\w\s]", " ", text).split()
    return words


def write_words_to_file(filepath: str, words: List[str]) -> None:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(" ".join(words))
    except Exception as e:
        print(f"An error occurred while writing to the file '{filepath}': {e}")


def get_nums_from_words(words: List[str]) -> List[int]:
    global word_to_num
    nums: List[int] = []
    for i in range(len(words)):
        num = word_to_num.get(words[i])
        if num is None:
            print(f"The word {words[i]} was not found in the dictionary")
            for char in words[i]:
                nums.append(word_to_num[char])
        else:
            nums.append(num)
    return nums


def get_words_from_nums(nums: List[int]) -> List[str]:
    global num_to_word
    words: List[str] = []
    for i in range(len(nums)):
        word = num_to_word.get(nums[i])
        if word is None:
            print(f"The number {nums[i]} was not found in the dictionary")
        else:
            words.append(word)
    return words


def encrypt_plaintext_nums(plain_nums: List[int], key: int) -> List[int]:
    global MODULO
    cipher_nums = []
    cipher_nums.append((plain_nums[0] + pow(key, key, MODULO)) % MODULO)
    for i in range(1, len(plain_nums)):
        cipher_nums.append(
            (plain_nums[i] + pow(key, plain_nums[i - 1], MODULO)) % MODULO
        )
    return cipher_nums


def decrypt_ciphertext_nums(cipher_nums: List[int], key: int) -> List[int]:
    global MODULO
    plain_nums = []
    plain_nums.append((cipher_nums[0] - pow(key, key, MODULO) + MODULO) % MODULO)
    for i in range(1, len(cipher_nums)):
        plain_nums.append(
            (cipher_nums[i] - pow(key, plain_nums[i - 1], MODULO) + MODULO) % MODULO
        )
    return plain_nums


def main(args: List[str] = sys.argv[1:]) -> None:
    """
    Parses command-line arguments and executes the selected action (-d or -e).
    """
    parser = argparse.ArgumentParser(
        description="A command-line tool for word encoding and decoding.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # 1. Positional Arguments (Required File Paths)
    parser.add_argument(
        "input_filepath",
        type=str,
        help="The path to the input file (e.g., file_in.txt).",
    )

    parser.add_argument(
        "output_filepath",
        type=str,
        help="The path where the resulting data should be saved (e.g., file_out.txt).",
    )

    parser.add_argument(
        "key",
        type=int,
        help="An integer key required for the encoding/decoding process (e.g., 5 or 10).",
    )

    # 2. Mutually Exclusive Group (Switches)
    # The user must specify EITHER -d or -e, but not both.
    mode_group = parser.add_mutually_exclusive_group(required=True)

    mode_group.add_argument(
        "-e", "--encode", action="store_true", help="Selects the ENCODE function."
    )

    mode_group.add_argument(
        "-d", "--decode", action="store_true", help="Selects the DECODE function."
    )

    # Parse the arguments provided by the user
    args = parser.parse_args(args)

    # 3. Execution Logic
    create_word_maps(WORD_LIST)
    global MODULO
    key = args.key % MODULO

    if args.encode:
        plaintext = get_text_from_file(args.input_filepath)
        plain_nums = get_nums_from_words(plaintext)
        cipher_nums = encrypt_plaintext_nums(plain_nums, key)
        ciphertext = get_words_from_nums(cipher_nums)
        write_words_to_file(args.output_filepath, ciphertext)
    elif args.decode:
        ciphertext = get_text_from_file(args.input_filepath)
        cipher_nums = get_nums_from_words(ciphertext)
        plain_nums = decrypt_ciphertext_nums(cipher_nums, key)
        plaintext = get_words_from_nums(plain_nums)
        write_words_to_file(args.output_filepath, plaintext)
    else:
        print("Error: You must specify either -d or -e.")
        parser.print_help()


if __name__ == "__main__":
    main()
