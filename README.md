# Personal Assistant Bot Lana

## Start bot command: hi_lana

## 📴 Commands list:

### 🙍 Manage by Contacts

| Command        | Arguments                                             | Description                                                    |
| -------------- | ----------------------------------------------------- | -------------------------------------------------------------- |
| add-contact    | add-contact [name] [phone]                            | add new contact or update existed with additional phone number |
| all-contact    | all-contact                                           | show all contacts in the Addressbot                            |
| change-contact | change-contact [name] [field] [old_value] [new_value] | change contact's fields such as PHONE, EMAIL, NAME, BIRTHDAY   |
| find-contact   | find-contact [name]                                   | show concrete contact's fields                                 |
| delete-contact | delete-contact [name]                                 | delete concrete contact from the Addressbot                    |

### ☎️ Manage by Phone

| Command    | Arguments         | Description                    |
| ---------- | ----------------- | ------------------------------ |
| show-phone | show-phone [name] | show concrete contact's phones |

### 🎂 Manage by Birthday

| Command       | Arguments                           | Description                                   |
| ------------- | ----------------------------------- | --------------------------------------------- |
| add-birthday  | add-birthday [name] [birthday date] | add contact's birthday                        |
| show-birthday | show-birthday [name]                | show concrete contact's birthday              |
| birthdays     | birthdays [quantity of days]        | show birthdays wihthin pointed period of time |

### ✉️ Manage by Email

| Command      | Arguments                   | Description                     |
| ------------ | --------------------------- | ------------------------------- |
| add-email    | add-email [name]            | add contact's emails            |
| show-email   | show-email [name]           | show concrete contact's emails  |
| delete-email | delete-email [name] [email] | delete contact's concrete email |

### 📭 Manage by Address

| Command        | Arguments                     | Description                     |
| -------------- | ----------------------------- | ------------------------------- | ------------- |
| add-address    | add-address [name]            | add contact's address           |
| show-address   | show-address [name]           | show concrete contact's address |
| delete-address | delete-address [name] [email] | delete contact's address        | НЕРЕАЛІЗОВАНО |

### 🗒️ Manage by Notes

| Command      | Arguments | Description |
| ------------ | --------- | ----------- |
| add-note     |           |             |
| show-notes   |           |             |
| change-notes |           |             |
| delete-notes |           |             |

## We use the following types of commits:

- Feat(PY) Added new functionality

- Fix(PY) Error correction

- Perf(PY) Changes to improve performance

- Refactor(PY) Code edits without fixing bugs or adding new features

- Revert(PY) Rollback to previous commits

- Style(PY) Code style edits

- Docs(MD) Documentation update

Choose from the list the description of the commit that fits your task, in brackets we write the file in which we worked, and in the body of the commit we write what we did (changed) etc.

## To run the bot, please install the following packages:

1. `pip install setuptools`
2. `pip install prompt_toolkit`
3. `pip install colorama`
4. `pip install -e .`
