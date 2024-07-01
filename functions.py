import dbfunctions as db

def get_bankAccounts(user_id):
    query = ('SELECT public."bankAccount".id, public."bankAccount".name, balance, iban, bank.name FROM public."bankAccount" INNER JOIN public."bank" ON bank.id = public."bankAccount".fk_bank WHERE fk_user = \'%s\';' %user_id)
    answer = db.executeQuery(query)
    return answer

def get_transactions(bankAccount_id):
    query = ('SELECT date, public."transactionType".name AS transactionType, public."transactionCategory".name AS transactionCategory, amount, description FROM transaction INNER JOIN public."transactionType" ON public."transactionType".id = transaction.fk_type INNER JOIN public."transactionCategory" ON public."transactionCategory".id = transaction.fk_category WHERE transaction."fk_bankAccount" = \'%s\';' %bankAccount_id)
    answer = db.executeQuery(query)
    return answer

def get_transactionsTypes():
    query = 'SELECT name FROM public."transactionType";'
    answer_raw = db.executeQuery(query)

    answer = []
    for row in answer_raw:
        answer.append(row[0])

    return answer

def get_transactionsCategories():
    query = 'SELECT name FROM public."transactionCategory";'
    answer_raw = db.executeQuery(query)

    answer = []
    for row in answer_raw:
        answer.append(row[0])

    return answer

def get_transactionCategory_id(name):
    query = ('SELECT id FROM public."transactionCategory" WHERE name = \'%s\';' % name)
    answer = db.executeQuery(query)
    return answer[0][0]

def get_transactionType_id(name):
    query = ('SELECT id FROM public."transactionType" WHERE name = \'%s\';' % name)
    answer = db.executeQuery(query)
    return answer[0][0]

def get_transactionBankAccount_id(name):
    query = ('SELECT id FROM public."bankAccount" WHERE name = \'%s\';' % name)
    answer = db.executeQuery(query)
    return answer[0][0]

def add_transaction(user_id, type_id, category_id, bankAccount_id, currency_id, date, amount, description):
    params = (user_id, type_id, category_id, bankAccount_id, currency_id, date, amount, description)
    query = ('INSERT INTO public.transaction(fk_user, fk_type, fk_category, "fk_bankAccount", fk_currency, date, amount, description) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' % params)
    print(query)
    db.executeWithoutFetch(query)