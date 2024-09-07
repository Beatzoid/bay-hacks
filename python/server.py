import base64
import udpsocket as U
import time

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

received_chunks = {}
expected_chunks = -1  # Set to -1 to signal that no chunks have been received yet

print("Listening")

while True:
    data = sock.ReadReceivedData()  # read data

    if data is not None:  # if NEW data has been received since last ReadReceivedData function call
        try:
            # Split chunk info and the actual base64 data
            chunk_info, chunk_data = data.split('|')
            chunk_index, total_chunks = map(int, chunk_info.split('/'))

            print(f"Received chunk {chunk_index}/{total_chunks}")

            # Set expected total chunks on first received chunk
            if expected_chunks == -1:
                expected_chunks = total_chunks

            # Store the chunk (chunk index starts at 1)
            received_chunks[chunk_index] = chunk_data

            print(f"Received {len(received_chunks)}/{expected_chunks} chunks")

            # Check if all expected chunks have been received
            if len(received_chunks) == expected_chunks:
                print("All chunks received.")

                # Sort chunks by their index
                sorted_chunks = [received_chunks[i] for i in range(1, expected_chunks + 1)]

                # Reassemble the full message
                full_base64_string = ''.join(sorted_chunks)

                # Decode the base64 string
                decoded_data = base64.b64decode(full_base64_string)

                # Optionally save it as a file (if it's an image, for example)
                with open("received_snapshot.png", "wb") as f:
                    f.write(decoded_data)

                print("Complete message received and decoded")

                # Reset for the next message
                expected_chunks = -1
                received_chunks.clear()

            # else:
            #     # Detect and log missing chunks
            #     missing_chunks = [i for i in range(1, expected_chunks + 1) if i not in received_chunks]
            #     if len(missing_chunks) > 0:
            #         print(f"Missing chunks: {missing_chunks}")

        except Exception as e:
            print(f"Error processing received data: {e}")
