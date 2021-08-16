#%%
c = 299_792_458
h = 6.62607004e-34
e = 1.60217662e-19
num = 4.135667516e-15*c/1e-9


def ev_to_joules(ev, **kwargs):
    return e*ev
def joules_to_ev(joules, **kwargs):
    return joules/e

def joules_to_hz(joules, **kwargs):
    return joules/h
def hz_to_joules(hz, **kwargs):
    return hz*h

def ev_to_hz(ev, **kwargs):
    return joules_to_hz(ev_to_joules(ev))
def hz_to_ev(hz, **kwargs):
    return joules_to_ev(hz_to_joules(hz))

def nm_to_hz(nm, laser):
    return (c/(laser*1e-9) - c/(nm*1e-9))

def hz_to_nm(hz, laser):
    return 1e9/(1/(laser*1e-9) - hz/c)

def cm_to_hz(cm, **kwargs):
    return cm*c*100
def hz_to_cm(hz, **kwargs):
    return 0.01*hz/c

def thz_to_hz(thz, **kwargs):
    return thz*1e12
def hz_to_thz(hz, **kwargs):
    return hz*1e-12

conversions = {'to_hz':
                        {'nm': nm_to_hz,
                        'ev': ev_to_hz,
                        'cm': cm_to_hz,
                        'thz': thz_to_hz},
                'hz_to': {'nm': hz_to_nm,
                        'ev': hz_to_ev,
                        'cm': hz_to_cm,
                        'thz': hz_to_thz}
                }

if __name__ == '__main__':
    laser = 633
    print(hz_to_nm(cm_to_hz(500), laser))

# %%
