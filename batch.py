from __future__ import division
import numpy as np
import scipy.misc
import scipy.optimize

import os
import sys
import warnings
warnings.simplefilter('ignore',np.ComplexWarning)

import ctypes
from ctypes import c_int
from ctypes import c_void_p

def gauss_1d(x,g0,g1,g2):
    return g0*np.exp(-(x**2)/(g1**2))+g2

def gauss_2d(x,g0,g1,g2):
    g1_sq = g1**2
    dim = int(np.sqrt(np.size(x)))
    return g0*np.exp((-((x//dim)**2+(x%dim)**2))/g1_sq)+g2

def call_core(lib,idata,isr,isg,isb,iside,ilim):
    lib.core(idata,isr,isg,isb,iside,ilim)
    
def call_execute(lib):
    lib.execute()

class DefaultConfig:
    side = 128
    input_directory = 'input/'
    output_directory = 'output/'
    name_min = 1
    name_max = 1
    name_format = '{:s}_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    dual_initial = np.array([1,10,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 32
    input_type = 'mixed'
    output_type = 'summary'

class SplitConfig:
    side = 128
    input_directory = 'input/'
    output_directory = 'output/'
    name_min = 1
    name_max = 1
    name_format = '{:s}_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    dual_initial = np.array([1,10,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 32
    input_type = 'split'
    output_type = 'summary'

class BadConfig:
    side = 512
    input_directory = 'accTests/inputs/badData/'
    output_directory = 'output/'
    name_min = 1
    name_max = 10
    name_format = '{:s}_{:03d}.bmp'
    dual_range = 20
    triple_range = 15
    dual_initial = np.array([1,10,0],dtype=np.float)
    triple_initial = np.array([50,2,0],dtype=np.float)
    triple_lim = 64
    input_type = 'split'
    output_type = 'summary'

def run():
    
    # setup the c library
    lib_dir = os.path.dirname(os.path.realpath(__file__))
    lib_path = os.path.join(lib_dir,'libbatch.so')
    lib = ctypes.cdll.LoadLibrary(lib_path)
    lib.core.argtypes = [c_void_p,c_void_p,c_void_p,c_void_p,c_int,c_int]
    lib.init.argtypes = [c_int,c_void_p]
    lib.execute.argtypes = []
    lib.destroy.argtypes = []
    
    # setup the configurations to use
    config = DefaultConfig()
    if not os.path.exists(config.output_directory):
        os.makedirs(config.output_directory)
    
    # declare python variables
    side = config.side
    image_split = np.empty((side,side), dtype=np.uint8)
    image_mixed = np.empty((side,side,3), dtype=np.uint8)
    image = np.empty((3,side,side))
    
    avg = np.empty(3)
    fft = np.empty((3,side,side), dtype=np.complex)
    conj_fft = np.empty((3,side,side), dtype=np.complex)
    dual_combinations = [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
    
    lim = config.triple_lim
    shifted = np.empty((3,side,side), dtype=np.complex)
    part_rgb = np.empty((6,lim,lim))
    
    # align data_rgb to 16-byte boundary
    nbytes = lim**4*16
    raw_data_rgb = np.empty(nbytes+16,dtype=np.uint8)
    start_idx = -raw_data_rgb.ctypes.data % 16
    data_rgb = raw_data_rgb[start_idx:start_idx+nbytes]\
        .view(dtype=np.complex).reshape(lim,lim,lim,lim)
    
    grid = np.ogrid[:lim,:lim]
    flip = 1-2*((grid[0]+grid[1])%2==1)
    
    dual_xdata = np.arange(config.dual_range**2)
    triple_xdata = np.arange(config.triple_range)
    
    # align dual_tmp to 16-byte boundary
    nbytes = side**2*16
    raw_dual_tmp = np.empty(nbytes+16,dtype=np.uint8)
    start_idx = -raw_dual_tmp.ctypes.data % 16
    dual_tmp = raw_dual_tmp[start_idx:start_idx+nbytes]\
        .view(dtype=np.complex).reshape(side,side)
    
    # store output results for dual correlations
    dual_out = np.empty((6,config.dual_range,config.dual_range))
    dual_cov = np.empty((6,3,3))
    dual_par = np.empty((6,3))
    
    # store output results for triple correlations
    triple_out = np.empty(config.triple_range)
    triple_cov = np.empty((3,3))
    triple_par = np.empty(3)
    
    name_min = config.name_min
    num_files = config.name_max-config.name_min+1
    
    # store summary results
    results = np.empty((num_files,32))
    
    # prepare arguments to pass to c code
    ilim = c_int(lim)
    iside = c_int(side)
    isr = shifted[0,:,:].ctypes.data_as(c_void_p)
    isg = shifted[1,:,:].ctypes.data_as(c_void_p)
    isb = shifted[2,:,:].ctypes.data_as(c_void_p)
    idata = data_rgb.ctypes.data_as(c_void_p);
    
    # initialize the c library
    lib.init(ilim,idata)
    
    for fnum in range(num_files):
        
        print str.format('Processing {:3d} of {:3d} ...', fnum+1, num_files)
        
        # read mixed input
        if config.input_type == 'mixed':
            fname = str.format(config.name_format,'rgb',name_min+fnum)
            fpath = config.input_directory + fname
            image_mixed = scipy.misc.imread(fpath)
            for i in range(3):
                image[i,:,:] = image_mixed[:,:,i].astype('d')
        # read split input
        elif config.input_type == 'split':
            for i in range(3):
                fname = str.format(config.name_format,'rgb'[i],name_min+fnum)
                fpath = config.input_directory + fname
                image_split = scipy.misc.imread(fpath)
                image[i,:,:] = image_split.astype('d')
        
        # perform some preprocessing
        for i in range(3):
            avg[i] = np.average(image[i,:,:])
            fft[i,:,:] = np.fft.fft2(image[i,:,:])
            conj_fft[i,:,:] = np.conj(fft[i,:,:])
        
        # perform dual correlation
        for i, comb in enumerate(dual_combinations):
            rval = config.dual_range
            denom = avg[comb[0]]*avg[comb[1]]*side**2
            dual_tmp = np.fft.ifft2(fft[comb[0],:,:]*conj_fft[comb[1],:,:])
            dual_out[i,:,:] = np.float64(dual_tmp[0:rval,0:rval])/denom - 1
            first_entry = dual_out[i,0,0]
            dual_out[i,0,0] = dual_out[i,0,1]
            (dual_par[i,:] ,dual_cov[i,:,:]) = \
                scipy.optimize.curve_fit(gauss_2d, dual_xdata,
                np.reshape(dual_out[i,:,:],rval**2),
                config.dual_initial)
            dual_par[i,1] = abs(dual_par[i,1])
            dual_out[i,0,0] = first_entry
        
        # perform triple correlation
        for i in range(3):
            shifted[i,:,:] = np.fft.fft2(image[i,:,:]-avg[i])
            shifted[i,:,:] = np.fft.fftshift(shifted[i,:,:])
        shifted[2,:,:] = np.conj(shifted[2,:,:])/(side**2)
        
        # call c functions
        call_core(lib,idata,isr,isg,isb,iside,ilim)
        call_execute(lib)
        
        # the line below uses the built-in function rather than fftw
        # if using this, multiply part_rgb by lim**4 later
        # data_rgb = np.fft.ifftn(data_rgb)
        
        part_rgb[0,:,:] = np.float64(data_rgb[:,:,0,0])
        part_rgb[1,:,:] = np.float64(data_rgb[0,:,:,0])
        part_rgb[2,:,:] = np.float64(data_rgb[0,0,:,:])
        part_rgb[3,:,:] = np.float64(data_rgb[0,:,0,:])
        part_rgb[4,:,:] = np.float64(data_rgb[:,0,:,0])
        part_rgb[5,:,:] = np.float64(data_rgb[:,0,0,:])
        part_rgb *= flip/(side**4*np.prod(avg))
        
        np.ndarray.fill(triple_out,0)
        for i in range(6):
            triple_out += part_rgb[i,0,0:config.triple_range]
            triple_out += part_rgb[i,0:config.triple_range,0]
        triple_out /= 12
        
        (triple_par[:], triple_cov[:,:]) = \
            scipy.optimize.curve_fit(gauss_1d,triple_xdata,
            triple_out, config.triple_initial)
        triple_par[1] = abs(triple_par[1])
        triple_par[1] = int(triple_par[1]*(side/lim)*10)/10
        
        # assign results for a single row
        results[fnum,0] = name_min+fnum
        results[fnum,1:4] = avg[:]/255
        for i in range(6):
            results[fnum,(i+1)*4:(i+2)*4-1] = dual_par[i,:]
            # add variance of dual below
            results[fnum,(i+2)*4-1] = np.float64(0)
        results[fnum,28:31] = triple_par[:]
        # add variance of triple below
        results[fnum,31] = np.float64(0)
        
        # perform output for a single image
        if config.output_type == 'summary': continue
        # add output type full

    # clean up the c library
    lib.destroy()
    
    # generate table header
    colors = '--r:--g:--b:-rg:-rb:-gb:rgb'.split(':')
    parameters = 'g(0):---w:ginf:-var'.split(':')
    temp_header_1 = ['']*28
    for i, color in enumerate(colors):
        for j, param in enumerate(parameters):
            temp_header_1[i*4+j] = str.format('|{}-{}-',color,param)
    scolors = '--r:--g:--b'.split(':')
    temp_header_2 = [str.format('|{}--avg-',color) for color in scolors]
    header = ' '*9 + ''.join(temp_header_2) + ''.join(temp_header_1)
    
    # output summary of results for the whole batch
    fpath = config.output_directory + 'results.txt'
    with open(fpath,'w') as f:
        f.write(header+'\n')
        np.savetxt(f,results,fmt='%9.5f',delimiter='|')
    print 'Done'

def main(): run()  
if __name__ == "__main__": main()
