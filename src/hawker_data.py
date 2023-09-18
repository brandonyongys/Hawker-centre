import requests
import pandas as pd 
import re

def FetchData(n_limit = 200):
    """
    Function:  get data from data.gov.sg API.
               Returns a json file with 3 keys ['help', 'success', 'result']
    """
    api_link = f"https://data.gov.sg/api/action/datastore_search?resource_id=b80cb643-a732-480d-86b5-e03957bc82aa&limit={n_limit}"
    return requests.get(api_link).json()

def GetRawData(n_limit = 200):
    # Fetch and convert json to dataframe
    raw_data = FetchData(n_limit)
    raw_data_df = pd.DataFrame(raw_data["result"]["records"])

    # Remove unwanted columns
    raw_data_df.drop(columns = ["serial_no",  "google_3d_view"], inplace = True)

    # Reorder columns
    cols = ['name','description_myenv','address_myenv', 'no_of_market_stalls', 'no_of_food_stalls', 
            'status', 'latitude_hc', 'longitude_hc', 'photourl',
            'q1_cleaningstartdate','q1_cleaningenddate','q2_cleaningstartdate','q2_cleaningenddate',  
            'q3_cleaningstartdate','q3_cleaningenddate', 'q4_cleaningstartdate', 'q4_cleaningenddate',
            'other_works_startdate','other_works_enddate',
            'remarks_q1','remarks_q2','remarks_q3', 'remarks_q4', 'remarks_other_works']
    raw_data_df = raw_data_df[cols]
    return raw_data_df

def CleanUpName(name):
    """
    Function: Extract the HC names in brackets if any.
    """
    pattern = r"\((.*)\)"
    try:
        return re.search(pattern, name).group(1)
    except:
        return name
        
def SplitRawData(raw_data_df):
    raw_data_df.rename(columns = {"name":"original_name"}, inplace = True)
    raw_data_df["clean_name"] = raw_data_df["original_name"].apply(lambda name: CleanUpName(name))
    
    hc_cols = ['original_name', 'clean_name', 'description_myenv','address_myenv', 'no_of_market_stalls', 'no_of_food_stalls', 
            'status', 'latitude_hc', 'longitude_hc', 'photourl']
    cleaning_cols = ['clean_name',
            'q1_cleaningstartdate','q1_cleaningenddate','q2_cleaningstartdate','q2_cleaningenddate',  
            'q3_cleaningstartdate','q3_cleaningenddate', 'q4_cleaningstartdate', 'q4_cleaningenddate',
            'other_works_startdate','other_works_enddate']
    remarks_cols = ['clean_name',
                    'remarks_q1','remarks_q2','remarks_q3', 'remarks_q4', 'remarks_other_works']
    
    hawker_centre_df = raw_data_df[hc_cols].copy()
    cleaning_dates_df = raw_data_df[cleaning_cols].copy()
    remarks_df = raw_data_df[remarks_cols].copy()
    
    return hawker_centre_df, cleaning_dates_df, remarks_df
    
def CleanUpHCData(hawker_centre_df):
    """
    Function:  Clean up HC Dataframe
    """
    hawker_centre_df["latitude_hc"] = hawker_centre_df["latitude_hc"].astype(float)
    hawker_centre_df["longitude_hc"] = hawker_centre_df["longitude_hc"].astype(float)

    return hawker_centre_df

def ExtractClosureType(activity_name):
    pattern = r"(.*)?((start|end)date)"
    result = re.search(pattern, activity_name)
    activity, datetype = result.group(1), result.group(2)

    activity = re.sub("_", " ", activity).strip()
    return activity, datetype
    
def CleanUpDatesData(cleaning_dates_df):
    """
    Function:   Convert the df from wide to long. Remove any non-date rows
                
    """
    # Convert wide to long df
    cleaning_dates_df = cleaning_dates_df.melt(id_vars = ["clean_name"], var_name = "activity", value_name = "date")
    
    # Clean up non-dates row
    criteria_1 = cleaning_dates_df["date"] != "TBC"
    criteria_2 = cleaning_dates_df["date"] != "NA"
    master_criteria = criteria_1 & criteria_2
    cleaning_dates_df = cleaning_dates_df[master_criteria]

    # Clean up the activity
    cleaning_dates_df["result"] = cleaning_dates_df["activity"].apply(lambda activity_name: ExtractClosureType(activity_name))
    cleaning_dates_df["activity"] = cleaning_dates_df["result"].apply(lambda result: result[0])
    cleaning_dates_df["datetype"] = cleaning_dates_df["result"].apply(lambda result: result[1])

    # Remove cols
    cleaning_dates_df.drop(columns = ["result"], inplace = True)

    # Convert to wide table
    cleaning_dates_df = pd.pivot(cleaning_dates_df, index = ["clean_name", "activity"],
               columns = "datetype",
               values = "date").reset_index()

    cols = ["clean_name", "activity", "startdate", "enddate"]
    cleaning_dates_df = cleaning_dates_df[cols]
    return cleaning_dates_df

def ExtractRemarkType(activity_name):
    pattern = r"(remarks)_(.*)"
    result = re.search(pattern, activity_name)
    activity = result.group(2)
    activity = re.sub("_", " ", activity).strip()
    if activity.startswith("q"):
        activity += " cleaning"
    return activity
    
def CleanUpRemarksData(remarks_df):
    """
    Function:   Convert the df from wide to long. Remove any non-date rows
                
    """
    # Convert wide to long df
    remarks_df = remarks_df.melt(id_vars = ["clean_name"], var_name = "activity", value_name = "remarks")
    
    # Remove nil remarks
    criteria_1 = remarks_df["remarks"] != "nil"
    remarks_df = remarks_df[criteria_1]
    
    # Extract remarks period
    remarks_df["activity"] = remarks_df["activity"].apply(lambda activity_name: ExtractRemarkType(activity_name))
    return remarks_df

def GetHawkerData(n_limit = 200):
    # Get raw data
    raw_data_df = GetRawData(n_limit)
    
    # Split into 3 dfs 
    hawker_centre_df, cleaning_dates_df, remarks_df = SplitRawData(raw_data_df)
    
    # Preprocess df
    hawker_centre_df = CleanUpHCData(hawker_centre_df)
    cleaning_dates_df = CleanUpDatesData(cleaning_dates_df)
    remarks_df = CleanUpRemarksData(remarks_df)
    
    return hawker_centre_df, cleaning_dates_df, remarks_df


if __name__ == "__main__":
    hawker_centre_df, cleaning_dates_df, remarks_df = GetHawkerData()