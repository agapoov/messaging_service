from rest_framework import serializers

from .models import Client, Mailing


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'

    def validate(self, attrs):
        if attrs['end_time'] <= attrs['start_time']:
            raise serializers.ValidationError('The start date exceeds the end date')
        
        if attrs['start_time'] == attrs['end_time']:
            raise serializers.ValidationError('The start date and end date cannot be the same')

        allowed_filters = ['tag', 'operator_code']
        filters = attrs.get('filter_params', {})

        if not filters:
            raise serializers.ValidationError('At least one filter parameter (tag or operator_code) must be specified')

        if filters:
            for input_filter in filters:
                if input_filter not in allowed_filters:
                    raise serializers.ValidationError(f'Invalid filtering parameter: {input_filter}')
        return attrs


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('phone_number', 'tag')
