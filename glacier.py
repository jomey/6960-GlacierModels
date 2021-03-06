class Glacier(object):
    ICE_DENSITY = 920       # Rho in kg/m^3
    MANTEL_DENSITY = 3200   # kg/m^3
    GRAVITY = 10
    SHEER_STRESS = 0.5e5    # Tau in Pascal
    ALPHA = 3               # m/2
    NU = 10
    BALANCE_RATE = 0.007    # m/yr

    ICE_CONSTANT = (2 * SHEER_STRESS) / (ICE_DENSITY * GRAVITY)

    def __init__(self, **kwargs):
        self._length = kwargs.get('length', 0)
        self._max_bed_height = kwargs.get('max_bed_height', 0)
        self._midpoint = self.length / 2
        self._slope = kwargs.get('slope', 0)
        self.mantel_density = kwargs.get('mantel_density', self.MANTEL_DENSITY)
        self.isostatic = kwargs.get('isostatic', False)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def slope(self):
        return self._slope

    @slope.setter
    def slope(self, value):
        self._slope = value

    @property
    def midpoint(self):
        return self._midpoint

    @property
    def max_bed_height(self):
        return self._max_bed_height

    @max_bed_height.setter
    def max_bed_height(self, value):
        self._max_bed_height = value

    @property
    def isostatic(self):
        return self._isostatic

    @isostatic.setter
    def isostatic(self, value):
        self._isostatic = value

    @property
    def mantel_density(self):
        return self._mantel_density

    @mantel_density.setter
    def mantel_density(self, value):
        self._mantel_density = value

    def isostacy(self):
        return self.ICE_DENSITY / (self.ICE_DENSITY - self.mantel_density)

    def surface_height(self, x):
        if x >= self.midpoint:
            x = self.length - x

        height = self.ICE_CONSTANT * x

        if self.isostatic:
            height = height * (1 + self.isostacy())

        return height ** (1 / 2)

    def bed_depth(self, y):
        return y * self.isostacy()

    """
    ############
    ## Length ##
    ############
    """

    def linear_equilibrium_length(self, ela_elevation, **kwargs):
        """
        Equation 2.1.7
        Assumes linear relationship between thickness and length
        """
        thickness = kwargs.get('thickness', self.static_mean_thickness())
        return (2 / self.slope) * thickness + \
            self.max_bed_height - ela_elevation

    @staticmethod
    def length_change(ela_change, slope):
        """
        Equation 2.1.8
        """
        return -(2 / slope) * ela_change

    def fractional_length_change(self, ela_elevation, ela_change, slope):
        """
        Equation 2.1.9
        """
        return -1 / (
                (self.SHEER_STRESS / (self.ICE_DENSITY * self.GRAVITY * slope))
                + self.max_bed_height - ela_elevation
        ) * ela_change

    def length_over_time(self, delta_time, ela):
        """
        Equation 3.2.6 after solving the integral
        """
        return (2 / 3) * (1 + self.NU * self.slope) / self.ALPHA \
            * self.mass_balance(ela) * self.length ** -0.5 * delta_time \
            + self.length

    """
    ###############
    ## Thickness ##
    ###############
    """

    def static_mean_thickness(self):
        """
        Integral from equation 2.2.1
        """
        return self.SHEER_STRESS / \
            (self.ICE_DENSITY * self.GRAVITY * self.slope)

    def mean_thickness(self):
        """
        Equation 2.3.1
        """
        return (self.ALPHA * self.length ** .5) / (1 + self.NU * self.slope)

    """
    ###########
    ##  ELA  ##
    ###########
    """

    def ela_from_length(self):
        """
        Derived for ela_elevation from 2.1.7
        """
        return self.static_mean_thickness() + \
            self.max_bed_height - (self.length * self.slope / 2)

    def critical_ela(self):
        """
        Equation 2.3.6
        """
        return (self.ALPHA ** 2 /
            (2 * self.slope * (1 + self.NU * self.slope) ** 2)) + \
            self.max_bed_height

    """
    ####################
    ##  Mass Balance  ##
    ####################
    """

    def mass_balance(self, ela):
        """
        Equation 3.2.7
        """
        return -0.5 * self.BALANCE_RATE * self.slope * self.length**2 \
            + self.BALANCE_RATE * self.length * (
                self.mean_thickness() + self.max_bed_height - ela
            )
