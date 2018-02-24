loading = load('dataGMM.mat');
X = loading.Data;
idx = kmeans(X', 4);

[p,n] = size(X);

pi = zeros(1,4);
mu = zeros(2,4);
sigma = zeros(2,2,4);

% initializing the parameters
for i = 1:4
    pi(i) = sum(idx == i);
    mu(:,i) = mean(X(:,idx == i),2);
    tempt = X(:,idx == i) - mu(:,i) *ones(1,pi(i));
    sigma(:,:,i) = tempt*tempt'/pi(i);
end
X = X';
mu = mu';
p = zeros(n,4);
Gauss = zeros(n,4);
count = 0;

Loss = 100;
preLoss = 0;
% E-M loops
while (abs((Loss-preLoss)/Loss)>0.0000001)
    preLoss = Loss;
    count = count + 1;
    oldmu = mu;
    oldsigma = sigma;
    oldpi = pi;
    for k = 1:4
    Gauss(:,k) = getGauss(X, mu(k,:), sigma(:,:,k), pi(k));
    end
    for k = 1:4
        % E step
        p(:,k) = Gauss(:,k) ./ sum(Gauss,2); 
        % M step
        nk = sum(p(:,k));
        mu(k,:) = p(:,k)'*X/nk;
        sigma(:,:,k) = zeros(2,2);
        centerX = (X - ones(n,1) * mu(k,:));
        for i = 1:300
            sigma(:,:,k) = sigma(:,:,k) + p(i,k)*centerX(i,:)'*centerX(i,:);
        end
        sigma(:,:,k) = sigma(:,:,k)/nk;
        pi(k) = nk/n;
    end
    Loss = sum(log(sum(Gauss,2)));
end
disp('the number of iterations to convergence is: ')
disp(count)