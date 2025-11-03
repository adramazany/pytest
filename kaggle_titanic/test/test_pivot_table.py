import pandas as pd
import re

from sklearn.ensemble import RandomForestClassifier

def load_train_data(path):
    df = pd.read_csv("../data/train.csv")
    print( df.to_string(max_rows=5) )
    return df

def extract_name(train_data):
    # str = "Cumings, Mrs. John Bradley (Florence Briggs Th...)"
    # str = "Vander Planke, Mrs. Julius (Emelia Maria Vande..."
    # str = "Healy, Miss. Hanora \\"Nora\\""
    # str = "Mellinger, Mrs. (Elizabeth Anne Maidment)"
    # str = "Penasco y Castellana, Mrs. Victor de Satode (M..."
    # str = "Stahelin-Maeglin, Dr. Max"
    # str = "Duff Gordon, Lady. (Lucille Christiana Sutherland) (""Mrs Morgan"")"
    # str = "Widegren, Mr. Carl/Charles Peter"
    str = "Rothes, the Countess. of (Lucy Noel Martha Dyer-Edwards)"
    # res = re.search(r\"([A-Z]+)\,\b+([A-Z]+)\..*\",st
    # res = re.match(r"([\w\s\'\\"]+),\s([A-Za-z]+)[\.\s]+([\w\s\'\\"]+)[\($]?([\w\s\'\\"\.]*)[\)$]?",str)
    # res = re.match(r"([\w\s\'\"]+),\s([A-Za-z]+)[\.\s]+([\w\s\'\"]+)[\($]?([\w\s\'\"\.]*)[\)$]?",str)
    res = re.match(r"([\w\s\'\"\-]+),\s([A-Za-z]+)[\.\s]+([\w\s\'\"]+)[\($]?([\w\s\'\"\.]*)[\)$]?", str)
    print(res.groups())

    # for i, r in df.iterrows():
    #     try:
    #         l = len( re.match(r"([\w\s\'\"\-]+),\s([A-Za-z]+)[\.\s]+([\w\s\'\"]+)[\($]?([\w\s\'\"\.]*)[\)$]?",r['Name']).groups() )
    #         print(r['Name'] if l!=4 else "")
    #     except Exception as ex:
    #         print(ex, r['Name'])

    train_data[['_No1', 'FirstName', 'Title', 'LastName', 'DescName', '_etc1']] = train_data['Name'].str.split(
        r"([\w\s\'\"\-]+),\s([A-Za-z]+)[\.\s]+([\w\s\'\"]+)[\($]?([\w\s\'\"\.]*)[\)$]?", expand=True)
    # del df['_No1'] #'_etc1']
    train_data.drop(columns=['_No1', '_etc1'], inplace=True)
    print(train_data.to_string(max_rows=5))
    # print(df.to_string())

def extract_ticket(train_data):
    # ticket = "W./C. 6609"
    # ticket = "A/5. 10482"
    # ticket = "STON/O2. 3101294"
    # ticket = "LINE"
    # ticket = "113767"
    ticket = "SC/AH Basle 541"
    # res = re.match(r"(\d+)\w([A-Za-z]+\.)\/([A-Za-z\.]+)?",ticket[::-1])
    # res = re.match(r"([\d]+) ([A-Za-z\.\w]+)/([A-Za-z\.\w]+)",ticket[::-1])
    # res = re.match(r"([A-Za-z\.]+/)?([A-Za-z\d\.]+ )?([\d]+|LINE)?",
    #                ticket.replace("O 2", "O2").replace("AH Basle", "AH.Basle"))
    # print(res.groups())

    # for i, r in train_data.iterrows():
    #     try:
    #         st = r['Ticket'].replace("O 2", "O2").replace("AH Basle", "AH.Basle")
    #         l = len( re.match(r"([\w\s\'\"\-]+),\s([A-Za-z]+)[\.\s]+([\w\s\'\"]+)[\($]?([\w\s\'\"\.]*)[\)$]?",st).groups() )
    #         if l!=4 : print(r['Ticket'])
    #     except Exception as ex:
    #         print(ex, r['Ticket'])

    # df2 = train_data['Ticket'].str.replace("O 2", "O2").str.replace("A. 2.","A.2.").str.replace("AH Basle", "AH.Basle").str.split(r"([A-Za-z\.]+/)?([A-Za-z\d\.]+ )?([\d]+|LINE)", expand=True).dropna(axis=1,how="all")
    # print(df2.to_string())

    train_data[['_No2', 'TicketType1', 'TicketType2', 'TicketNo', "_etc2"]] = (train_data['Ticket'].str.replace("O 2", "O2").str.replace("A. 2.","A.2.")
        .str.replace("AH Basle", "AH.Basle").str.split(r"([A-Za-z\.]+/)?([A-Za-z\d\.]+ )?([\d]+|LINE)", expand=True).dropna(axis=1,how="all"))
    del train_data['_No2']
    del train_data['_etc2']
    # df2=df['Ticket'].str.replace("O 2","O2").str.replace("AH Basle","AH.Basle").str.split(r"([A-Za-z\.]+/)?([A-Za-z\d\.]+ )?([\d]+|LINE)",expand=True).dropna(axis=1,how="all")
    print(train_data.to_string(max_rows=5))
    # print(df.to_string())

def extract_age_range(train_data):
    train_data['AgeRange'] = train_data['Age'] // 5
    train_data['AgeRange'].fillna(-1, inplace=True)
    print(train_data.to_string(max_rows=5))

def extract_fare_range(train_data):
    train_data['FareRange'] = train_data['Fare'] // 5
    train_data['FareRange'].fillna(-1, inplace=True)
    print(train_data.to_string(max_rows=5))


def guess1WomensSurvived(train_data):
    women = train_data.loc[train_data.Sex=='female']['Survived']
    rate_women = sum(women)/len(women)
    print("% of women who survived:", rate_women*100)

def guess1MensSurvived(train_data):
    women = train_data.loc[train_data.Sex=='male']['Survived']
    rate_women = sum(women)/len(women)
    print("% of men who survived:", rate_women*100)

def unknown_gender(train_data):
    unknown = train_data.loc[~train_data.Sex.isin(['male','female'])]
    print(unknown.to_string())

def predict(train_data, test_data, output_path= 'submission.csv', features= ["Pclass", "Sex", "SibSp", "Parch"]):
    y = train_data["Survived"]

    # features = ["Pclass", "Sex", "SibSp", "Parch"]
    # survival - Survival(0 = No; 1 = Yes)
    # pclass - Passenger Class(1 = 1st; 2 = 2nd; 3 = 3rd)
    # name - Name
    # sex - Sex
    # age - Age
    # sibsp - Number of Siblings/Spouses Aboard
    # parch - Number of Parents/Children Aboard
    # ticket - Ticket Number
    # fare - Passenger Fare
    # cabin - Cabin
    # embarked - Port of Embarkation (C = Cherbourg; Q = Queenstown; S = Southampton)
    # features = ["Pclass", "Sex", "SibSp", "Parch", "Embarked", "Title", "LastName", "TicketType1", "TicketType2", "AgeRange", "FareRange"]

    X = pd.get_dummies(train_data[features])
    X_test = pd.get_dummies(test_data[features])

    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    model.fit(X,y)
    predictions = model.predict(X_test)

    output = pd.DataFrame({'PassengerId':test_data.PassengerId, 'Survived': predictions})
    output.to_csv(output_path,index=False)
    print("Submission successfully saved!")
    return output



if __name__ == "__main__":
    train_data = pd.read_csv("../data/train.csv")
    extract_name(train_data)
    extract_ticket(train_data)
    extract_age_range(train_data)
    extract_fare_range(train_data)
    # extract_Cabin(train_data)

    guess1WomensSurvived(train_data)
    guess1MensSurvived(train_data)
    # unknown_gender(df)

    test_data = pd.read_csv("../data/test.csv")
    extract_name(test_data)
    extract_ticket(test_data)
    extract_age_range(test_data)
    extract_fare_range(test_data)


    output = predict(train_data, test_data, output_path='submission.csv')
    output2 = predict(train_data, test_data, output_path='submission2.csv', features= ["Pclass", "Sex", "SibSp", "Parch", "Embarked", "AgeRange", "FareRange"])
    # RandomForestClassifier does not accept missing values encoded as NaN natively.
    # AgeRange,
    # Feature names seen at fit time, yet now missing:
    # "Title", "LastName", "TicketType1", "TicketType2",


    # diff = pd.concat([output, output2]).drop_duplicates(keep=False)
    # print(diff.to_string())

    res = output
    res[['PassengerId2','Survived2']] = output2
    # print(res.to_string())
    # train_data.loc[train_data.Sex=='female']['Survived']
    print("Total=",len(res),
          "Survived=", len(res[res.Survived == 1]),
          "Survived2=", len(res[res.Survived2 == 1]),
          "Diff=", len(res[res.Survived != res.Survived2]),
          )



