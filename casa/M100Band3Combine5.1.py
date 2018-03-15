version = cu.version_string()
print "You are using " + version
if (version < '5.1.1'):
    print "YOUR VERSION OF CASA IS TOO OLD FOR THIS GUIDE."
    print "PLEASE UPDATE IT BEFORE PROCEEDING."
else:
    print "Your version of CASA is appropriate for this guide."
os.system('rm -rf M100_*m.ms.listobs')
listobs('M100_Band3_12m_CalibratedData.ms',listfile='M100_12m.ms.listobs')
listobs('M100_Band3_7m_CalibratedData.ms',listfile='M100_7m.ms.listobs')
os.system('rm -rf M100_12m_CO.ms')
split(vis='M100_Band3_12m_CalibratedData.ms',
      outputvis='M100_12m_CO.ms',spw='0',field='M100',
      datacolumn='data',keepflags=False)
os.system('rm -rf M100_7m_CO.ms')
split(vis='M100_Band3_7m_CalibratedData.ms',
      outputvis='M100_7m_CO.ms',spw='3,5',field='M100',
      datacolumn='data',keepflags=False)
os.system('rm -rf *m_mosaic.png')
au.plotmosaic('M100_12m_CO.ms',sourceid='0',figfile='12m_mosaic.png')
au.plotmosaic('M100_7m_CO.ms',sourceid='0',figfile='7m_mosaic.png')
os.system('rm -rf 7m_WT.png 12m_WT.png')
plotms(vis='M100_12m_CO.ms',yaxis='wt',xaxis='uvdist',spw='0:200',
       coloraxis='spw',plotfile='12m_WT.png')
plotms(vis='M100_7m_CO.ms',yaxis='wt',xaxis='uvdist',spw='0~1:200',
       coloraxis='spw',plotfile='7m_WT.png')
os.system('rm -rf M100_combine_CO.ms')
concat(vis=['M100_12m_CO.ms','M100_7m_CO.ms'],
       concatvis='M100_combine_CO.ms')
os.system('rm -rf combine_CO_WT.png')
plotms(vis='M100_combine_CO.ms',yaxis='wt',xaxis='uvdist',spw='0~2:200',
       coloraxis='spw',plotfile='combine_CO_WT.png')
os.system('rm -rf M100_combine_uvdist.png')
plotms(vis='M100_combine_CO.ms',yaxis='amp',xaxis='uvdist',spw='', avgscan=True,
       avgchannel='5000', coloraxis='spw',plotfile='M100_combine_uvdist.png')
os.system('rm -rf M100_combine_vel.png')
plotms(vis='M100_combine_CO.ms',yaxis='amp',xaxis='velocity',spw='', avgtime='1e8',avgscan=True,coloraxis='spw',avgchannel='5',
       transform=True,freqframe='LSRK',restfreq='115.271201800GHz', plotfile='M100_combine_vel.png')
vis='M100_combine_CO.ms'
prename='M100_combine_CO_cube'
myimage=prename+'.image'
myflux=prename+'.flux'
mymask=prename+'.mask'
myresidual=prename+'.residual'
imsize=800
cell='0.5arcsec'
minpb=0.2
restfreq='115.271201800GHz'
outframe='LSRK'
spw='0~2'
width='5km/s'
start='1400km/s'
nchan=70
robust=0.5
phasecenter='J2000 12h22m54.9 +15d49m15'
scales=[0]
smallscalebias=0.6
stop=3. 
pixelmin=0.5
os.system('rm -rf '+prename+'.* ' +prename+'_*')
tclean(vis=vis,imagename=prename,
      gridder='mosaic',deconvolver='hogbom',pbmask=minpb,
      imsize=imsize,cell=cell,spw=spw,
      weighting='briggs',robust=robust,phasecenter=phasecenter,
      specmode='cube',width=width,start=start,nchan=nchan,      
      restfreq=restfreq,outframe=outframe,veltype='radio',
      mask='',
      niter=0,interactive=False)
major=imhead(imagename=myimage,mode='get',hdkey='beammajor')['value']
minor=imhead(imagename=myimage,mode='get',hdkey='beamminor')['value']
pixelsize=float(cell.split('arcsec')[0])
beamarea=(major*minor*pi/(4*log(2)))/(pixelsize**2)
print 'beamarea in pixels =', beamarea
myimage=prename+'.image'
bigstat=imstat(imagename=myimage)
peak= bigstat['max'][0]
print 'peak (Jy/beam) in cube = '+str(peak)
thresh = peak / 4.
if True:  
    chanstat=imstat(imagename=myimage,chans='4')
    rms1= chanstat['rms'][0]
    chanstat=imstat(imagename=myimage,chans='66')
    rms2= chanstat['rms'][0]
    rms=0.5*(rms1+rms2)        
else:
    rms=0.011
print 'rms (Jy/beam) in a channel = '+str(rms)
os.system('rm -rf ' + prename +'_threshmask*')
os.system('rm -rf ' + prename +'_fullmask*')
os.system('rm -rf ' + prename +'.image*')
n=-1
while (thresh >= stop*rms):   
    n=n+1
    print 'clean threshold this loop is', thresh
    threshmask = prename+'_threshmask' +str(n)
    maskim = prename+'_fullmask' +str(n)
    immath(imagename = [myresidual],
           outfile = threshmask,
           expr = 'iif(IM0 > '+str(thresh) +',1.0,0.0)',
           mask=myflux+'>'+str(minpb))
    if (n==0):
        os.system('cp -r '+threshmask+' '+maskim+'.pb')
        print 'This is the first loop'
    else:
        makemask(mode='copy',inpimage=myimage,
                 inpmask=[threshmask,mymask],
                 output=maskim)
        imsubimage(imagename=maskim, mask=myflux+'>'+str(minpb),
                   outfile=maskim+'.pb')     
    print 'Combined mask ' +maskim+' generated.'
    os.system('cp -r '+maskim+'.pb ' +maskim+'.pb.min')
    maskfile=maskim+'.pb.min'
    ia.open(maskfile)
    mask=ia.getchunk()           
    labeled,j=scipy.ndimage.label(mask)                     
    myhistogram = scipy.ndimage.measurements.histogram(labeled,0,j+1,j+1)
    object_slices = scipy.ndimage.find_objects(labeled)
    threshold=beamarea*pixelmin
    for i in range(j):
        if myhistogram[i+1]<threshold:
            mask[object_slices[i]] = 0
    ia.putchunk(mask)
    ia.done()
    print 'Small masks removed and ' +maskim +'.pb.min generated.'
    os.system('rm -rf '+mymask+'')
    clean(vis=vis,imagename=prename,
          imagermode='mosaic',ftmachine='mosaic',minpb=minpb,
          imsize=imsize,cell=cell,spw=spw,
          weighting='briggs',robust=robust,phasecenter=phasecenter,
          mode='velocity',width=width,start=start,nchan=nchan,      
          restfreq=restfreq,outframe=outframe,veltype='radio',
          mask = maskim+'.pb.min',
          multiscale=scales,smallscalebias=smallscalebias,
          interactive = False,
          niter = 10000,
          threshold = str(thresh) +'Jy/beam')
    if thresh==stop*rms: break
    thresh = thresh/2.
    if (thresh < stop*rms and thresh*2.>1.05*stop*rms):
        thresh=stop*rms  
        os.system('cp -r '+myimage+' '+myimage+str(n))
viewer('M100_combine_CO_cube.image')
myimage='M100_combine_CO_cube.image'
chanstat=imstat(imagename=myimage,chans='4')
rms1= chanstat['rms'][0]
chanstat=imstat(imagename=myimage,chans='66')
rms2= chanstat['rms'][0]
rms=0.5*(rms1+rms2)
print 'rms in a channel = '+str(rms)
os.system('rm -rf M100_combine_CO_cube.image.mom0')
immoments(imagename = 'M100_combine_CO_cube.image',
         moments = [0],
         axis = 'spectral',chans = '9~61',
         mask='M100_combine_CO_cube.flux>0.3',
         includepix = [rms*2,100.],
         outfile = 'M100_combine_CO_cube.image.mom0')
os.system('rm -rf M100_combine_CO_cube.image.mom1')
immoments(imagename = 'M100_combine_CO_cube.image',
         moments = [1],
         axis = 'spectral',chans = '9~61',
         mask='M100_combine_CO_cube.flux>0.3',
         includepix = [rms*5.5,100.],
         outfile = 'M100_combine_CO_cube.image.mom1')
os.system('rm -rf M100_combine_CO_cube.image.mom*.png')
imview (raster=[{'file': 'M100_combine_CO_cube.image.mom0',
                 'range': [-0.3,25.],'scaling': -1.3,'colorwedge': True}],
         zoom={'blc': [190,150],'trc': [650,610]},
         out='M100_combine_CO_cube.image.mom0.png')
imview (raster=[{'file': 'M100_combine_CO_cube.image.mom1',
                 'range': [1440,1695],'colorwedge': True}],
         zoom={'blc': [190,150],'trc': [650,610]}, 
         out='M100_combine_CO_cube.image.mom1.png')
os.system('rm -rf M100_combine_CO_cube.flux.1ch')
imsubimage(imagename='M100_combine_CO_cube.flux',
           outfile='M100_combine_CO_cube.flux.1ch',
           chans='35')
os.system('rm -rf M100_combine_CO_cube.image.mom0.pbcor')
immath(imagename=['M100_combine_CO_cube.image.mom0', \
                       'M100_combine_CO_cube.flux.1ch'],
        expr='IM0/IM1',
        outfile='M100_combine_CO_cube.image.mom0.pbcor')
imview (raster=[{'file': 'M100_combine_CO_cube.image.mom0',
                 'range': [-0.3,25.],'scaling': -1.3},
                {'file': 'M100_combine_CO_cube.image.mom0.pbcor',
                 'range': [-0.3,25.],'scaling': -1.3}],
         zoom={'blc': [190,150],'trc': [650,610]})
os.system('rm -rf M100_combine_CO_cube.image.mom0.pbcor.png')
imview (raster=[{'file': 'M100_combine_CO_cube.image.mom0.pbcor',
                 'range': [-0.3,25.],'scaling': -1.3,'colorwedge': True}],
         zoom={'blc': [190,150],'trc': [650,610]},
         out='M100_combine_CO_cube.image.mom0.pbcor.png')
os.system('rm -rf *.fits')
exportfits(imagename='M100_combine_CO_cube.image',fitsimage='M100_combine_CO_cube.image.fits')
exportfits(imagename='M100_combine_CO_cube.flux',fitsimage='M100_combine_CO_cube.flux.fits')
exportfits(imagename='M100_combine_CO_cube.image.mom0',fitsimage='M100_combine_CO_cube.image.mom0.fits')
exportfits(imagename='M100_combine_CO_cube.image.mom0.pbcor',fitsimage='M100_combine_CO_cube.image.mom0.pbcor.fits')
exportfits(imagename='M100_combine_CO_cube.image.mom1',fitsimage='M100_combine_CO_cube.image.mom1.fits')
os.system('rm -rf M100_TP_CO_cube.regrid')
imregrid(imagename='M100_TP_CO_cube.bl.image',
         template='M100_combine_CO_cube.image',
         axes=[0, 1],
         output='M100_TP_CO_cube.regrid')
os.system('rm -rf M100_TP_CO_cube.regrid.subim')
imsubimage(imagename='M100_TP_CO_cube.regrid',
           outfile='M100_TP_CO_cube.regrid.subim',
           box='219,148,612,579')
os.system('rm -rf M100_combine_CO_cube.image.subim')
imsubimage(imagename='M100_combine_CO_cube.image',
           outfile='M100_combine_CO_cube.image.subim',
           box='219,148,612,579')
os.system('rm -rf M100_combine_CO_cube.flux.subim')
imsubimage(imagename='M100_combine_CO_cube.flux',
           outfile='M100_combine_CO_cube.flux.subim',
           box='219,148,612,579')
os.system('rm -rf M100_TP_CO_cube.regrid.subim.depb')
immath(imagename=['M100_TP_CO_cube.regrid.subim',
                  'M100_combine_CO_cube.flux.subim'],
       expr='IM0*IM1',
       outfile='M100_TP_CO_cube.regrid.subim.depb')
os.system('rm -rf M100_Feather_CO.image')
feather(imagename='M100_Feather_CO.image',
        highres='M100_combine_CO_cube.image.subim',
        lowres='M100_TP_CO_cube.regrid.subim.depb')
myimage = 'M100_TP_CO_cube.regrid.subim'
chanstat = imstat(imagename=myimage,chans='4')
rms1 = chanstat['rms'][0]
chanstat = imstat(imagename=myimage,chans='66')
rms2 = chanstat['rms'][0]
rms = 0.5*(rms1+rms2)  
os.system('rm -rf M100_TP_CO_cube.regrid.subim.mom0')
immoments(imagename='M100_TP_CO_cube.regrid.subim',
         moments=[0],
         axis='spectral',
         chans='10~61',
         includepix=[rms*2., 50],
         outfile='M100_TP_CO_cube.regrid.subim.mom0')
os.system('rm -rf M100_TP_CO_cube.regrid.subim.mom1')
immoments(imagename='M100_TP_CO_cube.regrid.subim',
         moments=[1],
         axis='spectral',
         chans='10~61',
         includepix=[rms*5.5, 50],
         outfile='M100_TP_CO_cube.regrid.subim.mom1')
os.system('rm -rf M100_TP_CO_cube.regrid.subim.mom*.png')
imview(raster=[{'file': 'M100_TP_CO_cube.regrid.subim.mom0',
                'range': [0., 1080.],
                'scaling': -1.3,
                'colorwedge': True}],
       out='M100_TP_CO_cube.regrid.subim.mom0.png')
imview(raster=[{'file': 'M100_TP_CO_cube.regrid.subim.mom1',
                'range': [1440, 1695],
                'colorwedge': True}], 
       out='M100_TP_CO_cube.regrid.subim.mom1.png')
myimage = 'M100_Feather_CO.image'
chanstat = imstat(imagename=myimage,chans='4')
rms1 = chanstat['rms'][0]
chanstat = imstat(imagename=myimage,chans='66')
rms2 = chanstat['rms'][0]
rms = 0.5*(rms1+rms2)  
os.system('rm -rf M100_Feather_CO.image.mom0')
immoments(imagename='M100_Feather_CO.image',
         moments=[0],
         axis='spectral',
         chans='10~61',
         includepix=[rms*2., 50],
         outfile='M100_Feather_CO.image.mom0')
os.system('rm -rf M100_Feather_CO.image.mom1')
immoments(imagename='M100_Feather_CO.image',
         moments=[1],
         axis='spectral',
         chans='10~61',
         includepix=[rms*5.5, 50],
         outfile='M100_Feather_CO.image.mom1')
os.system('rm -rf M100_Feather_CO.image.mom*.png')
imview(raster=[{'file': 'M100_Feather_CO.image.mom0',
                'range': [-0.3, 25.],
                'scaling': -1.3,
                'colorwedge': True}],
       out='M100_Feather_CO.image.mom0.png')
imview(raster=[{'file': 'M100_Feather_CO.image.mom1',
                'range': [1440, 1695],
                'colorwedge': True}], 
       out='M100_Feather_CO.image.mom1.png')
os.system('rm -rf M100_Feather_CO.image.pbcor')
immath(imagename=['M100_Feather_CO.image',
                  'M100_combine_CO_cube.flux.subim'],
       expr='IM0/IM1',
       outfile='M100_Feather_CO.image.pbcor')
os.system('rm -rf M100_combine_CO_cube.flux.1ch.subim')
imsubimage(imagename='M100_combine_CO_cube.flux.subim',
           outfile='M100_combine_CO_cube.flux.1ch.subim',
           chans='35')
os.system('rm -rf M100_Feather_CO.image.mom0.pbcor')
immath(imagename=['M100_Feather_CO.image.mom0',
                  'M100_combine_CO_cube.flux.1ch.subim'],
        expr='IM0/IM1',
        outfile='M100_Feather_CO.image.mom0.pbcor')
os.system('rm -rf M100_Feather_CO.image.mom0.pbcor.png')
imview(raster=[{'file': 'M100_Feather_CO.image.mom0.pbcor',
                'range': [-0.3, 25.],
                'scaling': -1.3,
                'colorwedge': True}],
       out='M100_Feather_CO.image.mom0.pbcor.png')
imstat('M100_combine_CO_cube.image.subim')
imstat('M100_combine_CO_cube.image.subim')['flux']*5.0
imstat('M100_TP_CO_cube.regrid.subim.depb')['flux']*5.0
imstat('M100_Feather_CO.image')['flux']*5.0
imstat('M100_Feather_CO.image.pbcor')['flux']*5.0
