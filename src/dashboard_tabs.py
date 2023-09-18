import dash_bootstrap_components as dbc
import pandas as pd 
from dash import html
from datetime import datetime
from hawker_data import GetHawkerData
from hawker_visualization import GetHCFigures
from dash import dash_table
import pytz 

def CreateHCMapTab():
    """
    Function:   Create the HC Map Tab using the figure filename
    """
    HCMapTab = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P(f"Accurate as of: {datetime.now(pytz.timezone('Asia/Singapore')).strftime('%d %b %Y %H:%M:%S')}"),
                    html.Iframe(
                        id = "hawker-map",
                        srcDoc = open("hawker-centres.html", "r").read(),
                        width = "100%",
                        height = "500",
                    ),
                    html.Br(),
                ]
            )
        ]
    )
    return HCMapTab

def CreateDataTable(hawker_df, hawker_centre_df, columns_params_dict_list = None):

    hawker_df, rename_cols_dict = CleanUpHawkerDataFrame(hawker_df, hawker_centre_df)
    numeric_cols = ["No of Market Stalls", "No of Food Stalls"]
    datetime_cols = ["Closure Start Date", "Closure End Date"]
    
    columns_params_dict_list = []
    for val in rename_cols_dict.values():
        data_type = "text"
        if val in numeric_cols:
            data_type == "numeric"
        elif val in datetime_cols:
            data_type = "datetime"

        columns_params_dict_list.append({"name":val, "id":val, "type":data_type})

    table = dash_table.DataTable(
        columns = columns_params_dict_list,
        data = hawker_df.to_dict('records'),
        filter_action = 'native',
        sort_action="native",
        style_data = {
            'textOverflow': 'ellipsis',
        },
        style_cell = {
            "whiteSpace": "normal",
            "height":"auto",
            'textAlign': 'left'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
    )

    return table


def CreateTableTab(hawker_df, hawker_centre_df):
    hawker_df, _ = CleanUpHawkerDataFrame(hawker_df, hawker_centre_df)

    table_tab = dbc.Table.from_dataframe(
        hawker_df, 
        striped=True, 
        bordered=True, 
        hover=True
        )
    return table_tab

def MapHCStatus(colour):
    HC_status_dict = {"Open":["green"],
                    "Closing within a month":["orange","#FF5F1F"],
                    "Closed":["red",]}
    for key, val in HC_status_dict.items():
        if colour in val:
            return key

def CleanUpHawkerDataFrame(hawker_df, hawker_centre_df):
    hawker_df = hawker_df.merge(hawker_centre_df, on = "clean_name", how = "left")

    # Change colour to status
    hawker_df["status"] = hawker_df["colour"].map(MapHCStatus)

    # Change dates to string
    hawker_df["startdate"] = hawker_df["startdate"].apply(lambda dt_obj: dt_obj.date())
    hawker_df["enddate"] = hawker_df["enddate"].apply(lambda dt_obj: dt_obj.date())

    # Proper sentence for activity
    hawker_df["activity"] = hawker_df["activity"].apply(lambda string: string.capitalize())

    # Reorder cols
    cols = ["clean_name", "address_myenv", "description_myenv", "no_of_market_stalls", "no_of_food_stalls", 
            "activity", "startdate", "enddate", "status"]
    hawker_df = hawker_df[cols]

    # Rename cols
    rename_cols_dict = {"clean_name":"Hawker Name", "address_myenv":"Hawker Address", "description_myenv":"Hawker Description", 
                        "no_of_market_stalls": "No of Market Stalls", "no_of_food_stalls": "No of Food Stalls", 
                        "activity":"Closure Activity", "startdate":"Closure Start Date", "enddate":"Closure End Date",
                        "status":"Current Status" }
    hawker_df.rename(columns = rename_cols_dict, inplace = True)

    return hawker_df, rename_cols_dict


def CreateDashboardTabs(n_limit = 200):
    """
    Function:   Create the necessary tabs for the dashboard
    """
    hawker_centre_df, cleaning_dates_df, remarks_df = GetHawkerData()
    open_hawkers_df, closing_1month_df, currently_closed_df = GetHCFigures(n_limit)

    # Combine the 3 hawker dfs
    hawker_df = pd.concat([open_hawkers_df, closing_1month_df, currently_closed_df])
    hawker_df.sort_values("clean_name", inplace = True)

    # Create tabs
    hc_map_tab = CreateHCMapTab()
    hawker_table_tab = CreateDataTable(hawker_df, hawker_centre_df)

    return hc_map_tab, hawker_table_tab





