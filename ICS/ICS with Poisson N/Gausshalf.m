function [Gaussout] = Gausshalf(G, N);


% Function calculates Gaussian distribution in one dimension according to
% the formula
% Gauss = G0 * exp[-(x-delta)^2/2 x w^2];
% N is a number of points in the distribution along axis x
% N must be odd


a = length(N);

for i = 1:a
    
    Gaussout(i) = (G(1)*exp ((-N(i)^2)/(G(2)^2)))+G(3);
    
end

Gaussout = Gaussout';