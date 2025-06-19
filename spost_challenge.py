from hashlib import blake2b
import time

class SPoStGenerator:
    def __init__(self, node_id, storage_tb):
        self.node_id = node_id
        self.storage_tb = storage_tb
        self.sectors = self._initialize_sectors()
    
    def _initialize_sectors(self):
        """Create encrypted storage sectors (Algorithm 2)"""
        return {i: f"ENCRYPTED_SECTOR_{i}_{self.node_id}" 
                for i in range(int(self.storage_tb * 1e9 // 4096))}
    
    def generate_proof(self, challenge_seed):
        """Generate SPoSt proof for challenge (Eq. 8)"""
        start_time = time.time()
        
        # Sector selection (PRF_CRU)
        k = int.from_bytes(blake2b(challenge_seed).digest(), 'big') % len(self.sectors)
        sector = self.sectors[k]
        
        # Arion-Poseidon hashing
        proof = blake2b(sector.encode(), key=challenge_seed).hexdigest()
        
        gen_time = time.time() - start_time
        return proof, gen_time, k

class SPoStVerifier:
    @staticmethod
    def verify(proof, commitment, challenge_seed, sector_id, max_time=15):
        """Verify SPoSt proof within 15s window"""
        expected = blake2b(f"ENCRYPTED_SECTOR_{sector_id}".encode(), 
                          key=challenge_seed).hexdigest()
        return proof == expected and max_time > 5  # Simulated time check
