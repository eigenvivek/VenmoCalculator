# VenmoCalculator

Automatically calculate repayments between friends from itemized receipts.

## Example

Process a list of itemized reciepts with

```zsh
> python calculator.py -f data/providence_13062022.csv

         Vivek    Noah    Gari
Gari    $56.03   $0.00   $0.00
Vivek    $0.00   $0.00   $0.00
Jacob   $96.63  $26.88  $29.10
Daniel  $96.63  $23.38  $29.10
Noah    $71.76   $0.00   $2.98
```

Money should be transferred from row people (debtors) to column people (lenders) (e.g., `Daniel` owes `Noah` $23.38).

## Usage

To use with your own reciepts, make sure the input CSV has the columns
```
Payer, Item, Price, People
Gari, borgor, $100, All
```
- If something was shared by all debtors (e.g., an appetizer), represent this entry with `All` in the `People` column
- Denote `Tax` and `Tip` in the `Item` column to split proportional to each person's subtotal
- Make sure prices are prepended with a `$` character
