import unittest

from utils import get_video_id, get_video_transcript, join_transcript


class TestUtilityFunctions(unittest.TestCase):
    def test_get_video_id(self):
        url = "https://www.youtube.com/watch?v=_Yn7QAS5Wpw"
        self.assertEqual(get_video_id(url), "_Yn7QAS5Wpw")

    def test_get_video_id_error(self):
        url = "https://notavideo.com/foo/bar"
        self.assertEqual(get_video_id(url), None)

    def test_get_video_transcript(self):
        url = "https://www.youtube.com/watch?v=tMiQIxSX64c"
        video_id = get_video_id(url)
        transcript = get_video_transcript(video_id)

        self.assertIsInstance(transcript, list)

    def test_join_transcript(self):
        transcript = [{"text": "hello"}, {"text": " world"}]
        full_text = join_transcript(transcript)

        self.assertEqual(full_text, " hello  world")


if __name__ == "__main__":
    unittest.main()
