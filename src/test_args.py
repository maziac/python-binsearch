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


if __name__ == '__main__':
    unittest.main()

