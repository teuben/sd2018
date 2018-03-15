version = cu.version_string()
print "You are using " + version
if (version < '5.1.0'):
    print "YOUR VERSION OF CASA IS TOO OLD FOR THIS GUIDE."
    print "PLEASE UPDATE IT BEFORE PROCEEDING."
else:
    print "Your version of CASA is appropriate for this guide."
importasdm('uid___A002_X85c183_X36f',
           asis='Antenna Station Receiver Source CalAtmosphere CalWVR', bdfflags=False)
os.system(os.environ['CASAPATH'].split()[0] + '/bin/bdflags2MS -f "COR DELA INT MIS SIG SYN TFB WVR ZER" uid___A002_X85c183_X36f uid___A002_X85c183_X36f.ms')
listobs(vis='uid___A002_X85c183_X36f.ms',
        listfile='uid___A002_X85c183_X36f.ms.listobs')
aU.getTPSampling(vis='uid___A002_X85c183_X36f.ms',
                 showplot=True,
                 plotfile='uid___A002_X85c183_X36f.ms.sampling.png')
gencal(vis='uid___A002_X85c183_X36f.ms',
       caltable='uid___A002_X85c183_X36f.ms.tsys',
       caltype='tsys')
plotbandpass(caltable='uid___A002_X85c183_X36f.ms.tsys',
             overlay='time',
             xaxis='freq',
             yaxis='amp',
             subplot=22,
             buildpdf=False,
             interactive=False,
             showatm=True,
             pwv='auto',
             chanrange='5~123',
             showfdm=True,
             field='',
             figfile='uid___A002_X85c183_X36f.ms.tsys.plots.overlayTime/uid___A002_X85c183_X36f.ms.tsys')
flagdata(vis = 'uid___A002_X85c183_X36f.ms',
       mode = 'manual',
       spw = '17:0~119;3960~4079,19:0~119;3960~4079,21:0~119;3960~4079,23:0~119;3960~4079',
       action = 'apply',
       flagbackup = True)
sdcal(infile = 'uid___A002_X85c183_X36f.ms',
    calmode = 'ps,tsys,apply',
    spwmap = {9:[17], 11:[19], 13:[21],15:[23]},
    spw = '17,19,21,23')
plotms(vis='uid___A002_X85c183_X36f.ms',
    xaxis='freq', yaxis='amp', ydatacolumn='corrected',
    field='M100',spw='23',
    scan='6,7,9,10,12,13,15',
    averagedata=True,avgtime='9999',
    gridcols=3,gridrows=3,iteraxis='scan',
    plotrange=[113.5, 116, -0.01, 0.08],
    plotfile='vis.png',
    showgui=False)
to_amp_factor = lambda x: 1. / sqrt(x)
split(vis='uid___A002_X85c183_X36f.ms',
    outputvis='uid___A002_X85c183_X36f.ms.cal.split',
    datacolumn='corrected',
    spw='17,19,21,23')
gencal(vis='uid___A002_X85c183_X36f.ms.cal.split',
    caltable='uid___A002_X85c183_X36f.ms.nlc',
    caltype='amp', spw='',
    parameter=[to_amp_factor(1.25)])
applycal(vis='uid___A002_X85c183_X36f.ms.cal.split',
    gaintable='uid___A002_X85c183_X36f.ms.nlc')
sdbaseline(infile='uid___A002_X85c183_X36f.ms.cal.split',
    datacolumn='corrected',
     spw='',
     blfunc='poly',
     order=1,
     outfile='uid___A002_X85c183_X36f.ms.bl',
     overwrite=True)
plotms(vis='uid___A002_X85c183_X36f.ms.bl',
    xaxis='freq', yaxis='amp', ydatacolumn='corrected',
    field='M100',spw='3',
    scan='6,7,9,10,12,13,15',
    averagedata=True,avgtime='9999',
    gridcols=3,gridrows=3,iteraxis='scan',
    plotrange=[113.5, 116, -0.01, 0.08],
    plotfile='vis_bl.png',
    showgui=False)
flagdata(vis='uid___A002_X8602fa_X2ab.ms.bl',
    antenna='PM02&&&')
flagdata(vis='uid___A002_X8602fa_X577.ms.bl',
    antenna='PM02&&&')
factors = [41.52, 42.47, 43.58, 42.98]
gencal(vis='uid___A002_X85c183_X36f.ms.bl',
    caltable='uid___A002_X85c183_X36f.ms.jy',
    caltype='amp',
    spw='0,1,2,3',
    parameter=[ to_amp_factor(v) for v in factors ])
applycal(vis='uid___A002_X85c183_X36f.ms.bl',
    gaintable='uid___A002_X85c183_X36f.ms.jy')
asdmlist = ['uid___A002_X85c183_X36f',
            'uid___A002_X85c183_X60b',
            'uid___A002_X8602fa_X2ab',
            'uid___A002_X8602fa_X577',
            'uid___A002_X864236_X2d4',
            'uid___A002_X864236_X693',
            'uid___A002_X86fcfa_X664',
            'uid___A002_X86fcfa_X96c',
            'uid___A002_X86fcfa_Xd9']
vislist = map(lambda x: x + '.ms.cal.jy', asdmlist)
spw = 23
imagename = 'M100_TP_CO_cube.spw%s.image'%(spw)
blimagename = imagename + '.bl'
integimagename = imagename + '.integ'
fwhmfactor = 1.13
diameter = 12
xSampling, ySampling, maxsize = aU.getTPSampling(vis='uid___A002_X85c183_X36f.ms', showplot=False)
msmd.open(vislist[0])
freq = msmd.meanfreq(spw)
msmd.close()
print "SPW %d: %.3f GHz" % (spw, freq*1e-9)
theorybeam = aU.primaryBeamArcsec(frequency=freq*1e-9,
                                  fwhmfactor=fwhmfactor,
                                  diameter=diameter)
cell = theorybeam/9.0
imsize = int(round(maxsize/cell)*2)
sdimaging(infiles=vislist,
    field='M100',
    spw='%s'%(spw),
    nchan=70,
    mode='velocity',
    start='1400km/s',
    width='5km/s',
    veltype='radio',
    outframe='lsrk',
    restfreq='115.271204GHz',
    gridfunction='SF',
    convsupport=6,
    stokes='I',
    phasecenter='J2000 12h22m54.9 +15d49m15',
    ephemsrcname='',
    imsize=imsize,
    cell='%sarcsec'%(cell),
    brightnessunit='Jy/beam',
    overwrite=True,
    outfile=imagename)
viewer(imagename)
imcontsub(imagename=imagename,
    linefile=blimagename,
    contfile='M100.residualbaseline.image',
    fitorder=1,
    chans='0~7;62~69')
os.system('rm -rf M100.residualbaseline.image')
immoments(imagename=blimagename,
    moments=[0],
    axis='spectral',
    chans='8~61',
    outfile=integimagename)
viewer(integimagename)
