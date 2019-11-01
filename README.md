# <img src="https://i.imgur.com/SUpMOAo.png" height=200/>


[![Documentation Status](https://img.shields.io/badge/docs-stable-brightgreen.svg)](http://htmlpreview.github.io/?https://github.com/magamig/duplicate_images_finder/blob/master/docs/main.html)
[![Maintainability](https://api.codeclimate.com/v1/badges/5610bfa34f6ce56a9052/maintainability)](https://codeclimate.com/github/magamig/duplicate_images_finder/maintainability)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmagamig%2Fduplicate_images_finder.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmagamig%2Fduplicate_images_finder?ref=badge_shield)

Find and delete duplicate images inside a directory.

## Running

```bash
> python main.py 'sample_images/'
[DUPLICATE FOUND] sample_images/road.jpg sample_images/road_duplicate.jpg
[DELETED] sample_images/road_duplicate.jpg
```
```bash
> python main.py -h
usage: main.py [-h] [-d] [-s] [--min_matches MIN_MATCHES]
               [--features_distance FEATURES_DISTANCE]
               directory

positional arguments:
  directory             directory with the images

optional arguments:
  -h, --help            show this help message and exit
  -d, --delete          delete the duplicate images found with smaller res
  -s, --silent          quiet execution without logging
  --min_matches MIN_MATCHES
                        minimum number of matching features to accept the
                        images as being similar
  --features_distance FEATURES_DISTANCE
                        [0,1] - higher number results in more matching
                        features but with less accuracy
```

##### Similar / Duplicate Images
![](example_duplicate.png)

##### Different Images
![](example_not_duplicate.png)


## Requirements

Before running this project you need to install its requirements.
```bash
> pip install -r requirements.txt
```

## Built With

* [Python](https://docs.python.org/3/) - Programming language
* [OpenCV](https://docs.opencv.org/) - Computer vision library

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## References

* D. G. Lowe, "Distinctive image features from scale-invariant keypoints", International Journal of Computer Vision, 60, 2 (2004), pp. 91-110. [[PDF](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf)]
* M. Muja and D. G. Lowe, "Scalable Nearest Neighbor Algorithms for High Dimensional Data", IEEE Transactions on Pattern Analysis and Machine Intelligence 36, 11 (2014), pp. 2227-2240. [[PDF](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf)]
