try:
    from qiskit.quantum_info import SparsePauliOp
except Exception:
    SparsePauliOp = None


def build_pauli(h, couplings):
    """Construct a SparsePauliOp when available, otherwise return a simple dict fallback.

    `couplings` is expected to be a dict keyed by (i, j) tuples.
    """
    n = len(h)
    paulis = []
    coeffs = []

    for i in range(n):
        z = ['I'] * n
        z[i] = 'Z'
        paulis.append("".join(z))
        coeffs.append(float(h[i]))

    for (i, j), val in (couplings or {}).items():
        z = ['I'] * n
        z[i] = z[j] = 'Z'
        paulis.append("".join(z))
        coeffs.append(float(val))

    if SparsePauliOp is not None:
        return SparsePauliOp(paulis, coeffs)
    return {"paulis": paulis, "coeffs": coeffs}