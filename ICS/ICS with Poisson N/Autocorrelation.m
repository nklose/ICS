function [Autocorrelationout] = Autocorrelation(AutoG, delta);


    dimension = size (delta);

    for a = 1:dimension(1,2)
        
        for b = 1:dimension(1,2)
            
                                
                    gmn(a, b) = AutoG(1)*exp((-(delta(1, a)^2+delta(2, b)^2))/(AutoG(2)^2))+ AutoG(3);
                    
                    
            
        end
        
    end
    



Autocorrelationout = gmn;