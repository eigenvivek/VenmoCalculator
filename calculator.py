from itertools import combinations

import click
import pandas as pd


def read_dataframe(filename, price_col="Price", payers_col="Payer"):
    df = pd.read_csv(filename)
    df[price_col] = df[price_col].apply(lambda x: float(x[1:]))
    df[payers_col] = df[payers_col].apply(lambda x: x.rstrip())
    return df


def get_attendees(df, all=None, people_col="People"):
    if all is None:
        attendees = []
    else:
        attendees = [person.lstrip() for person in all.split(",")]
    for people in df[people_col]:
        if people == "All":
            continue
        for person in people.split(","):
            person = person.lstrip()
            if person in attendees:
                continue
            else:
                attendees.append(person)
    return attendees


def get_payers(df, payers_col="Payer"):
    return df[payers_col].unique()


def get_ledger(
    df, attendees, payers, price_col="Price", payers_col="Payer", people_col="People"
):
    num_attendees = len(attendees)

    # Fill in the ledger of who owes whom what
    ledger = pd.DataFrame(0, columns=payers, index=attendees, dtype=float)
    for _, row in df.iterrows():
        payer, price, people = row[[payers_col, price_col, people_col]]
        if people == "All":
            for attendee in attendees:
                ledger.at[attendee, payer] += price / num_attendees
        else:
            people = people.split(",")
            for person in people:
                person = person.lstrip()
                ledger.at[person, payer] += price / len(people)

    # Simplify the ledger by removing redundancies across payers
    for payer in payers:
        ledger.at[payer, payer] = 0  # Don't pay yourself
    for payer_1, payer_2 in combinations(payers, r=2):
        back = min(
            ledger.at[payer_1, payer_2], ledger.at[payer_2, payer_1]
        )  # If two people owe each other money, subtract the minimum amount so only one transaction needs to happen
        ledger.at[payer_1, payer_2] -= back
        ledger.at[payer_2, payer_1] -= back

    # Convert to real money!
    ledger = ledger.applymap(lambda x: "${:.2f}".format(x))

    return ledger


@click.command()
@click.option("--filename", "-f", type=click.Path(exists=True), required=True)
@click.option("--all", type=str, required=False)
def main(filename, all):
    df = read_dataframe(filename)
    attendees = get_attendees(df, all)
    payers = get_payers(df)
    attendees = list(set(attendees).union(set(payers)))
    ledger = get_ledger(df, attendees, payers)
    print(ledger)


if __name__ == "__main__":
    main()
