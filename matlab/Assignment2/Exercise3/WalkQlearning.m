function WalkQlearning(s)
epsilon = 0.05;
gamma = 0.9;
alpha = 0.6;

Q = zeros(16,4);
state = s;
T = 10000;

flag = 1;% flag = 1: epsilon greedy
         % flag = 2: pure greedy
for t = 1:T
    oldQ = Q;
    % epsilon greedy policy
    if flag == 1
        probability = rand();
        if probability > 1-epsilon
            [~,action] = max(Q(state,:));
        else
            action = randi(4);
        end
    % pure greedy policy
    elseif flag == 2
        [~,action] = max(Q(state,:));
    end
    
    % update Q
    [newstate, reward] = SimulateRobot(state,action);
    Q(state,action) = Q(state,action) + alpha*(reward + gamma*max(Q(newstate,:))-Q(state,action));
    state = newstate;
    temptq = sum(sum(abs(Q-oldQ)));
    
    % convergence conditions
    if  temptq < 1*10^(-5) && temptq > 1*10^(-6)
        
        break
    end
    
end
[~,pi] = max(Q,[],2);% get the optimal policy

T = 16;
states = zeros(1,T);
states(1) = s;
[~,pi(s)] = max(Q(s,:));
delta = getdelta();
for i = 2:16
    states(i) = delta(states(i-1),pi(states(i-1)));
end
disp('the steps to get the optimal policy is: ')
disp(t)
disp('the sequence of  states is: ')
disp(states)
walkshow(states);

end