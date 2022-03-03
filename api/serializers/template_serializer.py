from rest_framework import serializers

import api.models as models


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Template
        fields = ['oid', 'name', 'requirements']


#     def update(self, instance, validated_data):
#         print(f'Validate: {validated_data}')
#         instance.name = validated_data.get('name', instance.name)
#         print('aAAAAAHAAAA')
#         instance.save()
#         return instance
