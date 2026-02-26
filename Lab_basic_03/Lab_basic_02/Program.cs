using System.Globalization;
using System.Net.Http.Headers;
using System.Runtime.CompilerServices;

Console.WriteLine ("Hello, Jerry");
Hello1();
Thread.Sleep(500);
Console.WriteLine ("Hello, Jerry2");
Hello1();
Thread.Sleep(500);
Hello1();

// список инструкций - функций
void Hello1()
{
Console.WriteLine("A"); 
Thread.Sleep(2000);
Console.WriteLine("B");
Thread.Sleep(2000);
Console.WriteLine ("C");
A();
A();
}

B();
C();
A();
A();
A();
A();

void A()
{
Console.WriteLine ("FUNC A");
}

void B()
{
Console.WriteLine ("FUNC B");
}

void C()
{
Console.WriteLine ("FUNC C");
}


void A1()
{
Console.WriteLine ("FUNC A1");
}

void B1()
{
Console.WriteLine ("FUNC B1");
}

void C1()
{
Console.WriteLine ("FUNC C1");
}

B1();
C1();
A1();

void NOFUNC()
{
Console.WriteLine ("FUNC NOFUNC");
}