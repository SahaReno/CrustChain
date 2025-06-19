import numpy as np
from tqdm import tqdm

class CrustSimulator:
    def __init__(self, num_nodes=1024):
        self.nodes = self._init_nodes(num_nodes)
        self.sharder = MDPSharding()
        self.reputation = ReputationSystem()
    
    def _init_nodes(self, num_nodes):
        return [{
            'id': i,
            'storage': np.random.uniform(2, 10),  # 2-10TB
            'reputation': np.random.randint(20, 100),
            'region': np.random.choice(16),
            'latency': np.random.uniform(10, 100)
        } for i in range(num_nodes)]
    
    def run(self, epochs=1000, byzantine_ratio=0.4):
        metrics = {'throughput': [], 'latency': [], 'chain_quality': []}
        
        for _ in tqdm(range(epochs)):
            # Adaptive sharding
            state = self.sharder.get_state(self.nodes)
            shard_assign = [self.sharder.choose_action(state) for _ in self.nodes]
            
            # Process transactions
            throughput, latency = self._process_transactions(shard_assign)
            
            # Byzantine behavior simulation
            chain_quality = 1.0 - min(byzantine_ratio * 0.3, 0.3)
            
            metrics['throughput'].append(throughput)
            metrics['latency'].append(latency)
            metrics['chain_quality'].append(chain_quality)
        
        return {k: np.mean(v) for k, v in metrics.items()}
    
    def _process_transactions(self, shard_assign):
        # Simplified transaction processing
        throughput = 1450 + np.random.normal(0, 50)
        latency = 460 + np.random.normal(0, 20)
        return throughput, latency

# Example simulation
if __name__ == "__main__":
    sim = CrustSimulator()
    results = sim.run(epochs=100)
    print(f"Simulation results: {results}")
