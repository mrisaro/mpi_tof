# Auxiliar functions for GenTec signals


def fun_gentec(t,signal):
    q1 = np.where(t<-1e-3)
    q2 = np.where((t>0)&(t<5e-3))

    bl = np.mean(savgol_filter(signal[q1[0]],19,2))
    pk = np.max(savgol_filter(signal[q2[0]],19,2))

    pk = pk-bl

    return pk
