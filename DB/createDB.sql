CREATE TABLE "session"(
    "id" BIGINT NOT NULL,
    "fk_user" BIGINT NOT NULL,
    "token" VARCHAR(32) NOT NULL,
    "valid_until" DATE
);
ALTER TABLE
    "session" ADD PRIMARY KEY("id");
CREATE TABLE "repetitiveExecution"(
    "id" BIGINT NOT NULL,
    "fk_user" BIGINT NOT NULL,
    "fk_senderAccount" BIGINT NOT NULL,
    "fk_receiverAccount" BIGINT NOT NULL,
    "fk_category" BIGINT NOT NULL,
    "fk_state" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "day" INTEGER NOT NULL,
    "startDate" DATE,
    "endDate" DATE,
    "amount" INTEGER NOT NULL,
    "custom_reciever" VARCHAR(255)
);
ALTER TABLE
    "repetitiveExecution" ADD PRIMARY KEY("id");
CREATE TABLE "currency"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL,
    "isoCode" VARCHAR(3) NOT NULL
);
ALTER TABLE
    "currency" ADD PRIMARY KEY("id");
CREATE TABLE "moneyPool"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "moneyPool" ADD PRIMARY KEY("id");
CREATE TABLE "poolPayment"(
    "id" BIGINT NOT NULL,
    "fk_user" BIGINT NOT NULL,
    "fk_pool" BIGINT NOT NULL,
    "fk_currency" BIGINT NOT NULL,
    "amount" INTEGER NOT NULL,
    "descripton" VARCHAR(255)
);
ALTER TABLE
    "poolPayment" ADD PRIMARY KEY("id");
CREATE TABLE "transactionCategory"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "transactionCategory" ADD PRIMARY KEY("id");
CREATE TABLE "bank"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "shortName" VARCHAR(255),
    "swift" VARCHAR(255)
);
ALTER TABLE
    "bank" ADD PRIMARY KEY("id");
CREATE TABLE "bankAccount"(
    "id" BIGINT NOT NULL,
    "fk_user" BIGINT NOT NULL,
    "fk_bank" BIGINT NOT NULL,
    "fk_currency" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "IBAN" VARCHAR(34),
    "balance" INTEGER
);
ALTER TABLE
    "bankAccount" ADD PRIMARY KEY("id");
CREATE TABLE "user"(
    "id" BIGINT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "mail" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "active" BOOLEAN NOT NULL,
    "resetcode" VARCHAR(8),
    "codeValidUntil" TIMESTAMP(0) WITHOUT TIME ZONE,
    "fullAccess" BOOLEAN NOT NULL
);
ALTER TABLE
    "user" ADD PRIMARY KEY("id");
CREATE TABLE "transaction"(
    "id" BIGINT NOT NULL,
    "fk_user" BIGINT NOT NULL,
    "fk_type" BIGINT NOT NULL,
    "fk_category" BIGINT NOT NULL,
    "fk_bankAccount" BIGINT NOT NULL,
    "fk_currency" BIGINT NOT NULL,
    "date" DATE NOT NULL,
    "amount" INTEGER NOT NULL,
    "description" VARCHAR(255)
);
ALTER TABLE
    "transaction" ADD PRIMARY KEY("id");
CREATE TABLE "transactionType"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "transactionType" ADD PRIMARY KEY("id");
CREATE TABLE "ZT_user_moneyPool"(
    "id" BIGINT NOT NULL,
    "fk_user" BIGINT NOT NULL,
    "fk_moneyPool" BIGINT NOT NULL
);
ALTER TABLE
    "ZT_user_moneyPool" ADD PRIMARY KEY("id");
CREATE TABLE "state"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "state" ADD PRIMARY KEY("id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_fk_currency_foreign" FOREIGN KEY("fk_currency") REFERENCES "currency"("id");
ALTER TABLE
    "ZT_user_moneyPool" ADD CONSTRAINT "zt_user_moneypool_fk_user_foreign" FOREIGN KEY("fk_user") REFERENCES "user"("id");
ALTER TABLE
    "ZT_user_moneyPool" ADD CONSTRAINT "zt_user_moneypool_fk_moneypool_foreign" FOREIGN KEY("fk_moneyPool") REFERENCES "moneyPool"("id");
ALTER TABLE
    "poolPayment" ADD CONSTRAINT "poolpayment_fk_user_foreign" FOREIGN KEY("fk_user") REFERENCES "user"("id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_fk_category_foreign" FOREIGN KEY("fk_category") REFERENCES "transactionCategory"("id");
ALTER TABLE
    "repetitiveExecution" ADD CONSTRAINT "repetitiveexecution_fk_receiveraccount_foreign" FOREIGN KEY("fk_receiverAccount") REFERENCES "bankAccount"("id");
ALTER TABLE
    "session" ADD CONSTRAINT "session_fk_user_foreign" FOREIGN KEY("fk_user") REFERENCES "user"("id");
ALTER TABLE
    "poolPayment" ADD CONSTRAINT "poolpayment_fk_pool_foreign" FOREIGN KEY("fk_pool") REFERENCES "moneyPool"("id");
ALTER TABLE
    "repetitiveExecution" ADD CONSTRAINT "repetitiveexecution_fk_senderaccount_foreign" FOREIGN KEY("fk_senderAccount") REFERENCES "bankAccount"("id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_fk_user_foreign" FOREIGN KEY("fk_user") REFERENCES "user"("id");
ALTER TABLE
    "repetitiveExecution" ADD CONSTRAINT "repetitiveexecution_fk_category_foreign" FOREIGN KEY("fk_category") REFERENCES "transactionCategory"("id");
ALTER TABLE
    "bankAccount" ADD CONSTRAINT "bankaccount_fk_user_foreign" FOREIGN KEY("fk_user") REFERENCES "user"("id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_fk_bankaccount_foreign" FOREIGN KEY("fk_bankAccount") REFERENCES "bankAccount"("id");
ALTER TABLE
    "bankAccount" ADD CONSTRAINT "bankaccount_fk_bank_foreign" FOREIGN KEY("fk_bank") REFERENCES "bank"("id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_fk_type_foreign" FOREIGN KEY("fk_type") REFERENCES "transactionType"("id");
ALTER TABLE
    "poolPayment" ADD CONSTRAINT "poolpayment_fk_currency_foreign" FOREIGN KEY("fk_currency") REFERENCES "currency"("id");
ALTER TABLE
    "bankAccount" ADD CONSTRAINT "bankaccount_fk_currency_foreign" FOREIGN KEY("fk_currency") REFERENCES "currency"("id");
ALTER TABLE
    "repetitiveExecution" ADD CONSTRAINT "repetitiveexecution_fk_state_foreign" FOREIGN KEY("fk_state") REFERENCES "state"("id");
ALTER TABLE
    "repetitiveExecution" ADD CONSTRAINT "repetitiveexecution_id_foreign" FOREIGN KEY("id") REFERENCES "user"("id");