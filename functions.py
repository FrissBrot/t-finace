import dbfunctions as db

def get_bank():
    query = ('SELECT * from bank')
    answer = db.executeQuery(query)
    print(answer)
    return answer