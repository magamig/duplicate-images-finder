import sys
import os
import argparse
import cv2 as cv
import time


FEATURES_DISTANCE = 0.3
MIN_MATCHES = 50
MAX_KEYPOINTS = 100
scale_percent = 12 # percent of original size

def collect_imgs(directory):

        imgs = []
        count = 0
        for file in os.listdir(directory):
                if(file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))):
                        try:
                                print('[ADDING IMAGES]', count)
                                path = os.path.join(directory, file)
                                imgs.append({
                                        'f': cv.imread(path, cv.IMREAD_GRAYSCALE),
                                        'p': path
                                });
                                
                        except:
                                print("[FAILURE OPENING FILE]", path)
                            
                count+=1
        

        return imgs
    
def resize_images(imgs):
    
        #resize images to scale factor                
        for i1 in range(len(imgs)):
                try:
                    h1, w1 = imgs[i1]['f'].shape[:2]
                
                    if(h1 >= 800 and w1 >= 800):
                            width = int(imgs[i1]['f'].shape[1] * scale_percent / 100)
                            height = int(imgs[i1]['f'].shape[0] * scale_percent / 100)
                            dim = (width, height)
                            imgs[i1]['f'] = cv.resize(imgs[i1]['f'], dim, interpolation = cv.INTER_AREA)
                except:
                    continue

        return imgs

def detect_features(imgs):
        
        #sift detection object max keypoints set globally
        sift = cv.SIFT_create(MAX_KEYPOINTS)

        for count, img in enumerate(imgs):
                print('[SCANNING IMAGE]', count)
                img['kp'], img['des'] = sift.detectAndCompute(img['f'], None)
                
        return imgs


def similarity_check(imgs):
   
        duplicates = []
        count = 0

        for i1 in range(len(imgs)):
                print('[MATCHING PHOTOS]', count)
                
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
                count+=1        
                
        return duplicates

def delete(duplicates):
        for count, path in enumerate(duplicates):
                try:
                        os.remove(path)
                        print('[DELETED]', count)
                except:
                        continue

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
        parser.add_argument("-min", '--min_matches', type=int,
                help="minimum number of matching features to accept the images as being similar")
        parser.add_argument("-f", '--features_distance', type=float,
                help="[0,1] - higher number results in more matching features but with less accuracy")
        parser.add_argument("-max", '--max_keypoints', type=int,
                help="max keypoints to mark on each photo when scanning for similarity")
        args = parser.parse_args()

        if(args.silent):
                sys.stdout = open(os.devnull, 'a')
        if(args.min_matches):
                MIN_MATCHES = args.min_matches
        if(args.features_distance):
                FEATURES_DISTANCE = args.features_distance
        if(args.max_keypoints):
                MAX_KEYPOINTS = args.max_keypoints

        return args


def main():
    
        start_time = time.time()
        
        args = argparser()
        imgs = collect_imgs(args.directory)
        imgs = resize_images(imgs)
        imgs = detect_features(imgs)
        duplicates = similarity_check(imgs)
      
        if args.delete:
                delete(duplicates)
                
        print("--- %.8s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":

    main()
