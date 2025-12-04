# SOLAR10 Function Analysis

## Real SOLAR10 Implementation

Based on analysis of https://github.com/bbopt/solar:

### Key Findings

1. **Dimension Mismatch**: 
   - Real SOLAR10 has **5 inputs**, not 10
   - Project specification requires **10 dimensions**
   - Solution: Mock maps 10D → 5D (uses first 5 dimensions)

2. **Problem Type**:
   - Problem ID: 10
   - Name: "MINCOST_UNCONSTRAINED"
   - Description: "cost of storage + penalties"
   - Objective: Minimize cost

3. **Deterministic**:
   - SOLAR10 is **deterministic** (no stochastic outputs)
   - Current mock incorrectly includes stochastic noise

4. **Input Bounds** (Real SOLAR10):
   - x[0]: `_centralReceiverOutletTemperature` [793, 995]
   - x[1]: `_hotStorageHeight` [2, 50]
   - x[2]: `_hotStorageDiameter` [2, 30]
   - x[3]: `_hotStorageInsulThickness` [0.01, 5]
   - x[4]: `_coldStorageInsulThickness` [0.01, 5]

5. **Best Known Value**: 42.416671

6. **Domain Transformation**:
   - Project uses: [-1, 1]^10
   - Real SOLAR10 uses: [lb, ub] for 5 variables
   - Mock transforms: [-1, 1]^10 → [lb, ub]^5 (first 5 dims)

## Current Implementation

### Mock Function (`solar_mock.py`)
- **Updated** to be deterministic (removed stochastic noise)
- Uses cost-minimization structure (not Rosenbrock)
- Maps 10D → 5D space
- Values in range ~40-200 (best known ~42.416671)

### Real Binary Wrapper (`solar_wrapper_real.py`)
- Calls the compiled C++ binary
- Handles 10D → 5D transformation
- Requires compiled SOLAR binary at `temp_solar_repo/bin/solar`

## How Close is the Mock?

### Similarities:
- ✅ Deterministic (no noise)
- ✅ Cost-minimization structure
- ✅ 10D input handling (with transformation)
- ✅ Values in reasonable range (~40-200)

### Differences:
- ❌ Mock is a simplified approximation
- ❌ Real function involves complex solar power plant simulation
- ❌ Mock doesn't capture all physics/constraints
- ❌ Dimension mismatch (10D vs 5D) requires transformation

## Recommendation

For accurate results, use the real SOLAR binary:
1. Clone: `git clone https://github.com/bbopt/solar.git temp_solar_repo`
2. Compile: `cd temp_solar_repo/src && make`
3. The wrapper will automatically use it if available

The mock is a reasonable approximation for testing the optimization algorithms, but results will differ from the real SOLAR10.

