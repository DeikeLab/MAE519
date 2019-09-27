# Pendant Drop: Feature Detection
A static drop, hanging from the tip of a needle, is shaped by gravity in a completely determined way.
Its profile obeys an ordinary non-linear differential equation [1], and given gravity value and liquid bulk properties the only remaining parameter is the liquid-air interfacial tension.
This measurement of surface tension needs the detection and extraction of the drop profile, which is processed in a later stage.
This module is a practical exemple of feature detection, an active and current field of investigation in vision research.

Two (at least) open source tools are available and of easy setup:
- the user-friendly [ImageJ](https://fiji.sc/) features many interactive image processing functions, from the most basic thresholding to contour and [ridge detection](https://imagej.net/Ridge_Detection) (Plugins/Ridge Detection). 
- the image processing libray [scikit-image](https://scikit-image.org/) (Skimage) is a project under active development. Written in [Python](https://www.python.org/), scripting and batch processing is easier than ImageJ, though less intuitive and user friendly. At a basic level, images are represented as 2D arrays/matrices of (generally) 8 bytes integers: each pixel (= row-column intersection) can take on 256 different values.

## Lab assignment
Adjust the experimental workbench to acquire a "good" picture of a pendant drop.
Run [`opendrop.py`](https://sites.google.com/site/opencolloids/) from [Spyder](https://www.spyder-ide.org/) to obtain the value of surface tension.

Open the image in ImageJ and extract the drop profile.
Following the method of the selected planes [2], measure the diameters at equator and in the selected plane, and then calculate the liquid surface tension.

Open the image within Spyder, extract the drop profile and measure the surface tension from the same method.

Plot the profiles from the last 2 methods on top of the drop picture.
Compare the 3 methods.

## References
[1][ Berry, J. D. et al. 2015](https://doi.org/10.1016/j.jcis.2015.05.012) “Measurement of Surface and Interfacial Tension Using Pendant Drop Tensiometry.” J. Coll. Interface Sci. 454, p. 226–37 [pdf](refs/Berry2015.pdf)

[2][ Misak, M. D. 1968](http://dx.doi.org/10.1016/0021-9797(68)90020-9) “Equations for Determining 1/H versus S Values in Computer Calculations of Interfacial Tension by the Pendent Drop Method.” Journal Coll. Interface Sci. 27 (1), p. 141–142 [pdf](refs/Misak1968.pdf)
