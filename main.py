import sys
import os
import argparse
import cv2 as cv

FEATURES_DISTANCE = 0.3 
MIN_MATCHES = 50 

# Creates list with the images of the directory
def collect_imgs(directory):
	imgs = []
	
	for file in os.listdir(directory):
		if(file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
			path = os.path.join(directory, file)
			imgs.append({
				'f': cv.imread(path, cv.IMREAD_GRAYSCALE),
				'p': path
			});

	return imgs

# Feature matching 
# Complexity: O(n!) instead of the naive approach with O(n^2)
def similarity_check(imgs):
	duplicates = []
	
	for i1 in range(len(imgs)):
		for i2 in range(i1 + 1, len(imgs)):
			sift = cv.xfeatures2d.SIFT_create()
			kp1, des1 = sift.detectAndCompute(imgs[i1]['f'], None)
			kp2, des2 = sift.detectAndCompute(imgs[i2]['f'], None)

			FLANN_INDEX_KDTREE = 1
			index_params = dict(
				algorithm = FLANN_INDEX_KDTREE,
				trees = 5
			)

			search_params = dict(checks=50)
			flann = cv.FlannBasedMatcher(index_params, search_params)
			matches = flann.knnMatch(des1, des2, k=2)
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

# Remove duplicates
def delete(duplicates):
	for path in duplicates:
		os.remove(path)
		print('[DELETED]', path)

def argparser():
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
	args = argparser()
	imgs = collect_imgs(args.directory)
	duplicates = similarity_check(imgs)
	if args.delete: 
		delete(duplicates)

if __name__ == "__main__":
    main()

