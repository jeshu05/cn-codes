import os, random, time

LOSS = 0.2     # chance that a frame is lost on the way (set 0 for no loss)
DELAY = 2      # seconds to wait for the receiver's reply

N = int(input("Enter window size: "))
msg = input("Enter text message: ")

base = 0                                     # first unacknowledged frame
while base < len(msg):
    end = min(base + N, len(msg))            # window = frames base .. end-1
    print(f"\nWindow: frames {base} to {end - 1}")

    # 1. Send frames [Frame no., DATA] -> screen + Sender_Buffer
    sent = ""
    for i in range(base, end):
        if random.random() < LOSS:
            print(f"  [{i}, {msg[i]}] lost")
        else:
            print(f"  [{i}, {msg[i]}] sent")
            sent += f"{i},{msg[i]}\n"
    open("Sender_Buffer", "w").write(sent)
    if os.path.exists("Receiver_Buffer"):
        os.remove("Receiver_Buffer")         # signals the receiver: new frames ready

    # 2. Wait for the receiver's reply (delay)
    reply = ""
    while not reply:
        time.sleep(DELAY)
        if os.path.exists("Receiver_Buffer"):
            reply = open("Receiver_Buffer").read()

    # 3. Check ACK / NACK number
    kind, n = reply.split()
    n = int(n)
    if kind == "ACK" and n == end:
        print(f"  {kind} {n} received as expected -> sliding window")
    else:
        print(f"  {kind} {n} received -> resending from frame {n}")
    base = n

print("\nMessage sent successfully")
