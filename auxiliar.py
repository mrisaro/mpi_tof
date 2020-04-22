## Auxiliar functions for Mass Spec analyisis

#%% Libraries I need
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
from scipy.io import savemat

#%% Functions to load

def fun_load_mat(file):
    data = loadmat(file)       # data in .mat file

    y1 = data['datos']['data1'][0][0]           # store ch1 data in np array
    y2 = data['datos']['data2'][0][0]           # store ch2 data in np array
    y3 = data['datos']['data3'][0][0]           # store ch2 data in np array
    y4 = data['datos']['data4'][0][0]           # store ch4 data in np array
    t  = data['datos']['t'][0][0]
    BNC = data['datos']['BNC'][0][0]            # store BNC struct. in dict.

    try:
        Euv = data['datos']['Euv'][0][0]
        return y1,y2,y3,y4,t,BNC,Euv
    except:
        return y1,y2,y3,y4,t,BNC


#%% Functions to analyze temporal signals

def fun_plot_mass(masa,sp):
    plt.figure(1,figsize=(10, 6))
    plt.subplot(221)
    plt.plot(masa, sp)
    plt.xlim(10,20)
    plt.grid(linestyle='--')
    plt.tight_layout()
    plt.pause(0.5)

    plt.subplot(222)
    plt.plot(masa, sp)
    #plt.xlim(24,34)
    plt.xlim(38,42)
    plt.grid(linestyle='--')
    plt.tight_layout()
    plt.pause(0.5)

    plt.subplot(223)
    plt.plot(masa, sp)
    plt.xlim(45,50)
    plt.grid(linestyle='--')
    plt.tight_layout()
    plt.pause(0.5)


    plt.subplot(224)
    plt.plot(masa, sp)
    plt.xlim(83,88)
    plt.grid(linestyle='--')
    plt.tight_layout()
    plt.pause(0.5)

def fun_find_pk(t,sp):
    mx = np.max(sp)
    q1,_ = np.where(t<1e-6)
    sp[q1] = np.random.normal(np.mean(sp[q1]), 0.05e-3, len(q1))
    locs,_ = find_peaks(sp,distance=500, height = [mx/100,mx])
    pk_sort = np.argsort(sp[locs])
    pk_sort = pk_sort[::-1]
    locs = locs[pk_sort[0:5]]

    return locs

# Function to perform the mass calibration
def fun_mass_calib(t,sp):

    locs = fun_find_pk(t,sp)
    my_dpi = 72
    plt.figure(1,figsize=(800/my_dpi, 600/my_dpi), dpi=my_dpi)
    plt.plot(t*1e6,sp)
    plt.plot(t[locs]*1e6,sp[locs],'*',markersize=10)
    plt.xlim(0,20)
    plt.grid(linestyle='--')
    plt.tight_layout()
    plt.pause(1)
    ar = list(map(int,input('Que masas son? (en orden):  ').split()))
    plt.close('1')
    p = np.polyfit(np.sqrt(ar),t[locs],1)

    kt = np.where(t>p[1])
    masa = ((t[kt]-p[1])/p[0])**2

    # check that the calibration works
    fun_plot_mass(masa,sp[kt[0]])

    plt.pause(0.5)
    comm = input('Lacalibración es correcta? (si/no):  ')
    if comm == 'si':
        plt.close('all')
        return masa, kt, p
    elif comm == 'no':
        plt.close('all')
        plt.pause(0.5)
        fun_mass_calib(t,sp)

    return masa, kt, p

# Function that detects peaks amplitude
def fun_pk(masa,sp,pk):
    z_pk = np.where((masa>pk-0.35)&(masa<pk+0.35))  # peak zone
    z_b1 = np.where((masa>pk-0.65)&(masa<pk-0.35))  # left baseline zone
    z_b2 = np.where((masa>pk+0.35)&(masa<pk+0.65))  # right baseline zone

    s_pk = np.max(savgol_filter(sp[z_pk],9,2))      # Savitsky filter in pk zone
    s_b1 = np.min(savgol_filter(sp[z_b1],9,2))      # Savitsky filter in bl zone
    s_b2 = np.min(savgol_filter(sp[z_b2],9,2))      # Savitsky filter in bl zone

    peak  = np.max(s_pk)-np.mean([s_b1,s_b2])   # Define peak amplitude
    m_vec = np.where(sp[z_pk]>peak/2)
    m_vec = m_vec[0]
    del_m = masa[z_pk[0][m_vec[-1]]]-masa[z_pk[0][m_vec[0]]]
    return peak, del_m

def fun_bunch_pk(masa,sp,pks):
    n = len(pks)
    pk_list = np.zeros(n)
    wi_list = np.zeros(n)

    for jj in range(n):
        pk_list[jj], wi_list[jj] = fun_pk(masa,sp,pks[jj])

    return pk_list, wi_list

def fun_gen_file(masa,sp,p,file):
    savemat(file,{'masa': masa, 'sp': sp, 'p':p})
