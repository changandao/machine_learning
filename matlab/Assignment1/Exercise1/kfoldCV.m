function [error]=kfoldCV(X,Y,kfold)
[n,s] = size(Y);
[n,m] = size(X);

error = 0;
%%kfold
for k = 1:kfold
    Xtrain = X;
    Xtrain(1+(k-1)*n/kfold:k*n/kfold,:) = [];
    Xtest = X(1+(k-1)*n/kfold:k*n/kfold,:);
    
    Ytrain = Y;
    Ytrain(1+(k-1)*n/kfold:k*n/kfold,:) = [];
    Ytest = Y(1+(k-1)*n/kfold:k*n/kfold,:);
    
    kparameter =(Xtrain'*Xtrain)\Xtrain'*Ytrain;
    Ypredict = Xtest * kparameter;
    if s== 2
        error = error+sum(sqrt(sum((Ytest-Ypredict).^2,2)));
    else 
        error = error+sum(sum(abs(Ytest-Ypredict)));
    end
end
error = error/n;
end
