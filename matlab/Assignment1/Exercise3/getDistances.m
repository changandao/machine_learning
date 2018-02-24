function distances = getDistances(A,B)
d1 = sum(A.^2, 2);
d2 = sum(B.^2, 2);
d = -2 * A * B';
d = d + d1 + d2';
distances = sqrt(d);
end