import random
import sys

def generate_random_dna(length):
    return ''.join(random.choices('ACGT', k=length))

def insert_pattern_allow_overlap(text, pattern, count):
    text = list(text)
    length = len(text)
    pattern_len = len(pattern)

    inserted_positions = []

    for _ in range(count):
        pos = random.randint(0, length - pattern_len)
        for i in range(pattern_len):
            text[pos + i] = pattern[i]
        inserted_positions.append(pos)

    return ''.join(text), inserted_positions

def find_exact_matches(text, pattern):
    pattern_len = len(pattern)
    positions = []
    for i in range(len(text) - pattern_len + 1):
        if text[i:i+pattern_len] == pattern:
            positions.append(i)
    return positions

def main(e, f):
    total_length = 10**e
    pattern = ''.join(random.choices('ACGT', k=f*5))
    insert_count = 100

    random_text = generate_random_dna(total_length)
    new_text, inserted_positions = insert_pattern_allow_overlap(random_text, pattern, insert_count)

    exact_positions = find_exact_matches(new_text, pattern)

    with open("dna_text.txt", "w") as f:
        f.write(new_text)

    with open("dna_positions.txt", "w") as f:
        f.write("Search Pattern: " + pattern + "\n")
        for pos in exact_positions:
            f.write(str(pos) + "\n")

if __name__ == "__main__":
    e = int(sys.argv[1])
    f = int(sys.argv[2])
    main(e, f)
