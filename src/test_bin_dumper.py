import bin_dumper
import unittest
import sys


class test_bin_dumper(unittest.TestCase):

    def test_read_file(self):
        bin_dumper.read_file("src/test_data/abcdefghijkl.bin")
        buf = bin_dumper.buffer
        self.assertFalse(buf is None)
        self.assertEqual(len(buf), 12)
        self.assertEqual(buf, b'abcdefghijkl')


    def test_read_file_empty(self):
        bin_dumper.read_file("src/test_data/empty.bin")
        buf = bin_dumper.buffer
        self.assertFalse(buf is None)
        self.assertEqual(len(buf), 0)


    def test_read_file_not_existing(self):
        with self.assertRaises(FileNotFoundError):
            bin_dumper.read_file("src/test_data/not_existing.bin")


    def test_dump_all(self):
        bin_dumper.read_file("src/test_data/abcdefghijkl.bin")
        alldata = bin_dumper.dump(0, sys.maxsize, None)
        self.assertEqual(alldata, b'abcdefghijkl')


    def test_dump(self):
        bin_dumper.read_file("src/test_data/abcdefghijkl.bin")
        # All
        part = bin_dumper.dump(0, 12, None);
        self.assertEqual(part, b'abcdefghijkl')
        # Right
        part = bin_dumper.dump(8, sys.maxsize, None)
        self.assertEqual(part, b'ijkl')
        # Left
        part = bin_dumper.dump(-4, 12, None)
        self.assertEqual(part, b'abcdefgh')
        # Partial
        part = bin_dumper.dump(1, 10, None)
        self.assertEqual(part, b'bcdefghijk')



if __name__ == '__main__':
    unittest.main()

