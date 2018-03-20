#########
# Simple examples of use of BoA with ArTeMiS data
# Prepared for the ESO SD2018 workshop
#
# F. Schuller - March 2018
#########

# First, define input directory (where the raw data files are located)
indir('/scratch/rawdata')  # adapt to your own configuration
ils()                      # this displays the list of files in 'indir'

# To process ArTeMiS data, you first need to execute the file 'artemis.boa',
# where a number of Artemis-specific functions are defined:
boadir = os.getenv('BOA_HOME')
execfile(boadir+'/artemis/artemis.boa')

# Example reduction of non-science scans
# Pointing and focus: usually this is required only at the telescope,
# during the observations
redpnt(77392)   # pointing reduction (450 mic data)
redmfoc(77373)  # reduction of a mapping focus (450 mic data)

# Calibration scans: important to calibrate your science data
redsky(77385)   # skydip reduction - default is to look at 450 mic data
redsky(77385,band=350)   # skydip reduction - 350 mic data
# By default, the opacity used to reduce calibration scans is derived from
# the amount of precipitable water vapour (PWV) recorded in the file
redcal(77372)   # reduction of a map on a primary calibrator (450 mic data)
redcal(77372,tau=0.55)   # you can give tau as an input
redcal(89982)   # reduction of a map on a secondary calibrator
                # default for all these functions is to process 450 mic data
redcal(89982,band=350)   # secondary calibrator, 350 mic data
redcal(89982,band=350,tau=1.0)

####
# Typical reduction of science scans: use function process
print process.__doc__   # this shows you the options available for this function
process(data,scannum=77389,band=350,subscans=range(40,80))  # for example
data.doMap(system='eq',oversamp=5)   # let BoA compute the map limits


####
# To combine several scans:
# List of scans on Ori-ISF-1
slist = [77389,77391]

# Initialise map list
mlist = []
x1,x2 = 83.98,83.62
y1,y2 = -5.53,-5.21

# Process each scan and build a map
for i in range(2):
    # let's use only 1/3 of the subscans (file is too big)
    subs = 1 + 3*arange(42)
    tst = process(data,scannum=slist[i],band=350,subscans=subs)
    data.doMap(system='eq',sizeX=[x1,x2],sizeY=[y1,y2],oversamp=5.)
    mlist.append(copy.deepcopy(data.Map))

# Combine the maps
mtot = mapsumfast(mlist)
mtot.display(aspect=1,limitsZ=[-120,500])
# 1/3-beam smoothing
m_smo = copy.deepcopy(mtot)
m_smo.smoothBy(2.5/3600.)
# Compute S/N map
snr = copy.deepcopy(m_smo)
snr.Data *= sqrt(m_smo.Weight)

# 2nd iteration: use S/N map to mask in the data
mlist2 = []
for i in range(2):
    tst = process(data,scannum=slist[i],subscans=subs)
    tst = process(data,scannum=slist[i],band=350,subscans=subs,
                  weak=1,mask=snr,threshold=25.)
    data.doMap(system='eq',sizeX=[x1,x2],sizeY=[y1,y2],oversamp=5.)
    mlist2.append(copy.deepcopy(data.Map))    

# Compute combined map
mtot2 = mapsumfast(mlist2)
mtot2.display(aspect=1,limitsZ=[-120,500])
# Export to FITS
mtot2.writeFits('Orion_350.fits')


