import sys

text = open(sys.argv[1] if len(sys.argv) > 1 else "input.txt").read().strip()

# 1. Convert to binary (if input is already 0s and 1s, keep it as is)
if set(text) <= set("01 \n"):
    data = "".join(text.split())
else:
    data = "".join(format(b, "08b") for b in text.encode())

# 2. Hamming code: find number of parity bits r
r = 0
while 2 ** r < len(data) + r + 1:
    r += 1
n = len(data) + r

# put data bits in non-power-of-2 positions (parity positions 1,2,4,8... stay 0)
code, k = [], 0
for i in range(1, n + 1):
    if i & (i - 1) == 0:
        code.append(0)
    else:
        code.append(int(data[k]))
        k += 1

# XOR of positions of all 1s tells which parity bits must be set (even parity)
x = 0
for i in range(1, n + 1):
    if code[i - 1] == 1:
        x ^= i
for p in range(r):
    code[2 ** p - 1] = (x >> p) & 1

# 3. Save to channel
open("channel", "w").write("".join(map(str, code)))
print("Data bits:", len(data), "| Code bits:", n, "| Saved to file: channel")
