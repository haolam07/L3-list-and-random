## List
A data structure that is mutable (changeable) ordered sequence of elements. Defined by having values between square brackets [ ]

Ex: 
``` groceryList = ["pie", "takis", "dino nuggets", "chicken tenders", "cheese", "pineapple", "sausage"] # List of strings ```

### indexing list
Each i tem in a list corresponds to an index number, which is an integer. Starting with 0. 

ex: `groceryList[3]` outputs --> chicken tenders

len() give us the length/number of items in our list
`len(groceryList)` --> 7 

### List functions
`List.append(Element)` --> adds an item to the end of a  list

`groceryList.append("bacon")`
```python
item = input("Enter a grocery list item: ") # Whatever the user inputs
groceryList.append(item) # add the user's input to the grocery list
```

List.insert(index, Element) --> add an item to the specific index location

- `groceryList.insert(0,"water")`

-List.remove(element) --> searches the list fo a specific element and removes it 

- `groceryList.remove("dino nuggets")` 

-List.pop(index) --> removes an item at specified index
 - `groceryList.pop(3)`


## Random

A class that random numbers. There is a function that lets the computer pick a random number between a given range

### Formula
```python
  import random #import a random class package library

  variable = random.randint(startNum, endNum)
  ex: 
  x = random.randint(0,10)
  
  
```