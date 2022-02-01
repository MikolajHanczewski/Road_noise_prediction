import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np 
import lightgbm as lgb
import seaborn as sns
import re
import time





class LearningUtils():
   
    @staticmethod
    def load_and_prepare(filename):
    
        df = pd.read_pickle(filename)
        
        df = df.rename(columns = lambda x:re.sub('[^A-Za-z0-9 ]+', '', x))
        del df['To w dB']
        del X['Laeq po korekcie w dB']
        Y = df['Laeq po korekcie w dB']
        
        return (X,Y)

    def plot_predictions(Y_true, Y_predicted):
        
        
        df_pred = pd.DataFrame({"Measured value": Y_true, "Predicted value": Y_predicted})
        val_min = 40
        val_max = 80
        figure = sns.jointplot('Measured value', 'Predicted value', df_pred,
                               xlim=(val_min, val_max),
                               ylim=(val_min, val_max),)
        figure.ax_joint.plot([val_min, val_max], [val_min, val_max], ':k') 
        figure.fig.set_figheight(8)
        figure.fig.set_figwidth(8)




database_file = 'db1819.pkl'

(X,Y) = LearningUtils.load_and_prepare(database_file)
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.1,random_state = 12)


t0 = time.time()  
lgb_model = lgb.LGBMRegressor(use_missing=False)
lgb_model.fit(X,Y)
    

Y_pred = lgb_model.predict(X_test)
       

t1= time.time()
error = np.sqrt(mean_squared_error(Y_test,Y_pred))    
r2 = r2_score(Y_test, Y_pred)
var = np.var(Y_pred)
MBE = np.mean(Y_pred - Y_test)
total_time = t1-t0
    


plot = Learning.plot_predictions(Y_test, Y_pred)
