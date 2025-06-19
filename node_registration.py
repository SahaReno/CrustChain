class NodeRegistry:
    def __init__(self, min_stake=100):
        self.nodes = {}
        self.min_stake = min_stake
    
    def register_node(self, node_id, storage_tb, stake):
        """Register node with storage and stake (Eq. 1)"""
        if stake < max(self.min_stake, 0.1 * storage_tb):
            return False
        
        self.nodes[node_id] = {
            'storage': storage_tb,
            'stake': stake,
            'reputation': 50,
            'status': 'active'
        }
        return True
    
    def slash_node(self, node_id, amount):
        """Slash stake for misbehavior"""
        if node_id in self.nodes:
            self.nodes[node_id]['stake'] -= amount
            self.nodes[node_id]['reputation'] -= 15
            if self.nodes[node_id]['stake'] < self.min_stake:
                self.nodes[node_id]['status'] = 'inactive'
    
    def get_storage_weights(self):
        """Calculate storage weights for consensus"""
        total = sum(node['storage'] * node['reputation'] for node in self.nodes.values())
        return {nid: (node['storage'] * node['reputation']) / total 
                for nid, node in self.nodes.items()}
