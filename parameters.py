
class Parameters:

    def __init__(self,irrelevant):

        self.C = 10
        self.sig_y = 2.5
        self.num_components = 1500
        self.sparse_proportion = 3/4
        self.x_dim = 4
        self.num_irr_dims = int(self.x_dim/4) if irrelevant else 0
        self.num_dense = 40
        self.num_sparse = 5
        self.num_range = 4
        self.t_max = 10