# Radar

Code to read in and display radar data

# gah_make_radar_plot
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
        
"""

# gah_loop_radar

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

