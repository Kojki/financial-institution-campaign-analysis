import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import tree
import pickle

df = pd.read_csv('Bank.csv')
df.head(2)

get_dummies = ['job', 'marital', 'education', 'default', 'housing', 'month', 'loan', 'contact']
GET_DUMMIES = pd.get_dummies(df[get_dummies], drop_first = True, dtype = int)
df2 = pd.concat([df, GET_DUMMIES], axis = 1)
df2 = df2.drop(get_dummies, axis = 1)
df2.head(2)

from sklearn.model_selection import train_test_split
train_val, test = train_test_split(df2, test_size = 0.2, random_state = 0)
train_val.isnull().sum()

train_val_median = train_val.median(numeric_only = True)
train_val2 = train_val.fillna(train_val_median)

colname = train_val2.columns
for name in colname:
    train_val2.plot(kind = 'scatter', x = name, y = 'y')

from sklearn.covariance import MinCovDet
mcd = MinCovDet(random_state = 0, support_fraction = 0.7)
mcd.fit(train_val2)
distance = mcd.mahalanobis(train_val2)
distance = pd.Series(distance)
distance.plot(kind = 'box')
tmp = distance.describe()
tmp

iqr = tmp['75%'] - tmp['25%']
jougen = tmp['75%'] + iqr * 1.5
kagen = tmp['25%'] - iqr * 2.5
outliner = distance[ (distance > jougen) | (distance < kagen) ]
outliner

outline = pd.DataFrame(outliner)
train_val3 = train_val2.drop(outline.columns, axis = 0)

rom sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

def learn(x, t):
    x_train, x_val, y_train, y_val = train_test_split(x, t, test_size = 0.3, random_state = 0)
    model = tree.DecisionTreeClassifier(max_depth = 10, random_state = 0)
    model.fit(x_train, y_train)

    y_train_pred = model.predict(x_train)
    y_val_pred = model.predict(x_val)
    train_score = accuracy_score(y_train, y_train_pred)
    val_score = accuracy_score(y_train, y_train_pred)

    print('Classification Report (Validation):')
    print(classification_report(y_val, y_val_pred))

    return train_score, val_score

train_cor = train_val3.corr()['y']
train_cor

abs_cor = train_cor.map(abs)
abs_cor.sort_values(ascending = False)

x = train_val3.loc[ : ,['duration', 'housing_yes', 'campaign', 'contact_sending _document',
                        'age', 'marital_single', 'marital_married',  
                        'loan_yes', 'previous']]
t = train_val3[['y']]
s1, s2 = learn(x, t)
print(s1, s2)

model_filename = 'Bank_train.pkl'
with open(model_filename, 'wb') as f:
    pickle.dump(s1, f)
