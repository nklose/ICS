function r = poissrnd(lambda,m,n)
%POISSRND Random matrices from Poisson distribution.
%   R = POISSRND(LAMBDA) returns a matrix of random numbers chosen   
%   from the Poisson distribution with parameter LAMBDA.
%
%   The size of R is the size of LAMBDA. Alternatively, 
%   R = POISSRND(LAMBDA,M,N) returns an M by N matrix. 
%
%   POISSRND uses a waiting time method for small values of LAMBDA,
%   and the method of Ahrens and Dieter for larger values of LAMBDA.

%   References:
%      [1]  L. Devroye, "Non-Uniform Random Variate Generation", 
%      Springer-Verlag, 1986 page 504.

%   Copyright 1993-2002 The MathWorks, Inc. 
%   $Revision: 2.12 $  $Date: 2002/03/31 22:26:56 $

if nargin == 1
    [errorcode rows columns] = rndcheck(1,1,lambda);
elseif nargin == 2
    [errorcode rows columns] = rndcheck(2,1,lambda,m);
elseif nargin == 3
    [errorcode rows columns] = rndcheck(3,1,lambda,m,n);
else
    error('Requires at least one input argument.'); 
end

if errorcode > 0
    error('Size information is inconsistent.');
end

if (prod(size(lambda)) == 1)
    lambda = lambda(ones(rows*columns,1));
else
    lambda = lambda(:);
end

%Initialize r to zero.
r = zeros(rows, columns);

j = (1:(rows*columns))';   % indices remaining to generate

% For large lambda, use the method of Ahrens and Dieter as
% described in Knuth, Volume 2, 1998 edition.
k = find(lambda >= 15);
if ~isempty(k)
   alpha = 7/8;
   lk = lambda(k);
   m = floor(alpha * lk);
   
   % Generate m waiting times, all at once
   x = gamrnd(m,1);
   t = x <= lk;
   
   % If we did not overshoot, then the number of additional times
   % has a Poisson distribution with a smaller mean.
   r(k(t)) = m(t) + poissrnd(lk(t)-x(t));
   
   % If we did overshoot, then the times up to m-1 are uniformly
   % distributed on the interval to x, so the count of times less
   % than lambda has a binomial distribution.
   r(k(~t)) = binornd(m(~t)-1, lk(~t)./x(~t));
   j(k) = [];
end

% For small lambda, generate and count waiting times.
p = zeros(length(j),1);
while ~isempty(j)
    p = p - log(rand(length(j),1));
    kc = [1:length(k)]';
    t = (p < lambda(j));
    j = j(t);
    p = p(t);
    r(j) = r(j) + 1;
end
    
% Return NaN if LAMBDA is negative.
r(lambda < 0) = NaN;
