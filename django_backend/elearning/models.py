from enum import Enum
from django.db import models

from django.db import models
from enum import Enum

class Role(Enum):
    ADMIN = 'admin'
    STUDENT = 'student'
    TUTOR = 'tutor'
    
    @classmethod
    def choices(cls):
        return [(member.value, member.name) for member in cls]

class DocType(Enum):
    PDF = 'PDF'
    PPTX = 'PPTX'
    DOCX = 'DOCX'
    PNG = 'PNG'
    
    @classmethod
    def choices(cls):
        return [(member.value, member.name) for member in cls]

class InteractionType(Enum):
    UPLOAD = 'upload'
    READ = 'read'
    WRITE = 'write'

class User(models.Model):
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=200, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices())
    date_joined = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos/students', max_length=200, null=True, blank=True)
    class Meta:
        db_table = 'user'
        ordering = ['userName']
    
    def __str__(self):
        return self.userName

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    enrollment_capacity = models.IntegerField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_tutored')
    participants = models.ManyToManyField(User, through='Enrollment', through_fields=('course', 'student'))
    class Meta:
        db_table = 'course'
        
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    enrollment_date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'enrollment'

class Material(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    document_type = models.CharField(max_length=20, choices=DocType.choices())
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'material'
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'assignment'
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'submission'

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.IntegerField(default=1, null=True, blank=True)
    feedback = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'grade'

class InteractionHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    interactionType = models.CharField(max_length=50, choices=[(type.name, type.value) for type in InteractionType])
    interactionDate = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'interactionHistory'

class ReadingState(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    readState = models.FloatField(default=0, null=True, blank=True)
    lastReadDate = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'readState'
