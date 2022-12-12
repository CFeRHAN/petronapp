from django.db import models


class AttachmentTemplate(models.Model):
    category = models.CharField(max_length=30, blank=False, null=True) #trader profile
    title = models.CharField(max_length=200, blank=True, null=True) # id card scan / registeration docs
    is_mandatory = models.BooleanField(default=False)
    sort_order = models.IntegerField()

    def __str__(self):
        return str(self.category + ' - ' +self.title)

class Attachment(models.Model):
    template = models.ForeignKey(AttachmentTemplate, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=50, blank=False, primary_key=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    original_file_name = models.CharField(max_length=50, blank=True, null=True)
    

    def __str__(self):
        return self.file_id