class ReputationSystem:
    def __init__(self):
        self.reputation = {}
    
    def update(self, node_id, success):
        """Dynamic reputation update (Eq. 11)"""
        current = self.reputation.get(node_id, 50)
        if success:
            new_rep = min(100, current + 2.5)
        else:
            penalty = 5 + 0.3 * current
            new_rep = max(0, current - penalty)
        self.reputation[node_id] = new_rep
    
    def block_probability(self, nodes):
        """Block proposal probability (Eq. 2)"""
        total = sum(node['storage'] * self.reputation.get(node['id'], 50) 
                  for node in nodes)
        return {node['id']: (node['storage'] * self.reputation.get(node['id'], 50)) / total
                 for node in nodes}
