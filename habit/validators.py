from rest_framework import serializers


class HabitDurationValidator:
    """Время выполнения должно быть не менее 0 и не более 120 секунд """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration = value.get('duration')
        if duration > 120:
            raise serializers.ValidationError('The execution time of the habit should be no more than 120 seconds.')
        if duration == 0:
            raise serializers.ValidationError('Execution time cannot be 0!')