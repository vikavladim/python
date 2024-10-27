import unittest


class Key:
    def __init__(self):
        # print(1)
        self.passphrase = 'zax2rulez'

    def __len__(self):
        return 1337

    def __getitem__(self, index):
        if index == 404:
            return 3
        else:
            raise Exception('Error!')

    def __gt__(self, other):
        return 9005 > other

    def __str__(self):
        return 'GeneralTsoKeycard'


class TestCheck(unittest.TestCase):
    # def __init__(self) :
    key = Key()

    def setUp(self):
        pass

    def test_check1(self):
        self.assertEqual(len(self.key), 1337)

    def test_check2(self):
        self.assertEqual(self.key[404], 3)

    def test_check3(self):
        self.assertGreater(self.key, 9000)

    def test_check4(self):
        self.assertEqual(self.key.passphrase, 'zax2rulez')

    def test_check5(self):
        self.assertEqual(str(self.key), 'GeneralTsoKeycard')


if __name__ == '__main__':
    unittest.main()
