import os, time

expected, message = 0, ""
open("Receiver_Buffer", "w").write("ACK 0")       # ready, expecting frame 0

while True:
    time.sleep(1)
    if os.path.exists("Receiver_Buffer"):          # no new frames from sender yet
        continue

    reply = "ACK"
    for line in open("Sender_Buffer"):             # each line = Frame no.,DATA
        no, data = line.rstrip("\n").split(",", 1)
        if int(no) != expected:                    # wrong frame no. -> frame was lost
            print(f"Frame {no}: expected {expected}")
            reply = "NACK"
            break
        print(f"Frame {no}: OK ({data})")
        message += data
        expected += 1

    open("Receiver_Buffer", "w").write(f"{reply} {expected}")
    print(f"-> wrote {reply} {expected} | Message so far: {message}\n")
