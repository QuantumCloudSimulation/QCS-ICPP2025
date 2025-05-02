import json
from mqt.bench import get_benchmark

def generate_qcloudsim_jobs(num_jobs=5, noise_models=None):
    """
    Generate QCloudSim-compatible jobs using circuits from MQT Bench.
    
    Parameters:
    - num_jobs (int): Number of jobs to generate.
    - noise_models (list): List of noise model names to randomly assign.
    
    Returns:
    - jobs_data (dict): A dictionary representing jobs in QCloudSim format.
    """
    jobs_data = {"jobs": []}
    noise_models = noise_models or ["ibmq_montreal", "rigetti_aspen", "ionq_arline"]
    
    # List of available benchmark names in MQT Bench (modify as needed)
    benchmark_names = ['ae', 'dj', 'grover-noancilla', 'grover-v-chain', 'ghz', 'graphstate', 'portfolioqaoa', 'portfoliovqe', 'qaoa', 'qft', 'qftentangled', 'qnn', 'qpeexact', 'qpeinexact', 'qwalk-noancilla', 'qwalk-v-chain', 'random', 'realamprandom', 'su2random', 'twolocalrandom', 'vqe', 'wstate', 'shor', 'pricingcall', 'pricingput', 'groundstate', 'routing', 'tsp']
    
    for job_id in range(1, num_jobs + 1):
        # Select a benchmark name based on job ID (cyclic selection)
        benchmark_name = 'dj'
        
        # Get a benchmark circuit from MQT Bench
        circuit = get_benchmark(
            benchmark_name=benchmark_name,
            level="mapped",           # Use "mapped" level for realistic benchmarks
            circuit_size=job_id,  # Circuit size increases with job_id
            device_name="ionq_harmony"  # Example device name
        )
        
        # Extract circuit details
        num_qubits = circuit.num_qubits
        depth = circuit.depth()
        gates = [{"gate": gate.name, "qubits": [q._index for q in gate.qubits]} for gate in circuit.data]
        
        # Create job entry
        job = {
            "job_id": job_id,
            "benchmark_name": benchmark_name,
            "num_qubits": num_qubits,
            "depth": depth,
            "gates": gates,
            "expected_exec_time": round(depth * 0.1, 2),  # Arbitrary example exec time
            "priority": 1 if job_id % 2 == 0 else 2,
            "noise_model": noise_models[job_id % len(noise_models)],
            "arrival_time": job_id * 5,  # Staggered arrival times
            "num_shots": 500
        }
        jobs_data["jobs"].append(job)
    
    return jobs_data

# Generate sample data
num_jobs = 5
noise_models = ["ibmq_montreal", "rigetti_aspen", "ionq_arline"]
qcloudsim_jobs = generate_qcloudsim_jobs(num_jobs, noise_models)

# Save to JSON file
with open(f"QCloudSimJobs_MQT_dj2.json", "w") as f:
    json.dump(qcloudsim_jobs, f, indent=4)

print(f"Generated {num_jobs} QCloudSim jobs and saved to QCloudSimJobs_MQT.json")