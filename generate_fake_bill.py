import numpy as np
import pandas as pd
import datetime

products = [
    'leche',
    'pan',
    'queso',
    'jugo',
    'arroz',
    'frijoles',
    'cereal',
    'tomate',
    'pepino',
    'azucar'
]

mapa = {'leche': 800, 'pan' : 1500, 'queso': 2000, 'jugo': 500, 'arroz':1000, 'frijoles':2000,
             'cereal':1500, 'tomate': 2500 , 'pepino': 1500, 'azucar': 2000}

places = ['pali santa ana',
          'automercado heredia',
          'masxmenos belen',
          'perimercados escazu']

N = np.random.randint(5,10)

def generar_precio(precio_medio, std=2, N=1):
  return np.around(np.random.normal(precio_medio, std, N), decimals=2)[-1]

def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')

def generate_products():
    return np.random.choice(a=products, size=N)

def generate_places():
    return np.random.choice(a=places, size=N)

def generate_date():
    return np.random.choice(pd.date_range(start='20100101', end=datetime.datetime.now()))

def generate_prices():
    return np.around(np.random.uniform(low=1000, high=10000, size=N), decimals=2, out=None)

def create_dataframe():
    return pd.DataFrame({
        'Fecha' : generate_date(),
        'Producto' : generate_products(),
        'Lugar' : generate_places(),
    })

if __name__ == '__main__':
    for _ in range(1000):
        df = create_dataframe()
        df['Precio'] = df['Producto'].map(mapa).apply(lambda x: generar_precio(x))
        df.to_csv(f'data/factura-{get_current_time()}.csv', index=False)