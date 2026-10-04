import unittest
import textstats


class TextStatsTests(unittest.TestCase):
    def test_word_count_simple(self):
        self.assertEqual(textstats.word_count("one two three"), 3)

    def test_word_count_extra_spaces(self):
        self.assertEqual(textstats.word_count("  one   two  "), 2)

    def test_word_count_empty(self):
        self.assertEqual(textstats.word_count(""), 0)

    def test_most_common_case_insensitive(self):
        self.assertEqual(textstats.most_common("The cat. the dog! THE end", 1), [("the", 3)])

    def test_most_common_ties_alphabetical(self):
        self.assertEqual(textstats.most_common("b a c a b", 3), [("a", 2), ("b", 2), ("c", 1)])

    def test_avg_word_length(self):
        self.assertEqual(textstats.avg_word_length("hi there!"), 3.5)

    def test_avg_word_length_empty(self):
        self.assertEqual(textstats.avg_word_length(""), 0.0)


if __name__ == "__main__":
    unittest.main()
