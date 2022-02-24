from typing import Any, Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Печатаю сообщение"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f}'
                f' км; Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        meanspeed = self.get_distance() / self.duration
        return meanspeed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.title(), self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return message

    def title(self) -> str:
        """Возвращает название тренировки"""
        pass


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration = self.MIN_IN_HOUR * self.duration
        spent_calories = (
            coeff_calorie_1 * super().get_mean_speed() - (
                coeff_calorie_2)) * self.weight / self.M_IN_KM * duration
        return spent_calories

    def title(self) -> str:
        """Возвращает название тренировки"""
        return 'Running'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        duration = self.MIN_IN_HOUR * self.duration
        spent_calories = (coeff_calorie_1 * self.weight + (
                          super().get_mean_speed() ** 2 // self.height) * (
                          coeff_calorie_2) * self.weight) * duration
        return spent_calories

    def title(self) -> str:
        """Возвращает название тренировки"""
        return 'SportsWalking'


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределяю среднюю скорость"""
        mean_speed = self.lenght_pool * self.count_pool / self.M_IN_KM / (
            self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Переопределяю затраченные калории"""
        swim_coef_1 = 1.1
        swim_coef_2 = 2
        spent_calories = (self.get_mean_speed() + swim_coef_1) * (
            swim_coef_2) * self.weight
        return spent_calories

    def title(self) -> str:
        """Возвращает название тренировки"""
        return 'Swimming'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training: Dict[str, Any] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    obj_training = type_training[workout_type](*data)
    return obj_training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
