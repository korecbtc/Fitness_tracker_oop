from typing import Dict, List
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration_h: float
    distance_km: float
    speed_kmph: float
    calories_kc: float
    MESSAGE: str = ('Тип тренировки: {}; '
                    'Длительность: {:0.3f} ч.; '
                    'Дистанция: {:0.3f} км; '
                    'Ср. скорость: {:0.3f} км/ч; '
                    'Потрачено ккал: {:0.3f}.')

    def get_message(self) -> str:
        """Возвращаю сообщение."""
        return self.MESSAGE.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        meanspeed_kmph: float = self.get_distance() / self.duration
        return meanspeed_kmph

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message: InfoMessage = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLE: float = 18
    CALORIES_MEAN_SPEED_MULTIPLE_SHIFT: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_m: float = self.MIN_IN_HOUR * self.duration
        spent_calories_kc: float = (
            self.CALORIES_MEAN_SPEED_MULTIPLE * super().get_mean_speed() - (
                self.CALORIES_MEAN_SPEED_MULTIPLE_SHIFT)) * self.weight / (
                    self.M_IN_KM) * duration_m
        return spent_calories_kc


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLE_FIRST: float = 0.035
    CALORIES_WEIGHT_MULTIPLE_SECOND: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_min: float = self.MIN_IN_HOUR * self.duration
        spent_calories_kc: float = (
            self.CALORIES_WEIGHT_MULTIPLE_FIRST * self.weight + (
                super().get_mean_speed() ** 2 // self.height) * (
                self.CALORIES_WEIGHT_MULTIPLE_SECOND) * (self.weight)
        ) * duration_min
        return spent_calories_kc


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MEAN_SPEED_SUM: float = 1.1
    WEIGHT_MULTIPLE: float = 2

    def __init__(
        self,
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
        """Переопределяю среднюю скорость."""
        mean_speed_kmph: float = self.lenght_pool * self.count_pool / (
            self.M_IN_KM) / self.duration
        return mean_speed_kmph

    def get_spent_calories(self) -> float:
        """Переопределяю затраченные калории."""

        spent_calories_kc: float = (
            self.get_mean_speed() + self.MEAN_SPEED_SUM) * (
            self.WEIGHT_MULTIPLE) * self.weight
        return spent_calories_kc


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in type_training:
        raise ValueError("Не правильный код тренировки.")
    obj_training: Training = type_training[workout_type](*data)
    return obj_training


def main(training: Training) -> None:
    """Главная функция."""
    info: Training = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
