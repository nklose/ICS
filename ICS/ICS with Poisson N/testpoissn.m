%
% 
% 
% 
%



clear all
close all

lambda = input('Enter the value of lambda for Poisson distribution    ');
numpoints = input('Enter the number of points for Poisson distribution     ');



ff = poissrnd (lambda, numpoints, 1);

ff = sort (reshape(ff, 1, [])); % put all values in ascending order


len = length (ff);

m = 1;
n = 1;
count = 1;

Int(n, 1) = ff(m, 1);
Int(n, 2) = count;

while m < len
    
    if ff(m) == ff(m+1)
        
        count = count + 1;
        Int(n, 2) = count;
        m = m+1;
        
    else
        
        n = n+1;
        m = m+1;
        count = 1;
        Int(n, 1) = ff(m);
        Int(n, 2) = count;
        
    end
    
end


figure;  plot (Int(:, 1), Int(:, 2), 'o');

