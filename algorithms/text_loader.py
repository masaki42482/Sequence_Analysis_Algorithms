def load_pattern_and_positions(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()
    pattern_line = lines[0]
    if not pattern_line.startswith("Search Pattern: "):
        raise ValueError("First line must start with 'Search Pattern: '")
    pattern = pattern_line[len("Search Pattern: "):]
    positions = [int(line) for line in lines[1:] if line.strip().isdigit()]
    return pattern, positions

def load_text(filename):
    with open(filename, "r") as f:
        return f.read()

def compare_matches(correct_positions, found_positions):
    correct_set = set(correct_positions)
    found_set = set(found_positions)

    correct_only = correct_set - found_set
    found_only = found_set - correct_set
    matched = correct_set & found_set

    print(f"Number of correct matches: {len(correct_positions)}")
    print(f"Number of found matches: {len(found_positions)}")
    print(f"Number of matches correctly found: {len(matched)}")
    if correct_only:
        print(f"Matches missed (correct but not found): {len(sorted(correct_only))}")
    if found_only:
        print(f"False positives (found but not correct): {len(sorted(found_only))}")