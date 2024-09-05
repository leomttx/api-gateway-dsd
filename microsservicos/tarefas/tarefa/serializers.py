from rest_framework import serializers
from .models import Tarefa
import requests
from rest_framework.reverse import reverse

class TarefaSerializer(serializers.ModelSerializer):
    etiqueta_id = serializers.IntegerField(required = False, allow_null = True)
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Tarefa
        fields = ['id', 'nome', 'descricao', 'etiqueta_id', '_links']

        extra_kwargs = {
            'etiqueta_id': {'required': False, 'allow_null': True},
        }

    def get__links(self, obj):
        request = self.context.get('request')  # Obtém o objeto de request do contexto
        base_url = request.build_absolute_uri()  # Gera a URL base para a aplicação
        
        links = {
            'self': reverse('tarefa-detail', args=[obj.pk], request=request),  # URL para o detalhe da tarefa
            'edit': reverse('tarefa-detail', args=[obj.pk], request=request),  # URL para editar (usando o mesmo endpoint de detalhe)
            'delete': reverse('tarefa-detail', args=[obj.pk], request=request),  # URL para deletar (usando o mesmo endpoint de detalhe)
        }
        if obj.etiqueta_id:
            links['etiqueta'] = f'http://localhost:8000/etiquetas/{obj.etiqueta_id}/'
        return links


    def validate_etiqueta_id(self, value):
        # Verifica se a etiqueta existe
        if value:
            print("Value = ", value)
            url = f'http://localhost:8000/etiquetas/{value}/'
            response = requests.get(url)
            if response.status_code != 200:
                raise serializers.ValidationError("Etiqueta não encontrada.")
            return value
        else:
            pass

    def create(self, validated_data):
        try:
            etiqueta_id = validated_data.pop('etiqueta_id')
        except KeyError:
            etiqueta_id = None
        return Tarefa.objects.create(etiqueta_id=etiqueta_id, **validated_data)