from __future__ import annotations

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .managers import ClassManager


class Class(models.Model):
    id = models.AutoField(verbose_name=_("ID"), auto_created=True, primary_key=True)
    grade = models.CharField(verbose_name=_("Grade"), max_length=10)
    section = models.CharField(verbose_name=_("Section"), max_length=10, null=True, blank=True)

    objects: ClassManager = ClassManager()

    class Meta:
        unique_together = ["grade", "section"]

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Class) and self.id == __o.id

    def __ne__(self, __o: object) -> bool:
        if not isinstance(__o, Class):
            return True
        return self.id != __o.id

    def __repr__(self) -> str:
        string = f"<Class id={self.id} grade={self.grade}"
        if self.section:
            string += f" section={self.section}"
        string += ">"
        return string

    def __str__(self) -> str:
        _class = self.grade
        if self.section:
            _class += " " + self.section
        return _class

    def __int__(self) -> int:
        return int(self.id)

    def get_class_teacher(self):
        try:
            return self.teacher
        except ObjectDoesNotExist:
            return None

    def get_teachers(self):
        return self.teacher_set.all()

    def get_students(self):
        return self.student_set.all()
