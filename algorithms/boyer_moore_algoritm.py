import time
import math

from resource_monitor import ResourceMonitor
from text_loader import load_text, load_pattern_and_positions, compare_matches

def boyer_moore_search(text, pattern, alphabet="ACGT"):
    """
    Search for occurrences of a pattern in a text using the Boyer-Moore algorithm.

    Args:
        text (str): The text in which to search.
        pattern (str): The pattern to search for.

    Returns:
        list: A list of starting indices where the pattern occurs.
    """
    
    text_len = len(text)
    pattern_len = len(pattern)
    
    if pattern_len == 0:
        raise ValueError("Pattern length must be greater than 0.")

    bad_char_table = {char: pattern_len for char in alphabet}
    
    for i in range(pattern_len - 1):
        char = pattern[i]
        distance_from_end = pattern_len - 1 - i
        bad_char_table[char] = distance_from_end

    found_indices = []
    text_index = 0

    while text_index <= text_len - pattern_len:
        pattern_index = pattern_len - 1

        while pattern_index >= 0 and pattern[pattern_index] == text[text_index + pattern_index]:
            pattern_index -= 1

        if pattern_index < 0:
            found_indices.append(text_index)
            text_index += 1
        else:
            bad_char = text[text_index + pattern_index]
            
            shift = bad_char_table.get(bad_char, pattern_len)
            
            text_index += shift
            
    return found_indices

def main():
    dna_text_file = "dna_text.txt"
    dna_positions_file = "dna_positions.txt"

    dna_sequence = load_text(dna_text_file)
    pattern, correct_positions = load_pattern_and_positions(dna_positions_file)

    print(f"Text length: {len(dna_sequence):,}")
    print(f"Pattern length: {len(pattern):,}")
    print("\nRunning boyer-moore matching with resource monitoring...")

    monitor = ResourceMonitor(interval=0.1)
    monitor.start()

    start_time = time.time()
    found_positions = boyer_moore_search(dna_sequence, pattern)
    end_time = time.time()

    monitor.stop()
    n = int(math.log10(len(dna_sequence)))
    m = len(pattern)
    monitor.save_log(f'Boyer_Moore_{n}_{m}_resource_log.csv')

    print(f"\nFinished in {end_time - start_time:.4f} seconds.")
    print(f"Found {len(found_positions):,} matches.")
    compare_matches(correct_positions, found_positions)

if __name__ == "__main__":
    main()