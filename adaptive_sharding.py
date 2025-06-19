import numpy as np
from collections import defaultdict

class MDPSharding:
    def __init__(self, num_shards=64, alpha=0.7, beta=0.2, gamma=0.1):
        self.num_shards = num_shards
        self.weights = {'throughput': alpha, 'latency': beta, 'migration': gamma}
        self.q_table = defaultdict(lambda: np.zeros(num_shards))
        
    def get_state(self, nodes):
        """Normalize node features: [locality, storage, reputation, netspeed]"""
        return tuple(np.mean([node[f] for node in nodes], axis=0) * 100)
    
    def choose_action(self, state, epsilon=0.1):
        """ε-greedy shard assignment"""
        if np.random.random() < epsilon:
            return np.random.randint(self.num_shards)
        return np.argmax(self.q_table[state])
    
    def update_q_value(self, state, action, reward, next_state, gamma=0.9, lr=0.1):
        """Q-learning update rule"""
        future = np.max(self.q_table[next_state])
        self.q_table[state][action] += lr * (reward + gamma * future - self.q_table[state][action])
    
    def calculate_reward(self, shard):
        """Compute sharding reward (Eq. 4)"""
        throughput = len(shard['pending_txs']) / max(1, shard['processing_time'])
        latency = 1 / (shard['avg_latency'] + 1e-5)
        migration = 1 / (shard['migration_cost'] + 1)
        return (self.weights['throughput'] * throughput + 
                self.weights['latency'] * latency + 
                self.weights['migration'] * migration)

# Example usage
if __name__ == "__main__":
    sharder = MDPSharding()
    nodes = [{'locality': 0.8, 'storage': 0.9, 'reputation': 0.7, 'netspeed': 0.6}]
    state = sharder.get_state(nodes)
    action = sharder.choose_action(state)
    print(f"Assigned to shard: {action}")
