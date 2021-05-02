from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from ..base_response import HttpErrorResponse,HttpSuccessResponse
from ..error_codes import get_error_code
from ..models import UserAnswer,Question,User
from..serializers.user_answer_serializer import UserAnswerSerializer,GetQuestionSerializer,GetScoreSerializer

class UserAnswerCreate(CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        serializer = UserAnswerSerializer(
            data=request.data,
            context={'user': request.user})
        if serializer.is_valid():
            if serializer.save(request.data):
                return HttpSuccessResponse("Answered successfully")

        kwargs_errors = {'error_code': get_error_code(
            serializer.errors.values())}
        return HttpErrorResponse(serializer.errors, **kwargs_errors)

class GetQuestionView(RetrieveAPIView):
    serializer_class = GetQuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        answered_questions = list(UserAnswer.objects.filter(user_exam__user=request.user).values_list('question',flat=True))
        question = Question.objects.exclude(id__in=answered_questions).first()
        if not question:
            kwargs_errors = {'error_code': get_error_code(
                [['No more questions left']])}
            return HttpErrorResponse({'non_field_errors': ['No more questions left']},
                                     **kwargs_errors)
        data = self.get_serializer(question).data
        return HttpSuccessResponse(data)

class GetScoreView(RetrieveAPIView):
    serializer_class = GetScoreSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        data = self.get_serializer(User.objects.filter(is_superuser=False), many=True).data
        return HttpSuccessResponse(data)