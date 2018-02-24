function WalkPolicyIteration(s)

delta = getdelta();
rew = getReward();
%% leaning process
policy = ceil(rand(16,1)*4);
gamma = 0.9;
count = 0;
V = zeros(16,1);

while 1
    oldV = V;
    count = count + 1;
    oldpi = policy;
    A = eye(16);
    b = zeros(16,1);
    
    % caculate V
    for i =1:16
        b(i) = rew(i,policy(i));
        A(i,delta(i,policy(i))) = A(i,delta(i,policy(i))) - gamma;
    end
    V = pinv(A)*b;
   
    % Policy optimaization
    for i = 1:16
        all_V = V(delta(i,:));
        tempt = rew(i,:) + gamma * all_V';
        [~,policy(i)] = max(tempt);
    end
    % convergence conditions
    TEMPV = (V-oldV); 
    if sum(abs(policy - oldpi)) <0.0000001 || sum(abs(TEMPV))<0.0000001
        break;
    end
end
% policy_star is the optimal policy
policy_star = policy;
%% test
T = 16; 
states = zeros(1,T);
states(1) = s;
for t = 2:T
    action = policy_star(states(t-1));
    states(t) = delta(states(t-1),action);
    test = delta(states(t-1),action);
end
disp('the number of iterations to convergence is: ')
disp(count)
disp('the sequence of  states is: ')
disp(states)
walkshow(states);
end