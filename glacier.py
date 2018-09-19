class Glacier(object):
    ICE_DENSITY = 920       # Rho in kg/m^3
    MANTEL_DENSITY = 3200   # kg/m^3
    GRAVITY = 10
    SHEER_STRESS = 0.5e5    # Tau in Pascal

    ICE_CONSTANT = (2 * SHEER_STRESS) / (ICE_DENSITY * GRAVITY)

    def __init__(self, **kwargs):
        self._length = kwargs.get('length', 0)
        self._midpoint = self.length / 2
        self.mantel_density = kwargs.get('mantel_density', self.MANTEL_DENSITY)
        self.isostatic = kwargs.get('isostatic', False)

    @property
    def length(self):
        return self._length

    @property
    def midpoint(self):
        return self._midpoint

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
