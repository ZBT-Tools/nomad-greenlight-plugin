from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

import os
import numpy as np
import pandas as pd
from collections import defaultdict
# import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import Quantity, SchemaPackage
from nomad.metainfo.data_type import m_str, m_float64

from nomad_greenlight_plugin import read_files as rf
import pint

configuration = config.get_plugin_entry_point(
    'nomad_greenlight_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


def decorator(cls):
    cls.initialize_quantities()
    return cls


def convert_units(units: dict):
    unit_conversion = {
        'dimensionless': ['N/A', '<enum>', '%', 'CYCLES',
                          'OFF/ON', 'POINTS', 'False/True'],
        'liter/minute': ['NLPM'],
        'deg': ['�'],
        'degC': ['�C'],
        'A/cm�': ['A/cm**2']
    }
    # Reverse key-value-order in unit_conversion dict
    uc_rev = {}
    for key, value in unit_conversion.items():
        for item in value:
            uc_rev[item] = key
    # Convert unit strings
    for key, value in units.items():
        if value in uc_rev:
            units[key] = uc_rev[value]
    return units


def make_quantity_dict(create_objects=True):
    # Initialize all data quantities from empty template csv file
    empty_file_path = os.path.join(os.path.dirname(__file__), 'greenlight_empty.csv')
    data_file_object = rf.read_single_file(empty_file_path)
    columns = data_file_object.data.columns
    units = convert_units(data_file_object.units)
    df = data_file_object.data
    type_dict = df.dtypes.to_dict()
    for k, v in type_dict.items():
        if isinstance(v, np.dtypes.ObjectDType):
            type_dict[k] = str
    quantities = {}
    for col in columns:
        if create_objects:
            try:
                quantities[col] = Quantity(type=type_dict[col], shape=['*'],
                                           unit=units[col])
            except (pint.errors.UndefinedUnitError, ValueError, AttributeError):
                quantities[col] = Quantity(type=type_dict[col], shape=['*'],
                                           unit='dimensionless')
        else:
            quantities[col] = "Quantity(type={}, shape=['*'], unit='{}')\n".format(
                type_dict[col], units[col])
    return quantities


def write_quantity_file():
    create_objects = True
    quantities = make_quantity_dict(create_objects=create_objects)
    quantity_file = os.path.join(os.path.dirname(__file__), 'quantities.py')
    with open(quantity_file, 'w') as file:
        if create_objects:
            for key, value in quantities.items():
                file.write("{} = Quantity(type={}, shape=['*'], unit='{}')\n".format(
                    key, value.type, value.unit))
        else:
            for key, value in quantities.items():
                file.write("{} = {})\n".format(key, value))


# write_quantity_file()


# @decorator
class GreenlightSchemaPackage(PlotSection, Schema):
    name = Quantity(
        type=str, a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    message = Quantity(type=str)

    time_stamp = Quantity(type=m_str(), shape=['*'], unit='dimensionless')
    elapsed_time = Quantity(type=m_float64(), shape=['*'], unit='second')
    file_mark = Quantity(type=m_str(), shape=['*'], unit='dimensionless')
    anode_inlet_rel_hum = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    anode_inlet_rel_hum_calc = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    anode_recipe_selector = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    anode_stoich = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    anode_stoich_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    anode_total_reactant_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cathode_inlet_rel_hum = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cathode_inlet_rel_hum_calc = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cathode_recipe_selector = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cathode_stoich = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cathode_stoich_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cathode_total_reactant_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cell_active_area = Quantity(type=m_float64(), shape=['*'], unit='centimeter')
    cell_count_total = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cell_voltage_001 = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_max = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_max_alarm = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_max_warning = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_mean = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_min = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_min_alarm = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_min_warning = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_open_cct = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cell_voltage_std = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cell_voltage_total = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    concentration_anode_h2 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    concentration_anode_h2_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    concentration_anode_n2 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    concentration_anode_n2_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    concentration_cathode_air = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    concentration_cathode_air_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    concentration_cathode_n2 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    concentration_cathode_n2_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    const_not_a_number = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    current = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    current_density = Quantity(type=m_float64(), shape=['*'], unit='ampere / centimeter ** 2')
    current_direction = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    current_internal_set = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    current_match_ratio = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    current_ramping_enable_flag = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    current_range_max = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    current_range_min = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    current_range_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    current_set = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    cv01_apex1_voltage_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cv01_apex2_hold_time_set = Quantity(type=m_float64(), shape=['*'], unit='second')
    cv01_apex2_voltage_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cv01_apex_scan_rate_set = Quantity(type=m_float64(), shape=['*'], unit='volt / second')
    cv01_clear_plot = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cv01_cycles_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cv01_final_hold_time_set = Quantity(type=m_float64(), shape=['*'], unit='second')
    cv01_final_scan_rate_set = Quantity(type=m_float64(), shape=['*'], unit='volt / second')
    cv01_final_voltage_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cv01_hold_time_set = Quantity(type=m_float64(), shape=['*'], unit='second')
    cv01_init_delay_set = Quantity(type=m_float64(), shape=['*'], unit='second')
    cv01_initial_hold_time_set = Quantity(type=m_float64(), shape=['*'], unit='second')
    cv01_initial_scan_rate_set = Quantity(type=m_float64(), shape=['*'], unit='volt / second')
    cv01_initial_voltage_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    cv01_meas_mode_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cv01_op_mode_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cv01_sample_mode_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cv01_sample_rate_set = Quantity(type=m_float64(), shape=['*'], unit='second')
    cv01_save_data = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cv01_save_image = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    cv01_scan_rate_set = Quantity(type=m_float64(), shape=['*'], unit='volt / second')
    cv01_start = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    deltat_mode = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    deltat_temp_coolant_diff = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    deltat_temp_coolant_diff_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    e_stop_cct_ready = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_ac_current_set = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    eis01_ac_voltage_set = Quantity(type=m_float64(), shape=['*'], unit='millivolt')
    eis01_add_plot = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_clear_plot = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_dc_current = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    eis01_dc_current_max_set = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    eis01_dc_current_min_set = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    eis01_dc_current_set = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    eis01_dc_voltage = Quantity(type=m_float64(), shape=['*'], unit='volt')
    eis01_dc_voltage_max_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    eis01_dc_voltage_min_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    eis01_dc_voltage_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    eis01_estimated_hfr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_estimated_z_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_final_frequency_set = Quantity(type=m_float64(), shape=['*'], unit='hertz')
    eis01_frequency = Quantity(type=m_float64(), shape=['*'], unit='hertz')
    eis01_ie_range = Quantity(type=m_float64(), shape=['*'], unit='volt')
    eis01_imag_z = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_initial_frequency_set = Quantity(type=m_float64(), shape=['*'], unit='hertz')
    eis01_max_voltage_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    eis01_model_no = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_modulus_z = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_op_mode_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_phase_z = Quantity(type=m_float64(), shape=['*'], unit='degree')
    eis01_points_per_decade_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_real_z = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_repeat_time_set = Quantity(type=m_float64(), shape=['*'], unit='minute')
    eis01_sample_mode_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_save_data = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_save_image = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_single_frequency_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_start = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_stdev_z = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    eis01_timestamp_z = Quantity(type=m_float64(), shape=['*'], unit='second')
    eis01_total_time_set = Quantity(type=m_float64(), shape=['*'], unit='hour')
    flow_anode_h2_mfc_total = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    flow_anode_h2_mfc_total_set = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    flow_anode_n2_mfc_total = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    flow_anode_n2_mfc_total_set = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    flow_cathode_air_mfc_total = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    flow_cathode_air_mfc_total_set = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    flow_cathode_n2_mfc_total = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    flow_cathode_n2_mfc_total_set = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    flow_control_alarm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    flow_control_disable = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    flow_coolant = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    flow_coolant_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    gas_purge_duration_estop = Quantity(type=m_float64(), shape=['*'], unit='second')
    gas_purge_duration_manual = Quantity(type=m_float64(), shape=['*'], unit='second')
    gas_purge_manual_request = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    gisys_no_alarms = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    gisys_no_loggers = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    gisys_no_overrides = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    gisys_no_scripts = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    gisys_no_warnings = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_dewpoint_a_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_dewpoint_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_dewpoint_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_endplate_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_endplate_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_heattape_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_heattape_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_humid_outlet_heattape_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_anode_humid_outlet_heattape_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_dewpoint_a_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_dewpoint_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_dewpoint_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_endplate_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_endplate_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_heattape_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_heattape_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_humid_outlet_heattape_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_cathode_humid_outlet_heattape_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_coolant_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heater_coolant_ssr = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heaters_enable = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    heaters_overtemp_shutdown = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    level_alarm_disable = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    level_anode_humid_high = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    level_anode_humid_low = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    level_cathode_humid_high = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    level_cathode_humid_low = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    level_coolant_high = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    level_coolant_low = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    load_follow_flag = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    min_stoich_current_set = Quantity(type=m_float64(), shape=['*'], unit='ampere')
    mode = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    mode_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    power = Quantity(type=m_float64(), shape=['*'], unit='watt')
    power_match_ratio = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    power_range_max = Quantity(type=m_float64(), shape=['*'], unit='watt')
    power_range_min = Quantity(type=m_float64(), shape=['*'], unit='watt')
    power_set = Quantity(type=m_float64(), shape=['*'], unit='watt')
    pressure_anode_bpc = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_anode_bpc_disable = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_anode_cathode_diff = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_anode_coolant_diff = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_anode_in_out_diff = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_anode_inlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_anode_inlet_absolute = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_anode_inlet_error = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_anode_lock_diff_limit = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_anode_lock_in_transition = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_anode_min_lock = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_anode_outlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_anode_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_cathode_bpc = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_cathode_coolant_diff = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_cathode_in_out_diff = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_cathode_inlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_cathode_inlet_absolute = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_cathode_inlet_error = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_cathode_lock_diff_limit = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_cathode_lock_in_transition = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_cathode_min_lock = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_cathode_outlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_cathode_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_coolant_bpc = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_coolant_in_out_diff = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_coolant_inlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_coolant_inlet_absolute = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_coolant_inlet_error = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_coolant_lock_diff_limit = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_coolant_lock_in_transition = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_coolant_min_lock = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_coolant_outlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_coolant_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_lock_cathode = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_lock_coolant = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_lock_lines_selection = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_lock_pause_flag = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_lock_ramp_diff = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_lock_ramp_step = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_lock_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_lock_step_timeout = Quantity(type=m_float64(), shape=['*'], unit='millisecond')
    pressure_nitrogen_supply = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_stack_compression = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_stack_compression_diff = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_stack_compression_diff_limit = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_stack_compression_inlet_error = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pressure_stack_compression_lock_in_transition = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pressure_stack_compression_min_lock = Quantity(type=m_float64(), shape=['*'], unit='kilopascal')
    pump_anode_dewpoint_on = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pump_cathode_dewpoint_on = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    pump_coolant_on = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    rh_calc_anode_01 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    rh_calc_anode_02 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    rh_calc_cathode_01 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    rh_calc_cathode_02 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    safeguard_flag_purging = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    scattergraph_add_point = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    scattergraph_clear_plot = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    scattergraph_profile_name = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    scattergraph_remove_point = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    scattergraph_sample_size = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    scattergraph_save_file = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    scattergraph_sort = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_e_stop = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_h2_sensor = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_h2_sensor_second = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_relay_fs_alarm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_relay_lvs_alarm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_reset_btn = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_shutdown = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_wd_read = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_in_zero_volt_pws_fault = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_e_stop = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_echem_on = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_flow_coolant_ip = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_light_green = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_light_red = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_pressure_anode_ip = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_pressure_cathode_ip = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_pressure_coolant_ip = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_pressure_stack_compression_ip = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_shutdown = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    signal_out_wd_hit = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    system_state = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    system_state_set = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_anode_cathode_diff = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_coolant_diff = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_dewpoint = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_dewpoint_heattape_ts = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_anode_dewpoint_puckheater_a_tsh = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_anode_dewpoint_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_dewpoint_water = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_endplate = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_endplate_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_gas_inlet_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_heattape = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_humid_outlet_heattape = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_humid_outlet_heattape_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_humid_outlet_heattape_ts = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_anode_in_out_diff = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_inlet = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_anode_inlet_heattape_ts = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_anode_outlet = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_coolant_diff = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_dewpoint = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_dewpoint_heattape_ts = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_cathode_dewpoint_puckheater_a_tsh = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_cathode_dewpoint_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_dewpoint_water = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_endplate = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_endplate_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_gas_inlet_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_heattape = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_humid_outlet_heattape = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_humid_outlet_heattape_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_humid_outlet_heattape_ts = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_cathode_in_out_diff = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_inlet = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_cathode_inlet_heattape_ts = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_cathode_outlet = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_chiller_return = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_coolant_heater = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_coolant_heater_tsh = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    temp_coolant_hex_outlet = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_coolant_in_out_diff = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_coolant_inlet = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_coolant_outlet = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    temp_coolant_set = Quantity(type=m_float64(), shape=['*'], unit='degree_Celsius')
    total_anode_stack_flow = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    total_anode_stack_flow_set = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    total_cathode_stack_flow = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    total_cathode_stack_flow_set = Quantity(type=m_float64(), shape=['*'], unit='liter / minute')
    valve_anode_dewpoint_hex_outlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_anode_dewpoint_hex_outlet_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_anode_dry_bypass = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_anode_h2_mfc_high = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_anode_humid_drain = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_anode_humid_fill = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_anode_humid_outlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_anode_n2_mfc_high = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_anode_n2_purge = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_air_mfc_high = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_dewpoint_hex_outlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_dewpoint_hex_outlet_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_dry_bypass = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_humid_drain = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_humid_fill = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_humid_outlet = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_n2_mfc_high = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_cathode_n2_purge = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_chiller_supply = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_coolant_drain = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_coolant_fill = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_di_coolant_hex_out = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_di_coolant_hex_out_pwm = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    valve_h2_supply = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_01 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_02 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_03 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_04 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_05 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_06 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_07 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_08 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_09 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_10 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_11 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_12 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_13 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_14 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_15 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_16 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_17 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_18 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_19 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_20 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_21 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_22 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_23 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_24 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_25 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_26 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_27 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_28 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_29 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    variable_30 = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    vlc_start_request = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    voltage = Quantity(type=m_float64(), shape=['*'], unit='volt')
    voltage_match_ratio = Quantity(type=m_float64(), shape=['*'], unit='dimensionless')
    voltage_range_max = Quantity(type=m_float64(), shape=['*'], unit='volt')
    voltage_range_min = Quantity(type=m_float64(), shape=['*'], unit='volt')
    voltage_set = Quantity(type=m_float64(), shape=['*'], unit='volt')
    time = Quantity(type=m_float64(), shape=['*'], unit='second')

    # Initial intention was to dynamically create the attributes with the
    # initialize_quantities classmethod, however since this classmethod can only
    # be called by the decorator afterward, the attributes are not completely
    # registered in the nomad system. Therefore, a manual attribute assignment
    # is used
    @classmethod
    def initialize_quantities(cls):
        quantities = make_quantity_dict()
        # Dynamically assign dictionary entries as object attributes
        for key, value in quantities.items():
            setattr(cls, key, value)
        setattr(cls, 'quantity_names',  list(quantities.keys()))

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        if logger is not None:
            logger.info('GreenlightSchema.normalize',
                        parameter=configuration.parameter)
        archive.metadata.entry_name = self.name

        # Make plot
        # Add figure
        plot_df = pd.DataFrame(
            dict(date_time=self.date_time,
                 current_density=self.current,
                 cell_voltage=self.cell_voltage_total))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add lines
        fig.add_trace(go.Scatter(x=plot_df['date_time'], y=plot_df['cell_voltage'], name="Cell Voltage / V"),
                      secondary_y=False)
        fig.add_trace(go.Scatter(x=plot_df['date_time'], y=plot_df['current'], name="Cell Voltage / V"),
                      secondary_y=True)
        # Set x-axis title
        fig.update_xaxes(title_text="Time / s")
        # Set y-axes titles
        fig.update_yaxes(title_text="Voltage / V", secondary_y=False)
        fig.update_yaxes(title_text="Current / A", secondary_y=True)
        self.figures.append(PlotlyFigure(fig.to_plotly_json()))

        # figure = px.line(plot_df, x='date_time', y='cell_voltage')
        # fig.add_scatter(x=plot_df['date_time'], y=plot_df['current'], mode='lines')
        # self.figures.append(
        #    PlotlyFigure(
        #        figure=px.line(
        #            pd.DataFrame(
        #                dict(
        #                    date_time=self.date_time,
        #                    current=self.current,
        #                    cell_voltage=self.cell_voltage_total,
        #                )
        #            ),
        #            x='current_density',
        #           y='cell_voltage',
        #        ).to_plotly_json()
        #    )
        # )


m_package.__init_metainfo__()
