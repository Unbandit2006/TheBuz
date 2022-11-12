# TheBuz

## New Name, New Look

This is the new start of TheBuz. Before there was a project named Beeper, but eventually that code base became bloated and too many files so this will be a new minimalistic approach to the problem.

## Naming Conventions

| Type                    | Naming Convention |
| ----------------------- | ----------------- |
| Class                   | UpperCamalCase    |
| File                    | UpperCamalCase    |
| Variable (Non Constant) | lower_snake_case  |
| Constant                | UPPERCASE         |
| Functions               | lower_snake_case  |

## Firebase Schema

IK Firebase has no schema but just for organizational purposes.

```
UniqueIdentifier(Email or Firebase Default Random Sequence):str
|
|-> amntOfHours(The Amount of hours the user wants):int
|-> birthdays(Contains All Birthday Data):Dictionary
    |
    |-> UniqueIdentifier: int
        |
        |-> List[Name:str(type 'me' for self) , Date:str]
|-> fname(First Name of the User):str
|-> lname(Last Name of the User):str
|-> number(Phone Number of the User):int
|-> time(Time the User wants to recieve at (works only by 24)):str
|-> zipcode(the zipcode the user lives at):str
```

## Tools

- Firebase

- WeatherAPI

- PyTextNow
