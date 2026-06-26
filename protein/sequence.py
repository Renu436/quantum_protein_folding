class ProteinSequence:
    def __init__(self, sequence: str):
        self.sequence = sequence.upper()

    def validate(self):
        return self.sequence and all(c in ['H', 'P'] for c in self.sequence)