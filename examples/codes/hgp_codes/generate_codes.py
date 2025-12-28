import numpy as np
from bposd.hgp import hgp

classical_seed_codes = ["mkmn_16_4_6.txt", "mkmn_20_5_8.txt", "mkmn_24_6_10.txt"]

for code in classical_seed_codes:
    seed_code = np.loadtxt(f"examples/codes/classical_seed_codes/{code}").astype(int)
    # print(seed_code)
    qcode = hgp(seed_code, compute_distance=True)

    # Logical operators are already computed in hgp.__init__() via compute_logicals()
    # No need to call canonical_logicals() as it doesn't exist

    qcode.test()

    # print(qcode.code_params)

    # Create filename from N, K, D parameters
    filename = f"hgp_({qcode.L},{qcode.Q})-[[{qcode.N},{qcode.K},{qcode.D}]]"
    
    # Convert sparse matrices to dense arrays before saving
    np.savetxt(f"examples/codes/hgp_codes/{filename}_hx.txt", qcode.hx.toarray(), fmt='%d')
    np.savetxt(f"examples/codes/hgp_codes/{filename}_hz.txt", qcode.hz.toarray(), fmt='%d')
    np.savetxt(f"examples/codes/hgp_codes/{filename}_lx.txt", qcode.lx.toarray(), fmt='%d')
    np.savetxt(f"examples/codes/hgp_codes/{filename}_lz.txt", qcode.lz.toarray(), fmt='%d')
