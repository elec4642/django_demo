# Create your views here.

from django.shortcuts import render
from map.models import Site
# import django-pandas to read Django qs into DF directly
from django_pandas.io import read_frame
import numpy as np
import datetime as dt
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import Vendors, get_provider
from bokeh.embed import components


def overview(request):
    return render (request, 'overview.html')

def site_list():

    # SELECT * FROM site_basic
    sites = Site.objects.all()
    # context = {'product_list':list_product}
    # #dict_product = dict(list_product)
    # return render(request, 'milk.html', context)
    geo_df_SC = read_frame(sites, fieldnames=['site_id','site_lat','site_long','site_cluster','site_state',
                                                        'site_rfnsa_id','site_status', 'site_last_end_date'])
    ########################## CALCULATION OF MERCATOR COORDINATE AND ADDITION IN NEW COLUMN ###########################
    geo_df_SC['site_lat'] = geo_df_SC['site_lat'].astype('float64')
    geo_df_SC['site_long'] = geo_df_SC['site_long'].astype('float64')
    # to calculate x,y mercator coordinates from long and lat
    r_major = 6378137
    geo_df_SC['long_merc'] = r_major * np.radians(geo_df_SC['site_long'])
    scale = r_major * np.radians(geo_df_SC['site_long']) / geo_df_SC['site_long']
    geo_df_SC['lat_merc'] = 180.0 / np.pi * np.log(np.tan(np.pi / 4.0 + geo_df_SC['site_lat'] * (np.pi / 180.0) / 2.0)) * scale

    ########################## CALCULATION OF MONTH INDEX AND ADDITION IN NEW COLUMN ###################################
    # calculate month index using apply on column 'month_index' added to DF
    # geo_df_SC['month_index'] = geo_df_SC['site_last_end_date']
    # geo_df_SC['month_index'] = geo_df_SC['month_index'].apply(return_month_index)

    ########################## Simplified Month Index Calculation ######################################################

    # change 'site_last_end_date' column to str type to strip year and month
    geo_df_SC['site_last_end_date'] = geo_df_SC['site_last_end_date'].astype('str')

    year_origin = dt.datetime.strptime('2018-03-01', '%Y-%m-%d').year
    month_origin = dt.datetime.strptime('2018-03-01', '%Y-%m-%d').month

    # strip year and month and save to two columns
    geo_df_SC['year'] = geo_df_SC['site_last_end_date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').year)
    geo_df_SC['month'] = geo_df_SC['site_last_end_date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d').month)

    # calculate month_index
    geo_df_SC['month_index'] = (geo_df_SC['year']-year_origin)*12+(geo_df_SC['month']-month_origin)

    return geo_df_SC

def map (site_df):
    # prepare data source to bokeh readable data
    site_CDS = ColumnDataSource(site_df)

    # select tile provider as openstreetmap
    tile_provider = get_provider(Vendors.OSM)

    # range bounds supplied in web mercator coordinates
    p = figure(x_range=(16793658, 16860450), y_range=(-4031487, -3997960),
               x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom")
    p.add_tile(tile_provider)
    source = site_CDS
    p.circle(x="long_merc", y="lat_merc", size=8, color='blue', line_width=3, fill_color='mediumblue', \
             fill_alpha=0.5, source=source)

    # axis details
    p.xaxis.axis_label = 'Longitude'
    p.xaxis.axis_label_text_font_size = '12pt'
    p.xaxis.axis_label_text_font_style = 'normal'
    p.xaxis.axis_label_text_font = 'Segoe UI'
    p.yaxis.axis_label = 'Latitude'
    p.yaxis.axis_label_text_font_size = '12pt'
    p.yaxis.axis_label_text_font_style = 'normal'
    p.yaxis.axis_label_text_font = 'Segoe UI'

    # configure visual properties on a plot's title attribute
    p.title.text = "Demo Map"
    p.title.align = "center"
    p.title.text_color = "orange"
    p.title.text_font_size = "25px"
    p.title.background_fill_color = "#aaaaee"


    # Hover too setup
    hover_mth = HoverTool()
    hover_mth.tooltips = [
        ('Site ID', '@site_id'),
        ('RFNSA ID', '@site_rfnsa_id'),
        ('Cluster', '@site_cluster'),
        ('Site progress', '@site_status'),
    ]

    # add hover tool
    p.add_tools(hover_mth)

    script, div = components(p)
    return script, div

def demo_map(request):
    site = site_list()
    script, div = map(site_df=site)
    return render(request, 'map.html', {'map_script': script, 'map_div': div,})



