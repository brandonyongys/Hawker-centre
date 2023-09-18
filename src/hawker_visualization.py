import pandas as pd 
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import folium
from hawker_data import GetHawkerData
import pytz 

def GetCutOffDates():
    """
    Function:  Get today's date as well as today's date in 1 month time
    """
    date_today = datetime.now(pytz.timezone('Asia/Singapore')).replace(tzinfo=None)
    date_today_1month_later = date_today + relativedelta(months=1)
    return date_today, date_today_1month_later

def GetNextClosureDates(cleaning_dates_df, date_today):
    """
    Function: Get the latest closure dates for each hawker centre. If the centre is currently closed, get that closure dates.
    """
    criteria_1 = cleaning_dates_df["startdate"] >= date_today
    criteria_2 = cleaning_dates_df["startdate"] <= date_today
    criteria_3 = date_today <= cleaning_dates_df["enddate"] 
    master_criteria = criteria_1 | (criteria_1 & criteria_2)
    
    closure_dates_df = cleaning_dates_df[master_criteria].copy()
    closure_dates_df = closure_dates_df.sort_values(["clean_name", "startdate"], ascending = True).drop_duplicates("clean_name")
    closure_dates_df.reset_index(inplace = True, drop = True)
    return closure_dates_df

def GetCurrentlyClosedHC(cleaning_dates_df, date_today):
    """
    Function: Get the currently closed hawkers
    """
    criteria_1 = cleaning_dates_df["startdate"] <= date_today
    criteria_2 = date_today <= cleaning_dates_df["enddate"] 
    master_criteria = criteria_1 & criteria_2
    currently_closed_df = cleaning_dates_df[master_criteria].copy()
    currently_closed_hc_list = currently_closed_df["clean_name"].unique().tolist()
    return currently_closed_df, currently_closed_hc_list

def GetClosureIn1MonthHC(cleaning_dates_df, date_today, date_today_1month_later):
    """
    Function: Get the hawker centres that would close in 1 month time
    """
    criteria_1 = cleaning_dates_df["startdate"] >= date_today
    criteria_2 = date_today_1month_later >= cleaning_dates_df["startdate"]
    master_criteria = criteria_1 & criteria_2 
    closing_1month_df = cleaning_dates_df[master_criteria].copy()
    closing_1month_hc_list = closing_1month_df["clean_name"].unique().tolist()
    return closing_1month_df, closing_1month_hc_list

def GetCurrentlyOpenHC(currently_closed_df, closing_1month_df, cleaning_dates_df, date_today_1month_later):
    """
    Function: Get hawker centres that are currently open and would not be closing in 1 month time
    """
    criteria_1 = cleaning_dates_df["clean_name"].isin(currently_closed_df["clean_name"].unique().tolist())
    criteria_2 = cleaning_dates_df["clean_name"].isin(closing_1month_df["clean_name"].unique().tolist())
    criteria_3 = cleaning_dates_df["startdate"] > date_today_1month_later
    master_criteria = ~(criteria_1 | criteria_2) & criteria_3
    open_hawkers_df = cleaning_dates_df[master_criteria].copy().drop_duplicates("clean_name")
    open_hawkers_list = open_hawkers_df["clean_name"].unique().tolist()
    return open_hawkers_df, open_hawkers_list

def CreateDescr(dataframe):
    """
    Function: Create description for the different hawker centres. The description will be used for plotting purpose.
    """
    descr = f'{dataframe["clean_name"]}'
    startdate = dataframe['startdate'].strftime('%d %b %Y')
    enddate = dataframe['enddate'].strftime('%d %b %Y')
    
    if dataframe["colour"] in ["green"]:
        descr += f" currently open. Next closure is from {startdate} to {enddate}."
    elif dataframe["colour"] in ["orange", "#FF5F1F"]:
        descr += f" will be closed soon from {startdate} to {enddate}." 
    elif dataframe["colour"] in ["red"]:
        descr += f" is currently closed until {enddate}."
    return descr

def PrepareVisData(dataframe, point_colour, hawker_centre_df):
    """
    Function: Prepare dataframe for visualization.
                1) Point colour
                2) Description to be plotted
    """
    dataframe["colour"] = point_colour
    dataframe["descr"] = dataframe.apply(CreateDescr, axis = 1)

    cols = ['clean_name', 'latitude_hc', 'longitude_hc']
    dataframe = dataframe.merge(hawker_centre_df[cols], on = "clean_name")
    return dataframe

def PlotDot(row, folium_map):
    """
    Function:   Plot the different hawker centre point the Singapore map
    """
    folium.CircleMarker(location = [row["latitude_hc"], row["longitude_hc"]],
                        radius=1.5,
                        weight=5,
                        color = row["colour"],
                        opacity=0.65,
                        tooltip = row["descr"]).add_to(folium_map)

def PlotHawkerCentres(dataframe_list):
    """
    Function:   Plot each hawker centres as a coloured dot in a Singapore folium map
    """
    kw = {"location":[1.3521, 103.8198], "zoom_start":11.5}
    folium_map = folium.Map(**kw)

    for dataframe in dataframe_list:
        for row in dataframe.iterrows():
            PlotDot(row[1], folium_map)

    folium_map.save("hawker-centres.html")


def GetHCFigures(n_limit = 200):
    """
    Function:   Get hawker data then plot and create hawker centre figure
    """
    hawker_centre_df, cleaning_dates_df, remarks_df = GetHawkerData(n_limit)

    date_today, date_today_1month_later = GetCutOffDates()
    cleaning_dates_df["startdate"] = pd.to_datetime(cleaning_dates_df['startdate'], format = "%d/%m/%Y")
    cleaning_dates_df["enddate"] = pd.to_datetime(cleaning_dates_df['enddate'], format = "%d/%m/%Y")

    # Various tables
    currently_closed_df, currently_closed_hc_list = GetCurrentlyClosedHC(cleaning_dates_df, date_today)
    closing_1month_df, closing_1month_hc_list = GetClosureIn1MonthHC(cleaning_dates_df, date_today, date_today_1month_later)
    open_hawkers_df, open_hawkers_list = GetCurrentlyOpenHC(currently_closed_df, closing_1month_df, cleaning_dates_df, date_today_1month_later)

    # Prepare visualization data
    open_hawkers_df = PrepareVisData(open_hawkers_df, "green", hawker_centre_df) # green
    closing_1month_df = PrepareVisData(closing_1month_df, "#FF5F1F", hawker_centre_df) # orange #FF5F1F
    currently_closed_df = PrepareVisData(currently_closed_df, "red", hawker_centre_df) # red 

    # Plot figures
    PlotHawkerCentres([open_hawkers_df, closing_1month_df, currently_closed_df])

    return open_hawkers_df, closing_1month_df, currently_closed_df


if __name__ == "__main__":
    open_hawkers_df, closing_1month_df, currently_closed_df = GetHCFigures(200)