=======================================
Blowfish encryption module for gocd-cli
=======================================

This is a module that uses `pycrypto`_ and their `Blowfish`_ implementation
to encrypt and decrypt values in the `gocd-cli`_ configuration file.


The module was created to fulfil a requirement that the password to access
the Go server had to be encrypted while not in use, and with an approved cipher.
It was fine to store the decryption password on the same machine. If your
security needs are more stringent, then this module at its current state
will not be enough for you. :)

You'll likely be happier using `SELinux`_ and defining which processes are
allowed to access the unencrypted password from the file on disk instead of
using this.

Installation
------------

Install the module from PyPi:

.. code-block:: shell

    $ pip install gocd-cli.encryption.blowfish

To prepare `gocd-cli`_ you need to add the encryption module to the
config file, so it understands which module to use to handle
decryption/encryption.

Example ``~/.gocd/gocd-cli.cfg``:

.. code-block:: ini

    [gocd]
    encryption_module = gocd_cli.encryption.blowfish

Usage
-----

To then encrypt the current plaintext password do:

.. code-block:: shell

    $ gocd settings encrypt --key password
    encryption_module = gocd_cli.encryption.blowfish
    password_encrypted = b3o9xrRHgY1fggQ2XXT6pX1VxTyJVSk8

To decrypt:

.. code-block:: shell

    $ gocd settings decrypt --key password
    encryption_module = gocd_cli.encryption.blowfish
    password = super secret

.. note::

    If you encrypt the same string multiple times you will get different
    ciphertext each time. This is because the encryption module uses a random
    `IV`_ each time it encrypts.

    If you haven't configured an encryption module the built-in `caesar cipher`_
    module from gocd-cli will be used.

.. _pycrypto: https://pypi.python.org/pypi/pycrypto
.. _Blowfish: https://en.wikipedia.org/wiki/Blowfish_(cipher)
.. _caesar cipher: https://en.wikipedia.org/wiki/Caesar_cipher
.. _gocd-cli: https://github.com/gaqzi/gocd-cli
.. _IV: https://en.wikipedia.org/wiki/Initialization_vector
.. _SELinux: https://en.wikipedia.org/wiki/Security-Enhanced_Linux
