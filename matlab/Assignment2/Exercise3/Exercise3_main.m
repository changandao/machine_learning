% main Excution function
clc
clear 
close all

% Policy Iteration
figure(1)
initstateP = 3;
WalkPolicyIteration(initstateP);

%Q Learning
figure(2)
initstateQ = 12;
WalkQlearning(initstateQ);
