# Particle Tracking Velocimetry
[Particle Tracking Velocimetry](https://en.wikipedia.org/wiki/Particle_tracking_velocimetry) (PTV) is an experimental technique to calculate the trajectory of individual particles.

The procedure runs in two successive steps:
1. detect the particles on every single frame.
2. link the particles from each frame to the next one.

Different algorithms and options are available for each step, depending on the experimental conditions and parameters. Open source tools are available online:
- [ImageJ](https://fiji.sc/) provides a basic Manual Tracking tool (Plugins/Tracking/Manual Tracking)
- [TrackMate](https://imagej.net/TrackMate), also in ImageJ, is a more elaborate, semi-automated tracking plugin (Plugins/Tracking/TrackMate)
- In [Python](https://www.anaconda.com/), researchers have developed [trackpy](soft-matter.github.io/trackpy/), a package to automate particle tracking, though not as user friendly as ImageJ.

## Lab assignment
Obtain the video of a single rising bubble.
Extract the location of the bubble at every timestep, and plot the trajectory, as well as the vertical and horizontal coordinates vs time.
Measure the oscillation period and wavelength of the bubble as it rises, and its terminal velocity.

Obtain a video with at least 2 distinct rising bubbles, and answer the same questions.
