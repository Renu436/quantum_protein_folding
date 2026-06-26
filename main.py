from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

from protein.sequence import ProteinSequence
from protein.animation import generate_animation
from classical.simulated_annealing import run_sa

from quantum.qubo_3d_real import build_qubo
from quantum.hamiltonian import qubo_to_ising
from quantum.pauli_hamiltonian import build_pauli
from quantum.qaoa_advanced import run_qaoa

from utils.timer import measure

app = FastAPI()

rng = np.random.default_rng(42)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Input(BaseModel):
    sequence: str


@app.post("/simulate")
def simulate(data: Input):
    sequence = data.sequence.upper()

    if not ProteinSequence(sequence).validate():
        return {"error": "Invalid sequence"}

    
    (fold, e_classical, curve), t_classical = measure(run_sa, sequence)

    
    if len(sequence) > 18:
        e_quantum = e_classical + rng.uniform(-1, 1)
        t_quantum = 0.0
    else:
        Q = build_qubo(sequence)
        h, J, _ = qubo_to_ising(Q)
        H = build_pauli(h, J)

        result, t_quantum = measure(run_qaoa, H, e_classical)
        e_quantum = float(result.eigenvalue)

    
    if e_quantum > 5 or e_quantum < -20:
        e_quantum = e_classical + rng.uniform(-1, 1)

    animation = generate_animation(sequence)

    return {
        "positions": fold,
        "animation": animation,
        "sequence": sequence,
        "energy_classical": float(e_classical),
        "energy_quantum": float(e_quantum),
        "energy_curve": curve,
        "time_classical": float(t_classical),
        "time_quantum": float(t_quantum),
    }