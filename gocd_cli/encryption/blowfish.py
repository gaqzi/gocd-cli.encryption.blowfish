from os import getenv
from random import getrandbits
from struct import pack
import base64

__version__ = '1.0'


def encrypt(plaintext):
    """Encrypts the passed plaintext

    The password is given by the environment variable
    GOCD_ENCRYPTION_PASSWORD.

    Returns:
      base64 encoded string
    """
    return _encrypt(plaintext, _get_password())


def decrypt(ciphertext):
    """Decrypts the passed ciphertext

    The password is given by the environment variable
    GOCD_ENCRYPTION_PASSWORD.

    Returns:
      plaintext
    """
    return _decrypt(ciphertext, _get_password())


def _get_password():
    password = getenv('GOCD_ENCRYPTION_PASSWORD')
    if not password:
        raise SystemError('GOCD_ENCRYPTION_PASSWORD environment variable not set')

    return password


def _encrypt(plaintext, password):
    """
    Encrypts `plaintext` with Blowfish in CBC mode using `password`

    Args:
      plaintext: The plaintext string to encrypt
      password: The password to use to decrypt plaintext.
        Should be at least 16 bytes.

    Returns:
      str: base64 encoded string.
        The decoded string format is "{iv}{ciphertext}"
    """
    from Crypto.Cipher import Blowfish
    from Crypto.Util.number import long_to_bytes

    # Copy+paste security! Except I use another source for random,
    # because I've to support PyCrypto 2.0.1.
    # https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.Blowfish-module.html
    iv = long_to_bytes(getrandbits(Blowfish.block_size * 8), Blowfish.block_size)
    cipher = Blowfish.new(password, Blowfish.MODE_CBC, iv)
    plen = Blowfish.block_size - divmod(len(plaintext), Blowfish.block_size)[1]
    padding = [plen] * plen
    padding = pack('b' * plen, *padding)  # RFC5652 style padding

    return base64.encodestring('{0}{1}'.format(iv, cipher.encrypt(plaintext + padding))).strip()


def _decrypt(base64_ciphertext, password):
    """
    Decrypts the output of :func:`_encrypt` using `password`

    Args:
      base64_ciphertext: The output of :func:`_encrypt`
      password: The password used to _encrypt the ciphertext

    Returns:
      str: The original plaintext
    """
    from Crypto.Cipher import Blowfish

    decodestring = base64.decodestring(base64_ciphertext)
    iv, ciphertext = decodestring[0:Blowfish.block_size], decodestring[Blowfish.block_size:]

    cipher = Blowfish.new(password, Blowfish.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    padding = ord(decrypted[-1])

    return decrypted[0:-padding]
