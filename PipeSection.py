class PipeSection:
    def __init__(self, diameter, length, fittings_k=None, elevation_change=0):
        """
        Initialize a pipe section with its properties
        """
        self.diameter = diameter
        self.length = length
        self.elevation_change = elevation_change
        self.fittings_k =  fittings_k if fittings_k is not None else []