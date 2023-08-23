import unittest
import sys
import args
import io


class test_args(unittest.TestCase):

    def test_get_nth_arg(self):
        self.assertEqual(args.get_nth_arg(0, []), None)
        self.assertEqual(args.get_nth_arg(0, ["a"]), "a")
        self.assertEqual(args.get_nth_arg(1, ["a"]), None)
        self.assertEqual(args.get_nth_arg(0, ["a", "b"]), "a")
        self.assertEqual(args.get_nth_arg(1, ["a", "b"]), "b")


    def test_parse_args_version(self):
        out = io.BytesIO()
        args.parse_args(["path", "--version"], out)
        part = out.getbuffer()
        self.assertTrue(part.tobytes().startswith(b'Version '))


    def test_parse_args_simple(self):
        out = io.BytesIO()
        args.parse_args(["path"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'')

        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'')

        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--size", "all"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'abcdefghijkl')


    def test_parse_args_dump_offs(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--offs", "3", "--size", "4"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'defg')


    def test_parse_args_2_slices(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--offs", "2", "--size", "3", "--size", "4"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'cdefghi')


    def test_parse_args_2_slices_offs(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--offs", "+1", "--size", "3", "--offs", "+4", "--size", "2"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'bcdij')


    def test_parse_args_out_of_range_3(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--offs", "-3", "--size", "3"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'')


    def test_parse_args_out_of_range_4(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--offs", "12", "--size", "1"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'')

    def test_parse_args_out_of_range_5(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--offs", "-2", "--size", "20"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'abcdefghijkl')


    def test_parse_args_two_files(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--offs", "5", "--size", "2", "src/test_data/mnopqrstuvwx.bin", "--offs", "+1", "--size", "4"], out)
        part = out.getbuffer()
        self.assertEqual(part.tobytes(), b'fgnopq')


    def test_parse_args_search_1(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--search", "a", "--size", "2"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'ab')


    def test_parse_args_search_2(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--search", "bcd", "--size", "2"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'bc')


    def test_parse_args_search_3(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--search", "kl", "--size", "5"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'kl')


    def test_parse_args_search_4(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--search", "", "--size", "2"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'ab')


    def test_parse_args_search_5(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--search", "xy", "--size", "2"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'')


    def test_parse_args_search_6(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdabcdaxyz.bin", "--search", "a", "--offs", "+1", "--search", "a", "--offs", "+1", "--search", "a", "--offs", "+1", "--size", "3"], out)
        part = out.getbuffer()
        self.assertEqual(part.tobytes(), b'xyz')


    def test_parse_args_search_decimal(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--search", "\\d98", "--size", "3"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'bcd')


    def test_parse_args_search_decimal_and_hex(self):
        out = io.BytesIO()
        args.parse_args(["path", "src/test_data/abcdefghijkl.bin", "--search", "\\d99,\\x64", "--size", "3"], out)
        part = out.getbuffer()
        self.assertEqual(part, b'cde')


if __name__ == '__main__':
    unittest.main()

