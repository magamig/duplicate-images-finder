import unittest
import os
import sys
import main

class TestMethods(unittest.TestCase):

	def setUp(self):
		self.directory = './sample_images'

	def test_imgs_len(self):
		length = len(os.listdir(self.directory))
		imgs = main.collect_imgs(self.directory)
		self.assertEqual(len(imgs), length)
		imgs = main.detect_features(imgs)
		self.assertEqual(len(imgs), length)

	def test_duplicates_found(self):
		imgs = main.collect_imgs(self.directory)
		imgs = main.detect_features(imgs)
		duplicates = main.similarity_check(imgs)
		self.assertEqual(duplicates, ['./sample_images/road_duplicate.jpg'])


if __name__ == '__main__':
	unittest.main()
