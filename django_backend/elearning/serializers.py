from rest_framework import serializers
from .models import *



class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'enrollment_date', 'student', 'course']

class UserSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'userName', 'password', 'email', 'role', 'date_joined', 'photo', 'enrollments']

class CourseSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'enrollment_capacity', 'tutor', 'participants']

class MaterialSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Material
        fields = ['id', 'title', 'content', 'upload_date', 'document_type', 'course']

class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'course']




class SubmissionSerializer(serializers.ModelSerializer):
    
    student=UserSerializer(read_only=True,many=True)
    assignment=AssignmentSerializer(read_only=True,many=True)
    class Meta:
        model = Submission
        fields='__all_'

class GradeSerializer(serializers.ModelSerializer):
    student=UserSerializer(read_only=True)
    assignment=AssignmentSerializer(read_only=True)

    class Meta:
        model = Grade
        fields='__all_'


class InteractionHistorySerializer(serializers.ModelSerializer):
    
    student=UserSerializer(read_only=True,many=True)
    material=MaterialSerializer(read_only=True, many=True)

    class Meta:
        model = InteractionHistory
        fields='__all_'


class ReadingStateSerializer(serializers.ModelSerializer):
    student=UserSerializer(read_only=True,many=True)
    material=MaterialSerializer(read_only=True, many=True)


    class Meta:
        model = ReadingState
        fields='__all_'