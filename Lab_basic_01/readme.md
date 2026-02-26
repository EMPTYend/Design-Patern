# Отчёт по запуску первого .NET приложения

## 1. Установка .NET SDK
На этом этапе был установлен .NET SDK.

![Скрин 1 — установка .NET SDK](./Screen01.png)

## 2. Запуск первого приложения
После установки выполнен запуск первого консольного приложения (`dotnet run`), в результате получен вывод `Hello, World!`.

![Скрин 2 — запуск первого приложения](./Screen02.png)

## 3. Проверка dotnet new console
Проверка (`dotnet new console`).

![Скрин 3 — dotnet new console](./Screen05.png)


## 4. Настройка Environment Variables
В переменные окружения добавлены пути для корректной работы `dotnet` из терминала.

![Скрин 3 — Environment Variables](./Screen03.png)
![Скрин 4 — пути в Environment Variables](./Screen04.png)

## Код проекта

### `Program.cs`
```csharp
using System;

Console.WriteLine("Hello, World!");
```

### `myproject.csproj`
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>
</Project>
```
