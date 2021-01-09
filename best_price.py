import pandas as pd
import datetime
from concat_files import load_csv2df


def review(item):
    return pd.Series({
        'Suma': item.sum(),
        'p_value': item[item.notna()].size / item.size,
        'missing': item[item.isna()].index.to_list()
    })


def cheapest(item):
    return item[item['Suma'] == item['Suma'].min()].iloc[-1]

def dia_to_ndia(dia):
    return (dia - datetime.datetime(1970, 1, 1)).days

def obtener_precio(producto, lugar, fecha_numero):
    # poner logica para leer el pickle file, largar el modelo, y correr la prediccion
    # escribir aqui la logica para entrenar y guardar en pickle.
    # arroz_pali.p
    import pickle
    from sklearn import linear_model
    import numpy as np
    nombre_archivo = f'{producto}_{lugar}.p'

    # Create linear regression object
    # load the model from disk
    modelo = pickle.load(open(nombre_archivo, 'rb'))
    vector_fechas = np.array([fecha_numero]).reshape(-1, 1)
    precio_predicho = modelo.predict(vector_fechas)
    return precio_predicho[0][0]

def rellenado(item):

    def otra_funcion(otro_elemento):
        lugar = otro_elemento.name[1]
        fecha = otro_elemento.name[0]
        producto = otro_elemento.index[0]

        # Predicción usando la fecha de hoy
        fecha_numero = dia_to_ndia(datetime.datetime.today())
        # producto, fecha, lugar -> fit "predecir" ----> numero (float)
        dato = obtener_precio(producto, lugar, fecha_numero)
        return pd.Series(dato)

    return item.to_frame().apply(otra_funcion, axis=1).iloc[:,0]


def best_price_by_list(data, lista):
    if data is None:
        print('No data available')
        return

    historico  = (
        data.groupby(['Fecha', 'Lugar', 'Producto'])['Precio'].min()
            .unstack(level=0)
            .swaplevel()
            .sort_index()
            .sort_index(axis=1)
    )

    selection = (
        historico.iloc[:, [-1]]
            .unstack()
            .loc[lista]
    )

    def entrenar_modelo(producto, lugar, vector_fechas, vector_precios):
        import pickle
        from sklearn import linear_model

        # escribir aqui la logica para entrenar y guardar en pickle.
        # arroz_pali.p
        nombre_archivo = f'{producto}_{lugar}.p'
        vector_fechas = vector_fechas.reshape(-1, 1)
        vector_precios = vector_precios.reshape(-1, 1)

        # Create linear regression object
        modelo = linear_model.LinearRegression()
        modelo.fit(vector_fechas, vector_precios)

        # save the model to disk
        pickle.dump(modelo, open(nombre_archivo, 'wb'))

    def entrenar(item):
        mi_serie_limpia = item.dropna()
        mi_serie_limpia.index = pd.to_datetime(mi_serie_limpia.index)
        mi_serie_limpia.index = mi_serie_limpia.reset_index().iloc[:, 0].apply(dia_to_ndia)
        producto, lugar = mi_serie_limpia.name
        entrenar_modelo(producto, lugar, mi_serie_limpia.index.values, mi_serie_limpia.values)

    # Habilitar para generar modelos entrenados y guardarlos como pickles files
    #historico.apply(entrenar, axis=1)

    # Método a aplicar el rellenado mediante regression lineal
    selection = selection.apply(rellenado , axis=1)

    # quitar un nivel. quitar el nivel de las fechas
    selection = selection.droplevel(level=0, axis=1)

    res = (
        selection.apply(review, axis=0)
        .T.reset_index()
        .groupby(['p_value']).apply(cheapest)
    )
    return res[res['p_value'] == 1]

if __name__ == '__main__':
    data = load_csv2df()
    product_list = ['arroz', 'frijoles']
    print(product_list)
    print(best_price_by_list(data=data, lista=product_list))

    print('-'* 100)
    product_list = ['pan', 'queso', 'tomate']
    print(product_list)
    print(best_price_by_list(data=data, lista=product_list))

    print('-' * 100)
    product_list = [ 'queso', 'tomate']
    print(product_list)
    print(best_price_by_list(data=data, lista=product_list))

    print('-' * 100)
    product_list = [ 'cereal', 'jugo']
    print(product_list)
    print(best_price_by_list(data=data, lista=product_list))