import sys
import os
import cv2 as cv

# between 0 and 1 - higher number results in more matches but with less accuracy
EUCLIDEAN_DISTANCE = 0.3 
# minimum number of matches to accept the images as being similar
MIN_MATCHES = 50 

if __name__ == "__main__":
	# Creates list with the images of the directory
	directory = sys.argv[1]
	imgs = []
	for file in os.listdir(directory):
		if(file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
			path = os.path.join(directory, file)
			imgs.append({
				'f': cv.imread(path, cv.IMREAD_GRAYSCALE),
				'p': path
			});

	# Feature matching 
	# Complexity: O(n!) instead of the naive approach with O(n^2)
	toDelete = []
	for i1 in range(len(imgs)):
		for i2 in range(i1 + 1, len(imgs)):
			sift = cv.xfeatures2d.SIFT_create()
			kp1, des1 = sift.detectAndCompute(imgs[i1]['f'], None)
			kp2, des2 = sift.detectAndCompute(imgs[i2]['f'], None)

			FLANN_INDEX_KDTREE = 1
			index_params = dict(
				algorithm = FLANN_INDEX_KDTREE,
				trees = 5)

			search_params = dict(checks=50)
			flann = cv.FlannBasedMatcher(index_params, search_params)
			matches = flann.knnMatch(des1, des2, k=2)
			matchesCount = 0
			for i,(m,n) in enumerate(matches):
				if m.distance < EUCLIDEAN_DISTANCE * n.distance:
					matchesCount += 1

			if(matchesCount > MIN_MATCHES):
				print('[DUPLICATE FOUND]', imgs[i1]['p'], imgs[i2]['p'])
				# Adds the lower resolution image to the deletion list
				h1, w1 = imgs[i1]['f'].shape[:2]
				h2, w2 = imgs[i2]['f'].shape[:2]
				toDelete.append(imgs[i2 if h1*w1 > h2*w2 else i1]['p'])
	
	# Uncomment to delete repeated images
	# for path in toDelete:
	# 	os.remove(path)
	# 	print('[DELETED]', path)
