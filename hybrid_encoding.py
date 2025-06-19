import numpy as np
from numpy.linalg import inv

class HybridEncoder:
    def __init__(self, k=3, m=2):
        self.k = k  # Data shards
        self.m = m  # Parity shards
        self.total_shards = k + m
    
    def encode(self, data):
        """Hybrid encoding (Eq. 12)"""
        data_shards = np.array_split(data, self.k)
        coding_matrix = np.random.rand(self.total_shards, self.k)
        encoded = [np.dot(coding_matrix[i], data_shards) for i in range(self.total_shards)]
        return encoded, coding_matrix
    
    def decode(self, shards, coding_matrix):
        """Network decoding (Eq. 11)"""
        shard_subset = shards[:self.k]
        matrix_subset = coding_matrix[:self.k, :self.k]
        return np.dot(inv(matrix_subset), shard_subset)

# Example usage
if __name__ == "__main__":
    encoder = HybridEncoder()
    data = np.random.rand(512 * 1024)  # 512KB data
    encoded, matrix = encoder.encode(data)
    print(f"Generated {len(encoded)} shards with {encoder.m} redundancy")
