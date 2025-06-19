import time
from hashlib import sha256

class TimeLockRetriever:
    def __init__(self, num_shards=5, threshold=3):
        self.num_shards = num_shards
        self.threshold = threshold
    
    def create_puzzle(self, cid, difficulty=25):
        """Create time-lock puzzle (Algorithm B2)"""
        nonce = 0
        target = 2**(256 - difficulty)
        start_time = time.time()
        
        while True:
            nonce += 1
            attempt = sha256(f"{cid}{nonce}".encode()).digest()
            if int.from_bytes(attempt, 'big') < target:
                duration = time.time() - start_time
                return nonce, duration
    
    def reconstruct(self, shards):
        """Reconstruct from threshold shards"""
        return b"".join(shards[:self.threshold])
    
    def retrieve_data(self, cid, storage_nodes):
        """Full retrieval workflow"""
        # Create puzzle
        nonce, _ = self.create_puzzle(cid)
        
        # Distribute to shards
        shards = [node.retrieve_shard(cid) for node in storage_nodes]
        
        # Wait for threshold responses
        valid_shards = [s for s in shards if s is not None][:self.threshold]
        
        if len(valid_shards) >= self.threshold:
            return self.reconstruct(valid_shards)
        return None
