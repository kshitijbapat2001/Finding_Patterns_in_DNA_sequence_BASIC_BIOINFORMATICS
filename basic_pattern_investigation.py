def read_fasta(file_path):
    """
    Read a FASTA file and return sequences as a dictionary.
    
    Args:
        file_path (str): Path to the FASTA file
        
    Returns:
        dict: Dictionary with sequence IDs as keys and sequences as values
    """
    sequences = {}
    current_id = None
    current_seq = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if current_id:
                    sequences[current_id] = ''.join(current_seq)
                current_id = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
        
        if current_id:
            sequences[current_id] = ''.join(current_seq)
    
    return sequences

def find_motif(sequence, motif):
    """
    Find all occurrences of a motif in a sequence.
    
    Args:
        sequence (str): DNA sequence to search
        motif (str): Motif to find
        
    Returns:
        list: List of starting positions (0-based) where motif occurs
    """
    positions = []
    for i in range(len(sequence) - len(motif) + 1):
        if sequence[i:i+len(motif)] == motif:
            positions.append(i)
    return positions

def calculate_gc_content(sequence):
    """
    Calculate GC content percentage in a sequence.
    
    Args:
        sequence (str): DNA sequence
        
    Returns:
        float: GC content percentage
    """
    gc_count = sequence.count('G') + sequence.count('C')
    total_length = len(sequence)
    return (gc_count / total_length) * 100 if total_length > 0 else 0

def find_repeats(sequence, min_length=4, min_count=2):
    """
    Find repeated sequences in DNA.
    
    Args:
        sequence (str): DNA sequence
        min_length (int): Minimum length of repeat
        min_count (int): Minimum number of occurrences
        
    Returns:
        dict: Dictionary with repeats and their positions
    """
    repeats = {}
    for i in range(len(sequence) - min_length + 1):
        for j in range(min_length, min(21, len(sequence) - i + 1)):
            substring = sequence[i:i+j]
            positions = find_motif(sequence, substring)
            if len(positions) >= min_count:
                repeats[substring] = positions
    return repeats

def find_palindromes(sequence, min_length=4, max_length=12):
    """
    Find palindromic sequences in DNA.
    
    Args:
        sequence (str): DNA sequence
        min_length (int): Minimum length of palindrome
        max_length (int): Maximum length of palindrome
        
    Returns:
        list: List of tuples containing palindromes and their positions
    """
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    palindromes = []
    
    def is_palindrome(seq):
        rev_comp = ''.join(complement.get(base, base) for base in reversed(seq))
        return seq == rev_comp
    
    for i in range(len(sequence) - min_length + 1):
        for j in range(min_length, min(max_length + 1, len(sequence) - i + 1), 2):
            substr = sequence[i:i+j]
            if is_palindrome(substr):
                palindromes.append((substr, i))
    
    return palindromes

def analyze_sequence(sequence_id, sequence):
    """
    Perform comprehensive analysis of a DNA sequence.
    
    Args:
        sequence_id (str): Identifier for the sequence
        sequence (str): DNA sequence
        
    Returns:
        dict: Dictionary containing analysis results
    """
    results = {
        'sequence_id': sequence_id,
        'length': len(sequence),
        'gc_content': calculate_gc_content(sequence),
        'repeats': find_repeats(sequence),
        'palindromes': find_palindromes(sequence),
        'base_composition': {
            'A': sequence.count('A'),
            'T': sequence.count('T'),
            'G': sequence.count('G'),
            'C': sequence.count('C')
        }
    }
    return results

# Example usage
if __name__ == "__main__":
    # Example FASTA file analysis
    file_path = "example.fasta"
    sequences = read_fasta(file_path)
    
    for seq_id, sequence in sequences.items():
        analysis = analyze_sequence(seq_id, sequence)
        
        print(f"\nAnalysis for sequence: {seq_id}")
        print(f"Length: {analysis['length']} bp")
        print(f"GC Content: {analysis['gc_content']:.2f}%")
        
        print("\nBase Composition:")
        for base, count in analysis['base_composition'].items():
            print(f"{base}: {count}")
        
        print("\nRepeated Sequences:")
        for repeat, positions in analysis['repeats'].items():
            if len(repeat) >= 6:  # Show only longer repeats for brevity
                print(f"{repeat}: {len(positions)} occurrences at positions {positions}")
        
        print("\nPalindromic Sequences:")
        for palindrome, position in analysis['palindromes']:
            print(f"{palindrome} at position {position}")
