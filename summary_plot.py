## script to plot the output 
## from fermipy,given a .npy file
## Sara Buson, Oct. 2017
## very basic, need to implement better 
## the reading of  png, laoding the npy

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import sys
from matplotlib.cbook import get_sample_data
import matplotlib.image as mpimg

def getLCdata(lc,f_scale,ts=''):
	if not ts>-10: ts=25
	print ts
	""" --  reading the LC output --- """
	s=lc.split('/')
	src=s[-1].split('_lightcurve.npy')[0]
	o = np.load(lc).flat[0]
        _ts = o['ts']
	mjd=o['tmin_mjd']
	mjd_width = mjd[1]-mjd[0]
	mjd_middle=mjd+mjd_width
	flux=o['flux']/f_scale
	flux_err=o['flux_err']/f_scale
        ul = o['flux100_ul95']/f_scale
        #ul_er = 0. /f_scale
	N_pred=o['npred']
	bin_qual= o['fit_quality']

	condition=_ts<ts  #array of True/False
	#x=np.where(condition)  #array of positions where condition is True
  
	y = [ (ul[i] if condition[i] else flux[i]) for i in xrange(len(mjd_middle)) ]
	ye =[ (np.array(flux_err).mean()  if condition[i] else flux_err[i]) for i in xrange(len(mjd_middle)) ]
	npred=[ ( 0 if condition[i] else N_pred[i]) for i in xrange(len(mjd_middle)) ]
	## need to implement the key in fermipy
	#index = [ (0 if condition[i] else Ind[i]) for i in xrange(len(mjd_middle)) ]
	#indexe =[ (0 if condition[i] else Inde[i]) for i in xrange(len(mjd_middle)) ]

	return src,mjd_middle, mjd_width, flux, flux_err, ul, npred, bin_qual, condition


def plotLC(lc, ts='',f_scale=1e-8, where='./',save=False):
	plt.rcParams['legend.handlelength'] = 2.4
	plt.rcParams['legend.numpoints'] = 1
	plt.rcParams['legend.handletextpad']=0.9
	plt.rcParams['legend.markerscale']=0
	#plt.rcParams['lines.linewidth']=0
	
	left  = 0.075  # the left side of the subplots of the figure
	right = 0.975    # the right side of the subplots of the figure
	bottom = 0.06   # the bottom of the subplots of the figure
	top = 0.95      # the top of the subplots of the figure
	wspace = 0.08   # the amount of width reserved for blank space between subplots
	hspace = 0.3   # the amount of height reserved for white space between subplots

	grid_size = (2, 3)
	fig, axs = plt.subplots(nrows=2, ncols=3, sharex=False,figsize=(12,8))

	""" FERMIPY LC """
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
	""" --  reading the LC output in separete function --- """
	f_scale_label=str(f_scale).split('-0')[-1]
	ax0 =plt.subplot2grid(grid_size, (0, 0), rowspan=1, colspan=3)  ## <<--------
	ax0.set_ylabel('[$10^{-%s} ph cm^{-2} s^{-1}$]'%f_scale_label)
	ax0.set_xlabel('Time [MJD]')
	ax0.grid()
	
	src,mjd_middle, mjd_width, flux, fluxerr, ul, N_pred,bin_qual, lolims = getLCdata(lc,f_scale,ts=ts)
	plt.errorbar(mjd_middle,flux, xerr=mjd_width, yerr=fluxerr, uplims=lolims,
              color='green',marker='o',markersize=4,ls='none',label='%s (%i-day binning; TS>%.1f)'%(src,mjd_width,ts))

	## coming..
	## to be included if the Sun is within the ROI
	## plt. plot([timeSun0,timeSun0],[0,5], label='SUN',ls='dashed', c='red',linewidth=2.0)

	leg0 = ax0.legend()
	plt.legend(loc='upper left')
	ax0.axes.get_xaxis().set_visible(True)

	## HERE PLOT NPRED  // QUALITY
	ax1 =plt.subplot2grid(grid_size, (1, 0), rowspan=1, colspan=1)  ## <<--------
	ax1.set_ylabel('Flux/Flux_err')
	ax1.set_xlabel('Npred/sqrt(Npred)')
	#ax1.set_xlim(lt,rt)
	#ax1.set_ylim(-0.01,3)
	ax1.grid()
	
	ratio_F_Fe= flux/fluxerr
	ratio_Npred= N_pred/np.sqrt(N_pred)
	plt.errorbar(ratio_Npred, ratio_F_Fe, xerr=0, yerr=0, uplims=False,
              color='orange',marker='o',markersize=4,ls='none',label='')#,xnewF, F_(xnewF),'-',xnewF1, F_(xnewF1),'-',lw=2,label='LAT',color='green')#, xnew, f2(xnew), '--')

	## coming..
	## to be included if the Sun is within the ROI
	## plt. plot([timeSun0,timeSun0],[0,5], label='SUN',ls='dashed', c='red',linewidth=2.0)

	leg1 = ax1.legend()
	plt.legend(loc='upper left')
	ax1.axes.get_xaxis().set_visible(True)

	## HERE PLOT TSMAP
	what='pointsource_powerlaw_2.00_tsmap_sqrt_ts.png'
	img=mpimg.imread(where+what)
	newax = plt.subplot2grid(grid_size, (1, 1), rowspan=1, colspan=1)
	imgplot = plt.imshow(img)
	newax.imshow(img)
	newax.axis('off')

	## HERE PLOT SED
	what='%s_sed.png'%src
	img_sed = plt.imread(where+what)
	newax = plt.subplot2grid(grid_size, (1, 2), rowspan=1, colspan=1)
	imgplot = plt.imshow(img_sed)
	newax.axis('off')
	
	plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top,
		wspace=wspace, hspace=hspace)
		      
	if save==True: plt.savefig('%s_summary.pdf'%src,transparent=True)
	plt.show()


if __name__ == "__main__":
	#try: 
		lcfile=sys.argv[1]
		if sys.argv[2]: TS=float(sys.argv[2])
		plotLC(lcfile,ts=TS,save=True)
	#except: print 'usage::   python LC_file.npy  ts'
