import random

from gocd_cli.encryption import blowfish


class TestBlowfish(object):
    password = 'm000'
    ciphertext = 'Yp9vvtgsB83B350U4U+DBw=='

    def test_successfully_encrypts_a_string(self):
        random.seed(0)
        assert blowfish._encrypt('secret', self.password) == self.ciphertext

    def test_successfully_decrypts_a_string(self):
        ciphertext = blowfish._encrypt('secret', self.password)

        assert blowfish._decrypt(ciphertext, self.password) == 'secret'

    def test_successfully_encrypts_decrypts_strings_up_to_100_characters(self):
        for i in range(1, 101):
            string = ''.join([chr(random.randint(33, 126)) for _ in range(0, i)])

            assert blowfish._decrypt(
                blowfish._encrypt(string, self.password),
                self.password
            ) == string
