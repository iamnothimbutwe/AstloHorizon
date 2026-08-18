


import click
from .astho import Asho
from rich.console import Console
#from rich.table import Table #table for showing astlo and astho horizons output.
import os
from importlib import resources
import time
import sys



try:
    
    from astlo import Contin, Vectors
except ModuleNotFoundError:
    raise ModuleNotFoundError(f'astlo is required for astlohorizons to run. install and then try again')

#handle the required version
contin  = Contin()

console = Console()
vectors = Vectors()

# ---------------------------------------------------------           # Copyright (c) 2026 Mark. All rights reserved.                       # Unauthorized copying of this file, via any medium, is               # strictly prohibited. Written by Mark (iamnothimbutwe) on Github.    # ---------------------------------------------------------


settings_root = resources.files('asho')
settings = settings_root / 'settings.txt'




@click.group()
@click.option('--reinfo','-re',default=None,help='giving a value to this will show the info tab')
@click.version_option(version='v0.1.100\nAstloHorizons an optional plugin to astlo. Property of Astlo Space Systems and r/kenyaspacenerds.\nThe ephemeris part is an open source property of NASA-JPL.\nAll rights reserved.')
@click.pass_context
def iam(ctx,reinfo=None):
   # if os.name=='nt':
    #    os.system('cls')
    #else:
     #   os.system('clear')

  #  settings_root = resources.files('asho')
   # settings = settings_root / 'settings.txt'

   # with open(settings,'r') as file:
  #      d = file.read().splitlines() #thebfirst line stores the value for explanation interface

    #if len(d)>1:
   #     pass
    #elif len(d)==0:

 #       console.print('[bold white]AstloHorizons. A plugin for Astlo that pulls data externally from the NASA-JPL SpiceKernels through skyfield.\n\nAstlo does not pull data from any external source.\nAstlo is accessible offline and so is AstloHorizons. AstloHorizons downside is that once the ephemeris expires, it will need to download updated ephemeris. The NASA-JPL ephemeris takes 1000s and 100s of years to expire though ;-)...\nThe default ephemeris file is de440.bsp for solar system objects.[/bold white]')
#
     #   enter = None #console.input('[bold white]Press any key to continue: [/bold white]')
    #    while enter==None:
   #         enter = console.input('[bold white]Press any key to continue: [/bold white]')

    if reinfo: #override
        sett('y') #override arg
    else:
        sett()


    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')

    if ctx.obj==None:
        ctx.obj = {'asho':Asho()}


def sett(override=None):
    '''the settings method'''
    ##checks if the file has inof value##

    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')


    with open(settings,'r') as file:
        d = file.read().splitlines() #thebfirst line stores the value for explanation interfac
        #if the first valie of the sett8ngs file is not None or contains a value, it does not show the info part.

    if len(d)>0:
        if d[0]=='True-info' and override==None: #first index is for this method, second is in astho module. astho settings dicontinued.
            print('\n.../\n')

    
        if d[0]!='True-info' and override==None:
            console.print('[bold white]AstloHorizons. A plugin for Astlo that pulls data externally from the NASA-JPL SpiceKernels through skyfield.\n\nAstlo does not pull data from any external source.\nAstlo is accessible offline and so is AstloHorizons. AstloHorizons downside is that once the ephemeris expires, it will need to download updated ephemeris. The NASA-JPL ephemeris takes 1000s and 100s of years to expire though ;-)...\nThe default ephemeris file is de440.bsp for solar system objects.\n\nIf the osculating elements relative the heliocenter and barycenter are needed, the respective orbital days, the gravitational accelerations, the 2D and 3D views, time stepping billions of years forwad and backwards,  use the main Astlo core engine.\n<Astlo Space Systems, r/kenyaspacenerds.>[/bold white]\n')
            time.sleep(30)

            with open(settings,'w') as file: #deletes the whole contents of the file and writes new.
                ret = file.write('True-info') #so as to continue and never print that again.


            enter = None #console.input('[bold white]Press any key to continue: [/bold white]')
            while enter==None:
                enter = console.input('[bold white]Press any key to continue: [/bold white]')
        
            print('\n.../\n')

            

    if override:
        with open(settings,'w') as file: #clears and rewrites
            data = file.write('not-info') #the override logic should clear the file and leave for next program/command call

        print('override - just call any command for the effect to take place')
        sys.exit(0) #the program should stop so that the user calls any command again for thw egfect to take place...sys.exit is better for the interface module...
            


@iam.command()
@click.option('--name','-n',default=None,help='the name of the object whose states are needed.\nNote that this method only works with solar system objects.',type=str)
@click.option('--relative','-re',default=None,help='give a value to this if the states of object Y relative object X are needed.\nuse it together with name if that is the case. name should be the object whose states are needed and relative should be the name of object that Y is relative to.',type=str)
@click.option('--ephem','-eph',default=440,help='the id of the solar shstem ephemeris that the user wishes to use.\ndiffrent ephemeris have diffrent experiry dates. They take 100s or even 1000s of years to expire though.\nEphemeris credit: NASA-JPL Spice Kernels\nAstlo is standalone and does not pull data externally.',type=int)
@click.option('--override','-ov',default=None,help='give a value to this if the user wants to understand the working of astlohorizons.')
@click.pass_context
def solsys(ctx,name,relative,ephem,override):

    if override:
        sett('y')
    elif override==None:
        sett()


    metric = ctx.obj['asho'].skysolsys(name,relative,ephem)
    if metric==None:
        return

    if name and relative==None:
        pos = []
        vel = []

        for _,idx in enumerate(metric['pos_vect']):
            pos.append(idx)
            vel.append(metric['vel_vect'][_])

#osc elems??

        console.print(f'\n[yellow]The states are relative the SSB. where the frame changes, it will be indicated.[/yellow]\n\n[cyan]Name: [/cyan][bold white]{metric['name']}[/bold white]\n[cyan]Time: [/cyan][bold white]{metric['time']} ¦ Unix:{metric['unix_time']} ¦ {metric['unix_time_simple']}[/bold white]\n[cyan]Position vector relative SSB: [/cyan][bold white]({pos[0]},{pos[1]},{pos[2]}) -km-[/bold white][yellow] magnitude = [/yellow][bold white]{metric['pos_magn']} -km- ¦ {(metric['pos_magn']*1000)/contin.AU_m} -AU-[/bold white]\n[cyan]Velocity vector relative SSB: [/cyan][bold white]({vel[0]},{vel[1]},{vel[2]}) km/s[/bold white][yellow] magnitude = [/yellow][bold white]{metric['vel_magn']} -km/s[/bold white]\n\n[cyan]Time: [/cyan][yellow]{metric['time']}[/yellow][magenta]¦ Unix-time ¦[/magenta][yellow] {time.time()} - {time.asctime()}[/yellow]\n')

        return

    if name and relative:
        pos = [] #the main object whose dtates were needed relative to X 
        vel = []
        pos_rel = [] #the object X that was relative to...relatuve SSB
        vel_rel = []
        nig = ['earth','moon']


        if name and relative in nig:
            defa = 'Earth-moon barycenter EMB'
        else:
            defa = '...'

        for _,idx in enumerate(metric['pos_vect']):
            pos.append(idx)
            vel.append(metric['vel_vect'][_])
            pos_rel.append(metric['pos_vect_rela'][_])
            vel_rel.append(metric['vel_vect_rela'][_])


        console.print(f'\n[yellow]The states are relative the SSB. where the frame changes, it will be indicated.\n{defa}[/yellow]\n\n[cyan]Name: [/cyan][bold white]{metric['name']} relative {metric['relative']}[/bold white]\n[cyan]Time: [/cyan][bold white]{metric['time']} ¦ Unix:{metric['unix_time']} ¦ {metric['unix_time_simple']}[/bold white]\n[cyan]{metric['name']} Position vector relative {metric['relative']}: [/cyan][bold white]({pos[0]},{pos[1]},{pos[2]}) -km-[/bold white][yellow] magnitude = [/yellow][bold white]{metric['pos_magn']} -km- ¦ {(metric['pos_magn']*1000)/contin.AU_m} -AU-[/bold white]\n[cyan]{metric['name']} Velocity vector relative {metric['relative']}: [/cyan][bold white]({vel[0]},{vel[1]},{vel[2]}) km/s[/bold white][yellow] magnitude = [/yellow][bold white]{metric['vel_magn']} -km/s[/bold white]\n[cyan]{metric['relative']} Position vector relative SSB: [/cyan][bold white]({pos_rel[0]},{pos_rel[1]},{pos_rel[2]}) -km-[/bold white][yellow] magnitude = [/yellow][bold white]{metric['pos_magn_rela']} -km- ¦ {(metric['pos_magn_rela']*1000)/contin.AU_m} -AU-[/bold white]\n[cyan]{metric['relative']} Velocity vector relative SSB: [/cyan][bold white]({vel_rel[0]},{vel_rel[1]},{vel_rel[2]}) -km/s-[/bold white][yellow] magnitude = [/yellow][bold white]{metric['vel_magn_rela']} -km/s-[/bold white]\n')
        return









@iam.command()
@click.option('--override','-ov',default=None,help='give a value to this if the user wants to understand the working of astlohorizons.')
@click.pass_context
def luna(ctx,override):

    if override:
        sett('y')
    else:
        sett()


    datluna = ctx.obj['asho'].luna()

    console.print('[bold white]The luna interface to the Earth-moon System. Astlo only shows the mean states for luna so astlohorizons was biult for tracking luna on top of astlo.\nThe frame here is the Earth-moon Barycenter EMB.\nThe raw inclination value is not corrected and therefore includes earth equitorial tilt relative the ecliptic. However the corrected value is included.\nThe Earth moon Barycenter EMB lies 4700km offset from earths center.[/bold white]\n')
    time.sleep(1.5)

    print('\n\ncontinuing.../')
    print('\n\n')

    console.print(f'''[yellow]The Earth-moon System relative the EMB - Earth-moon Barycenter[/yellow]\n[cyan]Name: [/cyan][bold white]{datluna['name']}[/bold white]\n[cyan]Time: [/cyan][bold white]{datluna['time']} ¦ Unix:{datluna['unix_time']} ¦ {datluna['unix_simple']}[/bold white]\n[cyan]Luna current distance relative EMB: [/cyan][bold white]{vectors.magn_vect(datluna['luna_pos_vect_rel_EMB'])/1000} -km-[bold white]\n[cyan]Luna current velocity relative EMB: [/cyan][bold white]{vectors.magn_vect(datluna['luna_vel_vect_rel_EMB'])/1000} -km/s-[/bold white]\n\n[yellow]Relative Earth true center -Geocenter-: [/yellow]\n[cyan]Luna current distance relative Geocenter: [/cyan][bold white]{vectors.magn_vect(datluna['moon_geo_pos_vect'])/1000} -km-[/bold white]\n[cyan]Luna current velocity relative Geocenter: [/cyan][bold white]{vectors.magn_vect(datluna['moon_geo_vel_vect'])/1000} -km/s-[/bold white]\n\n[yellow]current 'Phase'° degrees -emphasis on phase- and illumination element k.[/yellow]\n[cyan]Phase: [/cyan][bold white]{datluna['phase_deg']}°[/bold white]\n[cyan]Illumination element k and percentage k%: [/cyan][bold white]{datluna['face']} ¦ {datluna['face_perc']}%[/bold white]\n\n[cyan]Current Face: [/cyan][bold white]{ctx.obj['asho'].lunaface()}\n\n\n\n[yellow]Access the osculating elements through the SDK part of astlohorizons class Asho[/yellow]''')







        

##face recognization..do tht in astho....Done

##time..done..

##luna should be eye catching..almost..
