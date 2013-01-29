function [Crosscorrelationout] = Crosscorrelation(CrossG, delta);


    dimension = size (delta);

    for a = 1:dimension(1,2)
        
        for b = 1:dimension(1,2)
            
                                
                    gmn(a, b) = CrossG(1)*exp((-(delta(1, a)^2+delta(2, b)^2))/(CrossG(2)^2)) + CrossG(3);
                    
                    
            
        end
        
    end
    



Crosscorrelationout = gmn;