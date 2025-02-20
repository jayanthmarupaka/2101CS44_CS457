import random
from Crypto.Util import number
import time
import matplotlib.pyplot as plt
import psutil

# RSA Key Pair Generation
def generate_key_pair(key_size=2048):
    """
    Generates RSA public and private keys.
    :param key_size: Size of the key in bits
    :return: (public_key, private_key)
    """
    p = number.getPrime(key_size // 2)
    q = number.getPrime(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Common choice for e
    d = pow(e, -1, phi)

    return ((e, n), (d, n))

# RSA Encryption
def encrypt(message, public_key):
    """
    Encrypts a message using the RSA public key.
    :param message: Message string to encrypt
    :param public_key: Tuple containing (e, n)
    :return: Encrypted message as an integer
    """
    e, n = public_key
    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')

    if message_int >= n:
        raise ValueError("Message too large for the key size.")

    return pow(message_int, e, n)

# RSA Decryption
def decrypt(ciphertext, private_key):
    """
    Decrypts a ciphertext using the RSA private key.
    :param ciphertext: Encrypted message as an integer
    :param private_key: Tuple containing (d, n)
    :return: Decrypted message string
    """
    d, n = private_key
    message_int = pow(ciphertext, d, n)
    
    try:
        message_length = (message_int.bit_length() + 7) // 8
        return message_int.to_bytes(message_length, byteorder='big').decode('utf-8')
    except Exception as e:
        raise ValueError("Decryption failed: " + str(e))

# Performance Testing
def performance_test():
    key_sizes = [1024, 2048, 4096]
    message_sizes = [16, 32, 64]  # in bytes
    encryption_times = {}
    decryption_times = {}
    memory_usages = {}
    cpu_usages = {}

    for key_size in key_sizes:
        public_key, private_key = generate_key_pair(key_size)
        encryption_times[key_size] = []
        decryption_times[key_size] = []
        memory_usages[key_size] = []
        cpu_usages[key_size] = []

        for size in message_sizes:
            message = 'jayanth kumar'
            start_time = time.time()
            ciphertext = encrypt(message, public_key)
            encryption_time = time.time() - start_time

            start_time = time.time()
            decrypted_message = decrypt(ciphertext, private_key)
            decryption_time = time.time() - start_time

            memory_info = psutil.Process().memory_info().rss / (1024 ** 2)  # Memory in MB
            cpu_info = psutil.cpu_percent(interval=0.1)

            encryption_times[key_size].append(encryption_time)
            decryption_times[key_size].append(decryption_time)
            memory_usages[key_size].append(memory_info)
            cpu_usages[key_size].append(cpu_info)

            assert message == decrypted_message, "Decryption failed"

    visualize_performance(key_sizes, message_sizes, encryption_times, decryption_times, memory_usages, cpu_usages)

# Visualization
def visualize_performance(key_sizes, message_sizes, encryption_times, decryption_times, memory_usages, cpu_usages):
    for key_size in key_sizes:
        plt.figure(figsize=(10, 6))

        plt.subplot(2, 2, 1)
        plt.plot(message_sizes, encryption_times[key_size], label=f'Encryption {key_size}-bit')
        plt.xlabel('Message Size (bytes)')
        plt.ylabel('Time (s)')
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(message_sizes, decryption_times[key_size], label=f'Decryption {key_size}-bit')
        plt.xlabel('Message Size (bytes)')
        plt.ylabel('Time (s)')
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.plot(message_sizes, memory_usages[key_size], label=f'Memory {key_size}-bit')
        plt.xlabel('Message Size (bytes)')
        plt.ylabel('Memory (MB)')
        plt.legend()

        plt.subplot(2, 2, 4)
        plt.plot(message_sizes, cpu_usages[key_size], label=f'CPU {key_size}-bit')
        plt.xlabel('Message Size (bytes)')
        plt.ylabel('CPU Usage (%)')
        plt.legend()

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    performance_test()

