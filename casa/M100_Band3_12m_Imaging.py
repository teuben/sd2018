# Imaging script for M100, 12m data
# Tested in CASA version 4.3.0 revision 31966

#--------------------------------------------------------------------------------------#
#                     Data Preparation                                                 #
# -------------------------------------------------------------------------------------#

# Comment this step out if you are starting from the calibrated data
# M100_Band3_12m_CalibratedData.ms downloaded from the Science Portal

# Split off the M100 calibrated data
split (vis='uid___A002_X273b43_X146.ms.split.cal', field='M100', outputvis='M100_X146.ms.cal', datacolumn='data',keepflags=F)
split (vis='uid___A002_X2a5c2f_X220.ms.split.cal', field='M100', outputvis='M100_X220.ms.cal', datacolumn='data',keepflags=F)
split (vis='uid___A002_X2a5c2f_X54.ms.split.cal', field='M100', outputvis='M100_X54.ms.cal', datacolumn='data',keepflags=F)

# Combine all the ms into one
concat(vis=['M100_X146.ms.cal', 'M100_X220.ms.cal', 'M100_X54.ms.cal'],concatvis='M100_Band3_12m_CalibratedData.ms')

# From this point on you can proceed from M100_Band3_12m_CalibratedData.ms

#--------------------------------------------------------------------------------------#
#                             Imaging                                                  #
#--------------------------------------------------------------------------------------#

##################################################
# Check CASA version
 
version = casadef.casa_version
print "You are using " + version
if (version < '4.3.0'):
    print "YOUR VERSION OF CASA IS TOO OLD FOR THIS GUIDE."
    print "PLEASE UPDATE IT BEFORE PROCEEDING."
else:
    print "Your version of CASA is appropriate for this guide."

##################################################
# Identify Line-free SPWs and channels

finalvis='M100_Band3_12m_CalibratedData.ms' 

# Use plotms to identify line and continuum spectral windows
plotms(vis=finalvis, xaxis='channel', yaxis='amplitude',
       ydatacolumn='data',
       avgtime='1e8', avgscan=True, avgchannel='2',
       iteraxis='spw' )

##################################################
# Create an Averaged Continuum MS

# Average channels within spws
contspws='1,2,3' # from plotms output
contvis='M100_12m_cont.ms'
os.system('rm -rf ' + contvis)
split(vis=finalvis,
      spw=contspws,
      outputvis=contvis,
      width=[3840,3840,3840], # number of channels to average together. change to appropriate value for each spectral window.
      datacolumn='data')   

# these observations contain continuum-only SPWs: 1,2,3 (line is in SPW 0)



#############################################
# Imaging the Continuuum

contimagename = 'M100_12m_cont'

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual']:
    os.system('rm -rf ' + contimagename + ext)

clean(vis=contvis,
      imagename=contimagename,
      field='1~47' # science fields
      phasecenter='J2000 12h22m54.9 +15d49m15',     
      mode='mfs',
      psfmode='clark',
      imsize = [200,200], # size of image in pixels 
      cell= '0.5arcsec', # cell size for imaging
      weighting = 'briggs', 
      robust = 0.5,
      niter = 1000, 
      threshold = '0.0mJy',
      mask=[70,90,118,130],
      interactive = False,
      imagermode = 'mosaic')

# RMS ~ 0.12 mJy in a 3.7"x2.5" beam

########################################
# Continuum Subtraction for Line Imaging

fitspw = '0:200~1500;2500~3700,1~3:100~3700' # line-free channel for fitting continuum
linespw = '0' # line spectral windows.

uvcontsub(vis=finalvis,
          spw=linespw, # spw to do continuum subtraction on
          fitspw=fitspw, 
          combine='', 
          solint='int',
          fitorder=1,
          want_cont=False) 


##############################################
# Image line emission

linevis = finalvis+'.contsub'
lineimagename = 'M100_12m_CO' # name of line image


# If you do not wish to use the provided mask, comment out the line: "mask=''"

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    os.system('rm -rf ' + lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename, 
      field='1~47', # science fields
      spw='0:1500~2500',
      phasecenter='J2000 12h22m54.9 +15d49m15',        
      mode='velocity',
      start='1400km/s', # start velocity
      width='5km/s', # velocity width
      nchan= 70,  # number of channels
      outframe='LSRK', # velocity reference frame
      veltype='radio', # velocity type
      restfreq='115.271201800GHz', # rest frequency of primary line of interest
      niter=10000,  
      threshold='0.015Jy', 
      interactive=True,
      minpb=0.2,
      cell='0.5arcsec',
      imsize=800, 
      weighting='briggs', 
      robust=0.5,
      imagermode='mosaic',
      mask='M100_12m_CO_demo.mask')


# M100_12m_CO.image (and other files) created -- use .mask file to reproduce my masking by hand
# rms in line free channel (width 5 km/s): 11-12 mJy/beam

##############################################
# Apply a primary beam correction

impbcor(imagename='M100_12m_CO.image', pbimage='M100_12m_CO.flux', outfile='M100_12m_CO.pbcor')

##############################################
# Make moment maps of the CO(1-0) emission 

immoments(imagename = 'M100_12m_CO.image',
         moments = [0],
         axis = 'spectral',chans = '9~60',
         includepix = [0.02,100.],
         outfile = 'M100_12m_CO.image.mom0')

immoments(imagename = 'M100_12m_CO.image',
         moments = [1],
         axis = 'spectral',chans = '9~60',
         includepix = [0.05,100.],
         outfile = 'M100_12m_CO.image.mom1')

immoments(imagename = 'M100_12m_CO.pbcor',
         moments = [0],
         axis = 'spectral',chans = '9~60',
         includepix = [0.02,100.],
         outfile = 'M100_12m_CO.image.pbcor.mom0')

# Make some png plots 

imview (raster=[{'file': 'M100_12m_CO.image.mom0',
                 'range': [-0.3,25.],'scaling': -1.0,'colorwedge': T}],
         zoom={'blc': [190,150],'trc': [650,610]},
         out='M100_12m_CO.image.mom0.png')
imview (raster=[{'file': 'M100_12m_CO.image.mom1',
                 'range': [1455,1695],'colorwedge': T}],
         zoom={'blc': [190,150],'trc': [650,610]},
         out='M100_12m_CO.image.mom1.png')


##############################################
# Export the images

exportfits(imagename='M100_12m_CO.image', fitsimage='M100_12m_CO.image.fits')
exportfits(imagename='M100_12m_CO.flux', fitsimage='M100_12m_CO.flux.fits')
exportfits(imagename='M100_12m_CO.pbcor', fitsimage='M100_12m_CO.pbcor.fits')
exportfits(imagename='M100_12m_CO.image.mom0', fitsimage='M100_12m_CO.image.mom0.fits')
exportfits(imagename='M100_12m_CO.image.pbcor.mom0', fitsimage='M100_12m_CO.image.mom0.pbcor.fits')
exportfits(imagename='M100_12m_CO.image.mom1', fitsimage='M100_12m_CO.image.mom1.fits')

