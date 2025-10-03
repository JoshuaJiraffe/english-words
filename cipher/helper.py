import sys
import argparse
from typing import Dict, List

# --- GLOBAL VARIABLES (Matching the structure of the main cipher) ---
# Define the file name for the dictionary
WORD_LIST = "words_alpha.txt"
num_to_word: Dict[int, str] = {}
word_to_num: Dict[str, int] = {}
MODULO: int = -1

# --- DICTIONARY CREATION FUNCTION (Copied for independent operation) ---


def create_word_maps(filepath: str) -> bool:
    """
    Loads the word list from a file, populates the global word-to-number
    and number-to-word dictionaries, and sets the global MODULO value.

    Args:
        filepath: The path to the word list file (e.g., words_alpha.txt).

    Returns:
        True if maps were created successfully, False otherwise.
    """
    global num_to_word
    global word_to_num
    global MODULO

    words = []
    try:
        with open(filepath, "r") as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        print(
            f"Error: The file '{filepath}' was not found. Please ensure it is in the same directory."
        )
        return False
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return False

    count = 0
    for word in words:
        # Normalize the word to match the cipher's behavior
        cleaned_word = word.strip().lower()

        if cleaned_word:
            num_to_word[count] = cleaned_word
            word_to_num[cleaned_word] = count
            count += 1

    MODULO = count

    if MODULO == 0:
        print("Error: Word list loaded but contains no valid entries.")
        return False

    return True


# --- MAIN LOOKUP LOGIC ---


def lookup_main() -> None:
    """
    Initializes the dictionary and runs the word/int lookup in an interactive loop.
    The lookup mode (word or integer) is automatically detected based on the input type.
    """
    # 1. Load the word maps (Run once)
    if not create_word_maps(WORD_LIST):
        sys.exit(1)

    print(f"Dictionary loaded successfully. MODULO (Total words): {MODULO}")

    print("\n--- Interactive Lookup Mode ---")
    print("Enter a word (e.g., apple) for Word-to-Int lookup.")
    print("Enter a number (e.g., 55000) for Int-to-Word lookup.")
    print("Press Ctrl+C or Ctrl+D to exit.")

    # 2. Interactive Loop
    while True:
        try:
            # Get user input
            raw_input = input(f"\n[{MODULO} words] > ").strip()

            if not raw_input:
                continue

            # Attempt to convert input to integer first
            try:
                input_num = int(raw_input)

                # --- Int-to-Word logic ---
                if 0 <= input_num < MODULO:
                    result_word = num_to_word.get(input_num)
                    print(f"-> Index {input_num} corresponds to word: '{result_word}'")
                elif input_num >= MODULO:
                    print(
                        f"-> Error: Index {input_num} is too large. Max index is {MODULO - 1}."
                    )
                else:
                    print(
                        f"-> Error: Index {input_num} is invalid (must be non-negative)."
                    )

            except ValueError:
                # --- Word-to-Int logic (If input is not an integer) ---
                input_word = raw_input.strip().lower()
                result_num = word_to_num.get(input_word)

                if result_num is not None:
                    print(f"-> Word '{input_word}' corresponds to index: {result_num}")
                else:
                    print(f"-> Error: Word '{input_word}' not found in the dictionary.")

        except EOFError:  # Handles Ctrl+D/Ctrl+Z
            print("\nExiting lookup tool.")
            break
        except KeyboardInterrupt:  # Handles Ctrl+C
            print("\nExiting lookup tool.")
            break


if __name__ == "__main__":
    lookup_main()

# --- Example Usage (Run from your terminal) ---
#
# Run the tool in interactive mode:
#    python lookup_tool.py
#
# Inside the tool, enter:
#    apple
#    55000
#    (Press Ctrl+C to stop)
