function par=Exercise1(k)
tic
% Data is a struct contianing the input and the output
Data = load('Data.mat'); 

input = Data.Input;
output = Data.Output;%output contains the x,y and theta;

[m,n] = size(output); %n is the numbers of samples;

position = output(1:2,:)';
orientation = output(3,:)';

v = input(1,:)';
w = input(2,:)';
X = ones(n,1);

%predicting x,y
perror = [];
aerror = [];
for p1 = 1:6
    tmp = [v.^p1, w.^p1, (v.*w).^p1];
    X = [X,tmp];
    [poserror] = kfoldCV(X,position, k);
    [angerror] = kfoldCV(X,orientation, k);
    perror = [perror poserror];
    aerror = [aerror angerror];
end
[~, optimalp1] = min(perror);
optimalp1
[~, optimalp2] = min(aerror);
optimalp2
% for position estimation
par12 = getparameter(v,w,optimalp1,position);

% for orientation estimation
par3 = getparameter(v,w,optimalp2,orientation);

% save all parameters into cell
par = {par12(:,1),par12(:,2),par3};
toc
end