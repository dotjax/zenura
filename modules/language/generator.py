import random
import os
import importlib.util
from pathlib import Path

class NeuralNetwork:
    """
    Neural network that loads and queries all learned pattern files.
    """
    def __init__(self, learned_dir="data/neural/language/learned"):
        self.learned_dir = learned_dir
        self.patterns = {}
        self.meta_patterns = {}
        self.associations = {}
        self.reflections = {}
        self.load_all_learned_files()
    
    def load_all_learned_files(self):
        """Load all learned pattern files into the neural network."""
        if not os.path.exists(self.learned_dir):
            print(f"Warning: Learned directory {self.learned_dir} not found")
            return
        
        for filename in os.listdir(self.learned_dir):
            if filename.startswith("learned_") and filename.endswith(".py"):
                filepath = os.path.join(self.learned_dir, filename)
                self.load_learned_file(filepath)
        
        print(f"Neural network loaded: {len(self.patterns)} total patterns from {len([f for f in os.listdir(self.learned_dir) if f.startswith('learned_')])} learned files")
    
    def load_learned_file(self, filepath):
        """Load a single learned file into the network."""
        try:
            spec = importlib.util.spec_from_file_location("learned", filepath)
            learned = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(learned)
            
            # Check if this is a unifier file (has nested structure)
            if hasattr(learned.memory, 'get') and isinstance(learned.memory, dict):
                # Check if it has the unifier structure
                if 'coalesced_patterns' in learned.memory:
                    # This is a unifier file - extract all components
                    self.load_unifier_memory(learned.memory)
                else:
                    # Regular pattern file
                    self.merge_patterns(learned.memory)
            else:
                # Regular pattern file
                self.merge_patterns(learned.memory)
                    
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")
    
    def load_unifier_memory(self, memory):
        """Load memory from a unifier file with rich structure."""
        # Extract coalesced patterns (main patterns for generation)
        if 'coalesced_patterns' in memory:
            self.merge_patterns(memory['coalesced_patterns'])
        
        # Extract meta patterns for enhanced thinking
        if 'meta_patterns' in memory:
            for key, meta_data in memory['meta_patterns'].items():
                if key not in self.meta_patterns:
                    self.meta_patterns[key] = []
                self.meta_patterns[key].append(meta_data)
        
        # Extract associations
        if 'associations' in memory:
            for key, assoc_data in memory['associations'].items():
                if key not in self.associations:
                    self.associations[key] = []
                self.associations[key].append(assoc_data)
        
        # Extract reflections
        if 'reflections' in memory:
            for key, reflection_data in memory['reflections'].items():
                if key not in self.reflections:
                    self.reflections[key] = []
                self.reflections[key].append(reflection_data)
    
    def merge_patterns(self, memory):
        """Merge patterns from a regular memory file."""
        for pattern, outcomes in memory.items():
            if pattern not in self.patterns:
                self.patterns[pattern] = {}
            
            for outcome, count in outcomes.items():
                self.patterns[pattern][outcome] = self.patterns[pattern].get(outcome, 0) + count
    
    def query_network(self, pattern):
        """
        Query the neural network for a specific pattern.
        Returns weighted responses from across all learned patterns.
        """
        return self.patterns.get(pattern, {})
    
    def find_similar_patterns(self, target_pattern, tolerance=2):
        """
        Find patterns similar to the target pattern within tolerance.
        This allows the network to generalize and think beyond exact matches.
        """
        similar_patterns = {}
        
        for pattern, outcomes in self.patterns.items():
            # Check if patterns are similar within tolerance
            if (abs(pattern[0] - target_pattern[0]) <= tolerance and
                abs(pattern[1] - target_pattern[1]) <= tolerance and
                abs(pattern[2] - target_pattern[2]) <= tolerance):
                
                # Weight by similarity (closer patterns get higher weight) - 8-bit only
                distance = sum(abs(p - t) for p, t in zip(pattern, target_pattern))
                similarity = max(1, 255 - distance)  # 8-bit similarity (1-255)
                for outcome, count in outcomes.items():
                    if outcome not in similar_patterns:
                        similar_patterns[outcome] = 0
                    similar_patterns[outcome] += int(count) * similarity
        
        return similar_patterns
    
    def get_all_patterns(self):
        """Get all patterns in the neural network."""
        return list(self.patterns.keys())
    
    def get_meta_insights(self, pattern):
        """
        Get meta-insights about a pattern from the unifier data.
        """
        insights = []
        
        # Check for relevant meta patterns
        for meta_key, meta_list in self.meta_patterns.items():
            for meta_data in meta_list:
                if meta_data.get('type') == 'transition_meta':
                    if meta_data.get('pattern') == (pattern[0], pattern[1]):
                        insights.append(f"Strong transition pattern: {meta_data.get('strength')}")
                elif meta_data.get('type') == 'delta_meta':
                    if meta_data.get('delta') == pattern[1]:
                        insights.append(f"Common delta pattern: {meta_data.get('strength')}")
        
        return insights

def sample_from_distribution(distribution, temperature=1):
    """
    Sample a key from a dict {value: count} probabilistically,
    applying temperature for randomness control.
    """
    if not distribution:
        return None

    # Convert counts to probabilities
    values, counts = zip(*distribution.items())
    
    # Ensure all counts are integers
    counts = [int(count) for count in counts]

    # Apply temperature (8-bit only)
    # For temperature=1: no change, for temperature>1: reduce differences
    if temperature > 1:
        # Scale down differences for higher temperature (more random)
        adjusted_counts = [max(1, count // temperature) for count in counts]
    else:
        adjusted_counts = [count for count in counts]  # Ensure integers
    
    total = sum(adjusted_counts)
    if total == 0:
        return random.choice(values) # Fallback if all adjusted counts are zero
    
    # Create cumulative distribution for sampling
    cumulative = 0
    cumulative_dist = []
    for count in adjusted_counts:
        cumulative += count
        cumulative_dist.append(cumulative)
    
    # Sample according to cumulative distribution
    rand_val = random.randint(1, total)
    for i, cumul in enumerate(cumulative_dist):
        if rand_val <= cumul:
            return values[i]
    
    return values[-1]  # Fallback

def generate_response(memory=None, start_byte=None, max_length=100, temperature=1, use_neural_network=True):
    """
    Generate a byte sequence using the neural network.
    """
    if use_neural_network:
        # Use the full neural network
        network = NeuralNetwork()
        if not network.patterns:
            print("Warning: Neural network is empty, falling back to memory")
            use_neural_network = False
    
    if not use_neural_network:
        # Fallback to original memory-based generation
        if not memory:
            return []
        all_keys = list(memory.keys())
    else:
        all_keys = network.get_all_patterns()
    
    if not all_keys:
        return []
    
    # Pick a starting context
    if start_byte is not None:
        # Find all keys that start with the desired byte
        possible_starts = [k for k in all_keys if k[0] == start_byte]
        if possible_starts:
            context = random.choice(possible_starts)
        else:
            context = random.choice(all_keys) # Fallback to random if no match
    else:
        context = random.choice(all_keys)

    # Initialize the generated sequence with the first byte of the context
    generated = [context[0]]

    for _ in range(max_length - 1):
        # Get next options from the neural network or memory
        if use_neural_network:
            # Query the neural network for this pattern
            next_options = network.query_network(context)
            
            # If no exact match, try similar patterns (network generalization)
            if not next_options:
                next_options = network.find_similar_patterns(context)
            
            # Get meta insights for enhanced thinking (optional)
            if network.meta_patterns:
                insights = network.get_meta_insights(context)
                if insights:
                    # Could use insights to influence generation
                    pass
        else:
            next_options = memory.get(context)
        
        if not next_options:
            break # Dead end

        # Sample the next byte
        next_byte = sample_from_distribution(next_options, temperature)
        if next_byte is None:
            break # Sampling failed
        
        generated.append(next_byte)

        # To continue, find all known contexts that START with our newly generated byte
        possible_next_contexts = [k for k in all_keys if k[0] == next_byte]
        
        if not possible_next_contexts:
            break # Dead end, nowhere to go from this byte

        # Pick one of the possible next contexts at random to continue the chain
        context = random.choice(possible_next_contexts)

    return generated