from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# periods = [
#     {
#         "time": "",
#         "subject": "",
#     },
#     {
#         "time": "",
#         "subject": "",
#     },
# ]


class TimetableModel(models.Model):
    date = models.DateField(
        verbose_name=_("Date"),
        help_text=_("The date for which the timetable is valid. Represented by `datetime.date` instance."),
    )
    grade = models.CharField(
        verbose_name=_("Grade"),
        max_length=5,
        unique_for_date="date",
        help_text=_("The grade for which the timetable is valid. Should be a string"),
    )
    periods = models.JSONField(
        verbose_name=_("Periods"),
        default=[],
        help_text=_(
            "A list of dictionaries having field keys as `time` and `subject` and field values as the time in "
            "string valid for the period and the subject of which the period is respectively."
        ),
    )

    def save(self, *args, **kwargs) -> None:
        if TimetableModel.objects.filter(date=self.date, grade=self.grade).exists():
            raise ValidationError({"date": str(self.date), "grade": self.grade})
        return super().save(*args, **kwargs)
