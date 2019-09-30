# Particle Image Velocimetry (PIV)

[Particle image velocimetry](https://en.wikipedia.org/wiki/Particle_image_velocimetry) (PIV) is a experimental technique to calculate velocity fields based on the correlation between back-to-back images of particles in the flow.

In this module we'll use two open-source PIV packages, [OpenPIV-python](http://www.openpiv.net/openpiv-python/) in Python and [PIVLab](https://pivlab.blogspot.com/) in Matlab, to analyze a turbulent water jet. Make sure you have the following set up:

 - [Matlab](https://princeton.service-now.com/snap?id=kb_article&sys_id=cfaf4e73db601b00249b7b6b8c96199b), and I'd recommend getting the Parallel Computing Toolbox as well
 - [PIVLab 2.20](https://www.mathworks.com/matlabcentral/fileexchange/27659-pivlab-particle-image-velocimetry-piv-tool), a Matlab toolbox for PIV
 - Python 3, and I'd recommend the [Anaconda distribution](https://www.anaconda.com/distribution/)
 - [OpenPIV](http://www.openpiv.net/openpiv-python/), a Python package for PIV
 - This repository, and either install it as a package, or in Spyder (Anaconda), add it to the PYTHONPATH manager so you can `import mae519_piv`

## Getting a single flowfield snapshot

The end goal of the lab is to get a time-resolved 2-D flowfield--that is, a measure of the horizontal and vertical components of velocity over many times and locations in the flow. First we'll work with a single "snapshot" of the flowfield at one point in time, calculated with back-to-back images of the particles.

### With PIVLab

First we'll use the graphical user interface in PIVLab to compute a single "snapshot". The GUI can be launched by going to Apps -> PIVLab in Matlab once the PIVLab toolbox is installed.

Use the "Load Images" button to import the two frames in the [`/data/`](https://github.com/DeikeLab/MAE519/tree/master/PIV/data) folder in this repository. Image pre-processing can be controlled under Image settings -> Image pre-processing, and the PIV parameters (the size of the interrogation windows) can be controlled under Analysis -> PIV Settings. Once the analysis is run, velocity vectors will be superimposed on the particle image in the GUI, and they can be filtered or exported to the Matlab workspace or the disk.

### With OpenPIV

There's no GUI in OpenPIV, but the script [`process_snapshot_openpiv.py`](https://github.com/DeikeLab/MAE519/blob/master/PIV/scripts/process_snapshot_openpiv.py) walks through the process of calculating a velocity field with OpenPIV.

## Getting a time-resolved flowfield

Getting a time-resolved flowfield boils down to writing a loop that performs the single-snapshot calculation for each combination of "a" and "b" frames.

### With OpenPIV

To do this with OpenPIV, try taking code from [`process_snapshot_openpiv.py`](https://github.com/DeikeLab/MAE519/tree/master/PIV/scripts/process_snapshot_openpiv.py) to write a script that performs this loop. You'll need to make an array of "a" frames, which can be done using the `numpy.arange` function. For example, if you wanted the "a" frames of your velocity field snapshots to be [0,2,4,...98], you could use `np.arange(0,99,2)`.

Each velocity field snapshot involves two 2-D arrays of velocity values `u` and `v` for the two components of the velocity. If your PIV field of view has `nx` columns and `ny` rows of windows, the `shape` of `u` and `v` will each be `(ny,nx)`. It can be more convenient to have a *single* array for the velocity field which contains both components of velocity. We can call this array `snapshot`, and it will have 3 dimensions (vertical and horizontal position, as well as the component of the flow). This can be created with `snapshot=np.array([u,v])`, which has shape `(2,ny,nx)`. It might be more convenient to have the velocity component as the final axis, which can be done with `snapshot=np.moveaxis(snapshot,0,-1)`, which moves the first axis of the array to the end. We can get the two components of velocity with `u=snapshot[:,:,0]` and `v=snapshot[:,:,1]`.

Once we start considering snapshots at multiple times, it's convenient to have all the velocity data in a single 4-D array, where the first axis now indexes the time at which the snapshot is taken. In writing your loop to process all the velocity fields, try to have the final result be an array `ff` (for flowfield) where `ff[i,j,k,0]` and `ff[i,j,k,1]` will return the u- and v-components, respectively, of velocity at the position corresponding to the j-th row and k-th column in the PIV field at the i-th time.

### With PIVLab

To work with the output from PIVLab in Python, use the script [create_PIVLab_params_in_python.py](https://github.com/DeikeLab/MAE519/tree/master/PIV/scripts/create_PIVLab_params_in_python.py) to create a `.mat` file that contains the desired PIVLab parameters. Then run the Matlab script [run_pivlab_tiffImages.m](https://github.com/DeikeLab/MAE519/tree/master/PIV/piv_mae519/run_pivlab_tiffImages.m), which will use PIVLab to compute the snapshots at the desired points in time, saving the results in `..._u.txt` and `..._v.txt` files for each snapshot. Finally, the script [read_PIVLab_results_into_python.py](https://github.com/DeikeLab/MAE519/tree/master/PIV/scripts/read_PIVLab_results_into_python.py) can be run in Python to read in these `.txt` files and create a single 4-D array `ff` with all the velocity field data.

## Lab assignment

Obtain two PIV videos of the turbulent jet, one giving a large-scale view of the jet structure and one giving a zoomed-in view. Before taking the data, determine a good amount of seeding particles and camera frame rate to use.

After getting comfortable processing a single PIV snapshot with both PIVLab and OpenPIV (as described above), choose one of the two movies to analyze using both packages. With each result, characterize the jet in a few figures, showing quantities such as the time-averaged flowfield or the distribution of velocities measured. How do the results compare between the two packages? Why do the results differ?

Then, pick one of the two packages with which to analyze the other PIV movie (with the different field of view). Try analyzing the results with a few combinations of PIV processing parameters, such as changing the window size or number of movie frames separating "a" and "b" images. How do these parameters affect the results? Determine which set of parameters you think will give the best results. Plot the velocity at a single location in the flow over time. Does it look well-resolved?

Finally, do a comparison of results from the overlapping region of the two views you obtained. How do quantities like the mean flow and velocity distributions compare between the two views?

The takeaway from this exercise should be that PIV is a powerful tool to measure fluid flows, but the choice of experimental and processing parameters isn't trivial and can affect results.
