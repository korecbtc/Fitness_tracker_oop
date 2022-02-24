from typing import Any, Callable
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
        print(f'Тип тренировки: {self.training_type}; '
              f'Длительность: {round(self.duration, 3)} ч.; Дистанция: {round(self.distance, 3)}'
              f' км; Ср. скорость: {round(self.speed, 3)} км/ч; Потрачено ккал: {round(self.calories, 3)}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = 0.65
        self.M_IN_KM = 1000
        self.MIN_IN_HOUR = 60

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
        spent_calories = (coeff_calorie_1 * self.weight + (super().get_mean_speed() ** 2 // self.height) * coeff_calorie_2 * self.weight) * duration
        
        print()
      
        print(super().get_mean_speed())
        print(spent_calories)
        print(super().get_distance())
        return spent_calories




class Swimming(Training):
    """Тренировка: плавание."""
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
        self.LEN_STEP = 1.38


    def get_mean_speed(self) -> float:
        """Переопределяю среднюю скорость"""
        mean_speed = self.lenght_pool * self.count_pool / self.M_IN_KM / self.duration
        return mean_speed
    
    def get_spent_calories(self) -> float:
        """Переопределяю затраченные калории"""
        swim_coef_1 = 1.1
        swim_coef_2 = 2
        spent_calories = (self.get_mean_speed() + swim_coef_1) * swim_coef_2 * self.weight
        return spent_calories

#beg = SportsWalking(512,0.7,80,180)
#beg.get_spent_calories()
data = [7720, 2, 80, 25, 40]
swim = Swimming(*data)
print()
print(swim.get_mean_speed())
print(swim.get_spent_calories())
print(swim.get_distance())




def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training : dict[str, Any] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    obj_training = type_training[workout_type](720, 1, 80, 25, 40)
    return obj_training

read_package('SWM', data)

def main(training: Training) -> None:
    """Главная функция."""
    pass


info = training.show_training_info()
    print(info.get_message)       

#beg = SportsWalking(512,0.7,80,180)
#beg.get_spent_calories()
#swim = Swimming(1000, 0.7, 80, 25, 20)
#print()
#print(swim.get_mean_speed())
#print(swim.get_spent_calories())
#print(swim.get_distance())      