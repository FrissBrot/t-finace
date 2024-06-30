import dbfunctions as db

def get_bank():
    query = ('SELECT * from bank')
    answer = db.executeQuery(query)
    print(answer)
    return answer

def get_transactions():
    query = ('SELECT date, public."transactionType".name AS transactionType,'
             'public."transactionCategory".name AS transactionCategory, '
             'amount, description '
             'FROM transaction '
             'INNER JOIN public."transactionType" '
             'ON public."transactionType".id = transaction.fk_type '
             'INNER JOIN public."transactionCategory" '
             'ON public."transactionCategory".id = transaction.fk_category ')
    answer = db.executeQuery(query)
    return answer