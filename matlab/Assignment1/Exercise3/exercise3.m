clear
close all
tic
origin = load('gesture_dataset.mat');
motion_data = origin.gesture_l;
initial_cluster_label = origin.init_cluster_l;
Exercise3_kmeans(motion_data, initial_cluster_label, 7);
Exercise3_nubs(motion_data, 7);

motion_data = origin.gesture_o;
initial_cluster_label = origin.init_cluster_o;
Exercise3_kmeans(motion_data, initial_cluster_label, 7);
Exercise3_nubs(motion_data, 7);

motion_data = origin.gesture_x;
initial_cluster_label = origin.init_cluster_x;
Exercise3_kmeans(motion_data, initial_cluster_label, 7);
Exercise3_nubs(motion_data, 7);
toc