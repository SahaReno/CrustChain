from py_ecc.bls import G2ProofOfPossession as bls_pop
import random

class BLSThreshold:
    def __init__(self, nodes, threshold=7):
        self.nodes = nodes
        self.threshold = threshold
        self.private_keys = {}
        self.public_keys = {}
        self._generate_keys()
        
    def _generate_keys(self):
        """Generate keys for all nodes"""
        for node in self.nodes:
            private = bls_pop.KeyGen(node['seed'])
            public = bls_pop.SkToPk(private)
            self.private_keys[node['id']] = private
            self.public_keys[node['id']] = public
    
    def sign(self, message, node_id):
        """Generate partial signature"""
        return bls_pop.Sign(self.private_keys[node_id], message)
    
    def aggregate(self, signatures):
        """Aggregate partial signatures (Eq. 13)"""
        return bls_pop.Aggregate(signatures)
    
    def verify(self, signature, message):
        """Verify threshold signature"""
        public_keys = random.sample(list(self.public_keys.values()), self.threshold)
        return bls_pop.FastAggregateVerify(public_keys, message, signature)

# Example usage
if __name__ == "__main__":
    nodes = [{'id': i, 'seed': f"node-seed-{i}"} for i in range(10)]
    threshold_sig = BLSThreshold(nodes)
    
    msg = b"Important consensus message"
    sigs = [threshold_sig.sign(msg, i) for i in range(7)]
    agg_sig = threshold_sig.aggregate(sigs)
    
    print(f"Signature valid: {threshold_sig.verify(agg_sig, msg)}")
