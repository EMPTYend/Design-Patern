from __future__ import annotations
from typing import Generic, TypeVar, List, Protocol
from datetime import datetime

TContext = TypeVar("TContext")


# ---------------- Интерфейсы и базовые классы ----------------

class PipelineStep(Protocol, Generic[TContext]):
    def execute(self, context: TContext) -> None:
        ...


class Pipeline(Generic[TContext]):
    def __init__(self):
        self._steps: List[PipelineStep[TContext]] = []

    def add_step(self, step: PipelineStep[TContext]) -> Pipeline[TContext]:
        self._steps.append(step)
        return self

    def execute(self, context: TContext) -> None:
        for step in self._steps:
            # Интроспекция: проверяем, есть ли у контекста флаг is_done
            if hasattr(context, "is_done") and getattr(context, "is_done"):
                break
            step.execute(context)


# ---------------- Контексты ----------------

class OrderContext:
    def __init__(self, order_id: str, total: float, is_paid: bool):
        self.order_id = order_id
        self.total = total
        self.is_paid = is_paid
        self.is_done = False


class UserContext:
    def __init__(self, username: str):
        self.username = username
        self.is_valid = False
        self.is_done = False


# ---------------- Примеры шагов ----------------

class PaymentCheckStep(PipelineStep[OrderContext]):
    def execute(self, context: OrderContext) -> None:
        print(f"[PaymentCheck] Checking payment for order {context.order_id}...")
        if not context.is_paid:
            print("Payment missing. Stopping pipeline.")
            context.is_done = True


class DiscountStep(PipelineStep[OrderContext]):
    def execute(self, context: OrderContext) -> None:
        print(f"[Discount] Applying discount to order {context.order_id}")
        context.total *= 0.9


class ValidateUserStep(PipelineStep[UserContext]):
    def execute(self, context: UserContext) -> None:
        print(f"[ValidateUser] Checking username '{context.username}'")
        if not context.username.strip():
            print("Invalid username!")
            context.is_done = True
        else:
            context.is_valid = True


# ---------------- Декораторы ----------------

class LoggingDecorator(PipelineStep[TContext]):
    def __init__(self, inner: PipelineStep[TContext]):
        self._inner = inner

    def execute(self, context: TContext) -> None:
        print(f"[LOG] Starting {self._inner.__class__.__name__}")
        self._inner.execute(context)
        print(f"[LOG] Finished {self._inner.__class__.__name__}")


class TimeMeasureDecorator(PipelineStep[TContext]):
    def __init__(self, inner: PipelineStep[TContext]):
        self._inner = inner

    def execute(self, context: TContext) -> None:
        start = datetime.now()
        self._inner.execute(context)
        duration = (datetime.now() - start).total_seconds() * 1000
        print(f"[TIMER] {self._inner.__class__.__name__} took {duration:.2f} ms")


# ---------------- Демонстрация ----------------

def main():
    print("=== Order Pipeline ===")
    order_pipeline = Pipeline[OrderContext]() \
        .add_step(LoggingDecorator(PaymentCheckStep())) \
        .add_step(TimeMeasureDecorator(DiscountStep()))

    order = OrderContext(order_id="ORD123", total=100.0, is_paid=True)
    order_pipeline.execute(order)
    print(f"Final total: {order.total:.2f}\n")

    print("=== User Pipeline ===")
    user_pipeline = Pipeline[UserContext]() \
        .add_step(LoggingDecorator(ValidateUserStep()))

    user = UserContext(username="Iaroslav")
    user_pipeline.execute(user)
    print(f"Is user valid: {user.is_valid}\n")


if __name__ == "__main__":
    main()
