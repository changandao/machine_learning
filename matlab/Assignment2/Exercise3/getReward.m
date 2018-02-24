function rew = getReward()
% get the Reward Matrix
rew = zeros(16,4);
f = 5; % reward for forward
b = -5; % penal for backward
a = -5; % penal for raising one leg while the other is already in the air
g = -5; % penal for both foot maintain on the ground

rew(2:3,4) = b;
rew(14:15,4) = f;
rew(5,2) = b;
rew(9,2) = b;
rew(8,2) = f;
rew(12,2) = f;
rew(16,2) = f;
rew(16,4) = f;
rew(1,2) = b;
rew(1,4) = b;

rew(4,2) = g;
rew(4,4) = g;
rew(13,2) = g;
rew(13,4) = g;
rew(5,1) = a;
rew(8:9,1) = a;
rew(12,1) = a;
rew(2:3,3) = a;
rew(14:15,3) = a;

end