                
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define DATA_FILE "accounts.txt"
#define TRANS_FILE "transactions.txt"

int authenticate(char acc[], char pin[]) {
    FILE *fp = fopen(DATA_FILE, "r");
    char file_acc[50], file_pin[50];
    int balance;

    while (fscanf(fp, "%s %s %d", file_acc, file_pin, &balance) != EOF) {
        if (strcmp(acc, file_acc) == 0 && strcmp(pin, file_pin) == 0) {
            fclose(fp);
            return 1;
        }
    }

    fclose(fp);
    return 0;
}

int get_balance(char acc[]) {
    FILE *fp = fopen(DATA_FILE, "r");
    char file_acc[50], file_pin[50];
    int balance;

    while (fscanf(fp, "%s %s %d", file_acc, file_pin, &balance) != EOF) {
        if (strcmp(acc, file_acc) == 0) {
            fclose(fp);
            return balance;
        }
    }

    fclose(fp);
    return -1;
}

void update_balance(char acc[], int new_balance) {
    FILE *fp = fopen(DATA_FILE, "r");
    FILE *temp = fopen("temp.txt", "w");

    char file_acc[50], file_pin[50];
    int balance;

    while (fscanf(fp, "%s %s %d", file_acc, file_pin, &balance) != EOF) {
        if (strcmp(acc, file_acc) == 0) {
            fprintf(temp, "%s %s %d\n", file_acc, file_pin, new_balance);
        } else {
            fprintf(temp, "%s %s %d\n", file_acc, file_pin, balance);
        }
    }

    fclose(fp);
    fclose(temp);

    remove(DATA_FILE);
    rename("temp.txt", DATA_FILE);
}

void add_transaction(char acc[], char action[], int amount) {

    FILE *fp = fopen(TRANS_FILE, "a");
    fprintf(fp, "ACC%s %s %d\n", acc, action, amount);
    fclose(fp);
}

int main(int argc, char *argv[]) {

    char *operation = argv[1];
    char *acc = argv[2];
    char *pin = argv[3];
    int amount = atoi(argv[4]);

    // LOGIN
    if (strcmp(operation, "login") == 0) {
        if (authenticate(acc, pin)) {
            printf("Login Successful");
        } else {
            printf("Invalid Account or PIN");
        }
    }

    // BALANCE
    else if (strcmp(operation, "balance") == 0) {
        int bal = get_balance(acc);
        printf("Balance: %d", bal);
    }

    // DEPOSIT
    else if (strcmp(operation, "deposit") == 0) {
        int bal = get_balance(acc);
        bal += amount;
        update_balance(acc, bal);
        add_transaction(acc, "Deposited:", amount);
        printf("Deposited Successfully");
    }

    // WITHDRAW
    else if (strcmp(operation, "withdraw") == 0) {
        int bal = get_balance(acc);

        if (bal < amount) {
            printf("Insufficient Balance");
        } else {
            bal -= amount;
            update_balance(acc, bal);
            add_transaction(acc, "Withdrawn:", amount);
            printf("Withdraw Successful");
        }
    }

    // HISTORY
    else if (strcmp(operation, "history") == 0) {
       FILE *fp = fopen(TRANS_FILE, "r");
       char line[200];
       char search_str[100];
       sprintf(search_str, "ACC%s", acc);
       while (fgets(line, sizeof(line), fp)) {
           if (strstr(line, search_str)) {
               printf("%s", line);
           }
       }
       fclose(fp);

    }

    return 0;
}