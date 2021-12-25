import pandas as pd
import re
import seaborn as sns
pd.options.mode.chained_assignment = None



class DataPrep():
    
    @staticmethod
    def read_and_cleanup(filename):
        
        df = pd.read_csv(filename,sep=',',error_bad_lines=False,encoding='UTF-8')
        
        column_names = []
        for i in df.columns.values:
            if i[-1:] == '\xa0':
                column_names.append(i[:-1])
                print(i)
            else:
        
                column_names.append(i)
        
        
        df.columns = column_names
        df = df.rename(columns = lambda x:re.sub('\[dB\]', 'w dB', x))
        df = df.rename(columns = lambda x:re.sub('\[km\]', 'w km', x))
        df = df.rename(columns = lambda x:re.sub('(\[m\]|w mertach)', 'w metrach', x))
        df = df.rename(columns = lambda x:re.sub('\[km\/h\]', 'w km/h', x))

        return df
    
    @staticmethod
    def process(df):
        
        try:
            del df['Nazwa lab.']
        except:
            None
        
                          
        df = df.drop(['Nazwa odcinka drogi',
                    'Krajowy numer drogi',
                    'Kod odcinka drogi',
                    'Nachylenie podłużne',
                    'Nazwa punktu pomiarowego',
                    'Kod pomiaru',
                    'Data rozpoczęcia',
                    'Data zakończenia',
                    'Klasa drogi',
                    'Funkcja drogi',
                    'Wartość dopuszczalna dla pory dnia dla punktu w momencie pomiaru w dB',
                    'Wartość dopuszczalna dla pory nocy dla punktu w momencie pomiaru w dB',
                    'Przedział niepewności U95 w dB',
                    'Rodzaj pola akustycznego',
                    'Odległość punktu pomiarowego od elewacji budynku',
                    'Województwo',
                    'Współrzędne początku odcinka WGS84_Y',
                    'Miejscowość',
                    'Współrz. pp WGS84 (szer. geogr.)',
                    'Przedział niepewności U95- w dB',
                    'Opis odcinka drogi',
                    'Gmina',
                    'Współrzędne początku odcinka WGS84_X',
                    'Współrzędne końca odcinka WGS84_Y',
                    'Powiat',
                    'Współrzędne końca odcinka WGS84_X',
                    'Wysokość w metrach',
                    'Szacunkowa odległość pierwszej linii zabudowy od źródła w metrach',
                    'Opis pomiaru',
                    'Rodzaj drogi',
                    'Opis terenu',
                    'Cel pomiaru',
                    'Przedział niepewności U95+ w dB',
                    'Jakość pomiaru',
                    'Szacunkowa wysokość pierwszej linii zabudowy w metrach',
                    'Procedura',
                    'Kod pocztowy',
                    'Współrz. pp WGS84 (dł. geogr.)',
                    'Rodzaj terenu',
                    'Rodzaj ruchu',
                    'Ogólna długość dróg w mieście w km',
                    'Kod punktu pomiarowego',
                    'Charakterystyka częst.',
                    'Laeq przed korektą w dB',
                    'Długość analizowanego odcinka w km'
                    ],axis=1)
        

        null=[]
        for i in range (len(df)):
            if not df['Czas odniesienia'][i] == 'Dzień 16h':
                null.append(i)
            
        df = df.drop(null)
        df = df.reset_index()
        
        del df['Czas odniesienia']
        
        null=[]
        
        df.insert(17, 'Pojazdy ciężkie',0)
        df.insert(18, 'Udział pojazdów ciężkich',0)
        
        
        
        #preparation for calculations
        df['Klasa pojazdu'] = pd.Series(df['Klasa pojazdu'],dtype=str)
        df['Ilość pojazdów w czasie odniesienia'] = pd.Series(df['Ilość pojazdów w czasie odniesienia'],dtype=str)
        
        for i in range(len(df)):
            try:
                df['Ilość pojazdów w czasie odniesienia'][i] = re.sub(r'\xa0','', df['Ilość pojazdów w czasie odniesienia'][i])
            except:
                None
                
        df['Ilość pojazdów w czasie odniesienia'] = pd.Series(df['Ilość pojazdów w czasie odniesienia'],dtype=float)
        
        
        
        for i in range(len(df)):
        
            if df['Klasa pojazdu'][i][:4] == 'brak' or df['Klasa pojazdu'][i] == 'nan':
                null.append(i)
                
            for j in range(len(df)):
                
                if df['Doba (data i czas)'][j] == df['Doba (data i czas)'][i]:
                    if df['Laeq po korekcie w dB'][j] == df['Laeq po korekcie w dB'][i]:
                        
                    
                        if df['Klasa pojazdu'][i][:15] == 'Pojazdy ciężkie':
            
                            df['Pojazdy ciężkie'][j] = df['Ilość pojazdów w czasie odniesienia'][i]
                            df['Ilość pojazdów w czasie odniesienia'][j] = df['Ilość pojazdów w czasie odniesienia'][j] + df['Ilość pojazdów w czasie odniesienia'][i]
                            null.append(i)
            
                else:
                    continue
                
            
        df = df.drop(null)
        df = df.reset_index()
        del df['Doba (data i czas)']
        del df['level_0']
        
        df['Udział pojazdów ciężkich'] = df['Pojazdy ciężkie']/df['Ilość pojazdów w czasie odniesienia']

        for i in range(len(df.columns)):
            for j in range(len(df)):
                try:
                    df[df.columns[i]][j] = df[df.columns[i]][j].replace(',','.')
                except AttributeError:
                    continue
        
        del df['index']
    
        del df['Klasa pojazdu']
        
        del df['Pojazdy ciężkie']
        
    
        return df
    
    
    @staticmethod
    def classes(df):
        for i in range(len(df)):
            if df[df.columns[3]][i] == 'Brak danych':
                df[df.columns[3]][i] = 0
            elif df[df.columns[3]][i] == 'Odcinek prosty':
                df[df.columns[3]][i] = 1
            elif df[df.columns[3]][i] == 'Zakręt (łuk)':
                df[df.columns[3]][i] = 2
            elif df[df.columns[3]][i] == 'Skrzyżowanie':
                df[df.columns[3]][i] = 3
            elif df[df.columns[3]][i] == 'Rondo':
                df[df.columns[3]][i] = 4
        
            
        for i in range(len(df)):
            if df[df.columns[4]][i] == 'Brak danych':
                df[df.columns[4]][i] = 0
            elif df[df.columns[4]][i] == 'Nasyp':
                df[df.columns[4]][i] = 1
            elif df[df.columns[4]][i] == 'Poziom terenu':
                df[df.columns[4]][i] = 2
                
        for i in range(len(df)):
            if df[df.columns[5]][i] == 'Brak danych':
                df[df.columns[5]][i] = 0
            elif df[df.columns[5]][i] == 'Nawierzchnia wielowarstwowa':
                df[df.columns[5]][i] = 1
            elif df[df.columns[5]][i] == 'Asfalt gładki':
                df[df.columns[5]][i] = 2
            elif df[df.columns[5]][i] == 'Asfalt porowaty':
                df[df.columns[5]][i] = 3
            elif df[df.columns[5]][i] == 'Bruk':
                df[df.columns[5]][i] = 4
        
        for i in range(len(df)):
            if df[df.columns[6]][i] == 'Inna':
                df[df.columns[6]][i] = 0
            elif df[df.columns[6]][i] == 'Dobra':
                df[df.columns[6]][i] = 1
            elif df[df.columns[6]][i] == 'Uszkodzona':
                df[df.columns[6]][i] = 2
                
        for i in range(len(df)):
            if df[df.columns[7]][i] == 'brak danych':
                df[df.columns[7]][i] = 0
            elif df[df.columns[7]][i] == 'Płynny':
                df[df.columns[7]][i] = 1
            elif df[df.columns[7]][i] == 'Przerywany':
                df[df.columns[7]][i] = 2    
                
        
        
        for i in range(len(df)):
            if df[df.columns[8]][i] == 'brak danych':
                df[df.columns[8]][i] = 0
            elif df[df.columns[8]][i] == 'Inny':
                df[df.columns[8]][i] = 1
            elif df[df.columns[8]][i] == 'Brak zabudowy':
                df[df.columns[8]][i] = 2
            elif df[df.columns[8]][i] == 'Luźna':
                df[df.columns[8]][i] = 3
            elif df[df.columns[8]][i] == 'Zwarta':
                df[df.columns[8]][i] = 4   
                
        for i in range(len(df.columns)):
            try:
                df[df.columns[i]] = pd.to_numeric(df[df.columns[i]],errors='coerce')
            except ValueError:
                continue
        
        return df
        
    @staticmethod
    def postprocess(df):
                
        correlation_coeff = df.corr(method='spearman')        
        sns.heatmap(df.corr(method='spearman'))
        
        df = df.rename(columns = lambda x:re.sub('ą', 'a', x))
        df = df.rename(columns = lambda x:re.sub('ć', 'c', x))
        df = df.rename(columns = lambda x:re.sub('ę', 'e', x))
        df = df.rename(columns = lambda x:re.sub('ó', 'o', x))
        df = df.rename(columns = lambda x:re.sub('ś', 's', x))
        
        
        cc = correlation_coeff
        bad=[]
        
        for i in range(len(correlation_coeff)):
            if cc.loc['Laeq po korekcie w dB'][i] < 0.2 and cc.loc['Laeq po korekcie w dB'][i] > -0.2 or cc.loc['Laeq po korekcie w dB'][i] == float('nan'):
                bad.append(df.columns[i])
            
        for k in bad:        
            df = df.drop([k],axis=1)
        
        return (df,cc)
    
#use methods

csv_file1 = 'Raport_2018.csv'

data2k18 = DataPrep.read_and_cleanup(csv_file1)
data2k18 = DataPrep.process(data2k18)

csv_file2 = 'Raport_2019.csv'

data2k19 = DataPrep.read_and_cleanup(csv_file2)
data2k19 = DataPrep.process(data2k19)

database = data2k18.append(data2k19,ignore_index=True)

database = DataPrep.classes(database)
#database = DataPrep.postprocess(database)


