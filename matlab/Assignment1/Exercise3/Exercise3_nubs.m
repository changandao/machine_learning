function Exercise3_nubs(motion_data, K)
input = reshape(motion_data,600,3);
v = [0.08,0.05,0.02];

cluster_center = zeros(K,3);
cluster_center(1, :) = sum(input)/length(input');
d = getDistances(input, cluster_center(1, :));
[~,I] = min(d,[],2);
J = sum(d);
k=0;
while 1
    k = k+1;
    [~,Imax] = max(J);
    cluster_center(Imax,:) = cluster_center(Imax,:) + v;
    cluster_center(k+1,:)  = cluster_center(Imax,:) - v;
    indmax = find(I == Imax);
    dk = getDistances(input(indmax,:), cluster_center([Imax,k+1],:));
    [~,newI] = min(dk, [], 2);
    I(indmax(newI == 1)) = Imax;
    I(indmax(newI == 2)) = k+1;
    nnew1 = sum(newI == 1);
    nnew2 = sum(newI == 2);
    cluster_center(Imax,:) = sum(input(I == Imax, :))/nnew1;
    cluster_center(k+1,:) = sum(input(I == k+1, :))/nnew2;
    newd1 = getDistances(input(I == Imax, :), cluster_center(Imax,:));
    newd2 = getDistances(input(I == k+1, :), cluster_center(k+1,:));
    newJ1 = sum(newd1);
    newJ2 = sum(newd2);
    J(Imax) = newJ1;
    J(k+1) = newJ2; 
    
    if k == 6
        break
    end
end


color = ['b','k','r','g','m','y','c','b'];
figure 
hold on
for j = 1:K
    plot(input(I == j, 1), input(I == j, 2), 'o', 'Color', color(j))
    plot(cluster_center(j, 1), cluster_center(j, 2),'*','MarkerSize', 40, 'Color', color(j+1))
end
end