import time

class Neuron:
    """
    This class represents a single neuron modeled with 8-bit precision.
    It simulates basic neural properties such as activation, spiking,
    synaptic weights, plasticity, mutability, and stores local data for
    internal processing.

    All numeric values are capped between 0 and 255 to respect 8-bit limits.
    """

    def __init__(self, num_neighbors):
        """
        Initialize the neuron with default parameters.

        Args:
            num_neighbors (int): The number of neighboring neurons this neuron connects to.

        Attributes:
            activation (int): Current activation level of the neuron (0-255).
            timer (int): Counts time since last spike; resets to 255 when neuron spikes.
            weights (list[int]): Strengths of connections to neighbors, initialized mid-range (128).
            local_data (list[int]): A list of 8 bytes for internal neuron state and processing.
            threshold (int): Activation threshold above which the neuron 'fires' (spikes).
            persistent_storage (list[int]): 8 bytes for long-term local storage.
        """
        self.activation = 0  # Activation level
        self.timer = 0  # How often it spikes
        self.weights = [128] * num_neighbors  # Synapse strength to neighbors
        self.local_data = [0] * 8  # Internal state, 8 bytes for flexibility
        self.threshold = 128  # Activation threshold for spiking
        self.persistent_storage = [0] * 8  # Persistent storage for internal use

    def spike(self):
        """
        Determine if the neuron fires a spike.

        Returns:
            int: 1 if activation exceeds threshold (neuron spikes), else 0.
        """
        return 1 if self.activation > self.threshold else 0

    def update(self, neighbors):
        """
        Update the neuron's state based on inputs from neighbors and internal logic.

        This method performs:
        - Spike timing update (timer reset/decrement).
        - Hebbian-like weight adjustment influenced by plasticity.
        - Activation update with decay and weighted input from neighbors.
        - Threshold mutation based on local data.
        - Local data mutation to simulate internal state changes.

        Args:
            neighbors (list[Neuron]): List of neighboring neurons.
        """

        # Determine if this neuron currently spikes
        spk = self.spike()

        # Update timer: resets to max (255) if spiked, otherwise counts down to zero
        self.timer = 255 if spk else max(0, self.timer - 1)

        # Determine plasticity factor from local_data (element 0), use 1 if zero to avoid no updates
        plasticity_factor = self.local_data[0] or 1

        # Update weights to each neighbor based on Hebbian principle:
        # Increase weight if both this neuron and neighbor spike,
        # otherwise decrease weight, all capped between 0 and 255
        for i, neighbor in enumerate(neighbors):
            n_spk = neighbor.spike()
            if spk and n_spk:
                self.weights[i] = min(255, self.weights[i] + plasticity_factor)
            else:
                self.weights[i] = max(0, self.weights[i] - plasticity_factor)

        # Decay rate for activation update from local_data (element 1), default 1
        decay = self.local_data[1] or 1

        # Calculate total weighted input from neighbors that spike
        total_input = sum(w * neighbor.spike() for w, neighbor in zip(self.weights, neighbors))

        # Update activation with decay and input, keeping result within 0-255 bounds
        self.activation = min(255, max(0, (self.activation // decay) + total_input))

        # Mutate the activation threshold based on local_data (element 2),
        # ensures threshold stays within 0-255
        self.threshold = max(0, min(255, self.threshold + self.local_data[2]))

        # Mutate internal local data state with a custom rule
        self.local_data = self.mutate_local_data()

        # Example usage of persistent storage:
        # Let's say byte 0 stores a long-term firing count:
        if spk:
            self.persistent_storage[0] = (self.persistent_storage[0] + 1) % 256

    def mutate_local_data(self):
        """
        Example mutation for the neuron's internal state.

        This method cycles each byte in local_data by incrementing and wrapping at 255.

        Returns:
            list[int]: Updated local data list.
        """
        return [(x + 1) % 256 for x in self.local_data]


# Self-test block
if __name__ == "__main__":
    import time

    num_neighbors = 10000
    neuron = Neuron(num_neighbors)
    neighbors = [Neuron(num_neighbors) for _ in range(num_neighbors)]
    print("Initialized neuron with", num_neighbors, "neighbors.")
    time.sleep(1)
    print("Running update speed test on neuron...")

    start = time.time()
    neuron.update(neighbors)
    end = time.time()

    elapsed_us = (end - start) * 1000000
    print(f"Single neuron update with {num_neighbors} neighbors took {elapsed_us:.2f} microseconds.")
