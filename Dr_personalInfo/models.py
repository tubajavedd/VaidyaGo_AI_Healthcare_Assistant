from django.db import models

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

class DoctorPersonalInfo(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    mobile_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15, blank=True, null=True)

    email = models.EmailField(unique=True)

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    address = models.TextField()

    #photo = models.ImageField(upload_to='doctor_photos/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    REJECTION_CHOICES = [
    ('invalid_docs', 'Invalid Documents'),
    ('missing_info', 'Missing Information'),
    ('license_issue', 'License Issue'),
    ('other', 'Other'),
]


    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='incomplete')

    rejected_reason = models.CharField(max_length=255 ,choices=REJECTION_CHOICES, null = True,blank=True)
    rejected_message = models.TextField(null=True,blank=True)
    rejeted_file = models.FileField(upload_to='rejected/',null=True,blank=True)

