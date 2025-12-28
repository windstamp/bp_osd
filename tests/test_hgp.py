import numpy as np
from bposd.hgp import hgp

def generate_rep_code(n):
    """生成重复码的校验矩阵 [n, 1, n]"""
    # 重复码: 所有比特必须相同
    # 校验矩阵: 检查相邻比特是否相同
    h = np.zeros((n-1, n), dtype=np.uint8)
    for i in range(n-1):
        h[i, i] = 1
        h[i, i+1] = 1
    return h

def test_hgp_surface():
    print("=== Test: HGP Surface Code (Repetition Code) ===\n")
    
    # 使用重复码构造 surface-like HGP 码
    h = generate_rep_code(3)  # [3, 1, 3] 重复码
    
    print(f"Repetition code parity check matrix H:")
    print(h)
    print(f"Shape: {h.shape}\n")
    
    # 创建对称 HGP 码
    code = hgp(h, h)
    
    print(f"HGP Code Parameters:")
    print(f"  Physical qubits N = {code.N}")
    print(f"  Logical qubits K = {code.K}")
    print(f"  Code distance D = {code.D}")
    
    # 验证码
    print("\n=== Code Validation ===")
    is_valid = code.test(show_tests=True)
    
    print(f"\n{'✓' if is_valid else '✗'} Code is {'valid' if is_valid else 'invalid'}")
    
    # 显示校验矩阵维度
    print(f"\n=== Parity Check Matrices ===")
    print(f"Hx shape: {code.hx.shape}")
    print(f"Hz shape: {code.hz.shape}")
    print(f"H (combined) shape: {code.h.shape}")
    
    return is_valid

def test_hgp_hamming():
    print("\n\n=== Test: HGP Hamming Code ===\n")
    
    # Hamming [7,4,3] 码
    h = np.array([[1, 0, 0, 1, 0, 1, 1],
                  [0, 1, 0, 1, 1, 0, 1],
                  [0, 0, 1, 0, 1, 1, 1]], dtype=np.uint8)
    
    print(f"Hamming [7,4,3] parity check matrix:")
    print(h)
    print(f"Shape: {h.shape}\n")
    
    # 创建对称 HGP 码
    code = hgp(h, h, compute_distance=False)
    
    print(f"HGP Code Parameters:")
    print(f"  Physical qubits N = {code.N}")
    print(f"  Logical qubits K = {code.K}")
    print(f"  Expected: N = 7×7 + 3×3 = 58, K = 4×4 + 0×0 = 16")
    
    # 验证计算
    assert code.N == 58, f"Expected N=58, got {code.N}"
    assert code.K == 16, f"Expected K=16, got {code.K}"
    
    # 验证码
    print("\n=== Code Validation ===")
    is_valid = code.test(show_tests=True)
    
    print(f"\n{'✓' if is_valid else '✗'} Code is {'valid' if is_valid else 'invalid'}")
    
    return is_valid

def test_hgp_asymmetric():
    print("\n\n=== Test: Asymmetric HGP ===\n")
    
    # 两个不同的码
    h1 = np.array([[1, 1, 1, 0, 0],
                   [0, 0, 1, 1, 1]], dtype=np.uint8)  # [5,3] 码
    
    h2 = np.array([[1, 0, 1]], dtype=np.uint8)  # [3,2] 码
    
    print(f"Code 1 parity check matrix H1 (shape {h1.shape}):")
    print(h1)
    print(f"\nCode 2 parity check matrix H2 (shape {h2.shape}):")
    print(h2)
    
    # 创建非对称 HGP
    code = hgp(h1, h2)
    
    print(f"\nHGP Code Parameters:")
    print(f"  Physical qubits N = {code.N}")
    print(f"  Logical qubits K = {code.K}")
    
    # 手动计算验证
    n1, m1 = h1.shape[1], h1.shape[0]  # 5, 2
    n2, m2 = h2.shape[1], h2.shape[0]  # 3, 1
    expected_N = n1 * n2 + m1 * m2  # 5×3 + 2×1 = 17
    
    print(f"  Expected: N = {n1}×{n2} + {m1}×{m2} = {expected_N}")
    
    assert code.N == expected_N, f"Expected N={expected_N}, got {code.N}"
    
    # 验证码
    print("\n=== Code Validation ===")
    is_valid = code.test(show_tests=True)
    
    print(f"\n{'✓' if is_valid else '✗'} Code is {'valid' if is_valid else 'invalid'}")
    
    return is_valid

if __name__ == "__main__":
    print("=" * 60)
    print("HGP Code Tests")
    print("=" * 60)
    
    try:
        # 测试1: Surface-like 码（重复码）
        result1 = test_hgp_surface()
        
        # 测试2: Hamming 码
        result2 = test_hgp_hamming()
        
        # 测试3: 非对称 HGP
        result3 = test_hgp_asymmetric()
        
        # 总结
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"Surface Code Test: {'PASS ✓' if result1 else 'FAIL ✗'}")
        print(f"Hamming Code Test: {'PASS ✓' if result2 else 'FAIL ✗'}")
        print(f"Asymmetric HGP Test: {'PASS ✓' if result3 else 'FAIL ✗'}")
        
        if all([result1, result2, result3]):
            print("\n🎉 All tests passed!")
        else:
            print("\n❌ Some tests failed!")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()