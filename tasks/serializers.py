from rest_framework import serializers

from commons.models import Comment
from .models import Task


class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id',
                  'task',
                  'commented_on',
                  'commented_by',
                  'status_task',
                  'comment',
                  ]
        # fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    address = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    tasks_comments = CommentSerializer(many=True)

    class Meta:
        model = Task
        fields = ["id",
                  "address",
                  "category",
                  "apartment",
                  "porch",
                  "floor",
                  "phone",
                  "description",
                  "reu",
                  # "executor",
                  # "transmission_time",
                  "source_task",
                  # "sms_is_active",
                  # "sms_is_sended",
                  # "sms_is_queue",
                  # "sms_result",
                  "status_task",
                  # "status_time",
                  "comment_status",
                  "tasks_comments",
                  # "surname_name",
                  # "first_name",
                  # "patronymic_name",
                  # "author_eds",
                  "created_on",
                  "created_by",
                  # "updated_by",
                  ]
        # fields = '__all__'


class TaskInWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskInListViewInWorkSerializer(serializers.ModelSerializer):
    address = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    tasks_comments = CommentSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            'created_on',
            'id',
            'address',
            'apartment',
            'phone',
            'category',
            'description',
            'created_by',
            'status_task',
            'comment_status',
            'tasks_comments'
        ]
