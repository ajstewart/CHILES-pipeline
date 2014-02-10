#!/usr/bin/env python

import sys, subprocess, os

def run_casa(ms, sets):
	filename="{0}.py".format(ms)
	casafile=open(filename, "w")
	casafile.write("default('clean')")
	for i in sets:
		casafile.write("\n{0}={1}".format(i, sets[i]))
	casafile.write("\nclean()")
	casafile.write("\n\n")
	casafile.write("default('exportfits')\n")
	casafile.write("imagename={0}\n".format(sets["imagename"]))
	casafile.write("fitsimage={0}\n".format(sets["fitsimage"]))
	casafile.write("exportfits()\n")
	casafile.close()
	subprocess.call("casapy --logfile {0}.log --nologger -c {1}".format(ms, filename), shell=True)
	os.remove(filename)
	subprocess.call("mv *.log logs/", shell=True)
	subprocess.call("mv *.fits fitsimages/", shell=True)

datadir="/pi1storage/obs_data/evla/chiles_testdata/"

vis = sys.argv[1].split("/")[-1].split(".NEW")[0]
imagename=vis+".mfs_wProj"
clean_args = {
	"vis":"'{0}'".format(os.path.join(datadir,vis)),
	"imagename":"'{0}'".format(imagename),
	"spw": "''",
	"imsize": "[4096, 4096]",
	"cell": "['1.0arcsec']",
	"weighting": "'briggs'",
	   "robust": 0.0,
	"imagermode":"'csclean'",
	"stokes":"'I'",
	"mode":"'mfs'",
		"nterms":2,
	"gridmode":"'widefield'", 
	"wprojplanes":128,
	"threshold":"'0.02mJy'",
	"niter":10000,
	"fitsimage":"'{0}.fits'".format(imagename),
}

run_casa(vis, clean_args)
fitsfile=imagename+".fits"
print "Transferring {0} to Soton...".format(fitsfile)
subprocess.call("scp -r fitsimages/{0} as24v07@152.78.192.15:/media/RAIDC/CHILES/images/".format(fitsfile), shell=True)
print "Done!"
	
#For self-cal
    # models=[".model.tt0",".model.tt1"]
    # ft(vis=i,model=[name+j for j in models],nterms=2,reffreq='1.4GHz')
    # caltab=name+'.P0'
    # gaincal(vis=i,caltable=caltab,field='',refant='EA24',calmode='p',solint='200s',minsnr=3,solnorm = False)
    # applycal(vis=i,field="",spw="",intent="",selectdata=False,timerange="",uvrange="",antenna="",scan="",msselect="",gaintable=caltab,gainfield=[''],interp=['nearest'],spwmap=[],gaincurve=False,opacity=0.0,parang=True,calwt=False,flagbackup=True)
    # name=i.split("/")[-1]+".mfs_wProj.SELFTEST2_AFTER-SELF"
    # clean(vis=i,imagename=name,cell='1arcsec', gridmode='widefield', wprojplanes=128, niter=10000, imsize=4096, imagermode='csclean', threshold='0.01mJy', stokes='I', weighting='briggs', mode='mfs', nterms=2, reffreq="1.4GHz")
    # imname=name+".image.tt0"
    # exportfits(imagename=imname, fitsimage=imname+".fits")
	

# name="chiles_deep_try"
# clean(vis=toimage,imagename=name,cell='1arcsec', gridmode='widefield', wprojplanes=128, niter=10000, imsize=4096, imagermode='csclean', threshold='0.01mJy', stokes='I', weighting='briggs', mode='mfs', nterms=3)