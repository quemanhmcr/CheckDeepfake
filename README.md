# CheckDeepfake

```python
def knapsack(W, wt, val, n):
  # Tạo mảng dp
  dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

  # Duyệt qua từng món đồ
  for i in range(1, n + 1):
    # Duyệt qua từng trọng lượng
    for w in range(1, W + 1):
      # Nếu trọng lượng của món đồ thứ i nhỏ hơn hoặc bằng trọng lượng tối đa
      if wt[i - 1] <= w:
        # Lựa chọn giá trị tối ưu: chọn hoặc không chọn món đồ thứ i
        dp[i][w] = max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w])
      # Nếu trọng lượng của món đồ thứ i lớn hơn trọng lượng tối đa
      else:
        # Không thể chọn món đồ thứ i
        dp[i][w] = dp[i - 1][w]

  # Trả về giá trị tối ưu
  return dp[n][W]

# Ví dụ sử dụng
val = [60, 100, 120]
wt = [10, 20, 30]
W = 50
n = len(val)

result = knapsack(W, wt, val, n)
print(f"Giá trị tối ưu: {result}")
```
