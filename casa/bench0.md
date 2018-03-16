#   M100 Combination examples - just 1 channel

This markdown (md) file follows the benchmark "bench0.py" script in QAC/test

## Preparations

Get your data from http://admit.astro.umd.edu/~teuben/QAC/

    qac_bench.tar.gz      - the ALMA data (3 files)
    model4.fits           - new, model of a rotating galaxy

Go and visualize the images in casa or ds9:

    exportfits('M100_TP_CO_cube.bl.image', 'M100_TP_CO_cube.bl.fits')

    viewer('M100_TP_CO_cube.bl.image')
    viewer('model4.fits')

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

Luckily enough, cutting and pasting these will do no harm

## Do we have our files?

Did you really have all your files here? There is a 

    QAC.exists(tpim)
    QAC.exists(ms07)
    QAC.exists(ms12)

## Summary

You can use
[**listobs()**](https://casa.nrao.edu/casadocs/latest/global-task-list/task_listobs/about) 
and
[**imhead()**](https://casa.nrao.edu/casadocs/latest/global-task-list/task_imhead/about)  [OOPS]
but within QAC there is a summary that combines the information:


    qac_summary(tpim,[ms07,ms12])


## Some derived parameters


    tpms   = 'bench0/tp.ms'
    ptg    = 'bench0.ptg'
    tpim2  = tpim
    # tpim2 = tpim+'_'+chans
    # imsubimage(tpim,tpim2,chans=chans,overwrite=True)


## Properties of the TPIM: RMS

We will need to know the RMS in the TP for TP2VIS. For example, imstat can look at the first few and last channels:

    imstat(tpim,axes=[0,1])['rms'][:6].mean()
    imstat(tpim,axes=[0,1])['rms'][-6:].mean()

We also have a RMS as function of channel plotter in QAC, that visualizes this:

    plot5(tpim)

So, the answer is about 0.15 for the rms!


## Need a pointing file for TP2VIS

We also have **m100_aver.ptg** , but here we create one on the fly from the MS

    qac_ms_ptg(ms12,ptg)

Alternatively you can create one from an image using a hex-grid generator (**qac_im_ptg()**)

# run tp2vis and plot weights to compare to 12m/7m

Next you run **tp2vis**, in a vanilly CASA you would simply need to do

    execfile("tp2vis.py")

and have access to the 4 basic tp2vis functions. Here I am using a QAC routine.


    qac_tp_vis('bench0',tpim2,ptg,rms=0.15)
    #  mkdir bench0
    #  tp2vis('bench0/tp.ms',tpim2,ptg,rms=0.15)

and now     
    
    tp2vispl([tpms,ms07,ms12],outfig='bench0/tp2vispl_rms.png',show=True)

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

