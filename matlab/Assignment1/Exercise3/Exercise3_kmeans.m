function Exercise3_kmeans(motion_data, initial_cluster_label, K)
input = reshape(motion_data,600,3);

cluster_center = initial_cluster_label;%initialize the cluster 

count = 0;

J = 100;
TEMP = 0;
while J - TEMP >10^-3
    TEMP = J;
    clustertmp = cluster_center;
    count = count+1;
    d = getDistances(input, cluster_center);
    [M, I] = min(d, [], 2);
    for k = 1:K
        numofsamples = sum(I == k);
        cluster_center(k, :) = sum(input(I == k, :))/(numofsamples);
        dk = getDistances(input(I == k, :), cluster_center(k, :));
        J = J + sum(dk(:));
    end
    if cluster_center == clustertmp
        break
    end
    count;
end


color = ['b','k','r','g','m','y','c','b'];
figure 
hold on
for i = 1:K
    plot(input(I == i, 1), input(I == i, 2), 'o', 'Color', color(i))
    plot(cluster_center(i, 1),cluster_center(i, 2),'*','MarkerSize', 40, 'Color', color(i+1))
    
end

hold off
end

