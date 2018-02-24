function Gauss = getGauss(X,mu,sigma,pi)
posterior = mvnpdf(X, mu,sigma);
Gauss = pi * posterior;
end