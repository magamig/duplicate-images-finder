import sys
import os
import argparse
import cv2 as cv


FEATURES_DISTANCE = 0.3
MIN_MATCHES = 50


def collect_imgs(directory):
	"""
	Collect images in directory.

	Parameters
	----------
	directory : str
		Directory with the images to check for similarities

	Returns
	-------
	imgs : list(dict)
		List of the images to compare
	"""

	imgs = []

	for file in os.listdir(directory):
		if(file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
			path = os.path.join(directory, file)
			imgs.append({
				'f': cv.imread(path, cv.IMREAD_GRAYSCALE),
				'p': path
			});

	return imgs


def detect_features(imgs):
	"""
	Detect and computes features and descriptors.

	SIFT (Scale-Invariant Feature Transform) feature detection algorithm is
	used to calculate the features and descriptors of each image.

	Parameters
	----------
	imgs : list(dict)
		List of the images to compare

	Returns
	-------
	imgs : list(str)
		List of the images to compare with keypoins and descriptors
	"""

	sift = cv.SIFT_create()

	for img in imgs:
		img['kp'], img['des'] = sift.detectAndCompute(img['f'], None)

	return imgs


def similarity_check(imgs):
	"""
	Checks Similarity.

	Complexity: O(n!) instead of the naive approach which is O(n^2).
	Using FLANN (Fast Library for Approximate Nearest Neighbors) matching
	algorithm for comparing each of the images' descriptors.

	Parameters
	----------
	imgs : list(dict)
		List of the images to compare

	Returns
	-------
	duplicates : list(str)
		List of the lowest resolution duplicate images
	"""

	duplicates = []

	for i1 in range(len(imgs)):
		for i2 in range(i1 + 1, len(imgs)):
			FLANN_INDEX_KDTREE = 1
			index_params = dict(
				algorithm = FLANN_INDEX_KDTREE,
				trees = 5
			)

			search_params = dict(checks=50)
			flann = cv.FlannBasedMatcher(index_params, search_params)
			matches = flann.knnMatch(imgs[i1]['des'], imgs[i2]['des'], k=2)
			matchesCount = 0
			for i,(m,n) in enumerate(matches):
				if m.distance < FEATURES_DISTANCE * n.distance:
					matchesCount += 1

			if(matchesCount > MIN_MATCHES):
				print('[DUPLICATE FOUND]', imgs[i1]['p'], imgs[i2]['p'])
				# adds the lower resolution image to the deletion list
				h1, w1 = imgs[i1]['f'].shape[:2]
				h2, w2 = imgs[i2]['f'].shape[:2]
				duplicates.append(imgs[i2 if h1*w1 > h2*w2 else i1]['p'])

	return duplicates


def delete(duplicates):
	"""
	Removes duplicated images.

	Parameters
	----------
	duplicates : int
		Description of arg1
	"""

	for path in duplicates:
		os.remove(path)
		print('[DELETED]', path)


def argparser():
	"""
	Parses arguments.

	For more information run ``python main.py -h``.

	Returns
	-------
	args : dict
		Parsed arguments
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument("directory", type=str,
		help="directory with the images")
	parser.add_argument("-d", "--delete", action='store_true',
		help="delete the duplicate images found with smaller res")
	parser.add_argument("-s", "--silent", action='store_true',
		help="quiet execution without logging")
	parser.add_argument('--min_matches', type=int,
		help="minimum number of matching features to accept the images as being similar")
	parser.add_argument('--features_distance', type=float,
		help="[0,1] - higher number results in more matching features but with less accuracy")
	args = parser.parse_args()

	if(args.silent):
		sys.stdout = open(os.devnull, 'a')
	if(args.min_matches):
		MIN_MATCHES = args.min_matches
	if(args.features_distance):
		FEATURES_DISTANCE = args.features_distance

	return args


def main():
	"""
	Main function.
	"""

	args = argparser()
	imgs = collect_imgs(args.directory)
	imgs = detect_features(imgs)
	duplicates = similarity_check(imgs)
	if args.delete:
		delete(duplicates)


if __name__ == "__main__":
	main()
