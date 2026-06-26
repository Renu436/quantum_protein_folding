import numpy as np
from quantum.qubo_3d_real import build_qubo
from quantum.hamiltonian import qubo_to_ising
from quantum.pauli_hamiltonian import build_pauli


def test_build_qubo_shape_and_diagonal():
    seq = "HHPH"
    Q = build_qubo(seq)
    assert isinstance(Q, np.ndarray)
    assert Q.shape == (len(seq), len(seq))
    # diagonal should have negative contributions
    assert all(Q[i, i] <= 0 for i in range(len(seq)))


def test_qubo_to_ising_consistency():
    Q = np.zeros((2, 2))
    Q[0, 0] = -5
    Q[1, 1] = -5
    Q[0, 1] = -1

    h, couplings, offset = qubo_to_ising(Q)
    assert len(h) == 2
    assert isinstance(couplings, dict)
    assert (0, 1) in couplings
    assert isinstance(offset, (int, float))


def test_build_pauli_returns_expected_structure():
    h = [0.5, -0.5]
    couplings = {(0, 1): -0.25}
    P = build_pauli(h, couplings)

    # If qiskit is available, expect a SparsePauliOp; otherwise a dict fallback
    try:
        from qiskit.quantum_info import SparsePauliOp

        assert isinstance(P, SparsePauliOp)
        assert len(P) == 3  # two singles + one pair
    except Exception:
        assert isinstance(P, dict)
        assert "paulis" in P and "coeffs" in P
        assert len(P["paulis"]) == 3
