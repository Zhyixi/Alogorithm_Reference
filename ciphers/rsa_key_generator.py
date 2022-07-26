import os
import random
import sys

from . import cryptomath_module as cryptoMath
from . import rabin_miller as rabinMiller


def main() -> None:
    print("Making key files...")
    makeKeyFiles("rsa", 1024)
    print("Key files generation successful.")


def generateKey(keySize: int) -> tuple[tuple[int, int], tuple[int, int]]:
    print("Generating prime p...")
    p = rabinMiller.generateLargePrime(keySize)
    print("Generating prime q...")
    q = rabinMiller.generateLargePrime(keySize)
    n = p * q

    print("Generating e that is relatively prime to (p - 1) * (q - 1)...")
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptoMath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    print("Calculating d that is mod inverse of e...")
    d = cryptoMath.find_mod_inverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)
    return (publicKey, privateKey)


def makeKeyFiles(name: str, keySize: int) -> None:
    if os.path.exists(f"{name}_pubkey.txt") or os.path.exists(f"{name}_privkey.txt"):
        print("\nWARNING:")
        print(
            '"%s_pubkey.txt" or "%s_privkey.txt" already exists. \n'
            "Use a different name or delete these files and re-run this program."
            % (name, name)
        )
        sys.exit()

    publicKey, privateKey = generateKey(keySize)
    print(f"\nWriting public key to file {name}_pubkey.txt...")
    with open(f"{name}_pubkey.txt", "w") as out_file:
        out_file.write(f"{keySize},{publicKey[0]},{publicKey[1]}")

    print(f"Writing private key to file {name}_privkey.txt...")
    with open(f"{name}_privkey.txt", "w") as out_file:
        out_file.write(f"{keySize},{privateKey[0]},{privateKey[1]}")


if __name__ == "__main__":
    main()
