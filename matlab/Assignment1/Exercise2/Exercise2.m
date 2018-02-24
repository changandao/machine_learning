function [optimald, optimalerror, Cmatrix] = Exercise2(dmax)
tic
dmax = 60;

images = loadMNISTImages('train-images.idx3-ubyte');
labels = loadMNISTLabels('train-labels.idx1-ubyte');
test_images = loadMNISTImages('t10k-images.idx3-ubyte');
test_labels = loadMNISTLabels('t10k-labels.idx1-ubyte');

images_mean = mean(images,2);
images_reduced = images-images_mean;
images_reduced_cov = cov(images_reduced');
test_images_reduced = test_images - images_mean;
Lt = length(test_images);

[V,~] = eig(images_reduced_cov);
D = eig(images_reduced_cov);
[~,ID] = sort(D,'descend');
V = V(:,ID);

predictedlables = zeros(Lt, dmax);
errors = zeros(dmax,1);
for d = 1:dmax
    d
    projected_images = V(:,1:d)'*images_reduced;
    projected_test_images = V(:,1:d)'*test_images_reduced;
    
    liklihoods = zeros(Lt,10);
    
    for i = 0:9
        subimage = projected_images(:,labels == i);
        submean = mean(subimage,2);
        sigma = cov(subimage');
        liklihoods(:,i+1) = mvnpdf(projected_test_images', submean', sigma);
    end
    [M,I] = max(liklihoods,[],2);
    predictedlables(:,d) = I-1;
    errors(d) = sum(predictedlables(:,d) ~= test_labels)/length(test_images);
end
figure
plot(1:60, errors)
[optimalerror, optimald] = min(errors);
lab = predictedlables(:, optimald);
[Cmatrix, order] = confusionmat(test_labels(:), lab(:))
toc
end