# CScript
This is a dynamically typed, non-recursive language.
## Syntax
A descriptions of the relevant operators, their syntax, and restrictions.
### The Assignment operator
Variables must begin with an alphabetic [a-z,A-Z] character and otherwise be alphanumeric.
```
var1 = Function(var2)
```
#### Object Aliasing
When used on its own the `=` is used for aliasing and performs a shallow-copy. You may not implicity release memory by creating an alias.
#### Implicit Object Instantiation
When the assignment operator is used in conjunction with any other operator or function a new object is implicitly instantiated. This also implicitly calls `Release` on the variable's old contents and invalidates any aliases. Likewise using implicit object instantiation on an alias invalidates the original object and and of its other aliases.
```
var1 = Store("123")
var2 = var1 # Object aliasing
var2 = Store(456) # Implicit Object Instantiation, var1 is released.
Print(var1) # Outputs `Syntax error: unknown variable var1`
```
### The Addition Operator
This operator performs implicit object instantiation and as such must be used in conjunction with the assignment operator.
```
arg1 = 1 + 2
arg1 = Store(1 + 2) # invalid
```
### Completing Statements
Statements are completed with a newline or EOF.
## Standard Library
The following is an enumeration of the standard library. Syntaxes are presented with type annotations to appease people familiar with types but everything is dynamically typed.
### Functions
The standard library functions.
#### Store
Syntax:
```
Store(input: String | Integer | Boolean | Object) -> Object
```
Used to create a new object. Performs a deepcopy.
#### Release
Syntax:
```
Release(Object)
```
Used to release an object. Unsets all related aliases.
#### Print
Syntax:
```
Print(String | Integer | Boolean | Object)
```
When called on a standard library object it prints the relevant object contents. When called on an opaque object it resolves the object to standard library objects and prints those.
### Objects
The standard library objects
### Strings
Strings are enclosed by the `"`
Syntax:
```
str = Store("Hello World")
Print("Hello World")
```
### Integers
Integers are signed whole numbers consisting of the characters `0-9`. Negative numbers are prefixed by `-`.
### Booleans
Booleans are either `true` or `false`. As a result both of those names are reserved.
