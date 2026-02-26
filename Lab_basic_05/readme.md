# Lab Basic 05

## Концепты
- Логические значения: `true`, `false`
- Логические выражения
- Операторы сравнения чисел: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Логические операторы: `&&`, `||`, `==`, `!`, `!=`
- Lazy evaluation (короткое замыкание) для `&&` и `||`

## Вопросы на понимание

### 1
```csharp
bool a = true;
Console.WriteLine(a);
```
Ответ: выведется `True`.  
`bool` принимает только `true` или `false`, при выводе в консоль это текст `True/False`.

### 2
```csharp
bool a = null;
```
Ответ: ошибка компиляции.  
`bool` не может быть `null` (только `bool?` допускает `null`).

### 3
```csharp
bool a = 1 == 2;
Console.WriteLine(a);
```
Ответ: выведется `False`.

### 4
```csharp
int x = 3;
int y = 4;
bool b = x == y;
Console.WriteLine(b);
```
Ответ: выведется `False`.

### 5
```csharp
int x = 3;
int y = 4;
bool b = x * 2 == y + 4;
Console.WriteLine(b);
```
Ответ: выведется `False` (`6 == 8`).

### 6
```csharp
bool a = 1 > 2;
a = 3 == 3;
Console.WriteLine(a);
```
Ответ: выведется `True`.

### 7
```csharp
bool a = true;
F(a);

static void F(bool x)
{
    Console.WriteLine(x);
}
```
Ответ: выведется `True`.

```csharp
F(5 > 3);

static void F(bool flag)
{
    Console.WriteLine(flag);
}
```
Ответ: выведется `True`.  
Аргумент `5 > 3` вычисляется перед вызовом функции, в `flag` попадет `true`.

### 8
```csharp
bool result = F();
Console.WriteLine(result);

static bool F()
{
    return true;
}
```
Ответ: выведется `True`.

### 9
```csharp
bool result = IsGreater(5, 3);
Console.WriteLine(result);

static bool IsGreater(int a, int b)
{
    return a > b;
}
```
Ответ: выведется `True`.

### 10
```csharp
bool a = true;
bool b = false;
bool c = a == b;
Console.WriteLine(c);
```
Ответ: выведется `False`.  
Сравнение `true == false` дает `false`.

### 11
```csharp
bool a = false;
bool b = !a;
Console.WriteLine(b);
```
Ответ: выведется `True`.

### 12
```csharp
bool a = true;
bool b = false;
bool c = a && b;
Console.WriteLine(c);
```
Ответ: выведется `False`.

### 13
```csharp
bool result = A() && B();
 
static bool A()
{
    Console.WriteLine("A");
    return true;
}
 
static bool B()
{
    Console.WriteLine("B");
    return true;
}
```
Ответ: в консоль напечатается:
```text
A
B
```
`result = true`.

### 14
```csharp
bool result = A() && B();
 
static bool A()
{
    Console.WriteLine("A");
    return true;
}
 
static bool B()
{
    Console.WriteLine("B");
    return false;
}
```
Ответ: в консоль напечатается:
```text
A
B
```
`result = false`.

### 15
```csharp
bool result = A() && B();

static bool A()
{
    Console.WriteLine("A");
    return false;
}

static bool B()
{
    Console.WriteLine("B");
    return true;
}
```
Ответ: в консоль напечатается только:
```text
A
```
`B()` не вызовется (lazy evaluation для `&&`), `result = false`.

### 16
```csharp
bool result = A() || B();

static bool A()
{
    Console.WriteLine("A");
    return true;
}

static bool B()
{
    Console.WriteLine("B");
    return true;
}
```
Ответ: в консоль напечатается только:
```text
A
```
`B()` не вызовется (lazy evaluation для `||`), `result = true`.
