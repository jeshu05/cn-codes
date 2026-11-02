code = open("channel").read().strip()

# XOR of positions of all 1s: 0 = no error, otherwise it is the error position
error = 0
for i, bit in enumerate(code, 1):
    if bit == "1":
        error ^= i

if error:
    print("Error detected at bit position", error)
else:
    # remove parity bits (positions 1,2,4,8...)
    data = "".join(bit for i, bit in enumerate(code, 1) if i & (i - 1))
    print("No error detected.")
    print("Binary data:", data)
    if len(data) % 8 == 0:
        chars = bytes(int(data[i:i + 8], 2) for i in range(0, len(data), 8))
        print("Text output:", chars.decode(errors="replace"))
