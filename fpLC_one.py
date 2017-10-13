## script to plot the LC output 
## from fermipy,given a .npy file
## Sara Buson, Oct. 2017
## very basics, more coming  

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import sys

def plotLC(lc, f_scale=1e-8, save=False):
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

	grid_size = (1, 1)
	fig, axs = plt.subplots(nrows=1, ncols=1, sharex=False,figsize=(12,8))

	""" FERMIPY LC """
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

	""" --  reading the LC output --- """
	s=lc.split('/')
	src=s[-1].split('_lightcurve.npy')[0]
	o = np.load(lc).flat[0]
        ts = o['ts']
	mjd=o['tmin_mjd']
	mjd_width = mjd[1]-mjd[0]
	mjd_middle=mjd+mjd_width
	flux=o['flux']/f_scale
	flux_err=o['flux_err']/f_scale
        flux_ul = o['flux_ul95']/f_scale

	f_scale_lab=str(f_scale).split('-0')[-1]
	ax0 =plt.subplot2grid(grid_size, (0, 0), rowspan=1, colspan=1)  ## <<--------
	ax0.set_ylabel('[$10^{-%s} ph cm^{-2} s^{-1}$]'%f_scale_lab)
	ax0.set_xlabel('Time [MJD]')
	ax0.grid()
	
	ts_mask = ts>4
        ts_mask = np.asarray(ts_mask)
	plt.errorbar(mjd_middle[ts_mask],flux[ts_mask], xerr=mjd_width, yerr=flux_err[ts_mask], 
              color='orange',marker='o',markersize=4,ls='none',label='%s (%i-day binning)'%(src,mjd_width))#,xnewF, F_(xnewF),'-',xnewF1, F_(xnewF1),'-',lw=2,label='LAT',color='green')#, xnew, f2(xnew), '--')
        plt.plot(mjd_middle[~ts_mask],flux_ul[~ts_mask],color='grey',marker='v', ls='none',label='95% upper limits, if TS<4')

	## coming..
	## to be included if the Sun is within the ROI
	## plt. plot([timeSun0,timeSun0],[0,5], label='SUN',ls='dashed', c='red',linewidth=2.0)

	leg0 = ax0.legend()
	plt.legend(loc='upper left')
	ax0.axes.get_xaxis().set_visible(True)

	plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top,
		wspace=wspace, hspace=hspace)
		      
	if save==True: plt.savefig('%s_LC.pdf'%src,transparent=True)
	plt.show()

if __name__ == "__main__":
	#try: 
	lcfile=sys.argv[1]
	plotLC(lcfile,save=True)
	#except: print 'usage::   python LC_file.npy'

