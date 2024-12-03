import os
import numpy as np
import pandas as pd
from echem_data import electrochem_data as ed
from operator import itemgetter


def reset_dtype(data_frame: pd.DataFrame):
    for col, col_type in data_frame.dtypes.items():
        if not isinstance(col_type, float):
            try:
                data_frame[col] = data_frame[col].astype(float)
            except ValueError:
                data_frame[col] = data_frame[col].astype(str)
    return data_frame


def read_single_file(file_path, first_file_mark=None):
    data_file_object = ed.EChemDataFile(file_path, 'Greenlight')
    new_columns = {col: col.lower().replace(" ", "_").replace(".", "_")
                   for col in data_file_object.data.columns}
    data_file_object.data.rename(columns=new_columns, inplace=True)
    data = reset_dtype(data_file_object.data).copy()
    data_file_object.units = {new_columns[k]: v for k, v
                              in data_file_object.units.items()}
    if first_file_mark is not None:
        data.loc[0, 'file_mark'] = first_file_mark
    data['file_mark'] = data['file_mark'].ffill()
    date_time = pd.to_datetime(data['time_stamp'])
    nanoseconds = date_time.values.astype(np.int64)
    seconds = nanoseconds * 1e-9
    data['time'] = seconds
    data_file_object.data = data.copy()
    data_file_object.units['time'] = 's'
    return data_file_object


def read_multiple_files_and_combine(mainfile, root_name, split_char='_'):
    dir_path = os.path.dirname(mainfile)
    file_list = [file for file in os.listdir(dir_path) if root_name in file]
    sorted_file_list = sorted(
        file_list, key=lambda x: itemgetter(-1)(x.split(split_char)))
    first_file_mark = None
    data_file_objects = []
    for file in sorted_file_list:
        data_file_object = read_single_file(mainfile, first_file_mark)
        first_file_mark = data_file_object.data['file_mark'].iloc[-1]
        print(first_file_mark)
        data_file_object.data.set_index('time', inplace=True)
        data_file_objects.append(data_file_object)
    data_frame = pd.concat(
        [dfo.data for dfo in data_file_objects], join='outer')
    data_frame = data_frame.reset_index()
    data_file_object = data_file_objects[0]
    data_file_object.data = data_frame
    return data_file_object


def read_files(mainfile):
    split_char = '_'
    file_name = os.path.basename(mainfile)
    sub_names = file_name.split('.')[-2].split(split_char)
    root_name = split_char.join(sub_names[:-1])
    try:
        file_number = int(sub_names[-1])
    except ValueError:
        file_number = None
    if file_number is not None:
        # Load multiple files
        data_file_object = read_multiple_files_and_combine(
            mainfile, root_name, split_char=split_char)
    else:
        # Load stand-alone file
        data_file_object = read_single_file(mainfile)
    return data_file_object
