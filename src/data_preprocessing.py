import pandas as pd


def preprocess_data(df,processed_data_path):
    col_to_drop = ['link']
    df = df[(df['ceiling_height'] < 6) | (df['ceiling_height'].isna())]
    cat_columns = df.select_dtypes(include='object').columns.tolist()
    binary_columns = ['is_new','is_apartments']
    num_columns = df.select_dtypes(exclude='object').columns.tolist()
    num_columns = [col for col in num_columns if col not in binary_columns]
    df.drop_duplicates(subset='link',inplace=True,keep='first')
    one_hot=pd.get_dummies(df['region_of_moscow'],prefix='reg',drop_first=True) # по умолчанию dummy_na=False, null столбца не будет
    df = pd.concat([df,one_hot],axis=1)
    df.drop(['region_of_moscow'],axis=1,inplace=True)
    df = df[df['price']<300000000]
    df = df[df['price']>3000000]
    col_to_drop.extend(['number_of_floors','living_area','total_area'])
    df=df.drop(columns=col_to_drop)
    df.to_csv(processed_data_path,index=False)
    