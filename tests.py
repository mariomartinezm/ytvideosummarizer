import unittest

from utils import get_video_id


class TestUtilityFunctions(unittest.TestCase):
    def test_get_video_id(self):
        url = "https://www.youtube.com/watch?v=tMiQIxSX64c"
        self.assertEqual(get_video_id(url), "tMiQIxSX64c")

    def test_get_video_id_error(self):
        url = "https://notavideo.com/foo/bar"
        self.assertEqual(get_video_id(url), None)


if __name__ == "__main__":
    unittest.main()
