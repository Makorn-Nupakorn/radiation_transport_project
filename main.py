""" 
for usage of this project

1. You have to setting a config in "config.yaml"
2. run set of command in "run.sh" bash script
3. If you want to add an environment more than .venv, you can use "source .venv/bin/activate" for activation an environment

## Command for testing

sh run.sh

"""
from memory_profiler import profile
from typing import NoReturn, Any
from itertools import product
from rich import print
import yaml
import math

def read_config_file(file_path: str) -> dict:
    """Reads a configuration from a yaml file.

    Parameters:
        file_path `str` : The path to the pickle file.

    Returns:
        config `dict` : The configuration stored in the yaml file.
    """

    with open("config.yaml", "rb") as stream:
        try:
            config: dict = yaml.safe_load(stream)

        except yaml.YAMLError as exc:
            print(exc)

    return config

class Volume:
    """Class for calculating volume from neutron per volume.
    """
    def __init__(self, config_file: str) -> NoReturn:
        
        config: dict = read_config_file(config_file)
        

        self.parameter = config.get("config", "")
        parameter_values = list(self.parameter.values())

        self.check_parameters(parameter_values)

        self.radius: float | int = self.parameter.get("radius", 50)
        self.delta_radius_division: float | int = self.parameter.get("delta_radius_division", 10)
        self.azimuth_angle_division: float | int = self.parameter.get("azimuth_angle_division", 12)
        self.rotation_angle_division: float | int = self.parameter.get("rotation_angle_division", 9)

        # Check zero division
        try:
            self.delta_radius: float | int = self.radius / self.delta_radius_division
            self.azimuth_angle: float | int = math.pi / self.azimuth_angle_division
            self.rotation_angle: float | int = (2 * math.pi) / self.rotation_angle_division

        except ZeroDivisionError as e:
            return print(e)
        
        self.alpha = abs(self.test_sphere_equation() / self.calculate_volume_total())
    
    def __str__(self) -> str:
        """Text for checking a configuration.

        Parameters:
            None

        Returns:
            text_configs `str` : return configuration of calculator
        """

        config_function = self.parameter
        config_keys = list(config_function.keys())

        text_configs = "Configuration \n======================\n"
        
        for key in config_keys:

            text_config = f"{key} is {config_function.get(f"{key}", "No value specified")}"
            text_configs += f"{text_config} unit\n"
        
        return text_configs
    def check_parameters(self, parameter: dict) -> NoReturn:
        """_summary_

        Returns:
            NoReturn: _description_
        """
        for value in parameter:
            if (value < 0):
                raise ValueError("Parameter must be non-negative.")
            
        for value in parameter[1:]:
            if not isinstance(value, int):
                raise TypeError("Parameter must be an integer.")
            
    def _cartesian_product(self) -> product:
        """Cross product function for cartesian product.

        Parameters:
            None

        Returns:
            cartesian_product `product` : cartesian matrix
        """
        cartesian_product = product(range(1, self.delta_radius_division + 1), 
                                    range(1, self.azimuth_angle_division + 1), 
                                    range(1, self.rotation_angle_division + 1))
        
        return cartesian_product

    def get_neutron_per_volume(self, main_radius: float | int) -> float | None:
        """Calculates the neutron per volume.

        Parameters:
            main_radius `float or int` : radius that we focus on sphere

        Returns:
            neutron `float or int` : neutron per volume
        """
        
        a_constant: float | int = 1 / math.sinh(1)

        try:
            neutron: float | int = (10**5) * (1 - (a_constant * math.sinh(main_radius / self.radius)))
        
        except ZeroDivisionError as e:
            return print(e)

        return neutron
    
    def calculate_volume_total(self) -> float:
        """Calculates the total of volume in the shpere.

        Parameters:
            None

        Returns:
            V_total `float` : Total of volume
        """

        V_total: float | int = 0

        for i, j, k in self._cartesian_product():

            radius_i: float | int = (i - 0.5) * self.delta_radius
            theta_j: float | int = (j - 0.5) * self.azimuth_angle

            neutron_per_volume = self.get_neutron_per_volume(radius_i)

            V_total += self.delta_radius * (radius_i * self.azimuth_angle) * (radius_i * math.sin(theta_j) * self.rotation_angle)

        return round(V_total, 3)
    
    def calculate_neutron_total(self):
        """Function to calculate total of neutron.

        Parameters:
            None

        Returns:
            neutron_total `float` : Total of neutron
        """

        neutron_total: float | int = 0
            
        for i, j, k in self._cartesian_product():

            radius_i: float | int = (i - 0.5) * self.delta_radius
            theta_j: float | int = (j - 0.5) * self.azimuth_angle

            neutron_per_volume: float | int = self.get_neutron_per_volume(radius_i)

            volume: float | int = self.delta_radius * (radius_i * self.azimuth_angle) * (radius_i * math.sin(theta_j) * self.rotation_angle)

            neutron_total += neutron_per_volume * volume * self.alpha

        return round(neutron_total)
    
    def get_volume_total(self) -> float | None:
        """Function to calculate total of volume.

        Parameters:
            None

        Returns:
            V_total `float or None` : Total of volume
        """

        V_total: float | int = self.calculate_volume_total()

        test_volume: float | int = self.test_sphere_equation()
        check: bool = (self.alpha >= 0.99)

        if check is True:
            self.get_message(check)
            return round(V_total, 3)
    
        else:
            self.get_message(check)
            print(f"Error: Volume Total is not match Neutron Total")

    def get_neutron_current(self, radius: float | int) -> float:
        """_summary_

        Args:
            radius (float | int): _description_

        Returns:
            float: _description_
        """

        radius: float | int = self.radius
        neutron_total: float | int = self.calculate_neutron_total()

        neutron_current: float | int = neutron_total / (4 * math.pi * (radius ** 2))

        return round(neutron_current)
    
    def test_sphere_equation(self) -> bool:
        """Function to test result of sphere equation with total of volume.

        Parameters:
            None

        Returns:
            volume_equation `float` : Total volume from the sphere equation
        """

        radius: float | int = self.radius
        volume_equation: float | int = (4/3) * (math.pi * ((radius) ** 3))

        return round(volume_equation, 3)

    def get_message(self, test: bool = True) -> None:
        """Function for getting a message that indicates calculations.

        Parameters:
            test `bool` : Boolean value for reporting a measurement

        Returns:
            Message for calculation.
        """

        if test:
            return print(f"Calculated Success!")
        
        else:
            return print(f"Calculated Fail!")
    
        
    __all__ = [get_volume_total, calculate_neutron_total, read_config_file, test_sphere_equation]

_config_file = "config.yaml"

@profile
def main():
    """Function to test all of this python code.
    """

    test: Volume = Volume(_config_file)
    
    radius = test.radius
    
    print(test)

    try:
        print(f"Volume Total: {test.get_volume_total():,} unit^3\n")

    except Exception as e:
        print("")

    print(f"Check calculation \n\
====================== \n\
Check Sphere Equation: {test.test_sphere_equation():,} unit^3 \n\
Check Volume Equation: {test.calculate_volume_total():,} unit^3 \n\
Check Alpha Parameter: {test.alpha:,} \n\
Check Neutron Total: ~{test.calculate_neutron_total():,} neutron \n\
Check Neutron Current: ~{test.get_neutron_current(radius):,} neutron")

        
if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt as e:
        print(e)