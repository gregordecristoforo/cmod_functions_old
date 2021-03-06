import MDSplus as mds


def get_line_integrated_density(shot_number):
    """
    Extract line integrated density data.
    To get line-averaged density, you can use the function in this package, but it will only exist for certain shots.
    Otherwise divide by the chord length - this is derived from the equilibrium reconstruction.

    Args:
        shot_number: shot number(s) of interest.

    Returns:
        line_integrated_density_time: Time data for the ne_bar data.
        line_integrated_density: Line-integrated density measured in per sqaure metres (m^-2).
    """

    c = mds.Connection("alcdata")
    c.openTree("electrons", shot_number)

    line_integrated_density_dataname = "\ELECTRONS::TOP.TCI.RESULTS.NL_04"

    line_integrated_density = c.get(line_integrated_density_dataname).data()
    line_integrated_density_time = c.get(f"dim_of({line_integrated_density_dataname})").data()


    return line_integrated_density_time, line_integrated_density


def get_line_averaged_density(shot_number):
    """
    Extract line averaged density data.

    Args:
        shot_number: shot number(s) of interest.
                     NOTE: The data for a particular shot may not exist. 
                           They're only generated if someone asked for them previously.

    Returns:
        line_averaged_density_time: Time data for the ne_bar data.
        line_averaged_density: Line-averaged density measured in per cubic metres (m^-3).
    """

    c = mds.Connection("alcdata")
    c.openTree("electrons", shot_number)

    line_averaged_density_dataname = "\ELECTRONS::TOP.TCI.RESULTS.INVERSION.NEBAR_EFIT"

    line_averaged_density = c.get(line_averaged_density_dataname).data()
    line_averaged_density_time = c.get(f"dim_of({line_averaged_density_dataname})").data()


    return line_averaged_density_time, line_averaged_density


def get_plasma_current(shot_number):
    """
    Extract plasma current trace

    Args:
        shot_number: shot number(s) of interest.

    Returns:
        plasma_current_time: Time data for the plasma current data.
        plasma_current: Plasma current measures in  kilo Amps.
                        Negative sign means it's in the normal field direction.
                        Positive sign means it's in the reverse field direction.
    """

    c = mds.Connection("alcdata")
    c.openTree("magnetics", shot_number)

    plasma_current_dataname = "\MAGNETICS::IP/1000"
    plasma_current = c.get(plasma_current_dataname).data()
    plasma_current_time = c.get(f"dim_of({plasma_current_dataname})").data()

    return plasma_current_time, plasma_current


def get_toroidal_magnetic_field(shot_number):
    """
    Extract toroidal magnetic field data.

    Args:
        shot_number: shot number(s) of interest.

    Returns:
        toroidal_magnetic_field_time: time data for toroidal_magnetic_field data.
        toroidal_magnetic_field: toroidal magnetic field measured in Tesla (T).
    """

    c = mds.Connection("alcdata")
    c.openTree("magnetics", shot_number)

    toroidal_magnetic_field_dataname = "\MAGNETICS::BTOR"

    toroidal_magnetic_field = -c.get(toroidal_magnetic_field_dataname).data()
    toroidal_magnetic_field_time = c.get(f"dim_of({toroidal_magnetic_field_dataname})").data()


    return toroidal_magnetic_field_time, toroidal_magnetic_field


def average_plasma_parameter(
    variable_data, variable_time, time_start=None, time_end=None
):
    """
    Use: Calculates the average values of your plasma parameters

    Inputs:
        variable_data: Data of your variable.
                       This can be the plasma current, the line-averaged density, toroidal magnetic field etc.
        variable_time: Corresponding time data of your variable.
        time_start: The starting time of your time window.
                    Default set to None, which will take the minimum time of time data.
        time_end: The end time of your time window.
                  Default set to None, which will take the maximum time of time data.

    Outputs:
        variable_mean: Mean value of variable in the time window of choice.

    """

    if (time_start is None) & (time_end is None):
        time_start, time_end = np.amin(variable_time), np.amax(variable_time)

    time_interval = (variable_time < time_end) & (variable_time > time_start)
    variable_range = variable_data[time_interval]
    variable_mean = variable_range.mean()

    return variable_mean


def greenwald_density_limit(average_plasma_current, minor_radius=0.22):
    """
    Use: Calculates the Greenwald density limit

    Inputs:
        average_plasma_current: The average plasma current in Mega Amps.
        minor_radius: The minor radius in metres.
                      This is 0.22 metres for Alcator C-Mod by default.

    Outputs:
        greenwald_density_limit: The density limit in units of 10^20 m^-3.

    """
    return average_plasma_current / (np.pi * minor_radius * minor_radius)


def greenwald_fraction(average_line_averaged_density, greenwald_density):
    """
    Use: Calculates the Greenwald fraction which the ratio between the average line-averaged density and the Greenwald density limit.

    Inputs:
        average_line_averaged_density: The average line-averaged density in 10^20 m^-3 units.
        greenwald_density: The Greenwald density limit in 10^20 m^-3 units.

    Outputs:
        greenwald_fraction: The Greenwald fraction - should be between 0 and 1.

    """
    return average_line_averaged_density / greenwald_density
