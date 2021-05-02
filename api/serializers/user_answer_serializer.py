from rest_framework import serializers

from ..models import Question,Answer,UserExamDetail,UserAnswer,User

class UserAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(label=("question_id"))
    answer_id = serializers.IntegerField(label=("answer_id"))

    def validate(self, data):
        question_id = data.get('question_id')
        answer_id = data.get('answer_id')
        user = self.context.get('user')
        if not Question.objects.filter(pk = question_id).exists():
            raise serializers.ValidationError("Question doesnt exist")
        elif not Answer.objects.filter(pk = answer_id).exists():
            raise serializers.ValidationError("Answer doesnt exist")
        elif UserAnswer.objects.filter(user_exam__user =user, question_id =question_id).exists():
            raise serializers.ValidationError("Question already answered")
        return True

    def save(self, data):
        user = self.context.get('user')
        question_id = data.get('question_id')
        answer_id = data.get('answer_id')
        is_correct_answer = True if Question.objects.filter(id=question_id,answer_id=answer_id)\
                .exists() else False
        exam_detail,_ = UserExamDetail.objects.get_or_create(user=user)
        UserAnswer.objects.create(user_exam=exam_detail,question_id=question_id,answer_id=answer_id,
                                  is_correct=is_correct_answer)
        return True

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'answer')

class GetQuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self,obj):
        return AnswerSerializer(obj.choices, many=True).data

    class Meta:
        model = Question
        fields = ('id', 'question', 'answers')

class GetScoreSerializer(serializers.ModelSerializer):
    answered_count = serializers.SerializerMethodField()
    correct_answered_count = serializers.SerializerMethodField()

    def get_answered_count(self, obj):
        return UserAnswer.objects.filter(user_exam__user=obj).count()

    def get_correct_answered_count(self, obj):
        return obj.userexamdetail_set.first().number_of_correct_answer if obj.userexamdetail_set.first() else None

    class Meta:
        model = User
        fields = ('id', 'email', 'answered_count', 'correct_answered_count')