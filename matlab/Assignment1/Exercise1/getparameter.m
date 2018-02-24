function par = getparameter(v,w,p,y)
n = size(y,1);
X = ones(n,1);
for p1 = 1:p
    tmp = [v.^p1, w.^p1, (v.*w).^p1];
    X = [X,tmp];
end
par = (X'*X)\X'*y;
end