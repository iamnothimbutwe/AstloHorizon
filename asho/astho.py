
# Copyright © 2026 Mark Macharia [@iamnothimbutwe Github]
# All rights reserved.

#from astlo import __version__,Vectors
from skyfield.api import load
from rich.console import Console
import math
from collections.abc import Iterable
from importlib import resources
import time as ti

console = Console()

try:
    from astlo import Vectors,Contin

except ModuleNotFoundError:
    raise ModuleNotFoundError('Astlo is required to run. Please install then try again') #what if the program is already installed but the required version  for astlo is not met.
    #return 'astlo>=v5.63.53 not found'
    #sys.exit(0)
    #return

vectors = Vectors()
contin = Contin()



class Asho:
    def __init__(self):
        self.exp = 'the following are examples of NASA JPL ephemeris files.'
        self.eph_default = load('de440.bsp')
        self.eph_default_exp = 'de440 = Latest release, covers 1550–2650, improved accuracy.'
      #  self.eph_441 = load('de441.bsp')
     #   self.eph_441_exp = 'de441 = Extended long‑term version of DE440, 30,000 years.'      
   #     self.eph_430 = load('de430.bsp')
  #      self.eph_430_exp = 'de430 = High precision, 1550–2650, includes lunar librations.'
       # self.eph_431 = load('de431.bsp')
       # self.eph_431_exp = 'de431 = Ultra‑long range, 13,000 years (−13,200 to +17,191).'
       # self.eph_421 = load('de421.bsp')
       # self.eph_421_exp = 'de421 = Covers 1900–2050, lighter file, widely used.'
       # self.eph_422 = load('de422.bsp')
      #  self.eph_422_exp = 'de422 = Extended range, 3000 BC–3000 AD.'
      #  self.supported = #{421:self.eph_421,422:self.eph_422,430:self.eph_430,431:self.eph_431,{440:self.eph_default}#,441:self.eph_441}
        self.supported = {440:self.eph_default}

        datatxt = resources.files('asho')
        self.settings = datatxt / 'settings.txt'




    def skysolsys(self,name: str=None,relative: str=None,ephem: int=440):
        '''uses skyfield to pull live states from NASA-JPL ephemeris. the aim was to only use this method to track luna which is heavily purtubed by the sun and Earth. it can be used to pull any supported states for object X. use name if SSB states for that one object is needed. if example moon states relative earth are needed, use name 1st argumwnt as moon and relative 2nd argument as earth'''

        if name:
            name = name.lower()

        if relative:
            relative = relative.lower() #use relative if a bodys states relatjve object X are needed.eg if moon states relative earth are needed, pass moon as the name and earth as the value for relative

        if name==None:
            console.print('[red]Name of the target object is required.[/red]')
            return


        if name and relative==None:
            ephe = self.supported[ephem] #already loaded at the __init__
            try:
                obje = ephe[name]
            except KeyError as e:
                raise KeyError(f'passed name of object is not supported: {name}')

            ts = load.timescale()
            time = ts.now()
            astrometric = obje.at(time) #at() gives the body states relative SSB
            unix_time = ti.time()
            unix_time_simple = ti.asctime() 
            pos_vect = astrometric.position.km
            vel_vect = astrometric.velocity.km_per_s
            ls_pos = []
            ls_vel = []

            for _,idx in enumerate(pos_vect):
                ls_pos.append(idx)
                ls_vel.append(vel_vect[_])

            pos_magn = vectors.magn_vect(ls_pos)
            vel_magn = vectors.magn_vect(ls_vel)



            return {'pos_vect':pos_vect,'vel_vect':vel_vect,'vel_magn':vel_magn,'pos_magn':pos_magn,'units':'km and km/s','name':name,'frame':'SSB','time':time,'unix_time':unix_time,'unix_time_simple':unix_time_simple}

        if name and relative:
            
            ephe = self.supported[ephem]
            try:

                obje = ephe[name]
                rela = ephe[relative]
            except KeyError as e:
                raise KeyError(f'passed name of object or both objects is not supported: {name} ¦ {relative}')


            ts = load.timescale()
            time = ts.now() #you can add the repsective unix timw right now...bwcuas of the now() method used
            astrometric = rela.at(time).observe(obje) #observe() gives the states relatibe to body X
            astro2 = obje.at(time) #relative SSB
            astro3 = rela.at(time)
            unix_time = ti.time()
            unix_time_simple = ti.asctime()
            pos_vect = astrometric.position.km
            vel_vect = astrometric.velocity.km_per_s
            pos_obje = astro2.position.km #relative SSB
            vel_obje = astro2.velocity.km_per_s
            pos_rela = astro3.position.km
            vel_rela = astro3.velocity.km_per_s

           # print(pos_vect,vel_vect)
            ls_pos = []
            ls_vel = []
            ls_pos_2 = []
            ls_pos_3 = []
            ls_vel_2 = []
            ls_vel_3 = []

            for _,idx in enumerate(pos_vect):
                ls_pos.append(idx)
                ls_vel.append(vel_vect[_]) #relative body rela
                ls_pos_2.append(pos_obje[_])
                ls_vel_2.append(vel_obje[_]) #relative SSB
                ls_pos_3.append(pos_rela[_])
                ls_vel_3.append(vel_rela[_])

            pos_magn = vectors.magn_vect(ls_pos)
            vel_magn = vectors.magn_vect(ls_vel)
            pos_magn_2 = vectors.magn_vect(ls_pos_2)
            vel_magn_2 = vectors.magn_vect(ls_vel_2)
            pos_magn_3 = vectors.magn_vect(ls_pos_3)
            vel_magn_3 = vectors.magn_vect(ls_vel_3)



            return {'pos_vect':pos_vect,'vel_vect':vel_vect,'pos_magn':pos_magn,'vel_magn':vel_magn,'pos_vect_obje':pos_obje,'vel_vect_obje':vel_obje,'vel_obje_magn':vel_magn_2,'pos_obje_magn':pos_magn_2,'pos_vect_rela':pos_rela,'vel_vect_rela':vel_rela,'pos_magn_rela':pos_magn_3,'vel_magn_rela':vel_magn_3,'frame':f'pos_vect+magnitude and vel_vect+magnitude relative {rela} others variables relative SSB','units':'km and km/s','exp':f'{obje} as 1st argument relative {rela} as 2nd argument','time':time,'frame':'SSB','name':name,'relative':relative,'exp2':'if earth-moon system = True, the frame is relative the EMB. correct the vectors to get the true geocentric states.','time':time,'unix_time':unix_time,'unix_time_simple':unix_time_simple}




    def luna(self):
        '''luna the moon'''

      #  astrometric = self.sky('moon') #mooj relative SSB
        astromoon_rel_earth = self.skysolsys('moon','earth') #moon relative earth moon barycenter.....to get moons states relative earth true geocenter, subtract moons EMB states from Earths EMB states
        astromoon_rel_sol = self.skysolsys('moon','sun') #moon relatuve sol sun.....

        ##correcting the frame from EMB to geocentric true for inclination##
        astroearth_rel_moon = self.skysolsys('earth','moon')#earth relative EMB
       # ls_earth_emb_pos = [astroearth_rel_moon['pos_vect'][0],astroearth_rel_moon['pos_vect'][1],astroearth_rel_moon['pos_vect'][2]]
      #  ls_earth_emb_vel = [astroearth_rel_moon['vel_vect'][0],astroearth_rel_moon['vel_vect'][1],astroearth_rel_moon['vel_vect'][2]]
     #   moon_geocenter_pos = vectors.sub_vect() #pos vorrwction to geocentric true


        ls_pos = []
        ls_vel = []
        ls_moonearth_pos = [astromoon_rel_earth['pos_vect'][0]*1000,astromoon_rel_earth['pos_vect'][1]*1000,astromoon_rel_earth['pos_vect'][2]*1000]
        ls_moonsun_pos = [astromoon_rel_sol['pos_vect'][0]*1000,astromoon_rel_sol['pos_vect'][1]*1000,astromoon_rel_sol['pos_vect'][2]*1000]
        

        ##corrwctiom moved here##
 #       ls_earth_emb_pos = [astroearth_rel_moon['pos_vect'][0],astroearth_rel_moon['pos_vect'][1],astroearth_rel_moon['pos_vect'][2]]
  #      ls_earth_emb_vel = [astroearth_rel_moon['vel_vect'][0],astroearth_rel_moon['vel_vect'][1],astroearth_rel_moon['vel_vect'][2]]
   #     moon_geocenter_pos = vectors.sub_vect() #pos vorrwction to geocentric true

        for _,idx in enumerate(astromoon_rel_earth['pos_vect']):
            ls_pos.append(idx*1000) #relative EMB
            ls_vel.append(astromoon_rel_earth['vel_vect'][_]*1000) #meters


        ls_earth_emb_pos = [astroearth_rel_moon['pos_vect'][0]*1000,astroearth_rel_moon['pos_vect'][1]*1000,astroearth_rel_moon['pos_vect'][2]*1000]

        ls_earth_emb_vel = [astroearth_rel_moon['vel_vect'][0]*1000,astroearth_rel_moon['vel_vect'][1]*1000,astroearth_rel_moon['vel_vect'][2]*1000] #will convert to meters once the conversion to geocent is done..did it

        #to get the moon state vectors relative earth center##geocentric
        moon_geocenter_pos = vectors.sub_vect(ls_pos,ls_earth_emb_pos) #pos vorrwction to geocentric true
        moon_geocenter_vel = vectors.sub_vect(ls_vel,ls_earth_emb_vel)
####i tried the correction the subtractions to get the states relatuve earths center geocenter but it still gives that 28° inclination...
#eartgs equator is tilted 23° relative the ecliptic...so if i minus that 28 from 23 ill get 5°inclination for luna..

        ##osc elem##

        osc_elem_EMB = contin.oscelem(ls_pos,ls_vel) #relatuve EMB
      #  osc_elem_geocenter = contin.oscelem(moon_geocenter_pos,moon_geocenter_vel)
      #  i_geocenter = self.osci(moon_geocenter_pos,moon_geocenter_vel)

        osc_i_true = osc_elem_EMB['osc_i'] - contin.earth_equator_rel_ecliptic


        ##moon phase and face##
        dot_moon_sun = vectors.dot_vect(ls_moonearth_pos,ls_moonsun_pos)
        magn_moonearth_sun = vectors.magn_vect(ls_moonearth_pos,ls_moonsun_pos)
        phase_angle_cosine = (dot_moon_sun/magn_moonearth_sun[4])

        face = (1 + phase_angle_cosine)/2
        facetrunc_perc = (round(face,2)*100)

        phase_degrees = math.degrees(math.acos(phase_angle_cosine))

        return {'name':'luna','luna_pos_vect_rel_EMB':ls_pos,'luna_vel_vect_rel_EMB':ls_vel,'osc_elems_EMB':osc_elem_EMB,'osc_i_geocenter_ecliptic':osc_i_true,'phase_deg':phase_degrees,'face':face,'exp':'the states are relative the EMB except osc_i that requires a correction in the frames from EMB to geocentric True','units':'m and m/s','moon_geo_pos_vect':moon_geocenter_pos,'moon_geo_vel_vect':moon_geocenter_vel,'moongeo_magn_pos':vectors.magn_vect(moon_geocenter_pos),'moongeo_magn_vel':vectors.magn_vect(moon_geocenter_vel),'time':astromoon_rel_earth['time'],'unix_time':astromoon_rel_earth['unix_time'],'unix_simple':astromoon_rel_earth['unix_time_simple'],'face_perc':facetrunc_perc} #oscelem method returns the magnitudes of the two state vectors,,face is just the illumination elemnt k..



    def osci(self,r=None,v=None):
        '''gets the osculating element i'''

        if r==None or v==None:
            console.print('[red]requires both state vectors to continue[/red]')
            return
        

        if not isinstance(r,list) or not isinstance(v,list):
            return f'osci expected iterables but was given: {r} {v}'

        try:
            g=[]
            k=[]
            for _,idx in enumerate(r):
                g.append(float(idx))
                k.append(float(v[_]))

        except ValueError:
            raise ValueError(f'component type not supported: {idx} {v[_]}')

        h = vectors.cross_vect(g,k)#angular momwntum
        osc_i = math.degrees(math.acos(h[2]/h[3])) % 360

        return {'angular_momentum_h':h,'osc_i':osc_i}




    def lunaface(self):
        '''face recognition'''

        #k is 5he illumination element k##
        elemk = self.luna()
        k1 = elemk['face']
        ti.sleep(0.7)
        elemk2 = self.luna()
        k2 = elemk2['face']

        delta_k = k2 - k1  #if negative then waning and if positive the waxing
        if delta_k>0: #waxing
            exp = 'waxing'
        elif delta_k<0: #waning
            exp = 'waning'
        else:
            exp = '' #left out like that nkitaka

        k2_trunc = round(k2,2) #was using math.trunc hence the variable name
        
        Full_moon = [1.0,0.95,0.96,0.97,0.98,0.99]
        Half_moon = [0.5]
        New_moon = [0.0,0.01,0.02,0.03]


        if k2_trunc in Full_moon: #the keys
            return f'Full moon at {elemk2['face_perc']}% illumination'
        elif (k2_trunc not in Full_moon) and (k2_trunc not in Half_moon) and (k2_trunc not in New_moon) and k2_trunc>0.5: #gibbous..exp will apply the appr waxing waning phase..
            return f'{exp} Gibbous at {elemk2['face_perc']}% illumination'
        elif (k2_trunc not in Full_moon) and (k2_trunc not in Half_moon) and (k2_trunc not in New_moon) and k2_trunc<0.5:
            return f'{exp} Crescent at {elemk2['face_perc']}% illumination'
        elif k2_trunc in Half_moon: #donst have to be compec statmemtb k2trunc can only appear in one of the three full,half,new lists..
            return f'Half moon at {elemk2['face_perc']}% illumination'
        elif k2_trunc in New_moon:
            return f'New moon at {elemk2['face_perc']}% illumination'








