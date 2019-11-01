# Duplicate Images Finder
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmagamig%2Fduplicate_images_finder.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fmagamig%2Fduplicate_images_finder?ref=badge_shield)


Find and delete duplicate images inside a directory.

## Running

```bash
> python main.py 'sample_images/'
[DUPLICATE FOUND] sample_images/road.jpg sample_images/road_duplicate.jpg
[DELETED] sample_images/road_duplicate.jpg
```

##### Similar / Duplicate Images
![](example_duplicate.png)

##### Different Images
![](example_not_duplicate.png)

## Built With

* [Python](https://docs.python.org/3/) - Programming language
* [OpenCV](https://docs.opencv.org/) - Computer vision library

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmagamig%2Fduplicate_images_finder.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fmagamig%2Fduplicate_images_finder?ref=badge_large)

## References

* D. G. Lowe, "Distinctive image features from scale-invariant keypoints", International Journal of Computer Vision, 60, 2 (2004), pp. 91-110. [[PDF](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf)]
* M. Muja and D. G. Lowe, "Scalable Nearest Neighbor Algorithms for High Dimensional Data", IEEE Transactions on Pattern Analysis and Machine Intelligence 36, 11 (2014), pp. 2227-2240. [[PDF](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_pami2014.pdf)]