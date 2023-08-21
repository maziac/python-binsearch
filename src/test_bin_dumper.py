import bin_dumper
import unittest
import sys


class test_bin_dumper(unittest.TestCase):

    def test_read_file(self):
        bin_dumper.read_file("src/test_data/abcdefghijkl.bin")  # NOSONAR
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


    def test_parse_search_string(self):
        sc = bin_dumper.parse_search_string("abc")
        self.assertEqual(sc, b'abc')

        sc = bin_dumper.parse_search_string("")
        self.assertEqual(sc, b'')

        sc = bin_dumper.parse_search_string("\\d123")
        self.assertEqual(sc[0], 123)
        self.assertEqual(len(sc), 1)

        sc = bin_dumper.parse_search_string("\\xFA")
        self.assertEqual(sc, b'\xFA')
        self.assertEqual(len(sc), 1)

        sc = bin_dumper.parse_search_string("\\d129,a")
        self.assertEqual(sc, b'\x81a')
        self.assertEqual(len(sc), 2)

        sc = bin_dumper.parse_search_string("\\xFA")
        self.assertEqual(sc[0], 0xFA)
        self.assertEqual(len(sc), 1)

        sc = bin_dumper.parse_search_string("a\\xFA,\\d7,bc\\d9")
        self.assertEqual(sc, b'a\xFA\x07bc\x09')
        self.assertEqual(len(sc), 6)

        sc = bin_dumper.parse_search_string("a\\\\b")
        self.assertEqual(sc, b'a\\b')
        self.assertEqual(len(sc), 3)


    def test_parse_search_string_error_cases(self):
        with self.assertRaises(Exception) as ctx:
            bin_dumper.parse_search_string("\\a")
        self.assertEqual(str(ctx.exception),"Expected 'd' or 'x'.")


if __name__ == '__main__':
    unittest.main()

