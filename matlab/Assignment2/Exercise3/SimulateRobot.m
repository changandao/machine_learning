function [newstate, reward] = SimulateRobot(state, action)

rew = getReward(); 
delta = getdelta();

newstate = delta(state, action);
reward = rew(state, action);

end 