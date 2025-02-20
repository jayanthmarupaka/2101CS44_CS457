from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import time
import psutil
import matplotlib.pyplot as plt

# Key generation
def generate_key():
    return get_random_bytes(32)

# Encryption
def encrypt_file(input_file, output_file, key):

    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long for AES-256.")

    cipher = AES.new(key, AES.MODE_CBC)
    
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_file, 'wb') as f:
        # Write the IV followed by the ciphertext
        f.write(cipher.iv + ciphertext)

# Decryption
def decrypt_file(input_file, output_file, key):
    
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long for AES-256.")

    with open(input_file, 'rb') as f:
        iv = f.read(16)  # First 16 bytes are the IV
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    try:
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    except (ValueError, KeyError) as e:
        raise ValueError("Decryption failed. Ensure the correct key is used.") from e

    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Performance Testing
def performance_test():
    sizes = [1024, 1024 * 1024, 10 * 1024 * 1024, 100 * 1024 * 1024]  # 1KB, 1MB, 10MB, 100MB
    encryption_times = []
    decryption_times = []
    memory_usages = []
    cpu_usages = []

    key = generate_key()
    for size in sizes:
        input_file = f"test_{size}.bin"
        encrypted_file = f"test_{size}.enc"
        decrypted_file = f"test_{size}_dec.bin"

        # Generate a test file of the specified size
        with open(input_file, 'wb') as f:
            f.write(os.urandom(size))

        # Monitor memory and CPU usage, and encryption time
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss
        start_cpu = process.cpu_percent(interval=None)
        start_time = time.time()
        encrypt_file(input_file, encrypted_file, key)
        encryption_times.append(time.time() - start_time)
        cpu_usages.append(process.cpu_percent(interval=None) - start_cpu)
        memory_usages.append(process.memory_info().rss - start_memory)

        # Monitor decryption time
        start_time = time.time()
        decrypt_file(encrypted_file, decrypted_file, key)
        decryption_times.append(time.time() - start_time)

        # Cleanup
        os.remove(input_file)
        os.remove(encrypted_file)
        os.remove(decrypted_file)

    # Plot the results
    plt.figure(figsize=(12, 8))

    # Encryption/Decryption Times
    plt.subplot(3, 1, 1)
    plt.plot([size / 1024 for size in sizes], encryption_times, label="Encryption Time", marker='o')
    plt.plot([size / 1024 for size in sizes], decryption_times, label="Decryption Time", marker='o')
    plt.xlabel("Input Size (KB)")
    plt.ylabel("Time (s)")
    plt.title("Encryption/Decryption Time vs Input Size")
    plt.legend()

    # Memory Usage
    plt.subplot(3, 1, 2)
    plt.plot([size / 1024 for size in sizes], memory_usages, label="Memory Usage", marker='o')
    plt.xlabel("Input Size (KB)")
    plt.ylabel("Memory Usage (bytes)")
    plt.title("Memory Usage vs Input Size")
    plt.legend()

    # CPU Utilization
    plt.subplot(3, 1, 3)
    plt.plot([size / 1024 for size in sizes], cpu_usages, label="CPU Utilization", marker='o')
    plt.xlabel("Input Size (KB)")
    plt.ylabel("CPU Utilization (%)")
    plt.title("CPU Utilization vs Input Size")
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance_test()
