# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 18:58:19 2016

@author: Geoff


docformat = 'rst'


:Describe the file...
    Makes various radar plots from NEXRAD Level 2 files
    Images created can be looped into a video file
 
:Categories:
    Radar
    
:Examples:
    Create an example

:Uses:
    pyart: ARM radar toolkit
    ffmpeg : open spourced video creating/editing software

:Author:
    Geoffrey Heidelberger, NWS IWX (Northern Indiana) 
        geoffrey.heidelberger@noaa.gov
   
:History:
    Modification History::
        First written: October 2016
        Dec 2016: Added a few city names to display (FWA,SBN, radar site)
        Jan 2017: Added keywords to change radar variable default ranges
                  Added county outlines to map display

"""


    
def gah_make_radar_plot(files,radVar,cplot='False', lat_range = 'false', \
                        lon_range = 'false', save=0, dbz_range = None, \
                        vel_range = None, zdr_range = None, cc_range = None, \
                        PhiDP_range = None, sw_range = None):
    
    """
    Reads in NEXRAD Level 2 radar data and can create a PPI plot of the radar
    variable that is specified. If user wants, the PPI plots created can be 
    save as png files 
    
    :Returns:
     None
    
    :Params:
    files : in, required, type=array of NEXRAD LV2 radar files
        set to 'pick' to create a pop up window to allow user to select file
    radVar : in, required, type = string array
        Radar variables that are allowed are:
            reflectivity, velocity, differential_reflectivity, 
            differential_phase, cross_correlation_ratio, spectrum_width
      
    :Keywords:
    cplot : in, optional, type=2 element array
        User defined center of the plot coordinates
        Format = [latitude, longitude]
        Defualted to center of radar
    lat_range : in, optional, type = 2 element array
        User definced latitude range to plot
        Format = [min_latititude, max_latitude]
    lon_range : in, optional, type = 2 element array
        User definced longitude range to plot
        Format = [min_longitude, max_longitude]
    save : in, optional, type = Boolean
        If set, png images will be created for each set of plots
    dbz_range : in, optional, type = 2 element array
        Range of reflectivity values to display
        Format = [min dbz, max dbz]
    vel_range : in, optional, type = 2 element array
        Range of velocity values to display
        Format = [min V, max V]
    zdr_range : in, optional, type = 2 element array
        Range of differential reflectivity values to display
        Format = [min Zdr, max Zdr]
    cc_range : in, optional, type = 2 element array
        Range of Correlation Coefficient values to display
        Format = [min CC, max CC]
    PhiDP_range : in, optional, type = 2 element array
        Range of differential phase values to display
        Format = [min PhiDP, max PhiDP]
    sw_range : in, optional, type = 2 element array
        Range of spectrum width values to display
        Format = [min sw, max sw]

    #todo: Add a keyword that allows users to add other cities of their choosing
    #todo: Add a keyword that allows users to change the sweep displayed. Right now only base scan
    #todo: Play around with color maps --> add a keyword to pick color maps
    #todo: Either have user define a save file directory or have a default one that works for all users
    
    """
    
    #Packages used
    import pyart
    import matplotlib.pyplot as plt
    import sys
    import numpy as np
    import math
    
    
    #what version of python am I using
    version = sys.version.split()
    if version[0][0] == '3':
        
        #Apparently, basemap is preinstalled for python 2.7
        from mpl_toolkits.basemap import Basemap
        
        import tkinter as tink
        from tkinter import filedialog
        
        #create a popup window to allow the user to select a radar file
        if files == 'pick':
            
            print('Please pick a file in the pop up window')
            root = tink.Tk()
            files = root.filename = \
                    filedialog.askopenfilename(initialdir = "/",title = "Select file",\
                    filetypes = (("radar files","*_V06"),("all files","*.*")), \
                    multiple = 1)
    
    elif version[0][0] == '2':
        import Tkinter as tink
        import tkFileDialog
        
         #create a popup window to allow the user to select a radar file
        if files == 'pick':
            
            print('Please pick a file in the pop up window')
            root = tink.Tk()
            files = root.filename = \
                        tkFileDialog.askopenfilename(initialdir = "/",\
                        title = "Select file",filetypes = (("radar files","*_V06"), \
                        ("all files","*.*")), multiple = 1)
    
    #print the filenames that were selected
    print (root.filename)
    
    #close the popup window when done
    root.destroy()

    #make radar plot for all files provided
    #how many files?
    nfiles = len(files)
    
    for count, file_num in enumerate(range(nfiles)):
    
        #read in radar file
        radar = pyart.io.read_nexrad_archive(files[file_num])
       
        #Begin to build a display of radar on a basemap
        display = pyart.graph.RadarMapDisplay(radar) 
        
        #get the time of the radar scan
        tmp = radar.time['units']
        tmp = tmp.split()
        date = tmp[2]
        year = date.split('-')[0] 
        mon = date.split('-')[1]
        day = date.split('-')[2][0:2]
        hr  = date.split('-')[2][3:5]
        mn  = date.split('-')[2][6:8]
        sec = date.split('-')[2][9:11]
        
        # time of file used for title and/or save image
        radar_time = year + mon + day + '_T' + hr + mn + sec
    
        #Radar site name
        split_file_name = files[file_num].split('/')
        rsite =  split_file_name[-1][0:4]

        #Id user does not define variable ranges then
        #default ranges for each radar variable
        if dbz_range is None:    
            dbz_range = (0,64)  #reflectivity
        if vel_range is None:        
            vel_range = (-20,20)  #velocity
        if zdr_range is None: 
            zdr_range = (-8,8)    #differential reflectivity
        if cc_range is None:
            cc_range =  (0.5,1)   #correlation coefficient
        if PhiDP_range is None:        
            PhiDP_range = (0,360) #differential Phase
        if sw_range is None:
            sw_range =  (0,20)    #spectrum width
        
        # Define the plot ranges
     
        #If center of plot is defined
        if cplot != 'False':
            lat_0 = cplot[0]
            lon_0 = cplot[1]
        
        # If not given then default to radar location as center of plot
        elif cplot == 'False':
            lat_0 = radar.latitude['data'][0]
            lon_0 = radar.longitude['data'][0]
         
        # MAKE THIS A KEYWORD FOR USER SPECIFIED RANGES  
        if lon_range == 'false':  
            min_lon = lon_0 - 2.25 ; max_lon = lon_0 + 2.25            
        else:
            min_lon = lon_range[0] ; max_lon = lon_range[1]
            
        if lat_range == 'false':    
            min_lat = lat_0 - 1.75 ;   max_lat = lat_0 + 1.75
        else:
            min_lat = lat_range[0] ; max_lat = lat_range[0]
                 
        #plot the data
        nplots = len(radVar)
        
        #Lets make a 2 collumn plot
        nrows = math.ceil(nplots/2.)
        if nplots < 2:
            ncols = 1
        else:
            ncols = 2
            
        plt.figure(figsize=[5*ncols,4*nrows])
        
        
         #plot each field
        for plot_num in range(nplots):
            field = radVar[plot_num]
    
            if field == 'reflectivity':
                vmin,vmax = dbz_range
                sweep = 0
                units = 'Z (dbZ)'
              
            elif field == 'velocity':
                vmin,vmax = vel_range
                sweep = 1
                units = 'Vr (m/s)'
            
            elif field == 'differential_reflectivity':
                vmin,vmax = zdr_range
                sweep = 0
                units = '$\mathsf{Z_{dr}}$ (dBz)'
            
            elif field == 'cross_correlation_ratio':
                vmin,vmax = cc_range
                sweep = 0
                units = '$\mathsf{rho_{hv}}$ (ratio)'
                
            elif field == 'spectrum_width':
                vmin,vmax = sw_range
                sweep = 1
                units = 'Knots'
                
            elif field == 'differential_phase':
                vmin,vmax = PhiDP_range
                sweep = 0
                units = 'Phi DP (deg)'
             
                #More?
                
            plt.subplot(nrows,ncols,plot_num + 1)
            #display.plot(field,sweep, vmin=vmin,vmax=vmax, title_flag='false')
            #display.set_limits(xlim=xlim, ylim=ylim)
            
              #Create a basemap with counties drawn   
            def draw_map_background(m):     
                    m.fillcontinents(color='#FAFAFA', zorder=0)
                    m.drawcounties()
                    m.drawstates()
                    m.drawcountries()
                    m.drawcoastlines()
                
            m = Basemap(llcrnrlon = min_lon, llcrnrlat = min_lat, urcrnrlon = max_lon, \
                            urcrnrlat = max_lat, rsphere=(6378137.00,6356752.3142), \
                            resolution='i', projection='lcc',lat_0=lat_0, lon_0=lon_0)
            
        
             
            draw_map_background(m)
           
            display = pyart.graph.RadarMapDisplay(radar)         
   
            
            
            display.plot_ppi_map(field, sweep=sweep, vmin=vmin, vmax=vmax,\
                     basemap = m, title = field , colorbar_label = units)
    
#            display.plot_ppi_map(field, sweep=sweep, vmin=vmin, vmax=vmax,\
#                     min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,\
#                     lon_lines=np.arange(math.floor(min_lon), math.ceil(max_lon), 1.), \
#                     projection='lcc', resolution='h',\
#                     lat_lines=np.arange(math.floor(min_lat), math.ceil(max_lat), 1.),\
#                     lat_0=lat_0, lon_0=lon_0,\
#                     title = field , colorbar_label = units)
            
            #Add city names
            FWA = ["Fort Wayne",41.0799,-85.1386]
            SBN = ["South Bend",41.6834,-86.2500]
            
            #Label offset from points
            offset = 0.01
            
            #Plot the city names
            if rsite == 'KIWX':
                display.plot_point(FWA[2],FWA[1])
                FWA_x,FWA_y = m(FWA[2], FWA[1])
                plt.text(FWA_x+offset,FWA_y+offset, FWA[0])
                
                display.plot_point(SBN[2],SBN[1])
                SBN_x,SBN_y = m(SBN[2],SBN[1])
                plt.text(SBN_x+offset, SBN_y + offset, SBN[0])
                
             #Indicate the radar location with a point
            display.plot_point(radar.longitude['data'][0], radar.latitude['data'][0])
            rad_x,rad_y = m(radar.longitude['data'][0],radar.latitude['data'][0])
            plt.text(rad_x + offset, rad_y + offset, rsite)
    
        plt.suptitle(rsite + ' ' +  radar_time + ' UTC')   
         
        #Do you want to save the radar images? 
        if save == 0:
            plt.show()
        
        elif save == 1:
            directory = 'C:\\Users\\geoffrey.heidelberge\\Documents\\SingleCell\\'
        
            #get time from radar scan to use at output file name
            #plt.savefig(directory + radar_time + '.png')
        
            # Name the files sequencially because time of radar
            # does not loop together for ffmpeg
            #counter for file name
            img_count = "{0:0=3d}".format(count)
            
            plt.savefig(directory + 'img_' + img_count + '.png')
                                      
        #close the plot
        plt.close()
    

        
#program to loop plots together
def gah_loop_radar(image_location, output_file_name = 'output.avi', fps = '1' ):
    
    
    """
    Loops together png images created by gah_make_radar_plot
    Requires ffmpeg to be installed in your path
    
    :Returns:
     None
    
    :Params:
    image_location : in, required, type=directory of where images are located
        set to emty string ('') to create a pop up window to allow user to select directory
      
    :Keywords:
    output_file_name : in, optional, type= string
        Name of video file created
        Tested for .avi video format 
    fps : in, optional, type = Numeric
        Frame rate in Frames per second
        Defaulted to 1 fps

    
    """
    #packages needed
    import subprocess
    import os
    import sys
    
    #if no directory is given a pop up box to choose one
    if image_location == '':
        
        #what version of python am I using
        version = sys.version.split()
        if version[0][0] == '3':
        
            import tkinter as tink
            from tkinter import filedialog
            
            root = tink.Tk()
            image_location = root.filename = filedialog.askdirectory\
                (initialdir = "/",title = "Select directory")
        
        elif version[0][0] == '2':
            import Tkinter as tink
            import tkFileDialog
    
            root = tink.Tk()
            image_location = root.filename = tkFileDialog.askdirectory\
                (initialdir = "/",title = "Select directory")
      
        #close the popup box
        root.destroy()
    
    #go to directory where radar images are saved
    os.chdir(image_location)
    
    #run ffmpeg to loop images together from the command line
    #subprocess.call('ffmpeg -r 1 -f image2 -start_number 000 -i img_%3d.png output_new.avi')
    subprocess.call('ffmpeg -r ' + fps + ' -f image2 -start_number 000 -i img_%3d.png ' + output_file_name)
   
    
    #Helpful stuff:

#-r 30: frame rate of 30 fps
#-f image2: tells the program that your images are in a list
#-start_number: number of the first image you want to use
#-i <name of images> _ <image counter> 
#%5d: counter is 5 digits long
#output.avi: output file name that you want

#this might be the way if ffmpeg could ever be found     
#subprocess.call('ffmpeg -r 1 -f image2 -start_number 001 -i img_%3d.png codec:v prores -profile:v 2 output.avi')   