from itertools import combinations

import click
import pandas as pd


def read_dataframe(filename, price_col="Price"):
    df = pd.read_csv(filename)
    df[price_col] = df[price_col].apply(lambda x: float(x[1:]))
    return df


def get_attendees(df, people_col="People"):
    attendees = []
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


def get_ledger(df, attendees, payers):
    num_attendees = len(attendees)

    # Fill in the ledger of who owes whom what
    ledger = pd.DataFrame(0, columns=payers, index=attendees, dtype=float)
    for _, (payer, _, price, people) in df.iterrows():
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
        ledger.at[payer, payer] = 0
    for payer_1, payer_2 in combinations(payers, r=2):
        back = min(ledger.at[payer_1, payer_2], ledger.at[payer_2, payer_1])
        ledger.at[payer_1, payer_2] -= back
        ledger.at[payer_2, payer_1] -= back

    # Convert to real money!
    ledger = ledger.applymap(lambda x: "${:.2f}".format(x))

    return ledger


@click.command()
@click.option("--filename", "-f", type=click.Path(exists=True), required=True)
def main(filename):
    df = read_dataframe(filename)
    attendees = get_attendees(df)
    payers = get_payers(df)
    ledger = get_ledger(df, attendees, payers)
    print(ledger)


if __name__ == "__main__":
    main()
