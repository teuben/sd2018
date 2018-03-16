#   M100 Combination examples - just 1 channel


## parameters in this benchmark workflow

    phasecenter = 'J2000 12h22m54.900s +15d49m15.000s'
    line        = {"restfreq":"115.271202GHz","start":"1500km/s", "width":"5km/s","nchan":1}
    chans       = '20'                   # must agree with the line={}    @todo casa regrid bug?
    tpim        = 'M100_TP_CO_cube.bl.image'
    ms07        = 'M100_aver_7.ms'
    ms12        = 'M100_aver_12.ms'
    nsize       = 800
    pixel       = 0.5
    niter       = [0,1000]


## Command line parameters

In the real **bench0.py** script you can override these parameters using the simple QAC command line parser

    import sys
    for arg in qac_argv(sys.argv):
        exec(arg)

## Some derived parameters


    tpms   = 'bench0/tp.ms'
    ptg    = 'bench0.ptg'
    tpim2  = tpim
    # tpim2 = tpim+'_'+chans
    # imsubimage(tpim,tpim2,chans=chans,overwrite=True)

## Need a pointing file for TP2VIS

We also have **m100_aver.ptg** , but here we create one on the fly from the MS

    qac_ms_ptg(ms12,ptg)

Alternatively you can create one from an image using a hex-grid generator (**qac_im_ptg()**)

# run tp2vis and plot weights to compare to 12m/7m


    qac_tp_vis('bench0',tpim2,ptg,rms=0.15)
    #  mkdir bench0
    #  tp2vis('bench0/tp.ms',tpim2,ptg,rms=0.15)
    
    tp2vispl([tpms,ms07,ms12],outfig='bench0/tp2vispl_rms.png')

    # @todo subtle difference if imsubimage is done here instead of upfront
    imsubimage(tpim,'bench0/tp.im',chans=chans)
    tpim2 = 'bench0/tp.im'

# joint deconvolution of tp2vis using tclean

    qac_clean('bench0/clean',tpms,[ms12,ms07],nsize,pixel,niter=niter,phasecenter=phasecenter,do_alma=True,**line)

    # JvM tweak
    tp2vistweak('bench0/clean/tpalma', 'bench0/clean/tpalma_2')

# classic feather

    qac_feather('bench0','bench0/clean/tpalma_2.image',tpim2)

# Faridani's SSC

    qac_ssc('bench0','bench0/clean/tpalma_2.image',tpim2, regrid=True, cleanup=False)

# Comparison Plot

plot various comparisons; difference maps are in the 3rd column of the plot_grid


    i1    = 'bench0/clean/alma.image'
    i2    = 'bench0/clean/tpalma.image'
    i3    = 'bench0/clean/alma_2.image'
    i4    = 'bench0/clean/tpalma_2.image'
    i5    = 'bench0/clean/tpalma_2.tweak.image'
    i6    = 'bench0/feather.image'
    i7    = 'bench0/ssc.image'
    ygrid = ['7&12 + tp', '7&12 iter','7&12&tp iter','tweak', 'feather', 'ssc']
    box   = [200,200,600,600]
    qac_plot_grid([i1,i2, i1,i3, i2,i4, i5,i4, i6,i4, i6,i7],box=box,ygrid=ygrid,plot='bench0/bench0.cmp.png',diff=10.0)

## regression

These are valid for casa 5.1.1 or 5.2.2.    If you are writing scripts for comparison or development of algorithms,
it is essential to regress your results , and understand and update the magic numbers when they change.


    r = [
    '0.00015477320920210852 0.036285694517807124 -0.12811994552612305 0.37910208106040955 0.30861407063317348',
    '0.0081229104489462297 0.039351242931759012 -0.084907762706279755 0.42440503835678101 16.006177593355094',
    '0.0034475503699085723 0.019158814084816258 -0.036495275795459747 0.35947218537330627 13.804154300264859',
    '0.0038158045059339071 0.021278204727857387 -0.044892586767673492 0.36717483401298523 903.12842626894303',
    '0.0038164805921419888 0.021283930007764854 -0.044894065707921982 0.36724790930747986 15.281368312333418',
    ]

    qac_stats('bench0/clean/alma.image',          r[0])
    qac_stats('bench0/clean/tpalma.image',        r[1])
    qac_stats('bench0/clean/tpalma_2.tweak.image',r[2])
    qac_stats('bench0/ssc.image',                 r[3])
    qac_stats('bench0/feather.image',             r[4])

### Regression-2

When instead using 

    QAC_STATS: bench0/clean/alma.image 0.00015477320920210852 0.036285694517807124 -0.12811994552612305 0.37910208106040955 0.30861407063317348 OK
    QAC_STATS: bench0/clean/tpalma.image 0.0080584386373350834 0.039330467912751674 -0.084458544850349426 0.4243462085723877 15.879130461295242 FAILED regression
                                         0.0081229104489462297 0.039351242931759012 -0.084907762706279755 0.42440503835678101 16.006177593355094 EXPECTED
    QAC_STATS: bench0/clean/tpalma_2.tweak.image 0.0034224454700299313 0.01913626328083845  -0.035994738340377808 0.35849106311798096 13.703628293743353 FAILED regression
                                                 0.0034475503699085723 0.019158814084816258 -0.036495275795459747 0.35947218537330627 13.804154300264859 EXPECTED
    QAC_STATS: bench0/ssc.image 0.0038171493562112113 0.021261351739842747 -0.044264290481805801 0.36624270677566528 903.44672677742574 FAILED regression
                                0.0038158045059339071 0.021278204727857387 -0.044892586767673492 0.36717483401298523 903.12842626894303 EXPECTED
    QAC_STATS: bench0/feather.image 0.0038178026692358255 0.021267067383166954 -0.0442657470703125   0.36631572246551514 15.28665661329336 FAILED regression
                                    0.0038164805921419888 0.021283930007764854 -0.044894065707921982 0.36724790930747986 15.281368312333418 EXPECTED


"""
