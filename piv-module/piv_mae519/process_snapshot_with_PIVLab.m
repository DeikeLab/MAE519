function [x,y,u,v,typevector] = process_snapshot_with_PIVLab(filepath1,filepath2,n_passes,area1,step1,area2,area3,area4)

% need to have an output variable for some reason?
%none_var = 0;

% read in the A and B frames--can't be passed directly from Python, so we
% pass the filepaths to their text files instead
image1 = imread(filepath1);
image2 = imread(filepath2);

% FROM STEPHANE'S TREATPIV.M

% Standard PIV Settings
s = cell(10,2); % To make it more readable, let's create a "settings table"
%Parameter                       %Setting           %Options
s{1,1}= 'Int. area 1';           s{1,2}=area1;         % window size of first pass
s{2,1}= 'Step size 1';           s{2,2}=step1;         % step of first pass
s{3,1}= 'Subpix. finder';        s{3,2}=2;          % 1 = 3point Gauss, 2 = 2D Gauss
s{4,1}= 'Mask';                  s{4,2}=[];         % If needed, generate via: imagesc(image); [temp,Mask{1,1},Mask{1,2}]=roipoly;
s{5,1}= 'ROI';                   s{5,2}=[];         % Region of interest: [x,y,width,height] in pixels, may be left empty
s{6,1}= 'Nr. of passes';         s{6,2}=n_passes;          % 1-4 nr. of passes
s{7,1}= 'Int. area 2';           s{7,2}=area2;         % second pass window size
s{8,1}= 'Int. area 3';           s{8,2}=area3;         % third pass window size
s{9,1}= 'Int. area 4';           s{9,2}=area4;         % fourth pass window size
s{10,1}='Window deformation';    s{10,2}='spline'; % '*spline' is more accurate, but slower

roirect = [];
clahe = 1;
clahesize = double(area1);
highp = 1;
highpsize = 15;
intenscap = 0;
wienerwurst = 0;
wienerwurstsize = 3;
minintens = 0;
maxintens = 1;
image1 = PIVlab_preproc(image1,roirect,clahe, clahesize,highp,highpsize,intenscap,wienerwurst,wienerwurstsize,minintens,maxintens); %preprocess images
image2 = PIVlab_preproc(image2,roirect,clahe, clahesize,highp,highpsize,intenscap,wienerwurst,wienerwurstsize,minintens,maxintens); %preprocess images

[x,y,u,v,typevector] = piv_FFTmulti (double(image1),double(image2),s{1,2},s{2,2},s{3,2},s{4,2},s{5,2},s{6,2},s{7,2},s{8,2},s{9,2},s{10,2},0,0,0); % last three 0s are for repeat, mask_auto,and do_pad