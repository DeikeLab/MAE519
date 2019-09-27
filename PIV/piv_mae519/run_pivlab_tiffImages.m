%{
Use this script to perform the PIV calculation with PIVLab for an entire
PIV movie. Give it the location of a .mat file created with the Python
function piv_mae519.interface_PIVLab_with_python.create_dict_and_mat, and
it will import the PIV parameters.

Data will be saved as separate "..._u.txt" and "..._v.txt" files for each 
PIV snapshot. They can be read into Python with the function
piv_mae519.interface_PIVLab_with_python.reconstruct_from_Matlab.
%}

%% User input

% Where the data is
folder = 'D:\data_MILES_D\190923_PIV_mae519\piv_pump8V_fps4100_exposure190_dx49um_particleMass6g\\\\';
casename = 'piv_pump8V_fps4100_exposure190_dx49um_particleMass6g';

%% End user input

% load parameter file, which is created by Python
parameter_filepath = [folder,casename,'_matlabParams.mat'];
load(parameter_filepath)

% get a vector of the "a" frame for each snapshot
a_frames = start_frame:a_frame_skip:end_frame-1; % -1 so it's like np.arange

%% Main loop

fprintf('starting the loop')
% if the parallelization doesn't work, replace "parfor" with "for"
parfor ai = 1:length(a_frames)
    
    % get which a frame is being worked on in this iteration of the loop
    a = a_frames(ai);
    disp(a);
    
    % get the start of the filepath to the a and b images
    res_filepath_start = [folder,casename_start,num2str(a,'%06.f')];

    % get the filepaths to the two images
    fpath_a = [folder,casename,'_',num2str(a,'%06.f'),'.tif'];
    fpath_b = [folder,casename,'_',num2str(a+frame_diff,'%06.f'),'.tif'];

    % call the function which uses PIVLab to do the PIV computation
    [x,y,u,v,typevector] = process_snapshot_with_PIVLab(fpath_a,fpath_b,double(n_passes),double(area1),double(step1),double(area2),double(area3),double(area4));

    % save the u and v components of the velocity to separate .txt files
    dlmwrite([res_filepath_start,'_u.txt'],u);
    dlmwrite([res_filepath_start,'_v.txt'],v);
end