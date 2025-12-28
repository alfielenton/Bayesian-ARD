import numpy as np
import random
from matplotlib import pyplot as plt

class DataGenerator:

    def __init__(self,C,sig_y, sig_w,t_max,num_components,sparse_proportion,x_dim,num_irr_dims,num_dense,num_sparse,num_range):

        self.C = C
        self.sig_y = sig_y
        self.sig_w = sig_w
        self.t_max = t_max
        self.num_components = num_components
        self.sparse_proportion = sparse_proportion
        self.num_dense_range = range(num_dense - num_range, num_dense)
        self.num_sparse_range = range(num_sparse - num_range, num_sparse)
        self.x_dim = x_dim

        self.w = np.random.rand(x_dim) * self.sig_w
        self.irr_dims = np.random.choice(range(x_dim),num_irr_dims)
        self.w[self.irr_dims] = 0

        self.data = {}
        self.ids = []
        self.sparse_comp_start = int(self.sparse_proportion * self.num_components)

        for comp in range(self.num_components):

            sparse = comp >= self.sparse_comp_start
            id = f'{comp}'
            id = '#K' + '0' * ((len(f'{self.num_components}') + 2) - len(id)) + id
            self.data[id] = {}
            self.ids.append(id)

            R = self.num_sparse_range if sparse else self.num_dense_range
            N = np.random.choice(R)

            x = np.random.rand(self.x_dim)

            t = np.random.choice(np.linspace(0,self.t_max,1000),N)
            y = self.C * np.exp(-(self.w @ x) * t)
            y += np.random.randn(N) * self.sig_y

            self.data[id]['x'] = x
            self.data[id]['y'] = y
            self.data[id]['t'] = t
            self.data[id]['sparse'] = sparse

        with open('datasets//data.csv','w') as f:

            header = 'ID,Code'
            for i in range(self.x_dim):
                header += f',x{i}'
            header += ',obs,time\n'
            f.write(header)

            for code , id in enumerate(self.ids):
                comp = self.data[id]
                x = comp['x']
                x_string = ','.join([str(x_i) for x_i in x])
                y = comp['y']
                t = comp['t']
                for i in range(t.shape[0]):
                    f.write(id + f',{code},' + x_string + f',{y[i]},{t[i]}\n')

    def get_component(self,id=None,sparse=None):

        if id is None:
            if sparse is not None:
                if sparse:
                    id = random.choice(self.ids[self.sparse_comp_start:])
                else:
                    id = random.choice(self.ids[:self.sparse_comp_start])
            else:
                id = random.choice(self.ids)
            
            return id , self.data[id]
        
        return self.data[id]

    def plot_component(self,id=None,sparse=None,prediction=False):
        
        if id is None:
            id , component = self.get_component(id,sparse)
        else:
            component = self.get_component(id,sparse)

        t = component['t']
        y = component['y']
        x = component['x']

        t_test = np.linspace(0,self.t_max,1000)
        y_test = self.C * np.exp(-t_test * (self.w @ x))

        plt.figure(figsize=(10,10))
        plt.scatter(t,y,marker='x',s=10,color = 'green',label='Data')
        plt.plot(t_test,y_test,color='blue',label='True function')

        plt.xlabel('t')
        plt.ylabel('y')
        plt.title('Component ' + id)
        plt.legend()
        plt.tight_layout()
        plt.grid(True)

        if not prediction:
            plt.show()