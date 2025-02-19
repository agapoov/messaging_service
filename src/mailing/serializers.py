from rest_framework import serializers

from .models import Mailing, Client


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'

    def validate(self, attrs):
        allowed_filters = ['tag', 'operator_code']
        if attrs['end_time'] <= attrs['start_time']:
            raise serializers.ValidationError('The start date exceeds the end date')

        filters = attrs.get('filter_params', {})
        if filters:
            for input_filter in filters:
                if input_filter not in allowed_filters:
                    raise serializers.ValidationError(f'Invalid filtering parameter: {input_filter}')
        return attrs


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('phone_number', 'tag')
