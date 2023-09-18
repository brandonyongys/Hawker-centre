from dash import dcc 

info_tab = dcc.Markdown(
    """
## Background

This is a simple application developed by me to illustrate the current status as well as the closure dates of the different hawker centres across Singapore. 
This dashboard is purely for hawker centres managed by the Government of Singapore and does not include privately owned kopitiam, food centres etc. 
This may be a future improvement however it would require a significant effort to search and collate the closure dates as well as the specific food court details.

This dashboard is built using the data provided [data.gov.sg](https://data.gov.sg/dataset/dates-of-hawker-centres-closure). 
Should there be any inaccuracy in the hawker centre details, unfortunately I would not be able to correct it as this dashboard is merely a 
visualization of the provided data.

The inspiration of this Singapore Hawker Centre Dashboard is drawn from Benedict Soh's dengue dashboard post that I found [here](https://towardsdatascience.com/creating-a-web-application-to-analyse-dengue-cases-1be4a708a533).
I am thankful for his post as it formed the basis of this dashboard, which I subsequently adapted and tuned it to my liking. :) 
Of course there is still much to learn with regard to building a very informative and value adding dashboard.

My code may be found here: https://github.com/brandonyongys/Hawker-centre

If you have any feedback or suggestion, please feel free to contact me at byongys@gmail.com. 



## Concepts:
1. Dash by Plotly - Web framework in Python
1. Folium - Geospatial analytics


## Resources:
1. Data: https://data.gov.sg/dataset/dates-of-hawker-centres-closure


"""
)