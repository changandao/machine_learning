clear
close all
pi = load('pi.txt');
A = load('A.txt');
B = load('B.txt');
Test = load('Test.txt');
COUNT = 0;
gesture = zeros(1,10);
for sq = 1:10
    alpha = pi.* B(Test(1,sq),:);
    for t = 2:60
        alpha = (alpha*A).* B(Test(t,sq),:);
    end
    p = sum(alpha);
    if log(p)>-120
        gesture(sq) = 1;
        COUNT =COUNT+1;
    else
        gesture(sq) = 2;
    end
end
disp('the classificaiton result is: ')
disp(gesture)